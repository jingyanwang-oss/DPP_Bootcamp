# Chocolate Bar Ratings Dataset

## Overview
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

## Use Cases
- Regression: Predict chocolate bar ratings based on characteristics
- Feature engineering: Extract insights from ingredient combinations, analyze cocoa percentage effects
- Exploratory data analysis: Understand factors affecting chocolate quality and ratings
- Geographic analysis: Study relationships between bean origin, company location, and ratings
- Time series analysis: Analyze rating trends over years
- Model comparison: Test various regression algorithms

