# DPP Exam Experience - Francisco Morales
**Date:** January 14, 2026  
**Duration:** 60 minutes  
**Result:** Failed

**Reason for Failure:** Left an ID column in the dataset, which should have been removed as it would cause data leakage similar to the restaurant name column.

---

## Exam Setup

- **No introductions** - The proctor began immediately without formal introductions
- **Time constraint:** 60 minutes total
- **AI Assistant usage:** Used AI assistant for **all coding** and QA'd the generated code. Memorized prompting strategies and what was needed for each section to work efficiently. **It is required to be able to use AI effectively to write the required code for completion.**
- **Communication style:** Both **code completion** and **concept understanding/decision making** are required. While AI was used for all coding, the proctor was **less concerned about manually writing code** but **still expected effective use of AI to generate the necessary code**. The proctor was **more focused on concepts, decisions, and overall understanding** - demonstrating that you understand what code to generate, why you're generating it, and what decisions you're making throughout the process.

---

## Dataset Details

**Dataset Type:** Restaurant Ratings  
**Target Variable:** Rating column (0-5 scale)  
**Note:** This dataset is very similar to the [Chocolate Bar Ratings dataset](../datasets/chocolate_bars/) in this repository - both are regression/rating prediction problems with mixed data types.

**Key Characteristics:**
- Mixed data types (numeric and categorical columns)
- Restaurant name column that functioned as a unique identifier
- **Important:** Restaurant name column was removed entirely as it would cause data leakage

---

## EDA Approach (60 points - ~30 minutes)

I allocated approximately half of my time to Exploratory Data Analysis, speaking through all findings in detail.

### Quick Data Overview
- Used `dbutils.data.summarize(df)` to quickly review the dataset structure
- This Databricks built-in function provided comprehensive statistics efficiently

### Missing Value Analysis
- Performed thorough analysis on missing values
- Identified patterns and determined appropriate imputation strategies

### Outlier Detection
- Used **IsolationForest** to quickly identify outliers
- Later removed outliers due to small percentage (didn't significantly impact dataset size)

### Correlation Analysis
- Created correlation heatmap to identify multicollinearity
- Used this to inform feature selection decisions

### Feature Selection
- Performed **multivariate analysis using RandomForest** to identify most impactful variables
- This approach helped reduce the feature space effectively
- Spoke through the rationale for each feature selection decision

---

## Modeling Approach (25 points ~20 mins)

### Preprocessing Pipeline

Built a comprehensive sklearn pipeline:

**Numeric Features:**
- Imputation: Median strategy
- Scaling: StandardScaler

**Categorical Features:**
- Imputation: Missing values filled with "unknown"
- Encoding: OneHotEncoder

### Model Selection Strategy

**Key Insight:** While this appeared to be a multiclass classification problem, the target variable was a **rating column (0-5)**, making it an **ordinal classification** problem.

**Solution:** Used **Ordinal Classification** with **MAE (Mean Absolute Error)** as the evaluation metric, which is more appropriate for ordinal targets than standard classification metrics.

### Models Built

Implemented three models using different algorithms:
1. **XGBoost (XGB)** - Gradient boosting
2. **Random Forest (RF) Regressor** - Tree-based ensemble
3. **LightGBM (LGBM)** - Gradient boosting with leaf-wise growth

All models were configured for ordinal regression/classification.

---

## Reflection (15 points ~10 mins)

- Spoke through all decisions made throughout the exam
- Used AI Assistant to generate assumptions and wrap-up content for this section
- Articulated the reasoning behind each major choice:
  - Feature removal (restaurant name)
  - Outlier handling
  - Feature selection approach
  - Model selection (ordinal classification vs. standard classification)
  - Evaluation metric choice (MAE)

### Modeling Improvements Discussed

- **Hyperparameter Tuning:** Discussed the importance of tuning hyperparameters such as:
  - Learning rate, max_depth, n_estimators for gradient boosting models (XGB, LGBM)
  - n_estimators, max_depth, min_samples_split for Random Forest
  - Methods like GridSearchCV or Hyperopt for systematic hyperparameter optimization
- **Model Ensemble:** Mentioned potential improvements through ensemble methods combining the three models
- **Cross-Validation:** Discussed using k-fold cross-validation for more robust model evaluation
- **Regularization:** Addressed overfitting concerns (particularly with Random Forest) and discussed regularization techniques
- **Feature Engineering:** Expanded on potential feature engineering opportunities beyond what was implemented

---

## Key Questions Asked by Proctor

The proctor was particularly interested in academic understanding and theoretical knowledge. Key questions included:

1. **"What does stratify mean?"**
   - Testing understanding of stratified sampling in train/test splits

2. **"Explain why you decided to remove the underrepresented sample class and add the class back into the dataset after stratifying"**
   - Understanding of class imbalance handling and stratification requirements

3. **"What happens when a categorical variable makes the dataset wider than it is long?"**
   - Knowledge of the curse of dimensionality and one-hot encoding implications

4. **"Explain why you chose Ordinal Regression vs. other solutions"**
   - Understanding of when ordinal classification is appropriate vs. standard classification or regression

5. **"If I wanted to leave the restaurant name in the dataset, how could we feature engineer it to make it relevant?"**
   - Creative problem-solving and feature engineering knowledge
   - Potential answers: extract chain information, location-based features, popularity metrics, etc.

6. **"Why did RF overfit to the dataset?"**
   - Understanding of tree-based model behavior, overfitting causes, and regularization techniques

---

## Key Takeaways

### What Worked Well

1. **Time Management:** Allocating ~50% of time to EDA allowed thorough understanding of the data
2. **AI Assistant Strategy:** Used AI assistant for **all coding** and QA'd the generated code. **Memorized prompting strategies** and what was needed for each section, which allowed efficient workflow
3. **Communication:** Speaking through decisions helped demonstrate understanding
4. **Correct Problem Framing:** Recognizing ordinal classification vs. standard classification was crucial
5. **Feature Engineering Awareness:** Understanding when to remove identifiers vs. how to engineer them

### Important Lessons

1. **Both Code and Concepts Required:** Both **effective AI-assisted code generation** and **concept understanding/decision making** are required. You must be able to use AI effectively to write the required code for completion, AND demonstrate deep understanding of the concepts, decisions, and rationale behind your approach. The proctor expects you to know what code to generate, why you're generating it, and what decisions you're making.
2. **Proctor Focus:** While AI was used for all coding, the proctor was **less concerned about manually writing code from scratch** but **still expected effective use of AI to generate necessary code**. The proctor was **more focused on concepts, decisions, and overall understanding** - demonstrating that you understand what code to generate, why you're generating it, and what decisions you're making throughout the process.
2. **Ordinal Classification:** Understanding when and why to use ordinal methods is important
3. **Evaluation Metrics:** Choosing appropriate metrics (MAE for ordinal) demonstrates deeper understanding
4. **Feature Selection:** Using RandomForest for feature importance is a valid multivariate approach
5. **Outlier Handling:** IsolationForest is an efficient method, but removal should be justified by impact

### Advice for Future Candidates

1. **Master AI-assisted coding** - Practice using AI Assistant effectively to generate the required code. Memorize prompting strategies for each section. You must be able to use AI to write the code needed for completion.
2. **Prepare for theoretical questions** - Be ready to explain concepts, not just implement them. Understand the "why" behind your code choices.
3. **Understand ordinal vs. categorical** - Know when to use ordinal classification/regression
4. **Think out loud** - Articulate your reasoning throughout. Explain what code you're generating and why.
5. **Balance code and concepts** - Both are required: effective AI code generation AND deep concept understanding/decision making
6. **Know your evaluation metrics** - Understand why MAE is appropriate for ordinal targets
7. **Feature engineering knowledge** - Be prepared to discuss alternative approaches

---

## Technical Highlights

- **IsolationForest** for outlier detection
- **RandomForest feature importance** for multivariate feature selection
- **Ordinal Classification** with MAE evaluation
- **Sklearn pipelines** for production-ready preprocessing
- **Multiple model comparison** (XGB, RF, LGBM)

---

*This testimonial is intended to help future DPP exam candidates understand the exam format, expectations, and key areas of focus.*

