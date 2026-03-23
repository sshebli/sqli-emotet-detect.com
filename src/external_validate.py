# src/external_validate.py

import pandas as pd
import joblib
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score, confusion_matrix

MODEL_PATH = "models/rf_sqli.joblib"
VAL_PATH = "data/SQLiV3_features.csv"

def main():
    bundle = joblib.load(MODEL_PATH)
    rf = bundle["model"]
    feature_names = bundle["feature_names"]

    df = pd.read_csv(VAL_PATH)

    # detect label column
    if "Label" in df.columns:
        label_col = "Label"
    elif "label" in df.columns:
        label_col = "label"
    else:
        label_col = df.columns[-1]  # fallback

    y = df[label_col]
    X = df.drop(columns=[label_col])

    # keep only model features in the right order
    missing = [f for f in feature_names if f not in X.columns]
    extra = [c for c in X.columns if c not in feature_names]

    print("\n=== EXTERNAL VALIDATION DATA CHECK ===")
    print("Rows/Cols:", df.shape)
    print("Label column:", label_col)
    print("Missing features:", missing)
    print("Extra columns (ignored):", extra[:10], f"(+{max(0, len(extra)-10)} more)")

    if missing:
        print("\n❌ Cannot evaluate: SQLiV3.csv is missing required feature columns.")
        print("Fix: make SQLiV3 have the SAME 9 feature columns as training data.")
        return

    X = X[feature_names]

    y_pred = rf.predict(X)
    y_proba = rf.predict_proba(X)[:, 1]

    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    pr_auc = average_precision_score(y, y_proba)
    cm = confusion_matrix(y, y_pred)

    print("\n=== EXTERNAL VALIDATION METRICS ===")
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1:", round(f1, 4))
    print("PR-AUC:", round(pr_auc, 4))
    print("\nConfusion Matrix:")
    print(cm)

if __name__ == "__main__":
    main()