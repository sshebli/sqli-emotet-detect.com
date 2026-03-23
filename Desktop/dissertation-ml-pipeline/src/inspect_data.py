# src/inspect_data.py
import pandas as pd

DATA_PATH = "data/updated_file.csv"

def guess_label_column(cols):
    candidates = ["label", "Label", "class", "Class", "target", "Target", "y", "attack", "is_sqli", "is_sqli_attack"]
    for c in candidates:
        if c in cols:
            return c
    return None

def main():
    df = pd.read_csv(DATA_PATH)

    print("\n=== BASIC INFO ===")
    print("Shape (rows, cols):", df.shape)

    print("\n=== COLUMNS (first 30) ===")
    cols = df.columns.tolist()
    print(cols[:30])
    if len(cols) > 30:
        print(f"... (+{len(cols)-30} more)")

    label_col = guess_label_column(df.columns)

    print("\n=== LABEL GUESS ===")
    if label_col:
        print("Guessed label column:", label_col)
    else:
        print("No obvious label column name found.")
        print("Common fallback: last column might be label ->", cols[-1])

    # If we guessed label, show distribution
    if label_col:
        print("\n=== LABEL DISTRIBUTION ===")
        print(df[label_col].value_counts(dropna=False).head(20))

    print("\n=== SAMPLE ROW ===")
    print(df.head(1).to_string(index=False))

if __name__ == "__main__":
    main()
