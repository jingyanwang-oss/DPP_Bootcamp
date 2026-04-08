# Titanic - Dirty Dataset

## Overview
This is the "dirty" version of the Titanic dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Classic machine learning dataset used for binary classification of passenger survival. This dataset is one of the most well-known introductory datasets in data science and machine learning, providing a balanced mix of categorical and numerical features. The dataset is reasonably balanced, making it suitable for learning classification techniques.

## Data Description
- **Rows:** 891
- **Columns:** 12
- **Target Variable:** Survived (binary: 0 = did not survive, 1 = survived)
- **Class Distribution:**
  - Did not survive (0): 549 (61.6%)
  - Survived (1): 342 (38.4%)

### Features
- **PassengerId:** Unique identifier for each passenger
- **Survived:** Target variable indicating survival (0 = No, 1 = Yes)
- **Pclass:** Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd)
- **Name:** Passenger name
- **Sex:** Passenger sex (male/female)
- **Age:** Passenger age (may contain missing values)
- **SibSp:** Number of siblings/spouses aboard
- **Parch:** Number of parents/children aboard
- **Ticket:** Ticket number
- **Fare:** Passenger fare
- **Cabin:** Cabin number (may contain missing values)
- **Embarked:** Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 28% Age, 82% Cabin, 8% Embarked, 5% Fare
2. Inconsistent categorical: Sex (male/Male/M), Embarked (C/Cherbourg), Pclass (1/First/1st)
3. Text formatting: Extra whitespace in Name, Ticket, Cabin
4. Invalid values: Negative Fare/SibSp/Parch, Age outside 0-120
5. Duplicates: 2% duplicate rows
6. Noise columns: Added booking_reference, check_in_time, travel_agent_code


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
- Binary classification: Predict passenger survival
- Feature engineering: Extract titles from names, create family size features
- Missing value imputation: Handle missing Age and Cabin values
- Categorical encoding: Encode Sex, Embarked, and Pclass features
- Exploratory data analysis: Understand factors influencing survival rates

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
