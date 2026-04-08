# Spam vs Ham Dataset

## Overview
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

## Use Cases
- Binary text classification: Classify emails as spam or ham
- Feature engineering: Extract features from text (word counts, TF-IDF, n-grams)
- Natural language processing: Text preprocessing, tokenization, stemming
- Model comparison: Test various classification algorithms (Naive Bayes, SVM, neural networks)
- Unbalanced classification techniques: Handle class imbalance with SMOTE, class weights, etc.

