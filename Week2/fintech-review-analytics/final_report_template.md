# Customer Experience Analytics for Ethiopian Fintech Apps

## Executive Summary

This report analyzes Google Play Store reviews for Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank. The goal is to identify user sentiment, recurring themes, satisfaction drivers, pain points, and product recommendations.

## 1. Business Problem

Mobile banking reviews provide direct feedback about app reliability, transaction performance, account access, UI quality, and requested features.

## 2. Data Collection Methodology

Reviews were scraped using `google-play-scraper`. The target was at least 400 reviews per bank, with fields for review text, rating, date, bank, and source.

## 3. Data Quality Assessment

Document:

- Total reviews scraped per bank
- Duplicate reviews removed
- Missing values removed
- Final clean dataset size

## 4. Sentiment Analysis Methodology

Initial sentiment classification used VADER because it is lightweight and fast for baseline analysis. A transformer model such as DistilBERT can be added for improved accuracy.

## 5. Thematic Analysis

Reviews were grouped into business themes using keyword rules:

- Account Access Issues
- Transaction Performance
- OTP and Verification
- App Reliability
- UI and Experience
- Feature Requests

## 6. Database Design

The PostgreSQL database contains two tables: `banks` and `reviews`. The `reviews` table stores review text, rating, sentiment, theme, date, and source.

## 7. Key Findings

Add evidence from your generated charts and grouped summaries.

## 8. Bank-Specific Recommendations

### CBE

- Recommendation 1
- Recommendation 2

### BOA

- Recommendation 1
- Recommendation 2

### Dashen

- Recommendation 1
- Recommendation 2

## 9. Ethical Considerations and Limitations

Review data may overrepresent dissatisfied users. Scraping limits, date coverage, language mix, and app-version differences may also affect results.

## 10. Next Steps

- Improve sentiment classification with DistilBERT
- Add topic modeling with NMF or LDA
- Build a dashboard
- Create a support chatbot intent taxonomy
