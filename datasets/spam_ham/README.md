# Spam vs Ham Dataset

## Overview
This directory contains the Spam vs Ham dataset. This dataset has been intentionally modified to include various data quality issues commonly encountered in real-world data engineering and machine learning projects. Your task is to identify and resolve these issues through exploratory data analysis and data cleaning.

Classic unbalanced classification problem where emails must be classified as spam (scammer/unwanted email) or ham (legitimate email) based on text content. This dataset is scraped from the Enron email dataset and is excellent for text classification tasks, feature engineering, and natural language processing applications.

## Data Description
- **Rows:** 5,171
- **Columns:** 7 (4 original + 3 noise columns)
- **Target Variable:** label (spam/ham)
- **Class Distribution:**
  - Ham (legitimate): 3,672 (71.0%)
  - Spam (unwanted): 1,499 (29.0%)

### Features
- **Unnamed: 0:** Index column
- **label:** Target variable indicating email type (spam/ham)
- **text:** Full email text content
- **label_num:** Numeric encoding of label (0 = ham, 1 = spam)

## Exercise Objective
This dataset contains intentional data quality problems that need to be identified and resolved. Use your data cleaning and preprocessing skills to prepare this dataset for analysis.

## Use Cases
- Binary text classification: Classify emails as spam or ham
- Feature engineering: Extract features from text (word counts, TF-IDF, n-grams)
- Natural language processing: Text preprocessing, tokenization, stemming
- Model comparison: Test various classification algorithms (Naive Bayes, SVM, neural networks)
- Unbalanced classification techniques: Handle class imbalance with SMOTE, class weights, etc.

## Files
- `spam_ham_dataset.csv` - The dataset file containing email data with various data quality issues

---
*This dataset was programmatically generated for educational purposes.*
