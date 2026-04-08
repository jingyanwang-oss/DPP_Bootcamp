# Interview 1 - Live Data Science Coding

## Table of Contents

1. [Overview](#overview)
2. [Key Points](#key-points)
3. [Solution Outline](#solution-outline)
   - [EDA](#eda)
   - [Modeling](#modeling)
   - [Wrap-Up](#wrap-up)
4. [Next Steps](#next-steps)

---

## Overview

This will be a 1 hour coding interview with members of the Databricks team to work through a data science problem. This will take place in the Databricks platform - they will share data and a notebook with you via Databricks Free. The exam is 100 points and the breakdown is __ EDA, __ modeling, and 15 reflection.

## Key Points

- **Dataset Characteristics**: Expect a multi-class classification dataset with severe class imbalance, mix of categorical and numeric variables. Assume very dirty data (missingness/outliers/imbalance/multicollinearity)
- **Ordinal Targets**: Some datasets used also have ordinal categorical targets, you can use an ordinal encoder from sklearn to encode the targets and ensure the ordinality is accounted for at prediction time
- **AI Assistant Usage**: AI Assistant must be used to generate some code (for plotting, etc) or you will not be able to finish in time.
- **Communication**: It's important to think out loud, call things out as you see them and explain that they will need to be addressed and quickly explain how, even if you do not have time to code it up fully

### Data Quality Issues to Watch For

**Missingness**
- This will need to be handled in a robust way. Look for patterns that can give insight on how to handle it - is there a pattern to the missingness that makes sense in the context of the problem
- Just `dropna()` is an instant fail because it is not robust to production inference in cases where there is missingness on new datapoints (dataset is sparse)
- An example of robust handling is by using a pipeline with an imputer (see pipelines example below)

**Class Imbalance**
- Target class will likely be imbalanced. This will need to be addressed before or during modeling
- Expect a multi-class classification with some classes that may only have 1-2 samples
- An example of handling here would be:
  - Oversampling the minority classes (SMOTE or other techniques)
  - Using a model that supports class weighting (most scikit-learn models have a `class_weight='balanced'` flag that can be used to handle this

**Correlation**
- Look out for collinearity or features that are uncorrelated with the target
- Call out that, depending on the algorithm, this can pull weights (Logistic Regression), affect splitting criteria in tree-based models, etc.
- We can either remove the deeply-correlated predictors or use a feature selection method or statistical measure to choose these features
- We can just talk about this if time doesn't allow for implementation

**Outliers**
- Look for any odd distributions that could indicate the presence of outliers that will need to be handled
- Can drop rows if relatively few, or use a technique like isolation forest to determine automatically

## Solution Outline

### EDA

1. **Descriptive Statistics**
   - Look at the descriptive stats, missingness, and distribution of variables
   - Recommend using `dbutils.data.summarize(df)` to quickly do all of this at once using the built-in Databricks functionality
   - Examine these and call out missingness, outliers, and class imbalance

2. **Missingness Analysis**
   - Next, examine missingness - print all rows where one or more elements are missing, see if there is a pattern there that can inform how you fill
   - Decide how you will fill it for your overall pipeline (make sure to say this out loud)

3. **Plotting** (recommend using the AI assistant to generate plotting code for):
   - **Categorical variables**: Bar chart broken out by class
     - Call out any insights here
   - **Numeric variables**: Distribution broken out by class
     - Call out any insights here
   - **Numeric variables**: Correlation
     - Built heatmap to show this
     - Call out any insights here, especially relative predictive value based on correlations, or redundancies among variables

### Modeling

1. **Data Splitting**
   - Before we do anything, we need to split the dataset into train, test, and validation datasets using `train_test_split(df, stratify='y')`
   - It is extremely important to follow this, fitting on the full dataset is an instant fail
   - We should articulate that doing it this way allows us to ensure our model will generalize well by testing on out-of-sample data (validation set) and as we continue to experiment based on those results, have an unbiased final test (test set) before heading into production
   - **Note**: It is possible that some target classes may only have 1 (or < 3) instances, causing an error when attempting to stratify during split. In this case, we will need to slightly oversample those datapoints to make sure they are represented across the 3 classes

2. **Production-Ready Pipelines**
   - For the entire modeling process, it is important that we think about it from a production standpoint, meaning we should be using sklearn pipelines so that all preprocessing/missingness handling is encapsulated in a single pipeline that can be deployed directly as an endpoint and leveraged

3. **Preprocessing Pipeline**
   - For the preprocessing pipeline, I would recommend:
     - **A numeric pipeline** that takes all numeric variables, uses an imputer to impute missing values based on strategy from EDA (median or knn imputation is a good default if no pattern was noticed) and scales the variables
     - **A categorical pipeline** that takes all categorical variables, uses an imputer to impute missing values based on strategy from EDA (most_frequent is a good default if no pattern was noticed) and one-hot encodes the variables
     - A column transformer can be used to combine these two and produce the final preprocessor

   **Sample code:**
   ```python
   numeric_pipeline = Pipeline([
       ('imputer', SimpleImputer(strategy='mean')),
       ('scaler', StandardScaler())
   ])
   categorical_pipeline = Pipeline([
       ('imputer', SimpleImputer(strategy='constant', fill_value=my_fill_value)),
       ('onehot', OneHotEncoder(handle_unknown='ignore'))
   ])
                               
   preprocessor = ColumnTransformer([
       ('numeric', numeric_pipeline, numeric_features),
       ('categorical', categorical_pipeline, categorical_features)
   ])
   ```

4. **Model Experimentation**
   - We want to experiment with several models, each will have its own pipeline which will be fit on and then evaluated using:
     - **Classification metrics**, in particular f1 score
       ```python
       print(classification_report(y_val, rf_pipeline.predict(X_val)))
       ```
     - **Confusion Matrix plot**
       - Recommend generating this with the databricks assistant
   - We need to handle the class imbalance, which means choosing a model that can adjust to class imbalance by weighting classes
   - Finally, we choose based on these metrics the final pipeline, run a test on our test set, and declare this pipeline ready for production.
   - If time allows, we can use MLFlow to log the model and register it, and talk through using Databricks serving to create an endpoint and serve this pipeline

### Wrap-Up

- They will give you a chance at the end to discuss any next steps
- Make a list of the things you did not have time to address/things you would like to improve given more time

## Next Steps

- Pick an open-source, classification dataset and walk through a solution based on the above steps
- Be sure to do this in Databricks and practice using the Databricks AI Assistant to save time
- Make sure your solution follows the solution outline above and that you're able to complete most components in less than an hour
- If you want input on code quality, ask Elena or Steve
- When you feel ready, contact Steve for a mock interview

