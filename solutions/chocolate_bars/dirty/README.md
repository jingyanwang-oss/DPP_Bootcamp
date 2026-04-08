# Chocolate Bar Ratings - Dirty Dataset

## Overview
This is the "dirty" version of the Chocolate Bar Ratings dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Regression dataset used to predict chocolate bar ratings based on various characteristics including manufacturer, bean origin, cocoa percentage, and ingredients. This dataset contains ratings from chocolate bar reviews and is excellent for exploring factors that influence chocolate quality and taste preferences. The dataset is well-suited for regression tasks, feature engineering, and understanding the relationship between chocolate characteristics and consumer ratings.

## Data Description
- **Rows:** 2,530
- **Columns:** 10 (9 features + 1 target)
- **Target Variable:** rating (chocolate bar rating, typically on a scale of 0-5)
- **Format:** CSV with headers

### Features
1. **id:** Unique identifier for each chocolate bar review
2. **manufacturer:** Manufacturer name or ID
3. **company_location:** Location/country of the manufacturing company
4. **year_reviewed:** Year when the chocolate bar was reviewed
5. **bean_origin:** Country or region where the cocoa beans originated
6. **bar_name:** Name of the chocolate bar
7. **cocoa_percent:** Percentage of cocoa in the chocolate bar
8. **num_ingredients:** Number of ingredients in the chocolate bar
9. **ingredients:** List of ingredients (encoded, e.g., "B,S,C" for Beans, Sugar, Cocoa)
10. **rating:** Target variable - chocolate bar rating (typically 0-5 scale)

**Note:** The ingredients are encoded as abbreviations (B=Beans, S=Sugar, C=Cocoa, L=Lecithin, V=Vanilla, etc.). Some features may contain missing values or require preprocessing.

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 8% manufacturer and bean_origin, 5% ingredients, 3% rating
2. Inconsistent categorical: company_location with mixed case and abbreviations (U.S.A./USA/United States)
3. Invalid values: cocoa_percent outside 0-100, rating outside 0-5, negative num_ingredients
4. Data type issues: cocoa_percent and num_ingredients as strings with formatting (commas, units)
5. Text formatting: Extra whitespace in bar_name, manufacturer
6. Ingredient formatting: Mix of formats (B,S,C vs ['B','S','C'] vs B, S, C)
7. Year inconsistencies: Mix of formats (YYYY vs YYYY-MM-DD) and invalid years
8. Duplicates: 2% duplicate rows
9. Noise columns: Added review_timestamp, reviewer_id, data_source


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
- Regression: Predict chocolate bar ratings based on characteristics
- Feature engineering: Extract insights from ingredient combinations, analyze cocoa percentage effects
- Exploratory data analysis: Understand factors affecting chocolate quality and ratings
- Geographic analysis: Study relationships between bean origin, company location, and ratings
- Time series analysis: Analyze rating trends over years
- Model comparison: Test various regression algorithms

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
