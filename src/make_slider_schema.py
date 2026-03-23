# src/make_slider_schema.py

import pandas as pd
import numpy as np
import json

DATA_PATH = "data/updated_file.csv"
OUT_PATH = "outputs/slider_schema.json"

def main():
    df = pd.read_csv(DATA_PATH)

    # Drop non-feature columns
    X = df.drop(columns=["Label", "Query"])

    schema = []

    for col in X.columns:
        values = X[col].dropna()

        p5 = float(np.percentile(values, 5))
        p50 = float(np.percentile(values, 50))
        p95 = float(np.percentile(values, 95))

        is_integer = np.allclose(values, np.round(values))

        schema.append({
            "feature": col,
            "min": p5,
            "max": p95,
            "default": p50,
            "step": 1 if is_integer else "auto"
        })

    with open(OUT_PATH, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"✅ Saved slider schema -> {OUT_PATH}")
    print("\nPreview:")
    print(schema[:5])

if __name__ == "__main__":
    main()