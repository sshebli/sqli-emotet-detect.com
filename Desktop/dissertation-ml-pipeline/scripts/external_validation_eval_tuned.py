import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

INTERNAL_PATH = "data/updated_file.csv"
EXTERNAL_PATH = "data/zenodo_sample_20k_features.csv"

# Tuned hyperparameters (final)
TUNED_PARAMS = {
    "n_estimators": 300,
    "max_depth": 16,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "max_features": 0.5,
    "class_weight": "balanced",
    "bootstrap": True,
    "n_jobs": -1,
    "random_state": 42,
}

FEATURES = [
    'Sentence Length', 'AND Count', 'OR Count', 'UNION Count',
    'Single Quote Count', 'Double Quote Count', 'Constant Value Count',
    'Parentheses Count', 'Special Characters Total'
]

def eval_binary(y_true, y_pred, y_score):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, y_score),
    }

# --- Load internal ---
df_int = pd.read_csv(INTERNAL_PATH)
X_int = df_int[FEATURES]
y_int = df_int["Label"].astype(int)

Xtr, Xte, ytr, yte = train_test_split(
    X_int, y_int, test_size=0.2, random_state=42, stratify=y_int
)

# Train tuned RF on internal train split
rf = RandomForestClassifier(**TUNED_PARAMS)
rf.fit(Xtr, ytr)

# Internal test metrics
y_pred_int = rf.predict(Xte)
y_score_int = rf.predict_proba(Xte)[:, 1]
int_metrics = eval_binary(yte, y_pred_int, y_score_int)

# --- External dataset ---
df_ext = pd.read_csv(EXTERNAL_PATH)
missing = [c for c in (["Label"] + FEATURES) if c not in df_ext.columns]
if missing:
    raise ValueError(f"External dataset missing columns: {missing}")

X_ext = df_ext[FEATURES]
y_ext = df_ext["Label"].astype(int)

y_pred_ext = rf.predict(X_ext)
y_score_ext = rf.predict_proba(X_ext)[:, 1]
ext_metrics = eval_binary(y_ext, y_pred_ext, y_score_ext)

print("\n=== Tuned RF: Internal Test (80/20 split, train on 80%) ===")
for k, v in int_metrics.items():
    print(f"{k}: {v:.6f}")

print("\n=== Tuned RF: External (Zenodo sample 20k) ===")
for k, v in ext_metrics.items():
    print(f"{k}: {v:.6f}")

table = pd.DataFrame([
    {"Dataset": "Internal Test (Tuned)", **int_metrics},
    {"Dataset": "External (Zenodo 20k, Tuned)", **ext_metrics},
])

print("\n=== Table 3 – External Validation (Tuned) ===")
print(table.to_string(index=False))
