"""Clean scraped Google Play reviews."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_INPUT = Path("data/raw/raw_reviews.csv")
CLEAN_OUTPUT = Path("data/processed/clean_reviews.csv")

REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]


def clean_reviews(input_path: str | Path = RAW_INPUT, output_path: str | Path = CLEAN_OUTPUT) -> pd.DataFrame:
    """Clean raw review data and save the required five-column CSV."""
    df = pd.read_csv(input_path)

    original_rows = len(df)
    df = df.drop_duplicates(subset=["review", "bank"])
    after_duplicates = len(df)

    df = df.dropna(subset=["review", "rating"])
    after_missing = len(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df.dropna(subset=["date"])

    df["review"] = df["review"].astype(str).str.strip()
    df = df[df["review"] != ""]

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])
    df["rating"] = df["rating"].astype(int)

    df = df[REQUIRED_COLUMNS]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Preprocessing summary")
    print("---------------------")
    print(f"Original rows: {original_rows}")
    print(f"After removing duplicates: {after_duplicates}")
    print(f"After dropping missing review/rating: {after_missing}")
    print(f"Final rows: {len(df)}")
    print(f"Saved cleaned data to {output_path}")

    return df


if __name__ == "__main__":
    clean_reviews()
