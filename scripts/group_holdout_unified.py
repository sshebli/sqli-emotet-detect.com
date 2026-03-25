import os
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score

# --- CONFIG ---
DATA_PATH = "data/unified_multiclass_with_groups.csv"
MODEL_PATH = "models/rf_unified_multiclass.joblib"
FEATURES_PATH = "outputs/master_features_unified.json"
OUT_CSV = "outputs/group_holdout_results.csv"
OUT_TXT = "outputs/group_holdout_report.txt"

# Groups withheld from training
HOLDOUT_GROUPS = {"example5", "mta_2023_03_16", "normal_2017_04_30"}

CLASS_NAMES = ["Normal", "SQLi", "Emotet"]
CLASS_LABELS = [0, 1, 2]
SEED = 42


def main():
    os.makedirs("outputs", exist_ok=True)

    # Load data
    df = pd.read_csv(DATA_PATH)
    if "group_id" not in df.columns:
        raise ValueError("group_id column not found. Use unified_multiclass_with_groups.csv.")

    # Load frozen model and feature list
    rf_frozen = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, "r") as f:
        features = json.load(f)

    # Split by group
    test_mask = df["group_id"].isin(HOLDOUT_GROUPS)
    train_mask = ~test_mask

    df_train = df[train_mask].reset_index(drop=True)
    df_test = df[test_mask].reset_index(drop=True)

    if df_test.empty:
        raise ValueError(f"No rows found for holdout groups: {sorted(HOLDOUT_GROUPS)}")

    print(f"Train rows : {len(df_train)}")
    print(f"Test rows  : {len(df_test)}")
    print(f"\nTest group distribution:\n{df_test['group_id'].value_counts()}")
    print(f"\nTest class distribution:\n{df_test['y'].value_counts().sort_index()}")

    X_train = df_train[features]
    y_train = df_train["y"]
    X_test = df_test[features]
    y_test = df_test["y"]

    # Retrain using frozen hyperparams on training groups only
    params = rf_frozen.get_params()
    rf = RandomForestClassifier(**params)
    rf.fit(X_train, y_train)

    # Evaluate
    y_pred = rf.predict(X_test)

    report_text = classification_report(
        y_test,
        y_pred,
        labels=CLASS_LABELS,
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0,
    )

    report_dict = classification_report(
        y_test,
        y_pred,
        labels=CLASS_LABELS,
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )

    macro_f1 = f1_score(y_test, y_pred, labels=CLASS_LABELS, average="macro", zero_division=0)
    f1_normal = report_dict["Normal"]["f1-score"]
    f1_sqli = report_dict["SQLi"]["f1-score"]
    f1_emotet = report_dict["Emotet"]["f1-score"]

    support_normal = int(report_dict["Normal"]["support"])
    support_sqli = int(report_dict["SQLi"]["support"])
    support_emotet = int(report_dict["Emotet"]["support"])

    print("\n=== Group Holdout Classification Report ===")
    print(report_text)
    print(f"Macro F1  : {macro_f1:.4f}")
    print(f"F1 Normal : {f1_normal:.4f}")
    print(f"F1 SQLi   : {f1_sqli:.4f}")
    print(f"F1 Emotet : {f1_emotet:.4f}")

    # Save summary CSV
    results = pd.DataFrame([{
        "Split": "Group Holdout",
        "Holdout_Groups": str(sorted(HOLDOUT_GROUPS)),
        "Train_Rows": len(df_train),
        "Test_Rows": len(df_test),
        "Support_Normal": support_normal,
        "Support_SQLi": support_sqli,
        "Support_Emotet": support_emotet,
        "Macro_F1": round(macro_f1, 4),
        "F1_Normal": round(f1_normal, 4),
        "F1_SQLi": round(f1_sqli, 4),
        "F1_Emotet": round(f1_emotet, 4),
    }])
    results.to_csv(OUT_CSV, index=False)
    print(f"\nSaved: {OUT_CSV}")

    # Save full report
    with open(OUT_TXT, "w") as f:
        f.write(f"Holdout groups: {sorted(HOLDOUT_GROUPS)}\n")
        f.write(f"Train rows: {len(df_train)}\n")
        f.write(f"Test rows: {len(df_test)}\n\n")
        f.write("Test group distribution:\n")
        f.write(df_test["group_id"].value_counts().to_string())
        f.write("\n\nTest class distribution:\n")
        f.write(df_test["y"].value_counts().sort_index().to_string())
        f.write("\n\n")
        f.write(report_text)
        f.write(f"\nMacro F1  : {macro_f1:.4f}\n")
        f.write(f"F1 Normal : {f1_normal:.4f}\n")
        f.write(f"F1 SQLi   : {f1_sqli:.4f}\n")
        f.write(f"F1 Emotet : {f1_emotet:.4f}\n")
        f.write(
            "\nNote: SQLi support may be zero in this holdout if no SQLi source group "
            "is included in the test split.\n"
        )
    print(f"Saved: {OUT_TXT}")


if __name__ == "__main__":
    main()