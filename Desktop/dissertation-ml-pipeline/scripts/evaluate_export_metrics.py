import os
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from scripts.config import MODEL_PATH, DATA_PATH, LABEL_COL, OUT_METRICS_DIR


OUT_DIR = OUT_METRICS_DIR
OUT_METRICS_CSV = os.path.join(OUT_DIR, "sqli_metrics.csv")


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

    # predictions
    y_pred = model.predict(X)
    y_score = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else None

    metrics = {
        "model_file": os.path.basename(MODEL_PATH),
        "data_file": os.path.basename(DATA_PATH),
        "n_samples": int(len(y)),
        "n_features": int(X.shape[1]),
        "accuracy": float(accuracy_score(y, y_pred)),
        "precision": float(precision_score(y, y_pred, zero_division=0)),
        "recall": float(recall_score(y, y_pred, zero_division=0)),
        "f1": float(f1_score(y, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, y_score)) if y_score is not None else np.nan,
    }

    out_df = pd.DataFrame([metrics])
    out_df.to_csv(OUT_METRICS_CSV, index=False)

    print("✅ Saved:", OUT_METRICS_CSV)
    print(out_df.to_string(index=False))


if __name__ == "__main__":
    main()