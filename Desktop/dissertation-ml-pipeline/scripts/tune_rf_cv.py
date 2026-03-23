import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

OUT_CSV = "outputs/tuning/internal_cv_tuning.csv"

# Load frozen artifacts
obj = joblib.load("models/rf_sqli.joblib")
rf_frozen = obj["model"]
feature_names = list(obj["feature_names"])

print("Frozen feature count:", len(feature_names))
print("Frozen feature names (order matters):", feature_names)

# Load dataset
df = pd.read_csv("data/updated_file.csv")

# Detect label column
possible_labels = ["Label", "label", "y", "target", "class", "is_sqli", "sqli", "attack", "malicious"]
label_col = next((c for c in possible_labels if c in df.columns), None)
if label_col is None:
    raise SystemExit("Stop: label column not found. Please set label_col manually.")
print("Detected label column:", label_col)

# Enforce frozen schema
missing = [f for f in feature_names if f not in df.columns]
if missing:
    raise SystemExit(f"Stop: dataset missing frozen features: {missing}")

X = df[feature_names].copy()
y = df[label_col].copy()

print("\nClass distribution (counts):")
print(y.value_counts(dropna=False))

# 5-fold stratified CV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

BASE = rf_frozen.get_params()

# Controlled search space (small, hypothesis-driven)
grid = []
for max_depth in [None, 12, 8, 6]:
    for min_samples_leaf in [1, 2, 4]:
        for min_samples_split in [2, 5, 10]:
            for max_features in ["sqrt", 0.5, 0.75]:
                for class_weight in ["balanced_subsample", "balanced"]:
                    params = dict(BASE)
                    params.update({
                        "max_depth": max_depth,
                        "min_samples_leaf": min_samples_leaf,
                        "min_samples_split": min_samples_split,
                        "max_features": max_features,
                        "class_weight": class_weight,
                    })
                    grid.append(params)

print(f"\nTotal candidates: {len(grid)}")

rows = []
best = None

for i, params in enumerate(grid, start=1):
    fold_f1 = []
    for train_idx, val_idx in cv.split(X, y):
        rf = RandomForestClassifier(**params)
        rf.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = rf.predict(X.iloc[val_idx])
        fold_f1.append(f1_score(y.iloc[val_idx], preds))

    fold_f1 = np.array(fold_f1, dtype=float)
    mean_f1 = float(fold_f1.mean())
    std_f1 = float(fold_f1.std(ddof=1))

    row = {
        "cand": i,
        "mean_f1": mean_f1,
        "std_f1": std_f1,
        "max_depth": params["max_depth"],
        "min_samples_leaf": params["min_samples_leaf"],
        "min_samples_split": params["min_samples_split"],
        "max_features": params["max_features"],
        "class_weight": params["class_weight"],
        "n_estimators": params["n_estimators"],
        "random_state": params["random_state"],
    }
    rows.append(row)

    # selection rule: higher mean_f1, tie-breaker lower std_f1
    if best is None or (mean_f1 > best["mean_f1"]) or (mean_f1 == best["mean_f1"] and std_f1 < best["std_f1"]):
        best = row

    if i % 10 == 0 or i == 1 or i == len(grid):
        print(f"[{i:03d}/{len(grid)}] mean_f1={mean_f1:.6f} std={std_f1:.6f} params="
              f"(depth={row['max_depth']}, leaf={row['min_samples_leaf']}, split={row['min_samples_split']}, "
              f"max_feat={row['max_features']}, cw={row['class_weight']})")

# Save results
out_df = pd.DataFrame(rows).sort_values(["mean_f1", "std_f1"], ascending=[False, True]).reset_index(drop=True)

import os
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
out_df.to_csv(OUT_CSV, index=False)

print("\n✅ Saved:", OUT_CSV)
print("\nTOP 10:")
print(out_df.head(10).to_string(index=False))

print("\nBEST (by rule):")
print(best)
