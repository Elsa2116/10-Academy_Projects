"""Insert processed review data into PostgreSQL."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = Path("data/processed/final_reviews.csv")
REQUIRED_COLUMNS = [
    "review",
    "rating",
    "date",
    "bank",
    "source",
    "sentiment_label",
    "sentiment_score",
    "identified_theme",
]

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "bank_reviews"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def validate_database_config() -> None:
    """Ensure database connection settings are present before opening a connection."""
    missing_keys = [key for key, value in DB_CONFIG.items() if value in (None, "")]
    if missing_keys:
        raise ValueError(f"Missing database configuration values: {', '.join(missing_keys)}")


def validate_insert_input(csv_path: Path, df: pd.DataFrame) -> None:
    """Validate final processed data before database insertion."""
    if df.empty:
        raise ValueError(f"Final processed CSV contains zero rows: {csv_path}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for database insert: {', '.join(missing_columns)}")


def insert_data(csv_path: str | Path = CSV_PATH) -> None:
    """Insert final processed review CSV into banks and reviews tables."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Final processed CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    validate_insert_input(csv_path, df)
    validate_database_config()

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for bank in df["bank"].dropna().unique():
            cur.execute(
                """
                INSERT INTO banks (bank_name, app_name)
                VALUES (%s, %s)
                ON CONFLICT (bank_name) DO NOTHING;
                """,
                (bank, f"{bank} Mobile App"),
            )
        conn.commit()

        for _, row in df.iterrows():
            cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s;", (row["bank"],))
            result = cur.fetchone()
            if result is None:
                raise RuntimeError(f"Bank lookup failed for {row['bank']}")
            bank_id = result[0]

            cur.execute(
                """
                INSERT INTO reviews (
                    bank_id,
                    review_text,
                    rating,
                    review_date,
                    sentiment_label,
                    sentiment_score,
                    identified_theme,
                    source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    bank_id,
                    row["review"],
                    int(row["rating"]),
                    row["date"],
                    row.get("sentiment_label"),
                    float(row.get("sentiment_score", 0)),
                    row.get("identified_theme"),
                    row["source"],
                ),
            )

        conn.commit()
    except psycopg2.Error as exc:
        if conn is not None:
            conn.rollback()
        raise RuntimeError("Database insert failed; transaction was rolled back.") from exc
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    print("Data inserted successfully")


if __name__ == "__main__":
    insert_data()
