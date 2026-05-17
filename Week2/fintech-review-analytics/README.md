# Fintech Review Analytics

Customer experience analytics for Ethiopian fintech apps using Google Play Store reviews.

This folder contains the Week 2 submission prepared on the `task-2` branch.

This project analyzes reviews for:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The challenge requires scraping, cleaning, sentiment analysis, thematic analysis, PostgreSQL storage, visualization, and business recommendations.

## Project Structure

```text
fintech-review-analytics/
├── .github/workflows/unittests.yml
├── .gitignore
├── .vscode/settings.json
├── README.md
├── requirements.txt
├── schema.sql
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
│   └── figures/
├── scripts/
│   ├── scrape_reviews.py
│   ├── preprocess_reviews.py
│   ├── sentiment_analysis.py
│   ├── thematic_analysis.py
│   ├── visualize_reviews.py
│   └── insert_to_db.py
├── src/
└── tests/
    └── test_preprocessing.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Task 1: Data Collection and Preprocessing

Run scraping:

```bash
python scripts/scrape_reviews.py
```

Run preprocessing:

```bash
python scripts/preprocess_reviews.py
```

Expected clean dataset:

```text
data/processed/clean_reviews.csv
```

Required columns:

```text
review, rating, date, bank, source
```

> Note: Confirm the correct Google Play package names before final submission. If scraping returns fewer than 400 reviews for a bank, document the limitation and try expanding the date range or app version coverage.

## Task 2: Sentiment and Thematic Analysis

Run sentiment analysis:

```bash
python scripts/sentiment_analysis.py
```

Run theme classification:

```bash
python scripts/thematic_analysis.py
```

Expected final processed dataset:

```text
data/processed/final_reviews.csv
```

Expected added columns:

```text
review_id, sentiment_score, sentiment_label, identified_theme
```

Sentiment output evidence is documented in:

```text
reports/sentiment_output_evidence.md
```

The latest verified run applied `sentiment_score` and `sentiment_label` to 1,089 reviews, exceeding the 400-review requirement.

## Task 3: PostgreSQL Database

Create database:

```sql
CREATE DATABASE bank_reviews;
```

Apply schema:

```bash
psql -U postgres -d bank_reviews -f schema.sql
```

Set environment variables in a local `.env` file:

```text
DB_NAME=bank_reviews
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Insert data:

```bash
python scripts/insert_to_db.py
```

Verification queries:

```sql
SELECT b.bank_name, COUNT(*) AS total_reviews
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;
```

```sql
SELECT b.bank_name, ROUND(AVG(r.rating), 2) AS average_rating
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;
```

```sql
SELECT 
    COUNT(*) FILTER (WHERE review_text IS NULL) AS missing_reviews,
    COUNT(*) FILTER (WHERE rating IS NULL) AS missing_ratings,
    COUNT(*) FILTER (WHERE sentiment_label IS NULL) AS missing_sentiment
FROM reviews;
```

## Task 4: Visualizations and Recommendations

Generate plots:

```bash
python scripts/visualize_reviews.py
```

Charts are saved to:

```text
reports/figures/
```

Use `final_report_template.md` to write the final Medium-style report.

## Git Workflow

```bash
git init
git checkout -b task-1
git add .
git commit -m "chore: initialize fintech review analytics project"
```

Recommended branches:

- `task-1`: scraping and preprocessing
- `task-2`: sentiment and thematic analysis
- `task-3`: PostgreSQL storage
- `task-4`: insights, plots, and final report

## Notes and Limitations

- Review data may contain negativity bias because unhappy users are often more motivated to leave reviews.
- Reviews may mix English, Amharic, transliteration, and short informal phrases.
- Google Play scraping may be limited by app availability, package name accuracy, and rate limits.
- VADER is used as a fast baseline. For stronger results, compare it with `distilbert-base-uncased-finetuned-sst-2-english`.
- Pipeline scripts include basic file checks, required-column validation, and clearer error messages for scraping, CSV processing, visualization, and database insertion.
