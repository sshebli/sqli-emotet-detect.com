import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score
import joblib

# ----------------------------
# Load your saved RF bundle
# ----------------------------
bundle = joblib.load("models/rf_sqli.joblib")
rf_model = bundle["model"]
feature_names = bundle["feature_names"]

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("data/SQLiV3_features.csv")

label_col = "Label"  # confirmed earlier
X = df[feature_names]
y = df[label_col].astype(int)

# ----------------------------
# Train/Test Split (fixed for reproducibility)
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ----------------------------
# 1️⃣ Decision Tree
# ----------------------------
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

dt_train_f1 = f1_score(y_train, dt.predict(X_train))
dt_test_f1 = f1_score(y_test, dt.predict(X_test))

dt_cv = cross_val_score(
    dt, X, y, cv=5, scoring="f1"
)

# ----------------------------
# 2️⃣ Random Forest (retrain clean for fairness)
# ----------------------------
rf = RandomForestClassifier(
    n_estimators=rf_model.n_estimators,
    max_depth=rf_model.max_depth,
    random_state=42
)

rf.fit(X_train, y_train)

rf_train_f1 = f1_score(y_train, rf.predict(X_train))
rf_test_f1 = f1_score(y_test, rf.predict(X_test))

rf_cv = cross_val_score(
    rf, X, y, cv=5, scoring="f1"
)

# ----------------------------
# Results Table
# ----------------------------
results = pd.DataFrame([
    {
        "Model": "Decision Tree",
        "Train F1": dt_train_f1,
        "Test F1": dt_test_f1,
        "CV Mean F1": dt_cv.mean(),
        "CV Std": dt_cv.std()
    },
    {
        "Model": "Random Forest",
        "Train F1": rf_train_f1,
        "Test F1": rf_test_f1,
        "CV Mean F1": rf_cv.mean(),
        "CV Std": rf_cv.std()
    }
])

print("\nVariance Comparison Results:\n")
print(results)

results.to_csv("outputs/metrics/variance_comparison.csv", index=False)
print("\nSaved to outputs/metrics/variance_comparison.csv")