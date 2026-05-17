from pathlib import Path

import pandas as pd
import pytest

from scripts.sentiment_analysis import run_sentiment
from scripts.thematic_analysis import run_theme_analysis


def test_run_sentiment_rejects_missing_review_column(tmp_path: Path):
    input_path = tmp_path / "clean.csv"
    output_path = tmp_path / "sentiment.csv"

    pd.DataFrame(
        {
            "rating": [5],
            "date": ["2026-05-01"],
            "bank": ["CBE"],
            "source": ["Google Play"],
        }
    ).to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        run_sentiment(input_path, output_path)


def test_run_theme_analysis_rejects_missing_sentiment_columns(tmp_path: Path):
    input_path = tmp_path / "sentiment.csv"
    output_path = tmp_path / "final.csv"

    pd.DataFrame(
        {
            "review": ["Fast transfer"],
            "rating": [5],
            "date": ["2026-05-01"],
            "bank": ["CBE"],
            "source": ["Google Play"],
        }
    ).to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        run_theme_analysis(input_path, output_path)
