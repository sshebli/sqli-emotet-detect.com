# src/make_features_sqliV3.py

import re
import pandas as pd
import numpy as np

IN_PATH = "data/SQLiV3.csv"
OUT_PATH = "data/SQLiV3_features.csv"

RE_AND = re.compile(r"\bAND\b", re.IGNORECASE)
RE_OR = re.compile(r"\bOR\b", re.IGNORECASE)
RE_UNION = re.compile(r"\bUNION\b", re.IGNORECASE)

def count_regex(pattern, text: str) -> int:
    return len(pattern.findall(text))

def to_binary(series: pd.Series) -> pd.Series:
    """
    Convert series entries to 0/1 where possible.
    Anything else becomes NaN.
    """
    s = series.astype(str).str.strip()
    s = s.replace({"0.0": "0", "1.0": "1"})
    out = pd.to_numeric(s, errors="coerce")
    out = out.where(out.isin([0, 1]), np.nan)
    return out

def main():
    df = pd.read_csv(IN_PATH)

    # Must have Sentence
    if "Sentence" not in df.columns:
        raise ValueError(f"Expected 'Sentence' column. Columns: {list(df.columns)}")

    # Candidate label columns (we saw labels spread across these)
    candidate_label_cols = [c for c in ["Label", "Unnamed: 2", "Unnamed: 3"] if c in df.columns]
    if not candidate_label_cols:
        raise ValueError(f"No label-like columns found. Columns: {list(df.columns)}")

    # Build a clean label by taking first valid 0/1 across candidate columns
    y_final = None
    for c in candidate_label_cols:
        y_c = to_binary(df[c])
        y_final = y_c if y_final is None else y_final.fillna(y_c)

    before = len(df)
    df["Label_clean"] = y_final
    df = df.dropna(subset=["Label_clean"]).copy()
    after = len(df)

    df["Label_clean"] = df["Label_clean"].astype(int)

    print(f"Rows before: {before}")
    print(f"Rows kept (valid 0/1 label found): {after}")
    print(f"Rows dropped (no valid label): {before - after}")
    print("Label distribution:\n", df["Label_clean"].value_counts())

    s = df["Sentence"].fillna("").astype(str)

    feats = pd.DataFrame({
        "Query": s,
        "Label": df["Label_clean"],

        "Sentence Length": s.str.len(),
        "AND Count": s.apply(lambda x: count_regex(RE_AND, x)),
        "OR Count": s.apply(lambda x: count_regex(RE_OR, x)),
        "UNION Count": s.apply(lambda x: count_regex(RE_UNION, x)),

        "Single Quote Count": s.str.count("'"),
        "Double Quote Count": s.str.count('"'),

        "Constant Value Count": s.str.count(r"\b\d+\b"),
        "Parentheses Count": (s.str.count(r"\(") + s.str.count(r"\)")),
        "Special Characters Total": s.str.count(r"[^A-Za-z0-9\s]"),
    })

    feats.to_csv(OUT_PATH, index=False)
    print(f"\n✅ Saved -> {OUT_PATH}")
    print("Shape:", feats.shape)
    print("Columns:", list(feats.columns))
    print("\nSample row:")
    print(feats.head(1).to_string(index=False))

if __name__ == "__main__":
    main()