# Credit Card Approval - Dirty Datasets

## Overview
This directory contains the "dirty" versions of the Credit Card Approval datasets, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. These datasets contain intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

High-dimensionality classification dataset structurally similar to the heart failure dataset but in the financial domain. This dataset contains two related files: application records with applicant information and credit records with payment history. Used for predicting credit card approval decisions and analyzing credit risk factors.

## Data Description

### 1. Application Record Dataset (`application_record.csv`)

- **Rows:** 438,557
- **Columns:** 18
- **Description:** Contains applicant demographic and financial information

#### Features
- **ID:** Unique identifier for each applicant
- **CODE_GENDER:** Gender code (M/F)
- **FLAG_OWN_CAR:** Car ownership flag (Y/N)
- **FLAG_OWN_REALTY:** Realty ownership flag (Y/N)
- **CNT_CHILDREN:** Number of children
- **AMT_INCOME_TOTAL:** Total income amount
- **NAME_INCOME_TYPE:** Income type (Working, Commercial associate, etc.)
- **NAME_EDUCATION_TYPE:** Education level (Higher education, Secondary, etc.)
- **NAME_FAMILY_STATUS:** Family status (Married, Single, etc.)
- **NAME_HOUSING_TYPE:** Housing type (House/apartment, Rented apartment, etc.)
- **DAYS_BIRTH:** Days from birth (negative values)
- **DAYS_EMPLOYED:** Days employed (negative values)
- **FLAG_MOBIL:** Mobile phone flag
- **FLAG_WORK_PHONE:** Work phone flag
- **FLAG_PHONE:** Phone flag
- **FLAG_EMAIL:** Email flag
- **OCCUPATION_TYPE:** Occupation type (may contain missing values)
- **CNT_FAM_MEMBERS:** Number of family members

#### Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 18% OCCUPATION_TYPE, 4% AMT_INCOME_TOTAL, 3% DAYS_EMPLOYED
2. Inconsistent categorical: CODE_GENDER (M/Male/m), FLAG columns (Y/Yes/1)
3. Invalid values: Negative income, CNT_CHILDREN > 10, positive DAYS_EMPLOYED
4. Income formatting: Mix of formats ($50,000, 50000, 50,000.00)
5. Inconsistent capitalization: NAME_* columns with mixed case
6. Duplicates: 2% duplicate application records
7. Noise columns: Added application_source, branch_code, referral_code

### 2. Credit Record Dataset (`credit_record.csv`)

- **Rows:** 1,048,575
- **Columns:** 3
- **Unique IDs:** 45,985
- **Description:** Contains monthly credit payment history for applicants

#### Features
- **ID:** Applicant identifier (links to application_record)
- **MONTHS_BALANCE:** Month balance (negative values indicate months in the past)
- **STATUS:** Payment status
  - **C:** Paid off that month (442,031 records)
  - **0:** 1-29 days past due (383,120 records)
  - **X:** No loan for the month (209,230 records)
  - **1:** 30-59 days past due (11,090 records)
  - **2:** 60-89 days past due (868 records)
  - **3:** 90-119 days past due (320 records)
  - **4:** 120-149 days past due (223 records)
  - **5:** Overdue or bad debts (1,693 records)

#### Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Invalid STATUS codes: 2% with codes A, B, 6, 7, 8, 9 (not in valid range)
2. Data type issues: MONTHS_BALANCE as strings in 10% of rows
3. Duplicates: 3% duplicate credit records
4. Noise columns: Added transaction_id, processing_date

## How to Use These Datasets

These dirty datasets are designed for:
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
- Binary classification: Predict credit card approval
- Credit risk analysis: Analyze factors affecting creditworthiness
- Time series analysis: Analyze payment patterns over time
- Feature engineering: Create aggregated features from credit history
- Data merging: Join application and credit records on ID
- Exploratory data analysis: Understand relationships between demographics and credit behavior

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
