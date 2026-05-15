"""Insert processed review data into PostgreSQL."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = Path("data/processed/final_reviews.csv")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "bank_reviews"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def insert_data(csv_path: str | Path = CSV_PATH) -> None:
    """Insert final processed review CSV into banks and reviews tables."""
    df = pd.read_csv(csv_path)

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
        bank_id = cur.fetchone()[0]

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
    cur.close()
    conn.close()
    print("Data inserted successfully")


if __name__ == "__main__":
    insert_data()
