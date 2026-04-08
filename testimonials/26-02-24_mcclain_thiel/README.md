# DPP Exam Experience - McClain Thiel
**Date:** February 24, 2026  
**Duration:** 60 minutes  
**Result:** Passed

---

## Exam Setup

- **Intro:** Very short — 3–5 minutes of quick background, then straight into the problem.
- **Time constraint:** 1 hour maximum.
- **AI Assistant usage:** Proctors discouraged using the AI assistant (“for your own good”) but allowed it. They didn’t think it would help much; I used it anyway and found it very helpful.
- **Communication style:** I led the interaction by always doing three things:
  1. **Say what I want to do** (e.g., “I’m going to drop columns X, Y, Z and model on the rest”).
  2. **Say why I think it’s a good idea** (e.g., “Keeps it simple; we can add complexity later if needed”).
  3. **Ask for a quick check:** “Should I do that, or would you prefer option B?” (I’d briefly state option B.)

  That pattern limited how much they could quiz me and usually got a “that’s fine,” so I could keep moving.

---

## Dataset Details

**Dataset Type:** Restaurant Ratings (same as the [Franki Morales testimonial](../26-01-14_franki_morales/) — regression/rating prediction).

**Target Variable:** Rating.

**Key characteristics (same 60 / 25 / 15 EDA–modeling–reflection breakdown as Franki’s exam):**
- ~400 rows.
- Rating classes 1 and 2 are extremely rare — only about 3 examples combined.
- Relatively clean: dtypes were correct, not many outliers.
- Main issue: severe class imbalance in the target **and** in some predictor/categorical columns.

---

## EDA Approach

### Quick data overview

- **`dbutils.data.summarize(df)`** is very useful but can fail; be prepared to **replicate that summary from scratch** (value counts, dtypes, basic stats) if it breaks.
- For **every numeric column:** check the distribution.
- For **every categorical column:** check **cardinality and value counts**. Watch for disguised missingness — e.g. the string `"None"` (not `NaN`) appeared 6 times in one categorical column; you need to catch and handle that.

### Outlier / distribution

- I didn’t run a formal outlier-detection method; I used the distribution and cardinality analysis and made decisions from there.

### Collinearity

- **Plot collinearity** (e.g. correlation heatmap); some predictors were heavily correlated.
- Be ready to explain **what to do about it and why** from a modeling/theoretical perspective (e.g. redundancy, impact on coefficients or tree splits).

### Feature selection

- You can make **bold choices** (e.g. “I’m dropping X, Y, Z and modeling on the rest”) as long as you can **defend them**. I said we could come back and mine more signal later, but for now we’d keep it simple and add complexity only if needed.

---

## Preprocessing pipeline (framed as part of EDA)

I treated the data pipeline as part of EDA: build it early so you can inspect post-processed data.

- **Sklearn pipeline** with **ColumnTransformer**:
  - **Numeric columns:** imputation (mean), then scaling/normalization (e.g. StandardScaler).
  - **Categorical columns:** custom transformer to remove or fix the `"None"` strings → imputation (most frequent) → one-hot encoding.
- That produces a **preprocessor** object.
- **Do a bit more EDA on the post-processed training data** (e.g. after `preprocessor.fit_transform`) to confirm it behaves the way you expect.

---

## Modeling Approach

### Problem framing

- I framed it as **regression** (predicting rating) but **dropped the severely underrepresented classes** (rating 1 and 2 — only 3 examples total). I said we could do ordinal regression, but there’s effectively no signal in so few points, so we’d remove them and reframe the problem on the remaining classes.
- Regression (e.g. MSE) is fine; classification is also fine — **you need to know how to interpret the loss/metrics** you choose.

### Models and evaluation

- Models used:
  - **Linear Regression**.
  - **Lasso Regression**.
  - **Random Forest Regressor** with normalization.
- I added a **post-processor** that turned the regression output back into class predictions, then used a **confusion matrix** to diagnose remaining class imbalance and test a fix (e.g. class weights or threshold adjustment).

---

## Reflection

- **What worked well:** Leading with “what I’ll do, why, and do you prefer this or option B” kept the conversation focused and gave me control. Using the AI assistant despite the proctors’ caution saved time. Treating the pipeline as part of EDA and checking post-processed data caught issues early.
- **With more time:** Could revisit dropped features, try more targeted feature engineering, or tune the imbalance handling (e.g. class weights, sampling) more systematically.

---

## Key Questions Asked by Proctor

- **Why did you drop column X?**  
  I dropped the combo column that was simply the sum of three other columns (no additional signal, high redundancy).
- **Why did you frame it as a regression problem?**  
  Justified regression on the (cleaned) rating scale and explained how we’d interpret and post-process predictions.
- **Why stratify the train/test split?**  
  To preserve the (already imbalanced) class distribution across splits so evaluation matched the real-world class mix.
- **How would you handle rare / `\"None\"` categories?**  
  Discussed binning rare/`\"None\"` values into an `\"Other\"` category and how that affects signal vs. noise.

---

## Key Takeaways

### What worked well

1. **Communication pattern:** “What I’ll do → why → this or option B?” kept the proctor aligned and reduced surprise questions.
2. **Using the AI assistant** even when discouraged — it helped a lot; just be ready to justify or explain what you’re doing.
3. **Bold, defensible feature selection** — e.g. “drop X, Y, Z for now” — as long as you can explain the rationale.
4. **Pipeline early + EDA on processed data** so the preprocessor is part of your EDA story and you verify it before modeling.
5. **Reframing the problem** (dropping nearly empty classes) and explaining it clearly (no signal in 3 points) showed judgment.

### Important lessons / gotchas

1. **`dbutils.data.summarize`** — have a backup way to get distributions and cardinality; it can fail.
2. **Categorical “missing” values** — look for string placeholders like `"None"` in value counts, not just NaN.
3. **Collinearity** — plot it and be able to explain what you’d do and why (theory + modeling impact).
4. **Interpret loss/metrics** — whether you use regression or classification, know how to interpret the numbers and what they mean for imbalance.

### Advice for future candidates

1. Lead with a clear plan and rationale, then offer a quick “this or that?” so the proctor can say “that’s fine” and you keep the lead.
2. Don’t assume `dbutils.data.summarize` will work; be able to replicate its information manually.
3. Check every numeric distribution and every categorical cardinality/count; catch things like `"None"` strings.
4. You can keep feature selection simple and defend it (“simple first, add complexity as needed”).
5. Build the preprocessing pipeline as part of EDA and sanity-check the transformed data before modeling.
6. If a few target classes have almost no examples, consider dropping them and reframing, and explain why (no signal).
7. Use a post-processor + confusion matrix to turn regression (or probabilities) into classes and diagnose/fix imbalance.

---

## Technical Highlights

- **Custom transformer** to handle string `"None"` (and similar) in categorical columns before imputation/encoding.
- **ColumnTransformer** with separate numeric (impute + scale) and categorical (clean → impute → one-hot) pipelines.
- **Reframing the problem** by dropping severely underrepresented rating classes and explaining the rationale.
- **Post-processor** from regression output to class predictions + **confusion matrix** to diagnose and address class imbalance.

---

*This testimonial is intended to help future DPP exam candidates understand the exam format, expectations, and key areas of focus from McClain’s experience.*
