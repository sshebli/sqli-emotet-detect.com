import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# FINAL tuned configuration
FINAL_PARAMS = {
    "n_estimators": 300,
    "max_depth": 16,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "max_features": 0.5,
    "class_weight": "balanced",
    "random_state": 42,
    "bootstrap": True,
    "n_jobs": -1
}

obj = joblib.load("models/rf_sqli.joblib")
feature_names = list(obj["feature_names"])

df = pd.read_csv("data/updated_file.csv")

possible_labels = ["Label","label","y","target","class","is_sqli","sqli","attack","malicious"]
label_col = next((c for c in possible_labels if c in df.columns), None)
if label_col is None:
    raise SystemExit("Label column not found.")

X = df[feature_names]
y = df[label_col]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

f1s = []
for fold, (tr, va) in enumerate(cv.split(X, y), start=1):
    rf = RandomForestClassifier(**FINAL_PARAMS)
    rf.fit(X.iloc[tr], y.iloc[tr])
    pred = rf.predict(X.iloc[va])
    f1 = f1_score(y.iloc[va], pred)
    f1s.append(f1)
    print(f"Fold {fold} F1: {f1:.6f}")

f1s = np.array(f1s, dtype=float)
print("\nFINAL 5-fold Mean F1:", float(f1s.mean()))
print("FINAL 5-fold Std F1:", float(f1s.std(ddof=1)))
