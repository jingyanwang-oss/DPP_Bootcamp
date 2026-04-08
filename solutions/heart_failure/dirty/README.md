# Heart Failure - Dirty Dataset

## Overview
This is the "dirty" version of the Heart Failure dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Unbalanced binary classification dataset with ambiguity in columns and outcome variables. Generally used for binary classification tasks to predict death events, but can also be applied to regression tasks predicting the age of heart attack occurrence. This dataset is valuable for exploring medical risk factors and their relationship to patient outcomes.

## Data Description
- **Rows:** 299
- **Columns:** 13
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

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 12% missing in age, serum_creatinine, serum_sodium (MAR pattern)
2. Data type issues: age and platelets converted to strings with formatting (commas, units)
3. Inconsistent binary encoding: Mix of 0/1, Yes/No, True/False across binary columns
4. Invalid values: Ages outside 0-120, ejection_fraction outside 0-100%
5. Outliers: Extreme values in creatinine_phosphokinase and platelets (10x-100x)
6. Duplicates: 3% duplicate rows with slight variations
7. Noise columns: Added data_entry_timestamp, record_id_hash, source_system
8. Column name issues: Extra whitespace and inconsistent casing


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
- Binary classification: Predict death events based on clinical features
- Regression: Predict age of heart attack occurrence
- Feature importance analysis for medical risk factors
- Exploratory data analysis of cardiovascular health indicators

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
