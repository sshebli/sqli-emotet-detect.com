import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

DATA_PATH = "data/unified_multiclass_balanced.csv"
FEATURES_PATH = "outputs/master_features_unified_balanced.json"
OUT_MODEL = "models/rf_unified_multiclass_balanced.joblib"
OUT_METRICS = "outputs/unified_multiclass_balanced_metrics.json"

SEED = 42
CLASS_LABELS = {0: "Normal", 1: "SQLi", 2: "Emotet"}


def main():
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Load data
    df = pd.read_csv(DATA_PATH)
    with open(FEATURES_PATH, "r") as f:
        feature_names = json.load(f)

    X = df[feature_names]
    y = df["y"]

    print(f"Dataset: {DATA_PATH}")
    print(f"Shape: {X.shape}")
    print(f"Class distribution:\n{y.value_counts().sort_index()}")

    # 80/20 stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # Train Random Forest (no class_weight needed — data is already balanced)
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=SEED,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    # Evaluate
    y_pred = rf.predict(X_test)
    report = classification_report(
        y_test, y_pred,
        target_names=["Normal", "SQLi", "Emotet"],
        output_dict=True
    )

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["Normal", "SQLi", "Emotet"]))

    # Save metrics JSON
    metrics = {
        "accuracy": report["accuracy"],
        "classification_report": report,
    }
    with open(OUT_METRICS, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Saved metrics -> {OUT_METRICS}")

    # Save model (raw sklearn object)
    joblib.dump(rf, OUT_MODEL)
    print(f"Saved model -> {OUT_MODEL}")
    print("Done.")


if __name__ == "__main__":
    main()