# Boston Housing Dataset

## Overview
This directory contains the Boston Housing dataset. This dataset has been intentionally modified to include various data quality issues commonly encountered in real-world data engineering and machine learning projects. Your task is to identify and resolve these issues through exploratory data analysis and data cleaning.

Classic regression dataset used to predict median house values in Boston suburbs. The data was drawn from the Boston Standard Metropolitan Statistical Area (SMSA) in 1970. This dataset is well-known in machine learning but may require formatting adjustments. It's excellent for testing regression models and basic data engineering tasks.

## Data Description
- **Rows:** 516 (includes duplicates)
- **Columns:** 17 (13 features + 1 target + 3 noise columns)
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

## Exercise Objective
This dataset contains intentional data quality problems that need to be identified and resolved. Use your data cleaning and preprocessing skills to prepare this dataset for analysis.

## Use Cases
- Regression: Predict median house values
- Feature engineering: Create interaction features, handle mixed units
- Data preprocessing: Add column headers, handle missing values
- Exploratory data analysis: Understand factors affecting housing prices
- Model comparison: Test various regression algorithms

## Files
- `housing.csv` - The dataset file containing housing data with various data quality issues

---
*This dataset was programmatically generated for educational purposes.*
