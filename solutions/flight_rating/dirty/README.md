# Flight Rating - Dirty Dataset

## Overview
This is the "dirty" version of the Flight Rating dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Regression/classification dataset used to predict flight ratings based on customer demographics, travel characteristics, and flight performance metrics. This dataset contains customer flight experience data and is excellent for understanding factors that influence passenger satisfaction. The dataset is well-suited for both regression (predicting rating scores) and classification (predicting rating categories) tasks, as well as feature engineering and customer behavior analysis.

## Data Description
- **Rows:** 10,000
- **Columns:** 10 (9 features + 1 target)
- **Target Variable:** Rating (flight rating, typically on a scale of 0-5)
- **Format:** CSV with headers

### Features
1. **ID:** Unique identifier for each flight record
2. **Gender:** Passenger gender (Male/Female)
3. **Age:** Passenger age
4. **Customer_Type:** Type of customer (First-time/Returning)
5. **Type_of_Travel:** Purpose of travel (Business/Personal)
6. **Class:** Flight class (Business/Economy/Economy Plus)
7. **Flight_Distance:** Distance of the flight in miles/kilometers
8. **Departure_Delay:** Departure delay in minutes
9. **Arrival_Delay:** Arrival delay in minutes
10. **Rating:** Target variable - flight rating (typically 0-5 scale)

**Note:** Some features may contain missing values (e.g., Customer_Type may have null values). Delay times are measured in minutes, with 0 indicating no delay. The dataset includes a mix of categorical and numerical features that may require encoding and scaling.

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 5% Customer_Type, 8% Age, 3% Rating
2. Inconsistent categorical: Gender (Male/male/M/MALE), Type_of_Travel, Class with mixed case
3. Invalid values: Age outside 0-120, negative delays, Rating outside 0-5, negative Flight_Distance
4. Data type issues: Age, Flight_Distance, delays as strings with formatting (commas, units)
5. Text formatting: Extra whitespace in categorical columns
6. Customer_Type inconsistencies: First-time vs First time vs FirstTime
7. Duplicates: 3% duplicate rows
8. Noise columns: Added booking_id, flight_number, system_timestamp


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
- Regression: Predict flight ratings based on customer and flight characteristics
- Classification: Classify flights into rating categories (e.g., low/medium/high satisfaction)
- Feature engineering: Create interaction features, analyze delay impact on ratings
- Customer segmentation: Understand different customer types and their satisfaction patterns
- Exploratory data analysis: Identify factors most strongly correlated with flight satisfaction
- Business analysis: Analyze how flight class, delays, and customer type affect ratings
- Model comparison: Test various regression and classification algorithms

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
