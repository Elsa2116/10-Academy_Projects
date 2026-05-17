"""Assign sentiment labels and scores to bank app reviews."""

from __future__ import annotations

from pathlib import Path

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

INPUT_PATH = Path("data/processed/clean_reviews.csv")
OUTPUT_PATH = Path("data/processed/reviews_with_sentiment.csv")
REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]


def label_sentiment(score: float) -> str:
    """Convert VADER compound score into a sentiment label."""
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def validate_sentiment_input(input_path: Path, df: pd.DataFrame) -> None:
    """Check that the cleaned review file is ready for sentiment scoring."""
    if df.empty:
        raise ValueError(f"Clean review file contains zero rows: {input_path}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for sentiment analysis: {', '.join(missing_columns)}")

    if df["review"].isna().any():
        raise ValueError("Review text cannot contain missing values before sentiment analysis.")


def build_sentiment_analyzer() -> SentimentIntensityAnalyzer:
    """Create a VADER analyzer, downloading the lexicon only when it is missing."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        if not nltk.download("vader_lexicon", quiet=True):
            raise RuntimeError("Unable to download the VADER lexicon.")

    return SentimentIntensityAnalyzer()


def run_sentiment(input_path: str | Path = INPUT_PATH, output_path: str | Path = OUTPUT_PATH) -> pd.DataFrame:
    """Run VADER sentiment analysis and save the result."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Clean review file not found: {input_path}")

    try:
        analyzer = build_sentiment_analyzer()
    except Exception as exc:
        raise RuntimeError("Unable to initialize VADER sentiment analyzer.") from exc

    try:
        df = pd.read_csv(input_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Clean review file has no readable rows: {input_path}") from exc

    validate_sentiment_input(input_path, df)

    # VADER returns a compound score from -1 to 1; the label thresholds are standard defaults.
    df["sentiment_score"] = df["review"].apply(lambda text: analyzer.polarity_scores(str(text))["compound"])
    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Sentiment analysis complete")
    print(df["sentiment_label"].value_counts())

    return df


if __name__ == "__main__":
    run_sentiment()
