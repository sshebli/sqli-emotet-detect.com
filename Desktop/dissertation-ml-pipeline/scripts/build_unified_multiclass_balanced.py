import os
import json
import pandas as pd

SQLI_PATH = "data/SQLiV3_features.csv"          # swap to updated_file.csv if needed
EMOTET_PATH = "data/emotet/emotet_windows.csv"

OUT_UNIFIED = "data/unified_multiclass_balanced.csv"
OUT_FEATURES = "outputs/master_features_unified_balanced.json"

SEED = 42

# Target per-class counts for balancing (kept modest to avoid huge upsampling noise)
# We will:
# - take N SQLi samples (Label==1)
# - take N Emotet samples (y==2)
# - take N Normal samples (from both sources combined)
TARGET_PER_CLASS = 555  # equals current Emotet positives; edit later if Emotet increases

def main():
    os.makedirs("outputs", exist_ok=True)

    # --- Load SQLi engineered features ---
    sqli = pd.read_csv(SQLI_PATH)
    # drop raw text column if present (not a numeric feature)
    if 'Query' in sqli.columns:
        sqli = sqli.drop(columns=['Query'])
    if "Label" not in sqli.columns:
        raise ValueError(f"'Label' not found in {SQLI_PATH}")

    # SQLi dataset assumed binary: 0 normal, 1 sqli
    sqli_attacks = sqli[sqli["Label"] == 1].copy()
    sqli_normals = sqli[sqli["Label"] == 0].copy()

    # Keep only the SQLi feature columns that exist in unified schema
    sqli_feat_cols = [c for c in sqli.columns if c != "Label"]

    # Map into unified label space
    sqli_attacks["y"] = 1
    sqli_normals["y"] = 0

    # --- Load Emotet windows ---
    em = pd.read_csv(EMOTET_PATH)
    if "y" not in em.columns:
        raise ValueError(f"'y' not found in {EMOTET_PATH}")
    emotet_attacks = em[em["y"] == 2].copy()
    emotet_normals = em[em["y"] == 0].copy()

    emotet_feat_cols = [c for c in em.columns if c not in ["y", "dataset_id", "window_start"]]

    # --- Build unified feature set (union of both) ---
    all_features = sorted(set(sqli_feat_cols).union(set(emotet_feat_cols)))

    def align(df: pd.DataFrame) -> pd.DataFrame:
        # ensure all feature columns exist
        for c in all_features:
            if c not in df.columns:
                df[c] = 0
        return df[all_features + ["y"]]

    # --- Sample per class ---
    # Emotet attacks are the limiting class.
    n = min(TARGET_PER_CLASS, len(emotet_attacks))
    if n < 50:
        raise ValueError(f"Too few Emotet attack samples ({len(emotet_attacks)}). Increase Emotet extraction first.")

    # Sample attacks
    sqli_attacks_s = sqli_attacks.sample(n=min(n, len(sqli_attacks)), random_state=SEED)
    emotet_attacks_s = emotet_attacks.sample(n=n, random_state=SEED)

    # Sample normals from a pool (SQLi normals + Emotet normals)
    normals_pool = pd.concat([sqli_normals, emotet_normals], ignore_index=True)
    normals_pool = normals_pool.sample(frac=1, random_state=SEED)  # shuffle
    normals_s = normals_pool.sample(n=n, random_state=SEED)

    # Align schemas
    parts = [align(sqli_attacks_s), align(emotet_attacks_s), align(normals_s)]
    unified = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)

    # Save
    unified.to_csv(OUT_UNIFIED, index=False)
    json.dump(all_features, open(OUT_FEATURES, "w"), indent=4)

    print("Saved:", OUT_UNIFIED)
    print("Shape:", unified.shape)
    print("Class counts:\n", unified["y"].value_counts().sort_index())
    print("Num features:", len(all_features))
    print("Saved features:", OUT_FEATURES)

if __name__ == "__main__":
    main()
