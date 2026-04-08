# Dataset Catalog

This document provides detailed descriptions of all practice datasets available in this repository. Each dataset is available in both **practice** and **solution** versions for data science and machine learning practice.

> **⚠️ Important:** Please do not look at solutions until you have attempted to solve the data issues yourself. The practice datasets contain intentional data quality problems for you to identify and resolve.

## Available Datasets Summary

| Dataset | Type | Rows (Practice) | Columns (Practice) | Target Task |
|---------|------|----------------|-------------------|-------------|
| Boston Housing | Regression | 516 | 17 | Predict house prices |
| Chocolate Bar Ratings | Regression | 2,580 | 13 | Predict chocolate bar ratings |
| Credit Card Approval | Binary Classification | 447,328 / 1,080,032 | 20 / 5 | Predict credit approval |
| Flight Rating | Regression/Classification | 10,300 | 13 | Predict flight ratings |
| Heart Failure | Binary Classification | 307 | 16 | Predict death events |
| Spam vs Ham | Binary Classification | 5,171 | 7 | Classify emails as spam/ham |
| Spotify | Time Series / EDA | 8,753 / 8,953 | 18 / 17 | Track popularity analysis |
| Titanic | Binary Classification | 908 | 15 | Predict passenger survival |

---

## Boston Housing
**Location:** `datasets/boston_housing/` and `solutions/boston_housing/`

**Description:** Classic regression dataset for predicting house prices based on various town and property characteristics. Well-known but poorly formatted dataset from 1970 Boston SMSA.

**Files:**
- Practice: `datasets/boston_housing/housing.csv` (516 rows, 17 columns, space-separated, no headers)
- Solution: `solutions/boston_housing/clean/housing.csv` (506 rows, 14 columns, space-separated, no headers)

For detailed information, see `datasets/boston_housing/README.md` and `solutions/boston_housing/dirty/README.md`.

---

## Chocolate Bar Ratings
**Location:** `datasets/chocolate_bars/` and `solutions/chocolate_bars/`

**Description:** Regression dataset for predicting chocolate bar ratings based on manufacturer, bean origin, cocoa percentage, and ingredients.

**Files:**
- Practice: `datasets/chocolate_bars/chocolate_bar_ratings.csv` (2,580 rows, 13 columns)
- Solution: `solutions/chocolate_bars/clean/chocolate_bar_ratings.csv` (2,530 rows, 10 columns)

For detailed information, see `datasets/chocolate_bars/README.md` and `solutions/chocolate_bars/dirty/README.md`.

---

## Credit Card Approval
**Location:** `datasets/credit_card_approval/` and `solutions/credit_card_approval/`

**Description:** High-dimensionality classification dataset with two related files: application records and credit payment history.

**Files:**
- Practice:
  - `datasets/credit_card_approval/application_record.csv` (447,328 rows, 20 columns)
  - `datasets/credit_card_approval/credit_record.csv` (1,080,032 rows, 5 columns)
- Solution:
  - `solutions/credit_card_approval/clean/application_record.csv` (438,557 rows, 18 columns)
  - `solutions/credit_card_approval/clean/credit_record.csv` (1,048,575 rows, 3 columns)

For detailed information, see `datasets/credit_card_approval/README.md` and `solutions/credit_card_approval/dirty/README.md`.

---

## Flight Rating
**Location:** `datasets/flight_rating/` and `solutions/flight_rating/`

**Description:** Regression/classification dataset for predicting flight ratings based on customer demographics, travel characteristics, and flight performance metrics.

**Files:**
- Practice: `datasets/flight_rating/flight_rating.csv` (10,300 rows, 13 columns)
- Solution: `solutions/flight_rating/clean/flight_rating.csv` (10,000 rows, 10 columns)

For detailed information, see `datasets/flight_rating/README.md` and `solutions/flight_rating/dirty/README.md`.

---

## Heart Failure Prediction
**Location:** `datasets/heart_failure/` and `solutions/heart_failure/`

**Description:** Unbalanced binary classification dataset for predicting death events. Can also be used for regression on age of heart attack.

**Files:**
- Practice: `datasets/heart_failure/heart_failure_clinical_records_dataset.csv` (307 rows, 16 columns)
- Solution: `solutions/heart_failure/clean/heart_failure_clinical_records_dataset.csv` (299 rows, 13 columns)

For detailed information, see `datasets/heart_failure/README.md` and `solutions/heart_failure/dirty/README.md`.

---

## Spam vs Ham
**Location:** `datasets/spam_ham/` and `solutions/spam_ham/`

**Description:** Unbalanced binary classification dataset for classifying emails as spam or ham based on email text content. Scraped from Enron dataset.

**Files:**
- Practice: `datasets/spam_ham/spam_ham_dataset.csv` (5,171 rows, 7 columns)
- Solution: `solutions/spam_ham/clean/spam_ham_dataset.csv` (5,171 rows, 4 columns)

For detailed information, see `datasets/spam_ham/README.md` and `solutions/spam_ham/dirty/README.md`.

---

## Spotify
**Location:** `datasets/spotify/` and `solutions/spotify/`

**Description:** Well-structured dataset with Spotify track information suitable for time series analysis or exploratory data analysis. Contains two files: recent/contemporary tracks and popular tracks from 2009-2023.

**Files:**
- Practice:
  - `datasets/spotify/spotify_data clean.csv` (8,753 rows, 18 columns)
  - `datasets/spotify/track_data_final.csv` (8,953 rows, 17 columns)
- Solution:
  - `solutions/spotify/clean/spotify_data clean.csv` (8,582 rows, 15 columns)
  - `solutions/spotify/clean/track_data_final.csv` (8,778 rows, 15 columns)

For detailed information, see `datasets/spotify/README.md` and `solutions/spotify/dirty/README.md`.

---

## Titanic Dataset
**Location:** `datasets/titantic/` and `solutions/titantic/`

**Description:** Classic binary classification dataset for predicting passenger survival. Reasonably balanced: 549/891 died vs 342/891 survived.

**Files:**
- Practice: `datasets/titantic/Titanic-Dataset.csv` (908 rows, 15 columns)
- Solution: `solutions/titantic/clean/Titanic-Dataset.csv` (891 rows, 12 columns)

For detailed information, see `datasets/titantic/README.md` and `solutions/titantic/dirty/README.md`.

---

For detailed information about each dataset, see the individual README.md files in each dataset folder or refer to the solution READMEs in `solutions/{dataset}/dirty/README.md` for answer keys.

