# Flight Rating Dataset

## Overview
This directory contains the Flight Rating dataset. This dataset has been intentionally modified to include various data quality issues commonly encountered in real-world data engineering and machine learning projects. Your task is to identify and resolve these issues through exploratory data analysis and data cleaning.

Regression/classification dataset used to predict flight ratings based on customer demographics, travel characteristics, and flight performance metrics. This dataset contains customer flight experience data and is excellent for understanding factors that influence passenger satisfaction. The dataset is well-suited for both regression (predicting rating scores) and classification (predicting rating categories) tasks, as well as feature engineering and customer behavior analysis.

## Data Description
- **Rows:** 10,300 (includes duplicates)
- **Columns:** 13 (9 features + 1 target + 3 noise columns)
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

## Exercise Objective
This dataset contains intentional data quality problems that need to be identified and resolved. Use your data cleaning and preprocessing skills to prepare this dataset for analysis.

## Use Cases
- Regression: Predict flight ratings based on customer and flight characteristics
- Classification: Classify flights into rating categories (e.g., low/medium/high satisfaction)
- Feature engineering: Create interaction features, analyze delay impact on ratings
- Customer segmentation: Understand different customer types and their satisfaction patterns
- Exploratory data analysis: Identify factors most strongly correlated with flight satisfaction
- Business analysis: Analyze how flight class, delays, and customer type affect ratings
- Model comparison: Test various regression and classification algorithms

## Files
- `flight_rating.csv` - The dataset file containing flight data with various data quality issues

---
*This dataset was programmatically generated for educational purposes.*

