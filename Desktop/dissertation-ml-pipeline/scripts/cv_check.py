import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Load frozen artifacts
obj = joblib.load("models/rf_sqli.joblib")
rf_frozen = obj["model"]
feature_names = list(obj["feature_names"])

print("Frozen feature count:", len(feature_names))
print("Frozen feature names (order matters):", feature_names)

# Load dataset
df = pd.read_csv("data/updated_file.csv")
print("\nDataset shape:", df.shape)
print("Columns:", list(df.columns))

# Detect label column (based on your columns, it should be 'Label')
possible_labels = ["Label", "label", "y", "target", "class", "is_sqli", "sqli", "attack", "malicious"]
label_col = next((c for c in possible_labels if c in df.columns), None)

if label_col is None:
    print("\n❗Label column not found automatically.")
    print("Candidate label-like columns (<=5 unique values):")
    for c in df.columns:
        uniq = df[c].nunique(dropna=True)
        if uniq <= 5 and c not in feature_names:
            print(f" - {c} (unique={uniq}, sample_values={df[c].dropna().unique()[:10]})")
    raise SystemExit("Stop: please choose label column from above.")
else:
    print("\nDetected label column:", label_col)

# Enforce frozen schema
missing = [f for f in feature_names if f not in df.columns]
if missing:
    raise SystemExit(f"Stop: dataset missing frozen features: {missing}")

X = df[feature_names].copy()
y = df[label_col].copy()

# Class distribution
print("\nClass distribution (counts):")
print(y.value_counts(dropna=False))
print("\nClass distribution (percent):")
print((y.value_counts(normalize=True, dropna=False) * 100).round(3))

# 5-fold stratified CV using identical RF hyperparameters (no tuning)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

fold_f1 = []
for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), start=1):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    rf = RandomForestClassifier(**rf_frozen.get_params())
    rf.fit(X_train, y_train)

    preds = rf.predict(X_val)
    f1 = f1_score(y_val, preds)
    fold_f1.append(f1)

    print(f"Fold {fold} F1: {f1:.6f}")

fold_f1 = np.array(fold_f1, dtype=float)
print("\n5-fold CV Mean F1:", float(fold_f1.mean()))
print("5-fold CV Std F1:", float(fold_f1.std(ddof=1)))
