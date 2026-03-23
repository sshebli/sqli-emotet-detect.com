import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MODEL_PATH = "models/rf_sqli.joblib"
OUT_DIR = "outputs/figures"
OUT_PATH = os.path.join(OUT_DIR, "sqli_feature_importance.png")

def safe_mkdir(path: str):
    os.makedirs(path, exist_ok=True)

def main():
    safe_mkdir(OUT_DIR)

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    if not hasattr(model, "feature_importances_"):
        raise ValueError("Model does not support feature_importances_.")

    importances = model.feature_importances_

    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values(by="importance", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.barh(df["feature"], df["importance"])
    ax.set_xlabel("Feature Importance")
    ax.set_title("Feature Importance — SQLi Random Forest")

    plt.tight_layout()
    fig.savefig(OUT_PATH, dpi=300)
    plt.close(fig)

    print("✅ Saved:", OUT_PATH)
    print("\nTop 5 Features:")
    print(df.sort_values(by="importance", ascending=False).head())

if __name__ == "__main__":
    main()