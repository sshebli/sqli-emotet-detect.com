# src/inspect_sqliV3.py
import pandas as pd

PATH = "data/SQLiV3.csv"

def main():
    df = pd.read_csv(PATH)

    print("\n=== SHAPE ===")
    print(df.shape)

    print("\n=== COLUMNS ===")
    print(list(df.columns))

    print("\n=== HEAD (first 5 rows) ===")
    print(df.head(5).to_string(index=False))

    print("\n=== LABEL COLUMN TYPE + SAMPLE UNIQUE VALUES ===")
    if "Label" in df.columns:
        print("Label dtype:", df["Label"].dtype)
        # show a few weird values (non 0/1)
        sample = df["Label"].dropna().astype(str)
        non_binary = sample[~sample.isin(["0", "1", "0.0", "1.0"])].head(10)
        print("\nNon-binary Label examples (first 10):")
        print(non_binary.to_string(index=False))

    print("\n=== FIRST ROW RAW VALUES ===")
    print(df.iloc[0].to_dict())

if __name__ == "__main__":
    main()