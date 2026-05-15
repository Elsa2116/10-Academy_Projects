"""Assign sentiment labels and scores to bank app reviews."""

from __future__ import annotations

from pathlib import Path

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

INPUT_PATH = Path("data/processed/clean_reviews.csv")
OUTPUT_PATH = Path("data/processed/reviews_with_sentiment.csv")


def label_sentiment(score: float) -> str:
    """Convert VADER compound score into a sentiment label."""
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def run_sentiment(input_path: str | Path = INPUT_PATH, output_path: str | Path = OUTPUT_PATH) -> pd.DataFrame:
    """Run VADER sentiment analysis and save the result."""
    nltk.download("vader_lexicon", quiet=True)
    df = pd.read_csv(input_path)

    analyzer = SentimentIntensityAnalyzer()
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
