import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from scripts.config import MODEL_PATH, DATA_PATH, LABEL_COL, OUT_FIGURES_DIR


OUT_DIR = OUT_FIGURES_DIR
OUT_PATH = os.path.join(OUT_DIR, "sqli_confusion.png")


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

    y_pred = model.predict(X)

    cm = confusion_matrix(y, y_pred, labels=[0, 1])
    cm_norm = confusion_matrix(y, y_pred, labels=[0, 1], normalize="true")

    # Plot (counts)
    fig, ax = plt.subplots()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Benign (0)", "SQLi (1)"])
    disp.plot(ax=ax, values_format="d", colorbar=False)
    ax.set_title("Confusion Matrix (Counts) — SQLi Random Forest")
    plt.tight_layout()
    fig.savefig(OUT_PATH, dpi=300)
    plt.close(fig)

    tn, fp, fn, tp = cm.ravel()
    print("✅ Saved:", OUT_PATH)
    print(f"TN={tn} FP={fp} FN={fn} TP={tp}")
    print("Normalized (row-wise):")
    print(np.array2string(cm_norm, precision=4, suppress_small=True))


if __name__ == "__main__":
    main()