import os
import json
import pandas as pd

SQLI_PATH = "data/updated_file.csv"
EMOTET_PATH = "data/emotet/emotet_windows.csv"

OUT_UNIFIED = "data/unified_multiclass_balanced.csv"
OUT_FEATURES = "outputs/master_features_unified_balanced.json"

SEED = 42
TARGET_PER_CLASS = 2190  # equals Emotet positive count


def main():
    os.makedirs("outputs", exist_ok=True)

    # --- Load SQLi ---
    sqli = pd.read_csv(SQLI_PATH)
    if "Query" in sqli.columns:
        sqli = sqli.drop(columns=["Query"])

    sqli_attacks = sqli[sqli["Label"] == 1].copy()
    sqli_normals = sqli[sqli["Label"] == 0].copy()

    sqli_feat_cols = [c for c in sqli.columns if c != "Label"]

    sqli_attacks["y"] = 1
    sqli_normals["y"] = 0

    # --- Load Emotet ---
    em = pd.read_csv(EMOTET_PATH)
    emotet_attacks = em[em["y"] == 2].copy()
    emotet_normals = em[em["y"] == 0].copy()

    emotet_feat_cols = [c for c in em.columns if c not in ["y", "dataset_id", "window_start"]]

    # --- Unified feature set ---
    all_features = sorted(set(sqli_feat_cols).union(set(emotet_feat_cols)))

    def align(df):
        for c in all_features:
            if c not in df.columns:
                df[c] = 0
        return df[all_features + ["y"]]

    # --- Sample per class ---
    n = min(TARGET_PER_CLASS, len(emotet_attacks))
    if n < 50:
        raise ValueError(f"Too few Emotet samples ({len(emotet_attacks)}).")

    sqli_attacks_s = sqli_attacks.sample(n=min(n, len(sqli_attacks)), random_state=SEED)
    emotet_attacks_s = emotet_attacks.sample(n=n, random_state=SEED)

    normals_pool = pd.concat([sqli_normals, emotet_normals], ignore_index=True)
    normals_s = normals_pool.sample(n=n, random_state=SEED)

    parts = [align(sqli_attacks_s), align(emotet_attacks_s), align(normals_s)]
    unified = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)

    unified.to_csv(OUT_UNIFIED, index=False)
    json.dump(all_features, open(OUT_FEATURES, "w"), indent=4)

    print("Saved:", OUT_UNIFIED)
    print("Shape:", unified.shape)
    print("Class counts:\n", unified["y"].value_counts().sort_index())
    print("Features:", len(all_features))
    print("Saved features:", OUT_FEATURES)


if __name__ == "__main__":
    main()