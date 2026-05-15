"""Create stakeholder-ready visualizations for the final report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_PATH = Path("data/processed/final_reviews.csv")
FIGURE_DIR = Path("reports/figures")


def plot_sentiment_distribution(df: pd.DataFrame) -> None:
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
    df = pd.read_csv(INPUT_PATH)
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_theme_frequency(df)
    print(f"Charts saved to {FIGURE_DIR}")


if __name__ == "__main__":
    main()
