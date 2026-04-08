# Titanic Dataset

## Overview
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

## Use Cases
- Binary classification: Predict passenger survival
- Feature engineering: Extract titles from names, create family size features
- Missing value imputation: Handle missing Age and Cabin values
- Categorical encoding: Encode Sex, Embarked, and Pclass features
- Exploratory data analysis: Understand factors influencing survival rates

