"""Assign simple business themes to reviews using keyword rules."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/reviews_with_sentiment.csv")
OUTPUT_PATH = Path("data/processed/final_reviews.csv")
REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source", "sentiment_score", "sentiment_label"]

THEME_KEYWORDS = {
    "Account Access Issues": ["login", "password", "pin", "signin", "sign in", "account", "fingerprint"],
    "Transaction Performance": ["transfer", "transaction", "send", "receive", "slow", "loading", "delay"],
    "OTP and Verification": ["otp", "verification", "code", "sms"],
    "App Reliability": ["crash", "bug", "error", "failed", "not working", "freeze"],
    "UI and Experience": ["ui", "interface", "easy", "design", "user friendly", "simple"],
    "Feature Requests": ["feature", "add", "budget", "fingerprint", "update", "improve"],
}


def identify_theme(review: str) -> str:
    """Map a review to the first matching business theme."""
    review_lower = str(review).lower()
    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in review_lower for keyword in keywords):
            return theme
    return "Other"


def validate_theme_input(input_path: Path, df: pd.DataFrame) -> None:
    """Validate sentiment-enriched data before assigning business themes."""
    if df.empty:
        raise ValueError(f"Sentiment review file contains zero rows: {input_path}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for theme analysis: {', '.join(missing_columns)}")

    if df["review"].isna().any():
        raise ValueError("Review text cannot contain missing values before theme analysis.")


def run_theme_analysis(input_path: str | Path = INPUT_PATH, output_path: str | Path = OUTPUT_PATH) -> pd.DataFrame:
    """Add review IDs and identified themes, then save final processed data."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Sentiment review file not found: {input_path}")

    try:
        df = pd.read_csv(input_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Sentiment review file has no readable rows: {input_path}") from exc

    validate_theme_input(input_path, df)

    # Keyword rules keep theme assignment transparent for business reviewers.
    df["identified_theme"] = df["review"].apply(identify_theme)

    if "review_id" not in df.columns:
        df.insert(0, "review_id", range(1, len(df) + 1))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Theme analysis complete")
    print(df["identified_theme"].value_counts())

    return df


if __name__ == "__main__":
    run_theme_analysis()
