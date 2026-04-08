# Spam vs Ham - Dirty Dataset

## Overview
This is the "dirty" version of the Spam vs Ham dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Classic unbalanced classification problem where emails must be classified as spam (scammer/unwanted email) or ham (legitimate email) based on text content. This dataset is scraped from the Enron email dataset and is excellent for text classification tasks, feature engineering, and natural language processing applications.

## Data Description
- **Rows:** 5,171
- **Columns:** 4
- **Target Variable:** label (spam/ham)
- **Class Distribution:**
  - Ham (legitimate): 3,672 (71.0%)
  - Spam (unwanted): 1,499 (29.0%)

### Features
- **Unnamed: 0:** Index column
- **label:** Target variable indicating email type (spam/ham)
- **text:** Full email text content
- **label_num:** Numeric encoding of label (0 = ham, 1 = spam)

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Label inconsistencies: Mix of spam/SPAM/Spam and ham/HAM/Ham
2. Label mismatch: 5% of rows have mismatched label and label_num
3. Missing labels: 2% of rows with missing label
4. Text formatting: Extra whitespace in email text
5. Encoding issues: Special characters corrupted (é→Ã©, HTML entities not decoded)
6. Truncated emails: 3% of emails cut off mid-sentence
7. Empty text: 1% of emails contain only whitespace
8. Label noise: 2% of rows with incorrect labels (same text, different label)
9. Noise columns: Added email_id, received_timestamp, sender_ip_address


## How to Use This Dataset

This dirty dataset is designed for:
- **Data Cleaning Practice**: Identify and fix data quality issues
- **EDA Exercises**: Practice exploratory data analysis on messy data
- **Preprocessing Training**: Learn data preprocessing techniques
- **DPP Certification Preparation**: Practice real-world data engineering scenarios

## Recommended Cleaning Steps

1. **Identify Missing Values**: Use `.isna()`, `.isnull()`, or visualization to find missing data patterns
2. **Handle Missing Values**: Decide on imputation strategy (mean, median, mode, or removal)
3. **Fix Data Types**: Convert strings to appropriate numeric types, handle date formats
4. **Standardize Categorical Values**: Normalize case, remove whitespace, map variations to standard values
5. **Remove Duplicates**: Identify and handle duplicate rows
6. **Handle Outliers**: Detect and decide on treatment (remove, cap, or transform)
7. **Remove Invalid Values**: Filter out values outside acceptable ranges
8. **Clean Text Data**: Remove extra whitespace, fix encoding issues
9. **Remove Noise Columns**: Drop irrelevant columns that don't contribute to analysis
10. **Validate Data**: Ensure final dataset meets quality standards

## Comparison with Clean Dataset

Compare your cleaned dataset with the original clean version in the `clean/` folder to verify your data cleaning process.

## Use Cases
- Binary text classification: Classify emails as spam or ham
- Feature engineering: Extract features from text (word counts, TF-IDF, n-grams)
- Natural language processing: Text preprocessing, tokenization, stemming
- Model comparison: Test various classification algorithms (Naive Bayes, SVM, neural networks)
- Unbalanced classification techniques: Handle class imbalance with SMOTE, class weights, etc.

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
