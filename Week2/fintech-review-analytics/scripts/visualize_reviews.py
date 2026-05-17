"""Create stakeholder-ready visualizations for the final report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("data/processed/final_reviews.csv")
FIGURE_DIR = Path("reports/figures")
REQUIRED_COLUMNS = ["bank", "rating", "sentiment_label", "identified_theme"]


def validate_visualization_input(input_path: Path, df: pd.DataFrame) -> None:
    """Confirm the final dataset has the columns required by all charts."""
    if df.empty:
        raise ValueError(f"Final review file contains zero rows: {input_path}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for visualization: {', '.join(missing_columns)}")


def plot_sentiment_distribution(df: pd.DataFrame) -> None:
    """Save a stacked bar chart comparing sentiment labels by bank."""
    sentiment_counts = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)
    ax = sentiment_counts.plot(kind="bar", stacked=True, figsize=(10, 6))
    ax.set_title("Sentiment Distribution by Bank")
    ax.set_xlabel("Bank")
    ax.set_ylabel("Number of Reviews")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "sentiment_distribution_by_bank.png")
    plt.close()


def plot_rating_distribution(df: pd.DataFrame) -> None:
    """Save a grouped bar chart showing rating volume by bank."""
    rating_counts = df.groupby(["bank", "rating"]).size().unstack(fill_value=0)
    ax = rating_counts.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Rating Distribution by Bank")
    ax.set_xlabel("Bank")
    ax.set_ylabel("Number of Reviews")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "rating_distribution_by_bank.png")
    plt.close()


def plot_theme_frequency(df: pd.DataFrame) -> None:
    """Save one horizontal theme-frequency chart per bank."""
    theme_counts = df.groupby(["bank", "identified_theme"]).size().reset_index(name="count")
    for bank in df["bank"].unique():
        bank_counts = theme_counts[theme_counts["bank"] == bank].sort_values("count", ascending=True)
        ax = bank_counts.plot(kind="barh", x="identified_theme", y="count", legend=False, figsize=(10, 6))
        ax.set_title(f"Theme Frequency for {bank}")
        ax.set_xlabel("Number of Reviews")
        ax.set_ylabel("Theme")
        plt.tight_layout()
        safe_bank = str(bank).lower().replace(" ", "_")
        plt.savefig(FIGURE_DIR / f"theme_frequency_{safe_bank}.png")
        plt.close()


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Final review file not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    validate_visualization_input(INPUT_PATH, df)
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_theme_frequency(df)
    print(f"Charts saved to {FIGURE_DIR}")


if __name__ == "__main__":
    main()
