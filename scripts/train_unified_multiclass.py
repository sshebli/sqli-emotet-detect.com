import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    f1_score,
    roc_auc_score,
    average_precision_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_PATH = "data/unified_multiclass.csv"
FEATURES_PATH = "outputs/master_features_unified.json"
OUT_MODEL = "models/rf_unified_multiclass.joblib"
OUT_REPORT = "outputs/metrics/unified_classification_report.csv"
OUT_AUC = "outputs/metrics/unified_auc_pr.csv"
OUT_COMPARISON = "outputs/metrics/unified_model_comparison.csv"
OUT_CV = "outputs/metrics/unified_cross_validation.csv"
OUT_IMPORTANCE = "outputs/feature_importance_unified.csv"

SEED = 42
CLASS_LABELS = {0: "Normal", 1: "SQLi", 2: "Emotet"}


def main():
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs/metrics", exist_ok=True)

    # Load data
    df = pd.read_csv(DATA_PATH)
    with open(FEATURES_PATH, "r") as f:
        feature_names = json.load(f)

    X = df[feature_names]
    y = df["y"]

    print(f"Dataset: {DATA_PATH}")
    print(f"Shape: {X.shape}")
    print(f"Class distribution:\n{y.value_counts().sort_index()}")
    print(f"Features: {len(feature_names)}")

    # 80/20 stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=SEED,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    # Predictions
    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)

    # Classification report
    report = classification_report(
        y_test,
        y_pred,
        target_names=["Normal", "SQLi", "Emotet"],
        output_dict=True,
    )
    report_df = pd.DataFrame(report).T
    report_df.to_csv(OUT_REPORT)
    print("\n=== Classification Report ===")
    print(report_df.to_string())

    # AUC per class (one-vs-rest)
    auc_rows = []
    for cls_idx, cls_name in CLASS_LABELS.items():
        y_bin = (y_test == cls_idx).astype(int)
        roc = roc_auc_score(y_bin, y_proba[:, cls_idx])
        pr = average_precision_score(y_bin, y_proba[:, cls_idx])
        auc_rows.append({"": cls_name, "ROC_AUC": roc, "PR_AUC": pr})

    auc_df = pd.DataFrame(auc_rows)
    auc_df.to_csv(OUT_AUC, index=False)
    print("\n=== AUC ===")
    print(auc_df.to_string(index=False))

    # Logistic Regression comparison
    lr = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            max_iter=5000,
            random_state=SEED,
            class_weight="balanced",
            solver="lbfgs",
        ),
    )
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    comparison = pd.DataFrame(
        [
            {
                "Model": "Logistic Regression",
                "Macro_F1": f1_score(y_test, lr_pred, average="macro"),
                "F1_Normal": f1_score(y_test == 0, lr_pred == 0),
                "F1_SQLi": f1_score(y_test == 1, lr_pred == 1),
                "F1_Emotet": f1_score(y_test == 2, lr_pred == 2),
            },
            {
                "Model": "Random Forest",
                "Macro_F1": f1_score(y_test, y_pred, average="macro"),
                "F1_Normal": f1_score(y_test == 0, y_pred == 0),
                "F1_SQLi": f1_score(y_test == 1, y_pred == 1),
                "F1_Emotet": f1_score(y_test == 2, y_pred == 2),
            },
        ]
    )
    comparison.to_csv(OUT_COMPARISON, index=False)
    print("\n=== Model Comparison ===")
    print(comparison.to_string(index=False))

    # 5-fold cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    cv_scores = []
    for fold, (tr, va) in enumerate(cv.split(X, y), start=1):
        rf_cv = RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=SEED,
            n_jobs=-1,
        )
        rf_cv.fit(X.iloc[tr], y.iloc[tr])
        pred = rf_cv.predict(X.iloc[va])
        macro = f1_score(y.iloc[va], pred, average="macro")
        cv_scores.append({"Fold": fold, "Macro_F1": macro})
        print(f"Fold {fold}: Macro F1 = {macro:.6f}")

    cv_df = pd.DataFrame(cv_scores)
    cv_df.to_csv(OUT_CV, index=False)
    print(
        f"\nCV Mean: {cv_df['Macro_F1'].mean():.6f}, "
        f"Std: {cv_df['Macro_F1'].std():.6f}"
    )

    # Feature importance
    imp_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": rf.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    imp_df.to_csv(OUT_IMPORTANCE, index=False)

    # Save model (raw sklearn object, consistent with how dashboard loads it)
    joblib.dump(rf, OUT_MODEL)
    print(f"\nSaved model -> {OUT_MODEL}")
    print("Done.")


if __name__ == "__main__":
    main()