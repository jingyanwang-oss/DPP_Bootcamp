# Credit Card Approval Dataset

## Overview
High-dimensionality classification dataset structurally similar to the heart failure dataset but in the financial domain. This dataset contains two related files: application records with applicant information and credit records with payment history. Used for predicting credit card approval decisions and analyzing credit risk factors.

## Data Description

### application_record.csv
- **Rows:** 438,557
- **Columns:** 18
- **Description:** Contains applicant demographic and financial information

#### Features
- **ID:** Unique identifier for each applicant
- **CODE_GENDER:** Gender code (M/F)
- **FLAG_OWN_CAR:** Car ownership flag (Y/N)
- **FLAG_OWN_REALTY:** Realty ownership flag (Y/N)
- **CNT_CHILDREN:** Number of children
- **AMT_INCOME_TOTAL:** Total income amount
- **NAME_INCOME_TYPE:** Income type (Working, Commercial associate, etc.)
- **NAME_EDUCATION_TYPE:** Education level (Higher education, Secondary, etc.)
- **NAME_FAMILY_STATUS:** Family status (Married, Single, etc.)
- **NAME_HOUSING_TYPE:** Housing type (House/apartment, Rented apartment, etc.)
- **DAYS_BIRTH:** Days from birth (negative values)
- **DAYS_EMPLOYED:** Days employed (negative values)
- **FLAG_MOBIL:** Mobile phone flag
- **FLAG_WORK_PHONE:** Work phone flag
- **FLAG_PHONE:** Phone flag
- **FLAG_EMAIL:** Email flag
- **OCCUPATION_TYPE:** Occupation type (may contain missing values)
- **CNT_FAM_MEMBERS:** Number of family members

### credit_record.csv
- **Rows:** 1,048,575
- **Columns:** 3
- **Unique IDs:** 45,985
- **Description:** Contains monthly credit payment history for applicants

#### Features
- **ID:** Applicant identifier (links to application_record)
- **MONTHS_BALANCE:** Month balance (negative values indicate months in the past)
- **STATUS:** Payment status
  - **C:** Paid off that month (442,031 records)
  - **0:** 1-29 days past due (383,120 records)
  - **X:** No loan for the month (209,230 records)
  - **1:** 30-59 days past due (11,090 records)
  - **2:** 60-89 days past due (868 records)
  - **3:** 90-119 days past due (320 records)
  - **4:** 120-149 days past due (223 records)
  - **5:** Overdue or bad debts (1,693 records)

## Use Cases
- Binary classification: Predict credit card approval
- Credit risk analysis: Analyze factors affecting creditworthiness
- Time series analysis: Analyze payment patterns over time
- Feature engineering: Create aggregated features from credit history
- Data merging: Join application and credit records on ID
- Exploratory data analysis: Understand relationships between demographics and credit behavior

