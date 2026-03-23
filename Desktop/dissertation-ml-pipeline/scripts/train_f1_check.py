import joblib
import pandas as pd
from sklearn.metrics import f1_score

# Load frozen artifacts
obj = joblib.load("models/rf_sqli.joblib")
rf = obj["model"]
feature_names = list(obj["feature_names"])

# Load dataset
df = pd.read_csv("data/updated_file.csv")

X = df[feature_names]
y = df["Label"]

# Train F1 (on full dataset)
train_preds = rf.predict(X)
train_f1 = f1_score(y, train_preds)

print("Train F1:", train_f1)
