"""Clean scraped Google Play reviews."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_INPUT = Path("data/raw/raw_reviews.csv")
CLEAN_OUTPUT = Path("data/processed/clean_reviews.csv")

REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]


def validate_input_file(input_path: Path) -> None:
    """Fail early with a clear message when the raw review CSV is unavailable."""
    if not input_path.exists():
        raise FileNotFoundError(f"Raw review file not found: {input_path}")
    if input_path.stat().st_size == 0:
        raise ValueError(f"Raw review file is empty: {input_path}")


def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Ensure the raw data includes all fields required by downstream tasks."""
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")


def clean_reviews(input_path: str | Path = RAW_INPUT, output_path: str | Path = CLEAN_OUTPUT) -> pd.DataFrame:
    """Clean raw review data and save the required five-column CSV."""
    input_path = Path(input_path)
    validate_input_file(input_path)

    try:
        df = pd.read_csv(input_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Raw review file has no readable rows: {input_path}") from exc

    validate_columns(df, REQUIRED_COLUMNS)

    original_rows = len(df)
    if original_rows == 0:
        raise ValueError("Raw review data contains zero rows.")

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
    if df.empty:
        raise ValueError("No valid reviews remained after preprocessing.")

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
