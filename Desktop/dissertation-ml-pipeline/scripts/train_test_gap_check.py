import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

OBJ_PATH = "models/rf_sqli.joblib"
DATA_PATH = "data/updated_file.csv"

# Load frozen artifacts
obj = joblib.load(OBJ_PATH)
rf_frozen = obj["model"]
features = list(obj["feature_names"])

df = pd.read_csv(DATA_PATH)
X = df[features]
y = df["Label"].astype(int)

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Re-train a fresh RF using frozen hyperparams on TRAIN ONLY
rf = RandomForestClassifier(**rf_frozen.get_params())
rf.fit(Xtr, ytr)

# Compute F1 on train and test
train_f1 = f1_score(ytr, rf.predict(Xtr))
test_f1  = f1_score(yte, rf.predict(Xte))
gap = train_f1 - test_f1

print("Train F1 (on 80% train split):", f"{train_f1:.6f}")
print("Test F1  (on 20% holdout)    :", f"{test_f1:.6f}")
print("Train–Test Gap               :", f"{gap:.6f}")
