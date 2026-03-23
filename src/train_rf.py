# src/train_rf.py

import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    confusion_matrix,
)

DATA_PATH = "data/updated_file.csv"
RANDOM_STATE = 42


def main():
    df = pd.read_csv(DATA_PATH)

    # Target
    y = df["Label"]

    # Features: drop label + raw text query (baseline uses engineered numeric features only)
    X = df.drop(columns=["Label", "Query"])

    print("\nFeatures used:", list(X.columns))

    # 63/37 split (stratified keeps same class ratio in train/test)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.37,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print("Train size:", X_train.shape[0])
    print("Test size:", X_test.shape[0])

    # Model
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )

    rf.fit(X_train, y_train)

    # Predictions
    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)[:, 1]

    # Metrics
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    pr_auc = average_precision_score(y_test, y_proba)

    print("\n=== METRICS ===")
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1:", round(f1, 4))
    print("PR-AUC:", round(pr_auc, 4))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    # Save model artifact
    os.makedirs("models", exist_ok=True)

    joblib.dump(
    {"model": rf, "feature_names": list(X.columns)},
    "models/rf_sqli.joblib"
    )

    print("\nSaved model -> models/rf_sqli.joblib")

    # Feature importance export
    os.makedirs("outputs", exist_ok=True)

    importances = pd.DataFrame({
        "feature": X.columns,
        "importance": rf.feature_importances_
    }).sort_values("importance", ascending=False)

    importances.to_csv("outputs/feature_importance.csv", index=False)

    print("\nTop feature importances:")
    print(importances.head(10).to_string(index=False))
    print("\nSaved feature importance -> outputs/feature_importance.csv")


if __name__ == "__main__":
    main()