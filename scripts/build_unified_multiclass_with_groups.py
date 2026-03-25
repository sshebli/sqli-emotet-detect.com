import os
import json
import pandas as pd

SQLI_PATH = "data/updated_file.csv"
EMOTET_PATH = "data/emotet/emotet_windows.csv"

OUT_UNIFIED = "data/unified_multiclass_with_groups.csv"
OUT_FEATURES = "outputs/master_features_unified.json"

SEED = 42


def main():
    os.makedirs("outputs", exist_ok=True)

    # -----------------------------
    # Load SQLi data
    # -----------------------------
    sqli = pd.read_csv(SQLI_PATH)

    if "Label" not in sqli.columns:
        raise ValueError("Expected 'Label' column in SQLi dataset.")

    if "Query" in sqli.columns:
        sqli = sqli.drop(columns=["Query"])

    sqli_feat_cols = [c for c in sqli.columns if c != "Label"]

    # Map SQLi labels into unified target
    # 0 -> Normal, 1 -> SQLi
    sqli["y"] = sqli["Label"]
    sqli["group_id"] = "sqli_SQLiV3"
    sqli = sqli.drop(columns=["Label"])

    # -----------------------------
    # Load Emotet/normal data
    # -----------------------------
    em = pd.read_csv(EMOTET_PATH)

    required_em_cols = {"dataset_id", "y"}
    missing_em = required_em_cols - set(em.columns)
    if missing_em:
        raise ValueError(f"Missing required columns in Emotet dataset: {sorted(missing_em)}")

    emotet_feat_cols = [
        c for c in em.columns
        if c not in ["y", "dataset_id", "window_start"]
    ]

    # Preserve dataset source as group_id
    em_clean = em[emotet_feat_cols + ["y", "dataset_id"]].copy()
    em_clean = em_clean.rename(columns={"dataset_id": "group_id"})

    # -----------------------------
    # Build shared feature schema
    # -----------------------------
    all_features = sorted(set(sqli_feat_cols).union(set(emotet_feat_cols)))

    def align(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for c in all_features:
            if c not in df.columns:
                df[c] = 0
        return df[all_features + ["y", "group_id"]]

    sqli_aligned = align(sqli)
    em_aligned = align(em_clean)

    # -----------------------------
    # Combine and shuffle
    # -----------------------------
    unified = pd.concat([sqli_aligned, em_aligned], ignore_index=True)
    unified = unified.sample(frac=1, random_state=SEED).reset_index(drop=True)

    # -----------------------------
    # Save outputs
    # -----------------------------
    unified.to_csv(OUT_UNIFIED, index=False)

    # Save feature schema too, to keep it aligned with unified training
    with open(OUT_FEATURES, "w") as f:
        json.dump(all_features, f, indent=4)

    print("Saved:", OUT_UNIFIED)
    print("Shape:", unified.shape)

    print("\nClass counts:")
    print(unified["y"].value_counts().sort_index())

    print("\nGroup counts:")
    print(unified["group_id"].value_counts())

    print("\nClass counts by group:")
    print(pd.crosstab(unified["group_id"], unified["y"]))

    print("\nFeatures:", len(all_features))
    print("Saved features:", OUT_FEATURES)


if __name__ == "__main__":
    main()