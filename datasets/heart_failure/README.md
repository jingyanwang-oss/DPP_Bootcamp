# Heart Failure Dataset

## Overview
This directory contains the Heart Failure dataset. This dataset has been intentionally modified to include various data quality issues commonly encountered in real-world data engineering and machine learning projects. Your task is to identify and resolve these issues through exploratory data analysis and data cleaning.

Unbalanced binary classification dataset with ambiguity in columns and outcome variables. Generally used for binary classification tasks to predict death events, but can also be applied to regression tasks predicting the age of heart attack occurrence. This dataset is valuable for exploring medical risk factors and their relationship to patient outcomes.

## Data Description
- **Rows:** 307 (includes duplicates)
- **Columns:** 16 (13 original + 3 noise columns)
- **Target Variable:** DEATH_EVENT (binary: 0 = survived, 1 = death event)
- **Class Distribution:** 
  - Survived (0): 203 (67.9%)
  - Death Event (1): 96 (32.1%)

### Features
- **age:** Patient age
- **anaemia:** Presence of anaemia (binary)
- **creatinine_phosphokinase:** Level of CPK enzyme in blood (mcg/L)
- **diabetes:** Presence of diabetes (binary)
- **ejection_fraction:** Percentage of blood leaving the heart at each contraction
- **high_blood_pressure:** Presence of high blood pressure (binary)
- **platelets:** Platelet count in blood (kiloplatelets/mL)
- **serum_creatinine:** Level of serum creatinine in blood (mg/dL)
- **serum_sodium:** Level of serum sodium in blood (mEq/L)
- **sex:** Patient sex (binary: 0 = female, 1 = male)
- **smoking:** Smoking status (binary)
- **time:** Follow-up period (days)
- **DEATH_EVENT:** Target variable indicating death event during follow-up period

## Exercise Objective
This dataset contains intentional data quality problems that need to be identified and resolved. Use your data cleaning and preprocessing skills to prepare this dataset for analysis.

## Use Cases
- Binary classification: Predict death events based on clinical features
- Regression: Predict age of heart attack occurrence
- Feature importance analysis for medical risk factors
- Exploratory data analysis of cardiovascular health indicators

## Files
- `heart_failure_clinical_records_dataset.csv` - The dataset file containing clinical records with various data quality issues

---
*This dataset was programmatically generated for educational purposes.*
