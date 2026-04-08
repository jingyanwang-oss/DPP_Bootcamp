# Boston Housing - Dirty Dataset

## Overview
This is the "dirty" version of the Boston Housing dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Classic regression dataset used to predict median house values in Boston suburbs. The data was drawn from the Boston Standard Metropolitan Statistical Area (SMSA) in 1970. This dataset is well-known in machine learning but may require formatting adjustments. It's excellent for testing regression models and basic data engineering tasks.

## Data Description
- **Rows:** 506
- **Columns:** 14 (13 features + 1 target)
- **Target Variable:** MEDV (median value of owner-occupied homes in $1000s)
- **Format:** Space-separated values without headers

### Features (in order)
1. **CRIM:** Per capita crime rate by town
2. **ZN:** Proportion of residential land zoned for lots over 25,000 sq.ft.
3. **INDUS:** Proportion of non-retail business acres per town
4. **CHAS:** Charles River dummy variable (1 if tract bounds river; 0 otherwise)
5. **NOX:** Nitric oxides concentration (parts per 10 million)
6. **RM:** Average number of rooms per dwelling
7. **AGE:** Proportion of owner-occupied units built prior to 1940
8. **DIS:** Weighted distances to five Boston employment centers
9. **RAD:** Index of accessibility to radial highways
10. **TAX:** Full-value property-tax rate per $10,000
11. **PTRATIO:** Pupil-teacher ratio by town
12. **B:** 1000(Bk−0.63)² where Bk is the proportion of blacks by town
13. **LSTAT:** Percentage lower status of the population
14. **MEDV:** Median value of owner-occupied homes in $1000s (target variable)

**Note:** The input attributes have a mixture of units, which should be considered during preprocessing.

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 8% in CRIM, NOX, AGE; 4% in MEDV (target variable)
2. Invalid values: Negative CRIM, MEDV = 0 or > 100
3. Outliers: Extreme values in CRIM and TAX (10x-100x)
4. Data type issues: CHAS as both 0/1 and True/False strings
5. Duplicates: 2% duplicate rows
6. Noise columns: Added census_tract_id, data_collection_year, surveyor_id
7. Truncated data: 1% of rows with missing columns (simulating incomplete records)


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
- Regression: Predict median house values
- Feature engineering: Create interaction features, handle mixed units
- Data preprocessing: Add column headers, handle missing values
- Exploratory data analysis: Understand factors affecting housing prices
- Model comparison: Test various regression algorithms

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
