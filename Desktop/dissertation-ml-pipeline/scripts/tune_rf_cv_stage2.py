import os, joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

OUT_CSV = "outputs/tuning/stage2_internal_cv.csv"

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
BASE["n_estimators"] = 120  # fast tuning only

# Freeze Stage 1 winner structure:
BASE["max_depth"] = 16
BASE["min_samples_leaf"] = 1
BASE["min_samples_split"] = 2

cands = []
for max_features in ["sqrt", 0.5, 0.75]:
    for class_weight in ["balanced_subsample", "balanced"]:
        params = dict(BASE)
        params["max_features"] = max_features
        params["class_weight"] = class_weight
        cands.append(params)

print("Stage 2 candidates:", len(cands))

rows = []
for i, params in enumerate(cands, start=1):
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
        "max_features": params["max_features"],
        "class_weight": params["class_weight"],
        "n_estimators_tune": params["n_estimators"],
    })
    print(f"[{i}/{len(cands)}] mean={rows[-1]['mean_f1']:.6f} std={rows[-1]['std_f1']:.6f} "
          f"(max_feat={rows[-1]['max_features']}, cw={rows[-1]['class_weight']})")

out = pd.DataFrame(rows).sort_values(["mean_f1","std_f1"], ascending=[False, True]).reset_index(drop=True)
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
out.to_csv(OUT_CSV, index=False)

print("\n✅ Saved:", OUT_CSV)
print("\nRESULTS (sorted):")
print(out.to_string(index=False))
