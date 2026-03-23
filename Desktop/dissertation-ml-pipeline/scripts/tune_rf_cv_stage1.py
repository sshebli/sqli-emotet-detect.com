import os, joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

OUT_CSV = "outputs/tuning/stage1_internal_cv.csv"

obj = joblib.load("models/rf_sqli.joblib")
rf_frozen = obj["model"]
feature_names = list(obj["feature_names"])

df = pd.read_csv("data/updated_file.csv")

possible_labels = ["Label","label","y","target","class","is_sqli","sqli","attack","malicious"]
label_col = next((c for c in possible_labels if c in df.columns), None)
if label_col is None:
    raise SystemExit("Stop: label column not found.")
print("Detected label column:", label_col)

X = df[feature_names].copy()
y = df[label_col].copy()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

BASE = rf_frozen.get_params()

# FAST MODE: fewer trees during tuning (final model will go back to 300)
BASE["n_estimators"] = 120

# keep these fixed in stage 1
BASE["max_features"] = "sqrt"
BASE["class_weight"] = "balanced_subsample"

grid = []
for max_depth in [None, 16, 12, 8, 6]:
    for min_samples_leaf in [1, 2, 4]:
        for min_samples_split in [2, 5, 10]:
            params = dict(BASE)
            params.update({
                "max_depth": max_depth,
                "min_samples_leaf": min_samples_leaf,
                "min_samples_split": min_samples_split,
            })
            grid.append(params)

print("Stage 1 candidates:", len(grid))

rows = []
for i, params in enumerate(grid, start=1):
    f1s = []
    for tr, va in cv.split(X, y):
        rf = RandomForestClassifier(**params)
        rf.fit(X.iloc[tr], y.iloc[tr])
        pred = rf.predict(X.iloc[va])
        f1s.append(f1_score(y.iloc[va], pred))
    f1s = np.array(f1s, dtype=float)
    rows.append({
        "cand": i,
        "mean_f1": float(f1s.mean()),
        "std_f1": float(f1s.std(ddof=1)),
        "max_depth": params["max_depth"],
        "min_samples_leaf": params["min_samples_leaf"],
        "min_samples_split": params["min_samples_split"],
        "n_estimators_tune": params["n_estimators"],
        "max_features_fixed": params["max_features"],
        "class_weight_fixed": params["class_weight"],
    })
    if i % 5 == 0 or i == 1 or i == len(grid):
        print(f"[{i:02d}/{len(grid)}] mean={rows[-1]['mean_f1']:.6f} std={rows[-1]['std_f1']:.6f} "
              f"(depth={rows[-1]['max_depth']}, leaf={rows[-1]['min_samples_leaf']}, split={rows[-1]['min_samples_split']})")

out = pd.DataFrame(rows).sort_values(["mean_f1","std_f1"], ascending=[False, True]).reset_index(drop=True)
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
out.to_csv(OUT_CSV, index=False)

print("\n✅ Saved:", OUT_CSV)
print("\nTOP 8:")
print(out.head(8).to_string(index=False))
