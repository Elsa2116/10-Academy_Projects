"""Scrape Google Play Store reviews for Ethiopian bank apps."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews


# TODO: Confirm app package names from each Google Play Store URL before final submission.
APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp",
}

RAW_DIR = Path("data/raw")
RAW_OUTPUT = RAW_DIR / "raw_reviews.csv"


def scrape_bank_reviews(bank_name: str, app_id: str, count: int = 450) -> pd.DataFrame:
    """Scrape reviews for one bank app and return a standardized dataframe."""
    if not bank_name or not app_id:
        raise ValueError("Bank name and Google Play app id are required.")
    if count <= 0:
        raise ValueError("Review count must be greater than zero.")

    try:
        result, _ = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=count,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to scrape reviews for {bank_name} ({app_id}).") from exc

    rows = [
        {
            "review": item.get("content"),
            "rating": item.get("score"),
            "date": item.get("at"),
            "bank": bank_name,
            "source": "Google Play",
        }
        for item in result
    ]

    return pd.DataFrame(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_reviews: list[pd.DataFrame] = []

    for bank_name, app_id in APPS.items():
        print(f"Scraping {bank_name} from app id {app_id}...")
        bank_reviews = scrape_bank_reviews(bank_name, app_id)
        print(f"Collected {len(bank_reviews)} reviews for {bank_name}")
        all_reviews.append(bank_reviews)

    final_df = pd.concat(all_reviews, ignore_index=True)
    if final_df.empty:
        raise RuntimeError("No reviews were collected from Google Play.")

    final_df.to_csv(RAW_OUTPUT, index=False)
    print(f"Saved {len(final_df)} raw reviews to {RAW_OUTPUT}")


if __name__ == "__main__":
    main()
