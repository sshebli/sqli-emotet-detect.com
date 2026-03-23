import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

# Load frozen artifacts
obj = joblib.load("models/rf_sqli.joblib")
feature_names = list(obj["feature_names"])

# Load dataset
df = pd.read_csv("data/updated_file.csv")
X = df[feature_names]
y = df["Label"]

# 5-fold CV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

fold_f1 = []

for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), start=1):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)

    preds = dt.predict(X_val)
    f1 = f1_score(y_val, preds)
    fold_f1.append(f1)

    print(f"Fold {fold} F1: {f1:.6f}")

fold_f1 = np.array(fold_f1, dtype=float)

print("\nDecision Tree CV Mean F1:", float(fold_f1.mean()))
print("Decision Tree CV Std F1:", float(fold_f1.std(ddof=1)))
