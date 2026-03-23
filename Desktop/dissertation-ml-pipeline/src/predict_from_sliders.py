# src/predict_from_sliders.py

import json
import joblib
import pandas as pd
import argparse
import os

MODEL_PATH = "models/rf_sqli.joblib"
SCHEMA_PATH = "outputs/slider_schema.json"
IMPORTANCE_PATH = "outputs/feature_importance.csv"

def feature_to_argname(feature: str) -> str:
    return feature.replace(" ", "_")

def main():
    # Load model bundle
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    # Load slider schema
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)

    # Defaults from schema
    defaults = {item["feature"]: item["default"] for item in schema}

    # CLI
    parser = argparse.ArgumentParser(description="Predict SQLi probability from slider-like feature inputs.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Decision threshold for classifying as SQLi (default=0.5)")

    for item in schema:
        feat = item["feature"]
        arg = "--" + feature_to_argname(feat)
        parser.add_argument(arg, type=float, default=None, help=f"Override {feat} (default={item['default']})")

    args = parser.parse_args()

    # Apply overrides
    overrides = {}
    for item in schema:
        feat = item["feature"]
        argname = feature_to_argname(feat)
        val = getattr(args, argname)
        if val is not None:
            overrides[feat] = val

    final_input = defaults.copy()
    final_input.update(overrides)

    # Ensure correct feature order
    X_one = pd.DataFrame([[final_input[f] for f in feature_names]], columns=feature_names)

    # Predict probability
    proba = float(model.predict_proba(X_one)[0, 1])

    # Decision
    threshold = float(args.threshold)
    decision = "SQLi" if proba >= threshold else "Benign"

    print("\n=== PREDICTION ===")
    print("Overrides:", overrides if overrides else "(none)")
    print(f"SQLi probability: {proba:.4f}")
    print(f"Threshold: {threshold:.2f}")
    print(f"Decision: {decision}")

    # Show global top features (simple explainability panel)
    if os.path.exists(IMPORTANCE_PATH):
        imp = pd.read_csv(IMPORTANCE_PATH).sort_values("importance", ascending=False)
        top3 = imp.head(3)
        print("\nTop 3 global features (from training):")
        for _, row in top3.iterrows():
            print(f"- {row['feature']}: {row['importance']:.4f}")
    else:
        print("\n[WARN] feature_importance.csv not found. Run train_rf.py to generate it.")

if __name__ == "__main__":
    main()