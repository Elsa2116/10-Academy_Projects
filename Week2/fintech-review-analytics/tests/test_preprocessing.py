from pathlib import Path

import pandas as pd

from scripts.preprocess_reviews import clean_reviews


def test_clean_reviews_removes_duplicates_and_missing_values(tmp_path: Path):
    input_path = tmp_path / "raw.csv"
    output_path = tmp_path / "clean.csv"

    raw = pd.DataFrame(
        {
            "review": ["Good app", "Good app", None, "Bad login"],
            "rating": [5, 5, 1, 1],
            "date": ["2026-05-01", "2026-05-01", "2026-05-02", "2026-05-03"],
            "bank": ["CBE", "CBE", "BOA", "Dashen"],
            "source": ["Google Play"] * 4,
        }
    )
    raw.to_csv(input_path, index=False)

    cleaned = clean_reviews(input_path, output_path)

    assert len(cleaned) == 2
    assert list(cleaned.columns) == ["review", "rating", "date", "bank", "source"]
    assert output_path.exists()
