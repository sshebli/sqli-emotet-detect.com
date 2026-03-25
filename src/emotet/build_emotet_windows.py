import os
import pandas as pd
import numpy as np

# --- CONFIG ---
WIN_SECONDS = 5

LOGSETS = [
    # Malicious (Unit42 Emotet)
    ("example1", "data/emotet/zeek_logs/example1/conn.log", "10.1.6.206", 2),
    ("example2", "data/emotet/zeek_logs/example2/conn.log", "10.1.5.101", 2),
    ("example3", "data/emotet/zeek_logs/example3/conn.log", "10.1.4.205", 2),
    ("example4", "data/emotet/zeek_logs/example4/conn.log", "172.16.1.101", 2),
    ("example5", "data/emotet/zeek_logs/example5/conn.log", "192.168.100.101", 2),
    ("mta_2023_03_16", "data/emotet/zeek_logs/mta_2023_03_16/conn.log", "10.3.16.101", 2),


    # Clean (Stratosphere Normal captures)
    ("normal_2017_04_18", "data/emotet/zeek_logs/normal_2017_04_18/conn.log", "10.0.2.15", 0),
    ("normal_2017_04_25", "data/emotet/zeek_logs/normal_2017_04_25/conn.log", "10.0.2.15", 0),
    ("normal_2017_04_30", "data/emotet/zeek_logs/normal_2017_04_30/conn.log", "10.0.2.15", 0),
]

OUT_CSV = "data/emotet/emotet_windows.csv"


def read_zeek_fields(conn_log_path: str) -> list[str]:
    """Extract Zeek '#fields' column names from the log header."""
    with open(conn_log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("#fields"):
                parts = line.strip().split("\t")
                return parts[1:]  # drop '#fields'
    raise ValueError(f"Could not find #fields header in: {conn_log_path}")


def load_conn_log(conn_log_path: str) -> pd.DataFrame:
    cols = read_zeek_fields(conn_log_path)
    df = pd.read_csv(
        conn_log_path,
        sep="\t",
        comment="#",
        header=None,
        names=cols,
        low_memory=False,
    )
    return df


def safe_num(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce").fillna(0)
    # Zeek may use '-' for unset fields; above becomes NaN then 0, which is fine for our aggregates
    return s


def build_windows(df: pd.DataFrame, dataset_id: str, host_ip: str, y_value: int) -> pd.DataFrame:
    # Keep only flows originating from the target host IP for this capture
    df = df[df["id.orig_h"] == host_ip].copy()
    if df.empty:
        return pd.DataFrame()

    # numeric conversions
    df["ts"] = safe_num(df["ts"])
    df["duration"] = safe_num(df.get("duration", 0))
    df["orig_bytes"] = safe_num(df.get("orig_bytes", 0))
    df["resp_bytes"] = safe_num(df.get("resp_bytes", 0))
    df["orig_pkts"] = safe_num(df.get("orig_pkts", 0))
    df["resp_pkts"] = safe_num(df.get("resp_pkts", 0))

    # window start (epoch seconds floored to WIN_SECONDS)
    df["window_start"] = (np.floor(df["ts"] / WIN_SECONDS) * WIN_SECONDS).astype("int64")

    # helper flags
    service = df.get("service", pd.Series(["-"] * len(df), index=df.index)).fillna("-").astype(str)
    proto = df.get("proto", pd.Series(["-"] * len(df), index=df.index)).fillna("-").astype(str)
    conn_state = df.get("conn_state", pd.Series(["-"] * len(df), index=df.index)).fillna("-").astype(str)

    df["_is_tcp"] = (proto == "tcp").astype(int)
    df["_is_udp"] = (proto == "udp").astype(int)
    df["_is_dns"] = (service == "dns").astype(int)
    df["_is_ssl"] = (service == "ssl").astype(int)
    df["_is_http"] = (service == "http").astype(int)
    df["_is_rej"] = (conn_state == "REJ").astype(int)
    df["_has_rst"] = conn_state.str.contains("R", regex=False).astype(int)

    # group and aggregate
    g = df.groupby("window_start", sort=True)

    out = pd.DataFrame({
        "dataset_id": dataset_id,
        "window_start": g.size().index.astype("int64"),
        "e_conn_count": g.size().values.astype("int64"),
        "e_unique_dst_ip": g["id.resp_h"].nunique().values.astype("int64"),
        "e_unique_dst_port": g["id.resp_p"].nunique().values.astype("int64"),

        "e_mean_duration": g["duration"].mean().values,
        "e_std_duration": g["duration"].std(ddof=0).fillna(0).values,

        "e_mean_orig_bytes": g["orig_bytes"].mean().values,
        "e_mean_resp_bytes": g["resp_bytes"].mean().values,
        "e_mean_orig_pkts": g["orig_pkts"].mean().values,
        "e_mean_resp_pkts": g["resp_pkts"].mean().values,

        "e_tcp_ratio": (g["_is_tcp"].mean().values),
        "e_udp_ratio": (g["_is_udp"].mean().values),
        "e_dns_ratio": (g["_is_dns"].mean().values),
        "e_ssl_ratio": (g["_is_ssl"].mean().values),
        "e_http_ratio": (g["_is_http"].mean().values),

        "e_rej_ratio": (g["_is_rej"].mean().values),
        "e_rst_ratio": (g["_has_rst"].mean().values),
    })

    # interarrival std per window (beacon-ish regularity)
    inter_std = []
    for w, sub in g:
        ts_sorted = np.sort(sub["ts"].values)
        if ts_sorted.size < 3:
            inter_std.append(0.0)
        else:
            diffs = np.diff(ts_sorted)
            inter_std.append(float(np.std(diffs, ddof=0)))
    out["e_interarrival_std"] = inter_std

    out["y"] = y_value
    return out


def main():
    rows = []
    missing = []
    for dataset_id, path, host_ip, y_value in LOGSETS:
        if not os.path.exists(path):
            missing.append(path)
            continue
        df = load_conn_log(path)
        rows.append(build_windows(df, dataset_id, host_ip, y_value))

    if missing:
        print("WARNING: Missing conn.log files:")
        for p in missing:
            print(" -", p)

    out = pd.concat([r for r in rows if r is not None and not r.empty], ignore_index=True)

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    print("Saved:", OUT_CSV)
    print("shape:", out.shape)
    print("y counts:\n", out["y"].value_counts(dropna=False))


if __name__ == "__main__":
    main()
