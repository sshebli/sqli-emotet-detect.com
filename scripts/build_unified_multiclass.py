import os
import json
import pandas as pd

SQLI_PATH = "data/updated_file.csv"
EMOTET_PATH = "data/emotet/emotet_windows.csv"

OUT_UNIFIED = "data/unified_multiclass.csv"
OUT_FEATURES = "outputs/master_features_unified.json"

SEED = 42


def main():
    os.makedirs("outputs", exist_ok=True)

    # --- Load SQLi ---
    sqli = pd.read_csv(SQLI_PATH)
    if "Query" in sqli.columns:
        sqli = sqli.drop(columns=["Query"])

    sqli_feat_cols = [c for c in sqli.columns if c != "Label"]

    # Map labels: 0 stays 0, 1 stays 1
    sqli["y"] = sqli["Label"]
    sqli = sqli.drop(columns=["Label"])

    # --- Load Emotet ---
    em = pd.read_csv(EMOTET_PATH)
    emotet_feat_cols = [c for c in em.columns if c not in ["y", "dataset_id", "window_start"]]

    # Drop metadata columns
    em_clean = em[emotet_feat_cols + ["y"]].copy()

    # --- Build unified feature set ---
    all_features = sorted(set(sqli_feat_cols).union(set(emotet_feat_cols)))

    def align(df):
        for c in all_features:
            if c not in df.columns:
                df[c] = 0
        return df[all_features + ["y"]]

    sqli_aligned = align(sqli.copy())
    em_aligned = align(em_clean.copy())

    unified = pd.concat([sqli_aligned, em_aligned], ignore_index=True)
    unified = unified.sample(frac=1, random_state=SEED).reset_index(drop=True)

    # Save
    unified.to_csv(OUT_UNIFIED, index=False)
    json.dump(all_features, open(OUT_FEATURES, "w"), indent=4)

    print("Saved:", OUT_UNIFIED)
    print("Shape:", unified.shape)
    print("Class counts:\n", unified["y"].value_counts().sort_index())
    print("Features:", len(all_features))
    print("Saved features:", OUT_FEATURES)


if __name__ == "__main__":
    main()