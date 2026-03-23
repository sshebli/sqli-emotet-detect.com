import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score

from scripts.config import MODEL_PATH, DATA_PATH, LABEL_COL, OUT_FIGURES_DIR


OUT_DIR = OUT_FIGURES_DIR
OUT_PATH = os.path.join(OUT_DIR, "sqli_roc.png")


def safe_mkdir(path: str):
    os.makedirs(path, exist_ok=True)


def main():
    safe_mkdir(OUT_DIR)

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    df = pd.read_csv(DATA_PATH)

    # y
    if LABEL_COL not in df.columns:
        raise ValueError(f"Expected label column '{LABEL_COL}' in {DATA_PATH}")
    y = df[LABEL_COL].astype(int).values

    # X (enforce exact feature schema + order)
    missing = [f for f in feature_names if f not in df.columns]
    if missing:
        raise ValueError(f"Missing expected features in {DATA_PATH}: {missing}")
    X = df[feature_names].copy()

    if not hasattr(model, "predict_proba"):
        raise ValueError("Model does not support predict_proba (needed for ROC curve).")

    y_score = model.predict_proba(X)[:, 1]

    fpr, tpr, _ = roc_curve(y, y_score)
    auc_score = roc_auc_score(y, y_score)

    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, label=f"AUC = {auc_score:.4f}")
    ax.plot([0, 1], [0, 1], linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve — SQLi Random Forest")
    ax.legend(loc="lower right")

    plt.tight_layout()
    fig.savefig(OUT_PATH, dpi=300)
    plt.close(fig)

    print("✅ Saved:", OUT_PATH)
    print(f"AUC = {auc_score:.6f}")


if __name__ == "__main__":
    main()