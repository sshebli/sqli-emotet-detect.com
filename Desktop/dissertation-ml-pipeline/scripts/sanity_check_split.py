import joblib
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

obj = joblib.load("models/rf_sqli.joblib")
rf = obj["model"]
features = obj["feature_names"]

df = pd.read_csv("data/updated_file.csv")
X = df[features]
y = df["Label"]

# Full dataset F1 (this is what you'd get if you evaluated on everything)
full_f1 = f1_score(y, rf.predict(X))
print("Full dataset F1:", full_f1)

# Fresh 80/20 split WITHOUT retraining (true holdout check)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

split_f1 = f1_score(y_test, rf.predict(X_test))
print("Fresh split Test F1 (no retraining):", split_f1)
