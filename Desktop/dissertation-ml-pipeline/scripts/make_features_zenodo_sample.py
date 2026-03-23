import pandas as pd
import re

IN_PATH = "data/zenodo_sample_20k.csv"
OUT_PATH = "data/zenodo_sample_20k_features.csv"

df = pd.read_csv(IN_PATH, low_memory=False)

# Map Zenodo schema -> your project schema (no assumptions)
# Zenodo: full_query, label
# Your pipeline: Query, Label
if "full_query" not in df.columns:
    raise ValueError("Expected column 'full_query' not found in Zenodo sample.")
if "label" not in df.columns:
    raise ValueError("Expected column 'label' not found in Zenodo sample.")

df = df.rename(columns={"full_query": "Query", "label": "Label"})

# Keep only valid binary labels (0/1)
df["Label"] = pd.to_numeric(df["Label"], errors="coerce")
df = df[df["Label"].isin([0, 1])].copy()
df["Label"] = df["Label"].astype(int)

s = df["Query"].astype(str)

# --- Feature engineering (must match your existing logic) ---
# NOTE: If your src/make_features_sqliV3.py uses different exact regexes,
# we will mirror them line-for-line after you paste those specific lines.
df_feat = pd.DataFrame({
    "Query": s,
    "Label": df["Label"],
    "Sentence Length": s.str.len(),
    "AND Count": s.str.count(r"\bAND\b", flags=re.IGNORECASE),
    "OR Count": s.str.count(r"\bOR\b", flags=re.IGNORECASE),
    "UNION Count": s.str.count(r"\bUNION\b", flags=re.IGNORECASE),
    "Single Quote Count": s.str.count("'"),
    "Double Quote Count": s.str.count('"'),
    "Constant Value Count": s.str.count(r"\b\d+\b"),
    "Parentheses Count": s.str.count(r"[()]"),
    "Special Characters Total": s.str.count(r"[^A-Za-z0-9\s]"),
})

df_feat.to_csv(OUT_PATH, index=False)

print("✅ Saved ->", OUT_PATH)
print("Shape:", df_feat.shape)
print("Columns:", list(df_feat.columns))
print("\nLabel distribution:\n", df_feat["Label"].value_counts())
print("\nSample row:\n", df_feat.head(1).to_string(index=False))
