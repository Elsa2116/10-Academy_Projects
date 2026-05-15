"""Assign simple business themes to reviews using keyword rules."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/reviews_with_sentiment.csv")
OUTPUT_PATH = Path("data/processed/final_reviews.csv")

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


def run_theme_analysis(input_path: str | Path = INPUT_PATH, output_path: str | Path = OUTPUT_PATH) -> pd.DataFrame:
    """Add review IDs and identified themes, then save final processed data."""
    df = pd.read_csv(input_path)
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
