import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from sklearn.model_selection import train_test_split

OBJ_PATH = "models/rf_sqli.joblib"
INTERNAL_PATH = "data/updated_file.csv"
EXTERNAL_PATH = "data/zenodo_sample_20k_features.csv"

def eval_binary(y_true, y_pred, y_score):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, y_score),
    }

# Load frozen artifacts
obj = joblib.load(OBJ_PATH)
rf = obj["model"]
features = list(obj["feature_names"])

# --- Internal test (same split rule as before) ---
df_int = pd.read_csv(INTERNAL_PATH)
X_int = df_int[features]
y_int = df_int["Label"]

Xtr, Xte, ytr, yte = train_test_split(
    X_int, y_int, test_size=0.2, random_state=42, stratify=y_int
)

y_pred_int = rf.predict(Xte)
y_score_int = rf.predict_proba(Xte)[:, 1]
int_metrics = eval_binary(yte, y_pred_int, y_score_int)

# --- External dataset ---
df_ext = pd.read_csv(EXTERNAL_PATH)
# ensure schema
missing = [c for c in (["Label"] + features) if c not in df_ext.columns]
if missing:
    raise ValueError(f"External dataset missing columns: {missing}")

X_ext = df_ext[features]
y_ext = df_ext["Label"].astype(int)

y_pred_ext = rf.predict(X_ext)
y_score_ext = rf.predict_proba(X_ext)[:, 1]
ext_metrics = eval_binary(y_ext, y_pred_ext, y_score_ext)

# Print results
print("\n=== Internal Test (updated_file.csv, 80/20 split, random_state=42) ===")
for k, v in int_metrics.items():
    print(f"{k}: {v:.6f}")

print("\n=== External (Zenodo sample 20k, balanced 10k/10k) ===")
for k, v in ext_metrics.items():
    print(f"{k}: {v:.6f}")

# Table 3 output
table = pd.DataFrame([
    {"Dataset": "Internal Test", **int_metrics},
    {"Dataset": "External (Zenodo 20k sample)", **ext_metrics},
])

print("\n=== Table 3 – External Validation ===")
print(table.to_string(index=False))
