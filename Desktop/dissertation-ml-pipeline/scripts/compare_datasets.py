import pandas as pd
import hashlib

A_PATH = "data/updated_file.csv"
B_PATH = "data/SQLiV3_features.csv"  # <-- corrected path

FEATURES = [
    'Sentence Length','AND Count','OR Count','UNION Count',
    'Single Quote Count','Double Quote Count','Constant Value Count',
    'Parentheses Count','Special Characters Total'
]

def fingerprint(df: pd.DataFrame, cols):
    s = pd.util.hash_pandas_object(
        df[cols].sort_values(cols).reset_index(drop=True),
        index=False
    ).values
    return hashlib.sha256(s.tobytes()).hexdigest()

df_a = pd.read_csv(A_PATH)
df_b = pd.read_csv(B_PATH)

print("A shape:", df_a.shape, "B shape:", df_b.shape)

# Compare overlap using Query+Label if available
common_cols = [c for c in ["Query", "Label"] if c in df_a.columns and c in df_b.columns]
if len(common_cols) == 2:
    a_pairs = set(map(tuple, df_a[common_cols].astype(str).values))
    b_pairs = set(map(tuple, df_b[common_cols].astype(str).values))
    inter = len(a_pairs & b_pairs)
    union = len(a_pairs | b_pairs)
    print(f"Overlap on (Query,Label): {inter} rows")
    print(f"Jaccard similarity: {inter/union:.6f}")
else:
    print("Could not compare (Query,Label) overlap (missing columns).")

print("Feature fingerprint A:", fingerprint(df_a, FEATURES))
print("Feature fingerprint B:", fingerprint(df_b, FEATURES))
print("Fingerprints match?:", fingerprint(df_a, FEATURES) == fingerprint(df_b, FEATURES))