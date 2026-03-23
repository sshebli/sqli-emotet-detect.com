from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

MODEL_PATH = "models/rf_sqli.joblib"
SCHEMA_PATH = "outputs/slider_schema.json"
IMPORTANCE_PATH = "outputs/feature_importance.csv"

UNIFIED_MODEL_PATH = "models/rf_unified_multiclass.joblib"
UNIFIED_FEATURES_PATH = "outputs/master_features_unified.json"
UNIFIED_IMPORTANCE_PATH = "outputs/feature_importance_unified.csv"

CLASS_LABELS = {
    0: "Normal",
    1: "SQLi",
    2: "Emotet",
}

HOME_CARD_ASSET_MAP = {
    "sqli-card-image": "SQLi.png",
    "emotet-card-image": "Emotet.png",
    "relationship-card-image": "relationship.png",
    "pipeline-card-image": "pipeline.png",
}

UNIFIED_EMOTET_CONFIG = {
    "e_conn_count": {"min": 0.0, "max": 508.0, "default": 0.0, "step": 1.0},
    "e_dns_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_http_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_interarrival_std": {"min": 0.0, "max": 20.33678, "default": 0.0, "step": 0.1},
    "e_mean_duration": {"min": 0.0, "max": 2071.409, "default": 0.0, "step": 1.0},
    "e_mean_orig_bytes": {"min": 0.0, "max": 53069.25, "default": 0.0, "step": 10.0},
    "e_mean_orig_pkts": {"min": 0.0, "max": 1585.0, "default": 0.0, "step": 1.0},
    "e_mean_resp_bytes": {"min": 0.0, "max": 2478833.0, "default": 0.0, "step": 100.0},
    "e_mean_resp_pkts": {"min": 0.0, "max": 2021.059, "default": 0.0, "step": 1.0},
    "e_rej_ratio": {"min": 0.0, "max": 0.7142857, "default": 0.0, "step": 0.01},
    "e_rst_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_ssl_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_std_duration": {"min": 0.0, "max": 4630.022, "default": 0.0, "step": 1.0},
    "e_tcp_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_udp_ratio": {"min": 0.0, "max": 1.0, "default": 0.0, "step": 0.01},
    "e_unique_dst_ip": {"min": 0.0, "max": 117.0, "default": 0.0, "step": 1.0},
    "e_unique_dst_port": {"min": 0.0, "max": 10.0, "default": 0.0, "step": 1.0},
}

SQLI_DEMO_PRESET = {
    "sentence length": 48.0,
    "and count": 1.0,
    "or count": 1.0,
    "union count": 1.0,
    "single quote count": 1.0,
    "double quote count": 2.0,
    "constant value count": 8.0,
    "parentheses count": 0.0,
    "special characters total": 5.0,
}

EMOTET_DEMO_PRESET = {
    "e_conn_count": 9.0,
    "e_dns_ratio": 0.05,
    "e_http_ratio": 0.05,
    "e_interarrival_std": 0.30,
    "e_mean_duration": 0.0,
    "e_mean_orig_bytes": 30.0,
    "e_mean_orig_pkts": 2.0,
    "e_mean_resp_bytes": 120.0,
    "e_mean_resp_pkts": 3.0,
    "e_rej_ratio": 0.0,
    "e_rst_ratio": 0.0,
    "e_ssl_ratio": 0.0,
    "e_std_duration": 0.0,
    "e_tcp_ratio": 1.0,
    "e_udp_ratio": 0.0,
    "e_unique_dst_ip": 3.0,
    "e_unique_dst_port": 2.0,
}

HYBRID_SQLI_DEMO_PRESET = {
    "sentence length": 24.0,
    "and count": 1.0,
    "or count": 1.0,
    "union count": 0.0,
    "single quote count": 1.0,
    "double quote count": 0.0,
    "constant value count": 3.0,
    "parentheses count": 0.0,
    "special characters total": 2.0,
}

HYBRID_EMOTET_DEMO_PRESET = {
    "e_conn_count": 6.0,
    "e_dns_ratio": 0.03,
    "e_http_ratio": 0.02,
    "e_interarrival_std": 0.20,
    "e_mean_duration": 0.0,
    "e_mean_orig_bytes": 20.0,
    "e_mean_orig_pkts": 1.0,
    "e_mean_resp_bytes": 80.0,
    "e_mean_resp_pkts": 2.0,
    "e_rej_ratio": 0.0,
    "e_rst_ratio": 0.0,
    "e_ssl_ratio": 0.0,
    "e_std_duration": 0.0,
    "e_tcp_ratio": 1.0,
    "e_udp_ratio": 0.0,
    "e_unique_dst_ip": 2.0,
    "e_unique_dst_port": 1.0,
}

TAB_NAMES = ["Home", "Unified Model", "Explainability", "ML Pipeline Content", "Quiz"]
TAB_KEYS = ["home", "unified", "explainability", "pipeline", "quiz"]