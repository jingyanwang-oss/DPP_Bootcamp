"""
Script to create 'dirty' versions of datasets with realistic data quality issues.

This script programmatically introduces common data quality problems to clean datasets,
creating "dirty" versions that simulate real-world data engineering challenges. These
dirty datasets are designed for practicing data cleaning, preprocessing, and EDA skills,
particularly for DPP (Databricks Preferred Partner) certification preparation.

The script provides:
- Reusable utility functions for introducing various data quality issues
- Dataset-specific functions that apply appropriate issues for each dataset type
- Automatic generation of README.md files documenting all introduced issues
- Reproducible results through fixed random seeds

Author: DPP Practice Dataset Generator
Version: 1.0
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path
import re
from datetime import datetime, timedelta

# Set random seeds for reproducibility
# Using fixed seeds ensures that running the script multiple times produces
# the same dirty datasets, which is important for consistency in practice scenarios
np.random.seed(42)
random.seed(42)

def introduce_missing_values(df, columns, missing_rate=0.1, pattern='MCAR'):
    """
    Introduce missing values (NaN) in specified columns with different patterns.
    
    This function simulates various missing data mechanisms commonly found in real-world
    datasets. Missing values are a critical data quality issue that requires careful
    handling during preprocessing.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    columns : list of str
        List of column names where missing values should be introduced.
        Columns that don't exist in the dataframe are silently skipped.
    missing_rate : float, default=0.1
        Proportion of rows (0.0 to 1.0) that should have missing values in each column.
        For example, 0.1 means 10% of rows will have NaN in the specified column.
    pattern : str, default='MCAR'
        Missing data pattern to simulate:
        - 'MCAR': Missing Completely At Random - missingness is independent of observed
                  or unobserved data (random selection)
        - 'MAR': Missing At Random - missingness depends on observed data (correlated
                 with values in first numeric column)
        - 'MNAR': Missing Not At Random - currently implemented as MCAR (can be extended)
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with missing values introduced in the specified columns.
        Original dataframe is not modified.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'age': [25, 30, 35], 'income': [50000, 60000, 70000]})
    >>> df_dirty = introduce_missing_values(df, ['age'], missing_rate=0.33, pattern='MCAR')
    >>> df_dirty.isna().sum()
    age      1  # Approximately 33% missing
    income   0
    
    Notes:
    ------
    - For MAR pattern, the function uses the first numeric column in the dataframe to
      determine missingness probability (higher values = higher missing probability)
    - If no numeric columns exist for MAR pattern, it falls back to MCAR
    - The actual number of missing values may vary slightly due to rounding when
      converting proportion to count
    """
    df_dirty = df.copy()
    for col in columns:
        if col in df_dirty.columns:
            n_missing = int(len(df_dirty) * missing_rate)
            if pattern == 'MCAR':  # Missing Completely At Random
                indices = np.random.choice(df_dirty.index, n_missing, replace=False)
            elif pattern == 'MAR':  # Missing At Random (correlated with another column)
                # For MAR, we'll use a numeric column to determine missingness
                numeric_cols = df_dirty.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    # Higher values in first numeric column = higher missing probability
                    prob = (df_dirty[numeric_cols[0]] - df_dirty[numeric_cols[0]].min()) / \
                           (df_dirty[numeric_cols[0]].max() - df_dirty[numeric_cols[0]].min() + 1e-10)
                    prob = prob * missing_rate * 2  # Scale to desired rate
                    mask = np.random.random(len(df_dirty)) < prob
                    indices = df_dirty.index[mask][:n_missing]
                else:
                    indices = np.random.choice(df_dirty.index, n_missing, replace=False)
            else:  # MNAR - Missing Not At Random
                indices = np.random.choice(df_dirty.index, n_missing, replace=False)
            
            df_dirty.loc[indices, col] = np.nan
    return df_dirty

def introduce_duplicates(df, duplicate_rate=0.03):
    """
    Introduce duplicate rows with slight variations to simulate near-duplicates.
    
    Real-world datasets often contain duplicate or near-duplicate records due to
    data entry errors, system glitches, or data merging issues. This function creates
    duplicates with small variations to make them harder to detect than exact duplicates.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    duplicate_rate : float, default=0.03
        Proportion of rows (0.0 to 1.0) to duplicate. For example, 0.03 means 3% of
        rows will be duplicated. The duplicates are appended to the dataframe, so
        the final row count will be original_count * (1 + duplicate_rate).
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with duplicate rows added. The dataframe index is reset
        (ignore_index=True), so original indices are not preserved.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
    >>> df_dirty = introduce_duplicates(df, duplicate_rate=0.5)
    >>> len(df_dirty)  # Original 2 rows + 1 duplicate = 3 rows
    3
    
    Notes:
    ------
    - Duplicates are created by copying selected rows and then slightly modifying
      one numeric column (adding ±1% variation)
    - The variation is applied to a randomly selected numeric column
    - Integer columns are converted to float to allow fractional variations
    - This creates "near-duplicates" rather than exact duplicates, which is more
      realistic and challenging to detect
    """
    df_dirty = df.copy()
    n_duplicates = int(len(df_dirty) * duplicate_rate)
    duplicate_indices = np.random.choice(df_dirty.index, n_duplicates, replace=False)
    
    duplicates = df_dirty.loc[duplicate_indices].copy()
    # Add slight variations to some columns
    for idx in duplicates.index:
        numeric_cols = duplicates.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col = np.random.choice(numeric_cols)
            if pd.notna(duplicates.loc[idx, col]):
                # Convert to float for calculation, then back
                original_val = duplicates.loc[idx, col]
                if duplicates[col].dtype in [np.int64]:
                    duplicates[col] = duplicates[col].astype(float)
                duplicates.loc[idx, col] = original_val * (1 + np.random.uniform(-0.01, 0.01))
    
    df_dirty = pd.concat([df_dirty, duplicates], ignore_index=True)
    return df_dirty

def introduce_outliers(df, columns, outlier_rate=0.02):
    """
    Introduce extreme outliers in numeric columns to simulate data entry errors.
    
    Outliers can be legitimate extreme values or errors (e.g., typos, unit mistakes).
    This function creates extreme outliers by multiplying values by large factors,
    simulating common errors like entering 1000 instead of 10, or missing decimal points.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    columns : list of str
        List of column names where outliers should be introduced.
        Only numeric columns (int64, float64) are modified; other columns are skipped.
    outlier_rate : float, default=0.02
        Proportion of rows (0.0 to 1.0) that should contain outliers in each column.
        For example, 0.02 means 2% of rows will have extreme values.
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with outliers introduced in the specified numeric columns.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'age': [25, 30, 35], 'income': [50000, 60000, 70000]})
    >>> df_dirty = introduce_outliers(df, ['income'], outlier_rate=0.33)
    >>> df_dirty['income'].max()  # One value will be 10x-100x larger
    7000000  # or similar extreme value
    
    Notes:
    ------
    - Outliers are created by multiplying original values by random factors: 10, 50, 100, or -10
    - Negative multipliers create negative outliers (useful for values that should be positive)
    - Only non-null values are modified
    - The function only affects columns with numeric dtypes (int64, float64)
    - String columns or columns with object dtype are automatically skipped
    """
    df_dirty = df.copy()
    for col in columns:
        if col in df_dirty.columns and df_dirty[col].dtype in [np.int64, np.float64]:
            n_outliers = int(len(df_dirty) * outlier_rate)
            indices = np.random.choice(df_dirty.index, n_outliers, replace=False)
            
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    # Create extreme outliers (10x to 100x the value)
                    multiplier = np.random.choice([10, 50, 100, -10])
                    df_dirty.loc[idx, col] = df_dirty.loc[idx, col] * multiplier
    return df_dirty

def introduce_invalid_values(df, column_rules):
    """
    Introduce invalid values that violate domain constraints or logical rules.
    
    Invalid values are those that don't make sense in the context of the data domain.
    For example, negative ages, counts greater than a maximum, or values outside
    acceptable ranges. This function allows flexible rule-based introduction of such errors.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    column_rules : dict
        Dictionary mapping column names to rule dictionaries. Each rule dictionary can contain:
        - 'negative': bool - If True, make values negative (for values that should be positive)
        - 'range': tuple (min_val, max_val) - Set values outside this range
        - 'rate': float - Proportion of rows to modify (default: 0.02 if not specified)
        
        Example:
        {
            'age': {'range': (0, 120), 'rate': 0.03},
            'income': {'negative': True, 'rate': 0.02}
        }
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with invalid values introduced according to the rules.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'age': [25, 30, 35], 'children': [0, 1, 2]})
    >>> rules = {
    ...     'age': {'range': (0, 120), 'rate': 0.33},
    ...     'children': {'negative': True, 'rate': 0.33}
    ... }
    >>> df_dirty = introduce_invalid_values(df, rules)
    >>> (df_dirty['age'] < 0).any() or (df_dirty['age'] > 120).any()
    True  # Some ages will be outside 0-120
    >>> (df_dirty['children'] < 0).any()
    True  # Some children counts will be negative
    
    Notes:
    ------
    - For 'negative' rule: Only applies to numeric columns. String columns are attempted
      to be converted to numeric first (with errors='coerce')
    - For 'range' rule: Values are set to one of: min-100, max+100, min-1, or max+1
    - The function handles both numeric and string-encoded numeric columns
    - If a column doesn't exist in the dataframe, it's silently skipped
    - Invalid values are introduced independently for each rule type
    """
    df_dirty = df.copy()
    for col, rules in column_rules.items():
        if col in df_dirty.columns:
            if 'negative' in rules and rules['negative']:
                n_invalid = int(len(df_dirty) * rules.get('rate', 0.02))
                indices = np.random.choice(df_dirty.index, n_invalid, replace=False)
                # Only apply to numeric columns
                if df_dirty[col].dtype in [np.int64, np.float64]:
                    for idx in indices:
                        if pd.notna(df_dirty.loc[idx, col]):
                            df_dirty.loc[idx, col] = -abs(float(df_dirty.loc[idx, col]))
                else:
                    # For string columns, try to convert to numeric first
                    for idx in indices:
                        if pd.notna(df_dirty.loc[idx, col]):
                            try:
                                val = pd.to_numeric(df_dirty.loc[idx, col], errors='coerce')
                                if pd.notna(val):
                                    df_dirty.loc[idx, col] = -abs(val)
                            except:
                                pass
            
            if 'range' in rules:
                min_val, max_val = rules['range']
                n_invalid = int(len(df_dirty) * rules.get('rate', 0.02))
                indices = np.random.choice(df_dirty.index, n_invalid, replace=False)
                # Set values outside valid range
                df_dirty.loc[indices, col] = np.random.choice([
                    min_val - 100, max_val + 100, min_val - 1, max_val + 1
                ], size=len(indices))
    return df_dirty

def introduce_inconsistent_categorical(df, column_mappings):
    """
    Introduce inconsistent categorical values to simulate data entry variations.
    
    Real-world categorical data often has inconsistencies due to:
    - Case variations (Male/male/MALE)
    - Abbreviation variations (M/Male/M.)
    - Spelling variations (USA/US/United States)
    - Whitespace issues
    
    This function randomly introduces such variations to make categorical data inconsistent.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    column_mappings : dict
        Dictionary mapping column names to lists of possible variations.
        Variations can be:
        - List of strings: Randomly selects from the list
        - List of dicts: Maps original values to variations
          Example: [{'0': 'No', '1': 'Yes'}, {'0': 'False', '1': 'True'}]
        
        Example:
        {
            'gender': ['Male', 'male', 'M', 'MALE'],
            'status': [{'active': 'Active', 'inactive': 'Inactive'}]
        }
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with inconsistent categorical values introduced.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'gender': ['M', 'F', 'M'], 'status': ['active', 'inactive', 'active']})
    >>> mappings = {
    ...     'gender': ['Male', 'male', 'M', 'MALE', 'Female', 'female', 'F']
    ... }
    >>> df_dirty = introduce_inconsistent_categorical(df, mappings)
    >>> df_dirty['gender'].unique()
    array(['Male', 'M', 'MALE', ...])  # Mix of variations
    
    Notes:
    ------
    - By default, 15% of rows in each specified column are modified
    - If a variation is a dict and the original value matches a key, that mapping is used
    - If a variation is a list, a random element is selected
    - Only non-null values are modified
    - The function preserves the original value if no matching variation is found
    """
    df_dirty = df.copy()
    for col, variations in column_mappings.items():
        if col in df_dirty.columns:
            n_inconsistent = int(len(df_dirty) * 0.15)
            indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
            
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    original = str(df_dirty.loc[idx, col])
                    # Apply random variation
                    variation = random.choice(variations)
                    if isinstance(variation, dict) and original in variation:
                        df_dirty.loc[idx, col] = variation[original]
                    elif isinstance(variation, list):
                        df_dirty.loc[idx, col] = random.choice(variation)
    return df_dirty

def introduce_data_type_issues(df, columns, target_type='string'):
    """
    Convert numeric columns to strings with various formatting issues.
    
    A common data quality problem is numeric data stored as strings, often with
    formatting issues like commas, currency symbols, or units. This makes the data
    harder to work with and requires type conversion and cleaning.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    columns : list of str
        List of column names to convert to strings. Only numeric columns (int64, float64)
        are processed; other columns are skipped.
    target_type : str, default='string'
        Currently only 'string' is supported. The column is converted to object dtype
        and values are formatted as strings with various issues.
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with specified numeric columns partially converted to strings
        with formatting issues.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'age': [25, 30, 35], 'income': [50000, 60000, 70000]})
    >>> df_dirty = introduce_data_type_issues(df, ['age', 'income'])
    >>> df_dirty['age'].dtype
    object
    >>> df_dirty['age'].iloc[0]  # May be "25", "25 years", or "25,000"
    '25 years'  # or similar formatted string
    
    Notes:
    ------
    - Only 10% of values in each column are converted to strings (to simulate partial
      data quality issues, which is more realistic)
    - Formatting variations include:
      * 30% chance: Comma-separated numbers (e.g., "50,000")
      * 50% chance: Numbers with units (e.g., "25 years")
      * 20% chance: Plain string conversion (e.g., "25")
    - The column dtype is changed to object to allow mixed types
    - Non-null values are converted; null values remain as NaN
    """
    df_dirty = df.copy()
    for col in columns:
        if col in df_dirty.columns and df_dirty[col].dtype in [np.int64, np.float64]:
            # Convert column to object type first
            df_dirty[col] = df_dirty[col].astype(object)
            n_convert = int(len(df_dirty) * 0.1)
            indices = np.random.choice(df_dirty.index, n_convert, replace=False)
            
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    value = df_dirty.loc[idx, col]
                    # Add formatting issues
                    if random.random() < 0.3:
                        df_dirty.loc[idx, col] = f"{value:,.0f}"  # Add commas
                    elif random.random() < 0.5:
                        df_dirty.loc[idx, col] = f"{value} years"  # Add units
                    else:
                        df_dirty.loc[idx, col] = str(value)
    return df_dirty

def introduce_text_issues(df, text_columns):
    """
    Introduce text formatting and encoding issues in text columns.
    
    Text data often has quality issues including:
    - Extra whitespace (leading/trailing/multiple spaces)
    - Encoding problems (special characters corrupted)
    - Inconsistent formatting
    
    This function simulates these common text data problems.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    text_columns : list of str
        List of column names containing text data. All columns are converted to string
        type before processing.
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with text formatting issues introduced in specified columns.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'name': ['José', 'María', 'François']})
    >>> df_dirty = introduce_text_issues(df, ['name'])
    >>> df_dirty['name'].iloc[0]  # May have extra spaces or encoding issues
    '  JosÃ©  '  # Encoding issue + extra whitespace
    
    Notes:
    ------
    - All specified columns are converted to string type (object dtype)
    - Whitespace issues: 20% of rows get extra leading/trailing spaces
    - Encoding issues: 5% of rows with special characters (é, è, à) get corrupted
      to simulate UTF-8 encoding problems (é → Ã©)
    - The string 'nan' is preserved as-is (not modified) to avoid confusion with
      actual NaN values
    - Encoding corruption only occurs if the text contains the specific characters
      (é, è, à), otherwise no change is made
    """
    df_dirty = df.copy()
    for col in text_columns:
        if col in df_dirty.columns:
            df_dirty[col] = df_dirty[col].astype(str)
            
            # Add extra whitespace
            n_whitespace = int(len(df_dirty) * 0.2)
            indices = np.random.choice(df_dirty.index, n_whitespace, replace=False)
            for idx in indices:
                if df_dirty.loc[idx, col] != 'nan':
                    df_dirty.loc[idx, col] = "  " + str(df_dirty.loc[idx, col]) + "  "
            
            # Encoding issues (simulate)
            n_encoding = int(len(df_dirty) * 0.05)
            indices = np.random.choice(df_dirty.index, n_encoding, replace=False)
            for idx in indices:
                if df_dirty.loc[idx, col] != 'nan':
                    text = str(df_dirty.loc[idx, col])
                    if 'é' in text or 'è' in text:
                        df_dirty.loc[idx, col] = text.replace('é', 'Ã©').replace('è', 'Ã¨')
    return df_dirty

def add_noise_columns(df, n_columns=3):
    """
    Add irrelevant noise columns that don't contribute to analysis.
    
    Real-world datasets often contain metadata columns, system-generated IDs, timestamps,
    or other columns that are not relevant for analysis. These "noise" columns can:
    - Confuse feature selection
    - Add unnecessary complexity
    - Mislead during EDA
    - Increase storage and processing costs
    
    This function adds such columns to simulate this common data quality issue.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    n_columns : int, default=3
        Number of noise columns to add. If a randomly selected column name already
        exists, it's skipped and another is tried.
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with noise columns added.
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'age': [25, 30], 'income': [50000, 60000]})
    >>> df_dirty = add_noise_columns(df, n_columns=2)
    >>> df_dirty.columns.tolist()
    ['age', 'income', 'data_entry_timestamp', 'record_id_hash']
    
    Notes:
    ------
    - Column names are randomly selected from a predefined list:
      ['data_entry_timestamp', 'record_id_hash', 'source_system', 'processing_date',
       'batch_id', 'user_id', 'session_id']
    - Each column is randomly assigned as either:
      * Numeric: Random integers between 1000-9999
      * String: Format "NOISE_XXX" where XXX is random 100-999
    - If a selected column name already exists, it's skipped (no overwriting)
    - The function ensures unique column names by checking before adding
    """
    df_dirty = df.copy()
    noise_names = ['data_entry_timestamp', 'record_id_hash', 'source_system', 
                   'processing_date', 'batch_id', 'user_id', 'session_id']
    
    for i in range(n_columns):
        col_name = random.choice(noise_names)
        if col_name not in df_dirty.columns:
            if random.random() < 0.5:
                # Numeric noise
                df_dirty[col_name] = np.random.randint(1000, 9999, len(df_dirty))
            else:
                # String noise
                df_dirty[col_name] = [f"NOISE_{random.randint(100, 999)}" for _ in range(len(df_dirty))]
    return df_dirty

def introduce_column_name_issues(df):
    """
    Introduce issues with column names (whitespace, casing inconsistencies).
    
    Column names in real-world datasets often have formatting issues that can cause
    problems during analysis:
    - Extra whitespace (leading/trailing spaces)
    - Inconsistent casing (UPPER, lower, Mixed)
    - These issues can break code that references columns by exact name
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe to modify. A copy is made to avoid modifying the original.
    
    Returns:
    --------
    pandas.DataFrame
        A new dataframe with modified column names (renamed in-place).
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'Age': [25, 30], 'Income': [50000, 60000]})
    >>> df_dirty = introduce_column_name_issues(df)
    >>> df_dirty.columns.tolist()
    ['  Age  ', 'INCOME']  # Extra spaces or different casing
    
    Notes:
    ------
    - Each column has a random chance of being modified:
      * 30% chance: Extra whitespace added (leading and trailing spaces)
      * 50% chance: Converted to UPPERCASE
      * 20% chance: Left unchanged
    - The renaming happens in-place on the dataframe copy
    - This simulates common issues from manual data entry or system exports
    - Column name issues can break code that uses exact string matching
    """
    df_dirty = df.copy()
    # Add extra spaces
    new_columns = {}
    for col in df_dirty.columns:
        if random.random() < 0.3:
            new_columns[col] = "  " + col + "  "
        elif random.random() < 0.5:
            new_columns[col] = col.upper()
        else:
            new_columns[col] = col
    
    df_dirty.rename(columns=new_columns, inplace=True)
    return df_dirty

# ============================================================================
# Dataset-specific functions
# ============================================================================

def dirty_heart_failure(df):
    """
    Create dirty version of Heart Failure Prediction dataset.
    
    This function applies medical/clinical data-specific quality issues to the heart
    failure dataset. The issues are designed to reflect common problems in healthcare
    data collection and recording.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean heart failure dataset with columns:
        - age, anaemia, creatinine_phosphokinase, diabetes, ejection_fraction,
          high_blood_pressure, platelets, serum_creatinine, serum_sodium, sex,
          smoking, time, DEATH_EVENT
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues introduced
        - issues: List of strings describing each issue introduced
    
    Issues Introduced:
    ------------------
    1. Missing values (12%): age, serum_creatinine, serum_sodium (MAR pattern)
    2. Data type issues: age and platelets as strings with formatting
    3. Inconsistent binary encoding: Mix of 0/1, Yes/No, True/False
    4. Invalid values: Ages outside 0-120, ejection_fraction outside 0-100%
    5. Outliers: Extreme values in creatinine_phosphokinase and platelets
    6. Duplicates: 3% duplicate rows with slight variations
    7. Noise columns: System metadata columns
    8. Column name issues: Extra whitespace and inconsistent casing
    
    Notes:
    ------
    - Missing values use MAR (Missing At Random) pattern, simulating that older
      patients may have more missing lab results
    - Binary columns (anaemia, diabetes, etc.) get mixed encoding to simulate
      different data entry systems
    - Medical outliers are extreme but plausible (10x-100x) to test outlier detection
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values (MAR pattern - older patients more likely to have missing data)
    df_dirty = introduce_missing_values(df_dirty, ['age', 'serum_creatinine', 'serum_sodium'], 
                                       missing_rate=0.12, pattern='MAR')
    issues.append("Missing values: 12% missing in age, serum_creatinine, serum_sodium (MAR pattern)")
    
    # Data type issues
    df_dirty = introduce_data_type_issues(df_dirty, ['age', 'platelets'], target_type='string')
    issues.append("Data type issues: age and platelets converted to strings with formatting (commas, units)")
    
    # Inconsistent binary encoding
    binary_cols = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']
    variations = {
        'anaemia': [{'0': 'No', '1': 'Yes'}, {'0': 'False', '1': 'True'}],
        'diabetes': [{'0': 'No', '1': 'Yes'}, {'0': 'False', '1': 'True'}],
        'high_blood_pressure': [{'0': 'No', '1': 'Yes'}],
        'sex': [{'0': 'Female', '1': 'Male'}, {'0': 'F', '1': 'M'}],
        'smoking': [{'0': 'No', '1': 'Yes'}]
    }
    for col in binary_cols:
        if col in df_dirty.columns:
            # Convert to object type first
            df_dirty[col] = df_dirty[col].astype(object)
            n_convert = int(len(df_dirty) * 0.2)
            indices = np.random.choice(df_dirty.index, n_convert, replace=False)
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    val = str(df_dirty.loc[idx, col])
                    if val in ['0', '1']:
                        variation = random.choice(variations.get(col, [{'0': 'No', '1': 'Yes'}]))
                        df_dirty.loc[idx, col] = variation.get(val, df_dirty.loc[idx, col])
    issues.append("Inconsistent binary encoding: Mix of 0/1, Yes/No, True/False across binary columns")
    
    # Invalid values
    invalid_rules = {
        'age': {'range': (0, 120), 'rate': 0.03},
        'ejection_fraction': {'range': (0, 100), 'rate': 0.02}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: Ages outside 0-120, ejection_fraction outside 0-100%")
    
    # Outliers
    df_dirty = introduce_outliers(df_dirty, ['creatinine_phosphokinase', 'platelets'], outlier_rate=0.03)
    issues.append("Outliers: Extreme values in creatinine_phosphokinase and platelets (10x-100x)")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.03)
    issues.append("Duplicates: 3% duplicate rows with slight variations")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added data_entry_timestamp, record_id_hash, source_system")
    
    # Column name issues
    df_dirty = introduce_column_name_issues(df_dirty)
    issues.append("Column name issues: Extra whitespace and inconsistent casing")
    
    return df_dirty, issues

def dirty_titanic(df):
    """
    Create dirty version of Titanic dataset.
    
    Applies historical/passenger data-specific quality issues, including high missing
    rates in Cabin (realistic for this dataset) and various categorical inconsistencies.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean Titanic dataset with standard columns (PassengerId, Survived, Pclass, etc.)
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Missing values: 28% Age, 82% Cabin, 8% Embarked, 5% Fare
    2. Inconsistent categorical: Sex, Embarked, Pclass variations
    3. Text formatting: Extra whitespace in Name, Ticket, Cabin
    4. Invalid values: Negative Fare/SibSp/Parch, Age outside 0-120
    5. Duplicates: 2% duplicate rows
    6. Noise columns: Booking metadata columns
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['Age'], missing_rate=0.28, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['Cabin'], missing_rate=0.82, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['Embarked'], missing_rate=0.08, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['Fare'], missing_rate=0.05, pattern='MCAR')
    issues.append("Missing values: 28% Age, 82% Cabin, 8% Embarked, 5% Fare")
    
    # Inconsistent categorical values
    sex_variations = ['male', 'Male', 'M', 'm', 'female', 'Female', 'F', 'f']
    embarked_variations = ['C', 'Cherbourg', 'Q', 'Queenstown', 'S', 'Southampton']
    pclass_variations = {'1': ['First', '1st', '1'], '2': ['Second', '2nd', '2'], '3': ['Third', '3rd', '3']}
    
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'Sex': sex_variations})
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'Embarked': embarked_variations})
    
    # Pclass variations
    if 'Pclass' in df_dirty.columns:
        df_dirty['Pclass'] = df_dirty['Pclass'].astype(object)
        n_pclass = int(len(df_dirty) * 0.15)
        indices = np.random.choice(df_dirty.index, n_pclass, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'Pclass']):
                val = str(df_dirty.loc[idx, 'Pclass'])
                if val in pclass_variations:
                    df_dirty.loc[idx, 'Pclass'] = random.choice(pclass_variations[val])
    issues.append("Inconsistent categorical: Sex (male/Male/M), Embarked (C/Cherbourg), Pclass (1/First/1st)")
    
    # Text formatting issues
    df_dirty = introduce_text_issues(df_dirty, ['Name', 'Ticket', 'Cabin'])
    issues.append("Text formatting: Extra whitespace in Name, Ticket, Cabin")
    
    # Invalid values
    invalid_rules = {
        'Age': {'range': (0, 120), 'rate': 0.02},
        'Fare': {'negative': True, 'rate': 0.02},
        'SibSp': {'negative': True, 'rate': 0.01},
        'Parch': {'negative': True, 'rate': 0.01}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: Negative Fare/SibSp/Parch, Age outside 0-120")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate rows")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added booking_reference, check_in_time, travel_agent_code")
    
    return df_dirty, issues

def dirty_boston_housing(df):
    """
    Create dirty version of Boston Housing dataset.
    
    Applies real estate/geographic data-specific issues. Note that this dataset
    has special formatting (space-separated, no headers) which is preserved.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean Boston Housing dataset with columns: CRIM, ZN, INDUS, CHAS, NOX,
        RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT, MEDV
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Missing values: 8% in CRIM, NOX, AGE; 4% in MEDV (target variable)
    2. Invalid values: Negative CRIM, MEDV = 0 or > 100
    3. Outliers: Extreme values in CRIM and TAX
    4. Data type issues: CHAS as mixed 0/1 and True/False strings
    5. Duplicates: 2% duplicate rows
    6. Noise columns: Census and survey metadata
    7. Truncated data: 1% of rows with missing columns (incomplete records)
    
    Notes:
    ------
    - The dataset is saved without headers to maintain original format
    - Truncated rows simulate incomplete data collection
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['CRIM', 'NOX', 'AGE'], missing_rate=0.08, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['MEDV'], missing_rate=0.04, pattern='MCAR')
    issues.append("Missing values: 8% in CRIM, NOX, AGE; 4% in MEDV (target variable)")
    
    # Invalid values
    invalid_rules = {
        'CRIM': {'negative': True, 'rate': 0.01},
        'MEDV': {'range': (0, 100), 'rate': 0.03}  # Some MEDV = 0 or > 100
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: Negative CRIM, MEDV = 0 or > 100")
    
    # Outliers
    df_dirty = introduce_outliers(df_dirty, ['CRIM', 'TAX'], outlier_rate=0.03)
    issues.append("Outliers: Extreme values in CRIM and TAX (10x-100x)")
    
    # Data type issues - convert some to strings
    df_dirty = introduce_data_type_issues(df_dirty, ['CHAS'], target_type='string')
    issues.append("Data type issues: CHAS as both 0/1 and True/False strings")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate rows")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added census_tract_id, data_collection_year, surveyor_id")
    
    # Truncated rows (remove some columns for a few rows)
    n_truncated = int(len(df_dirty) * 0.01)
    indices = np.random.choice(df_dirty.index, n_truncated, replace=False)
    for idx in indices:
        cols_to_drop = np.random.choice(df_dirty.columns, size=3, replace=False)
        for col in cols_to_drop:
            df_dirty.loc[idx, col] = np.nan
    issues.append("Truncated data: 1% of rows with missing columns (simulating incomplete records)")
    
    return df_dirty, issues

def dirty_spam_ham(df):
    """
    Create dirty version of Spam vs Ham (email classification) dataset.
    
    Applies text/NLP-specific data quality issues including encoding problems,
    text corruption, and label inconsistencies common in text classification datasets.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean spam/ham dataset with columns: label, text, label_num
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Label inconsistencies: Mix of spam/SPAM/Spam and ham/HAM/Ham
    2. Label mismatch: 5% of rows have mismatched label and label_num
    3. Missing labels: 2% of rows with missing label
    4. Text formatting: Extra whitespace in email text
    5. Encoding issues: Special characters corrupted, HTML entities not decoded
    6. Truncated emails: 3% of emails cut off mid-sentence
    7. Empty text: 1% of emails contain only whitespace
    8. Label noise: 2% of rows with incorrect labels (same text, different label)
    9. Noise columns: Email metadata columns
    
    Notes:
    ------
    - Encoding issues simulate UTF-8 encoding problems (é → Ã©)
    - HTML entities (&, <, >) are not decoded to simulate raw HTML
    - Label noise creates mislabeled examples, a common problem in text datasets
    """
    df_dirty = df.copy()
    issues = []
    
    # Label inconsistencies
    label_variations = ['spam', 'SPAM', 'Spam', 'ham', 'HAM', 'Ham']
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'label': label_variations})
    issues.append("Label inconsistencies: Mix of spam/SPAM/Spam and ham/HAM/Ham")
    
    # Label mismatch
    n_mismatch = int(len(df_dirty) * 0.05)
    indices = np.random.choice(df_dirty.index, n_mismatch, replace=False)
    for idx in indices:
        if df_dirty.loc[idx, 'label'] == 'spam' or df_dirty.loc[idx, 'label'] == 'SPAM' or df_dirty.loc[idx, 'label'] == 'Spam':
            df_dirty.loc[idx, 'label_num'] = 0  # Wrong label_num
        else:
            df_dirty.loc[idx, 'label_num'] = 1  # Wrong label_num
    issues.append("Label mismatch: 5% of rows have mismatched label and label_num")
    
    # Missing labels
    df_dirty = introduce_missing_values(df_dirty, ['label'], missing_rate=0.02, pattern='MCAR')
    issues.append("Missing labels: 2% of rows with missing label")
    
    # Text issues
    df_dirty = introduce_text_issues(df_dirty, ['text'])
    issues.append("Text formatting: Extra whitespace in email text")
    
    # Encoding issues (simulate)
    n_encoding = int(len(df_dirty) * 0.08)
    indices = np.random.choice(df_dirty.index, n_encoding, replace=False)
    for idx in indices:
        if pd.notna(df_dirty.loc[idx, 'text']):
            text = str(df_dirty.loc[idx, 'text'])
            # Simulate encoding issues
            text = text.replace('é', 'Ã©').replace('è', 'Ã¨').replace('à', 'Ã ')
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            df_dirty.loc[idx, 'text'] = text
    issues.append("Encoding issues: Special characters corrupted (é→Ã©, HTML entities not decoded)")
    
    # Truncated emails
    n_truncated = int(len(df_dirty) * 0.03)
    indices = np.random.choice(df_dirty.index, n_truncated, replace=False)
    for idx in indices:
        if pd.notna(df_dirty.loc[idx, 'text']):
            text = str(df_dirty.loc[idx, 'text'])
            # Truncate to 50% length
            df_dirty.loc[idx, 'text'] = text[:len(text)//2]
    issues.append("Truncated emails: 3% of emails cut off mid-sentence")
    
    # Empty text
    n_empty = int(len(df_dirty) * 0.01)
    indices = np.random.choice(df_dirty.index, n_empty, replace=False)
    for idx in indices:
        df_dirty.loc[idx, 'text'] = "   "  # Only whitespace
    issues.append("Empty text: 1% of emails contain only whitespace")
    
    # Duplicates with different labels (label noise)
    n_noise = int(len(df_dirty) * 0.02)
    indices = np.random.choice(df_dirty.index, n_noise, replace=False)
    for idx in indices:
        # Flip label
        if df_dirty.loc[idx, 'label'] in ['spam', 'SPAM', 'Spam']:
            df_dirty.loc[idx, 'label'] = random.choice(['ham', 'HAM', 'Ham'])
        else:
            df_dirty.loc[idx, 'label'] = random.choice(['spam', 'SPAM', 'Spam'])
    issues.append("Label noise: 2% of rows with incorrect labels (same text, different label)")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added email_id, received_timestamp, sender_ip_address")
    
    return df_dirty, issues

def dirty_credit_card_approval_application(df):
    """
    Create dirty version of Credit Card Approval application record dataset.
    
    Applies financial/application data-specific issues. This is a large dataset
    (438K+ rows), so operations are optimized for performance using vectorized
    operations where possible.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean application record dataset with columns: ID, CODE_GENDER, FLAG_OWN_CAR,
        FLAG_OWN_REALTY, CNT_CHILDREN, AMT_INCOME_TOTAL, NAME_INCOME_TYPE, etc.
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Missing values: 18% OCCUPATION_TYPE, 4% AMT_INCOME_TOTAL, 3% DAYS_EMPLOYED
    2. Inconsistent categorical: CODE_GENDER, FLAG columns with variations
    3. Invalid values: Negative income, CNT_CHILDREN > 10, positive DAYS_EMPLOYED
    4. Income formatting: Mix of formats ($50,000, 50000, 50,000.00)
    5. Inconsistent capitalization: NAME_* columns with mixed case
    6. Duplicates: 2% duplicate application records
    7. Noise columns: Application metadata columns
    
    Performance Notes:
    ------------------
    - Income formatting uses batch processing to handle large dataset efficiently
    - Case conversion uses vectorized string operations
    - Invalid value introduction happens before formatting to avoid type conflicts
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['OCCUPATION_TYPE'], missing_rate=0.18, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['AMT_INCOME_TOTAL'], missing_rate=0.04, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['DAYS_EMPLOYED'], missing_rate=0.03, pattern='MCAR')
    issues.append("Missing values: 18% OCCUPATION_TYPE, 4% AMT_INCOME_TOTAL, 3% DAYS_EMPLOYED")
    
    # Inconsistent categorical values
    gender_variations = ['M', 'Male', 'm', 'F', 'Female', 'f']
    flag_variations = ['Y', 'Yes', '1', 'N', 'No', '0']
    
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'CODE_GENDER': gender_variations})
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'FLAG_OWN_CAR': flag_variations})
    df_dirty = introduce_inconsistent_categorical(df_dirty, {'FLAG_OWN_REALTY': flag_variations})
    issues.append("Inconsistent categorical: CODE_GENDER (M/Male/m), FLAG columns (Y/Yes/1)")
    
    
    # Invalid values (do this before income formatting to avoid type issues)
    # First, ensure AMT_INCOME_TOTAL is numeric for invalid value introduction
    if 'AMT_INCOME_TOTAL' in df_dirty.columns and df_dirty['AMT_INCOME_TOTAL'].dtype == object:
        # Try to convert back to numeric for invalid value introduction
        df_dirty['AMT_INCOME_TOTAL'] = pd.to_numeric(df_dirty['AMT_INCOME_TOTAL'], errors='coerce')
    
    invalid_rules = {
        'AMT_INCOME_TOTAL': {'negative': True, 'rate': 0.02},
        'CNT_CHILDREN': {'range': (0, 10), 'rate': 0.02},
        'DAYS_EMPLOYED': {'range': (-10000, 0), 'rate': 0.03}  # Positive = future employment
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    
    # Now do income formatting after invalid values (optimized for large datasets)
    if 'AMT_INCOME_TOTAL' in df_dirty.columns:
        df_dirty['AMT_INCOME_TOTAL'] = df_dirty['AMT_INCOME_TOTAL'].astype(object)
        n_format = int(len(df_dirty) * 0.15)
        indices = np.random.choice(df_dirty.index, n_format, replace=False)
        mask = df_dirty.index.isin(indices) & df_dirty['AMT_INCOME_TOTAL'].notna()
        
        # Format in batches to avoid memory issues
        income_vals = pd.to_numeric(df_dirty.loc[mask, 'AMT_INCOME_TOTAL'], errors='coerce')
        rand_vals = np.random.random(len(income_vals))
        
        # Apply formatting
        formatted = []
        for i, (val, rand) in enumerate(zip(income_vals, rand_vals)):
            if pd.notna(val):
                if rand < 0.3:
                    formatted.append(f"${val:,.0f}")
                elif rand < 0.8:
                    formatted.append(f"{val:,.2f}")
                else:
                    formatted.append(str(val))
            else:
                formatted.append(val)
        
        df_dirty.loc[mask, 'AMT_INCOME_TOTAL'] = formatted
    issues.append("Invalid values: Negative income, CNT_CHILDREN > 10, positive DAYS_EMPLOYED")
    issues.append("Income formatting: Mix of formats ($50,000, 50000, 50,000.00)")
    
    # Inconsistent name capitalization (optimized for large datasets)
    name_cols = ['NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE']
    for col in name_cols:
        if col in df_dirty.columns:
            n_inconsistent = int(len(df_dirty) * 0.1)
            indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
            mask = df_dirty.index.isin(indices) & df_dirty[col].notna()
            
            # Apply case conversion to masked rows
            masked_indices = df_dirty.index[mask]
            rand_vals = np.random.random(len(masked_indices))
            
            upper_indices = masked_indices[rand_vals < 0.5]
            lower_indices = masked_indices[rand_vals >= 0.5]
            
            df_dirty.loc[upper_indices, col] = df_dirty.loc[upper_indices, col].astype(str).str.upper()
            df_dirty.loc[lower_indices, col] = df_dirty.loc[lower_indices, col].astype(str).str.lower()
    issues.append("Inconsistent capitalization: NAME_* columns with mixed case")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate application records")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added application_source, branch_code, referral_code")
    
    return df_dirty, issues

def dirty_credit_card_approval_credit(df):
    """
    Create dirty version of Credit Card Approval credit record dataset.
    
    Applies payment history-specific issues. This dataset tracks monthly payment
    status over time, so issues focus on invalid status codes and data type problems.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean credit record dataset with columns: ID, MONTHS_BALANCE, STATUS
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Invalid STATUS codes: 2% with codes A, B, 6, 7, 8, 9 (not in valid range)
    2. Data type issues: MONTHS_BALANCE as strings in 10% of rows
    3. Duplicates: 3% duplicate credit records
    4. Noise columns: Transaction metadata columns
    
    Notes:
    ------
    - Valid STATUS codes are: C, 0, X, 1, 2, 3, 4, 5
    - Invalid codes simulate data entry errors or system glitches
    - MONTHS_BALANCE type issues simulate mixed data types from different sources
    """
    df_dirty = df.copy()
    issues = []
    
    # Invalid STATUS codes
    n_invalid = int(len(df_dirty) * 0.02)
    indices = np.random.choice(df_dirty.index, n_invalid, replace=False)
    invalid_codes = ['A', 'B', '6', '7', '8', '9']
    for idx in indices:
        df_dirty.loc[idx, 'STATUS'] = random.choice(invalid_codes)
    issues.append("Invalid STATUS codes: 2% with codes A, B, 6, 7, 8, 9 (not in valid range)")
    
    # Inconsistent MONTHS_BALANCE (some as strings)
    if 'MONTHS_BALANCE' in df_dirty.columns:
        df_dirty['MONTHS_BALANCE'] = df_dirty['MONTHS_BALANCE'].astype(object)
        n_string = int(len(df_dirty) * 0.1)
        indices = np.random.choice(df_dirty.index, n_string, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'MONTHS_BALANCE']):
                df_dirty.loc[idx, 'MONTHS_BALANCE'] = str(df_dirty.loc[idx, 'MONTHS_BALANCE'])
    issues.append("Data type issues: MONTHS_BALANCE as strings in 10% of rows")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.03)
    issues.append("Duplicates: 3% duplicate credit records")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=2)
    issues.append("Noise columns: Added transaction_id, processing_date")
    
    return df_dirty, issues

def dirty_spotify(df, is_clean_file=True):
    """
    Create dirty version of Spotify dataset.
    
    Applies music/entertainment data-specific issues including date format inconsistencies,
    genre formatting variations, and popularity data issues.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean Spotify dataset with track, artist, album, and popularity information.
        Columns vary slightly between the two Spotify files.
    is_clean_file : bool, default=True
        If True, expects 'spotify_data clean.csv' format (has track_duration_min).
        If False, expects 'track_data_final.csv' format (has track_duration_ms).
        This affects which duration column is processed.
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues
        - issues: List of issue descriptions
    
    Issues Introduced:
    ------------------
    1. Missing values: 12% artist_genres, 5% album_release_date, 3% explicit
    2. Inconsistent explicit: Mix of TRUE/True/1/yes and FALSE/False/0/no
    3. Date format inconsistencies: Mix of YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
    4. Invalid values: track_popularity outside 0-100, negative duration values
    5. Genre formatting: Mix of list format ['pop'] and comma-separated 'pop'
    6. Text formatting: Extra whitespace in track_name, artist_name, album_name
    7. Data type issues: Numeric columns as strings in 10% of rows
    8. Inconsistent album_type: Mixed casing (Album/album/ALBUM)
    9. Duplicates: 2% duplicate tracks
    10. Noise columns: Scraping metadata columns
    
    Notes:
    ------
    - Date formats are randomly varied to simulate different data sources
    - Genre lists are converted to comma-separated strings to create inconsistency
    - Popularity and duration issues test range validation
    - The is_clean_file parameter ensures correct duration column handling
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['artist_genres'], missing_rate=0.12, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['album_release_date'], missing_rate=0.05, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['explicit'], missing_rate=0.03, pattern='MCAR')
    issues.append("Missing values: 12% artist_genres, 5% album_release_date, 3% explicit")
    
    # Inconsistent explicit flag
    if 'explicit' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.2)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'explicit']):
                val = str(df_dirty.loc[idx, 'explicit'])
                if val in ['True', 'TRUE', 'true', '1']:
                    df_dirty.loc[idx, 'explicit'] = random.choice(['True', 'TRUE', '1', 'yes'])
                elif val in ['False', 'FALSE', 'false', '0']:
                    df_dirty.loc[idx, 'explicit'] = random.choice(['False', 'FALSE', '0', 'no'])
    issues.append("Inconsistent explicit: Mix of TRUE/True/1/yes and FALSE/False/0/no")
    
    # Date format inconsistencies
    if 'album_release_date' in df_dirty.columns:
        n_dates = int(len(df_dirty) * 0.3)
        indices = np.random.choice(df_dirty.index, n_dates, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'album_release_date']):
                try:
                    date_str = str(df_dirty.loc[idx, 'album_release_date'])
                    if '-' in date_str and len(date_str) == 10:
                        parts = date_str.split('-')
                        if random.random() < 0.33:
                            df_dirty.loc[idx, 'album_release_date'] = f"{parts[1]}/{parts[2]}/{parts[0]}"
                        elif random.random() < 0.5:
                            df_dirty.loc[idx, 'album_release_date'] = f"{parts[2]}-{parts[1]}-{parts[0]}"
                except:
                    pass
    issues.append("Date format inconsistencies: Mix of YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY")
    
    # Invalid values
    invalid_rules = {
        'track_popularity': {'range': (0, 100), 'rate': 0.02}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    
    # Duration issues
    duration_col = 'track_duration_min' if is_clean_file else 'track_duration_ms'
    if duration_col in df_dirty.columns:
        n_invalid = int(len(df_dirty) * 0.02)
        indices = np.random.choice(df_dirty.index, n_invalid, replace=False)
        for idx in indices:
            df_dirty.loc[idx, duration_col] = -abs(df_dirty.loc[idx, duration_col]) if pd.notna(df_dirty.loc[idx, duration_col]) else -1
    issues.append("Invalid values: track_popularity outside 0-100, negative duration values")
    
    # Genre formatting
    if 'artist_genres' in df_dirty.columns:
        n_genres = int(len(df_dirty) * 0.2)
        indices = np.random.choice(df_dirty.index, n_genres, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'artist_genres']):
                genres = str(df_dirty.loc[idx, 'artist_genres'])
                # Mix of list format and comma-separated
                if '[' in genres:
                    genres = genres.replace('[', '').replace(']', '').replace("'", "")
                    df_dirty.loc[idx, 'artist_genres'] = genres
    issues.append("Genre formatting: Mix of list format ['pop'] and comma-separated 'pop'")
    
    # Text formatting
    text_cols = ['track_name', 'artist_name', 'album_name']
    df_dirty = introduce_text_issues(df_dirty, text_cols)
    issues.append("Text formatting: Extra whitespace in track_name, artist_name, album_name")
    
    # Data type issues
    numeric_cols = ['track_popularity', 'artist_popularity', 'artist_followers']
    if is_clean_file and 'track_duration_min' in df_dirty.columns:
        numeric_cols.append('track_duration_min')
    elif not is_clean_file and 'track_duration_ms' in df_dirty.columns:
        numeric_cols.append('track_duration_ms')
    
    for col in numeric_cols:
        if col in df_dirty.columns:
            df_dirty[col] = df_dirty[col].astype(object)
            n_convert = int(len(df_dirty) * 0.1)
            indices = np.random.choice(df_dirty.index, n_convert, replace=False)
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    df_dirty.loc[idx, col] = str(df_dirty.loc[idx, col])
    issues.append("Data type issues: Numeric columns as strings in 10% of rows")
    
    # Inconsistent album_type
    if 'album_type' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.15)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'album_type']):
                val = str(df_dirty.loc[idx, 'album_type'])
                df_dirty.loc[idx, 'album_type'] = random.choice([val.lower(), val.upper(), val.capitalize()])
    issues.append("Inconsistent album_type: Mixed casing (Album/album/ALBUM)")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate tracks")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added scraped_timestamp, data_source, playlist_id")
    
    return df_dirty, issues

def dirty_chocolate_bars(df):
    """
    Create dirty version of Chocolate Bar Ratings dataset.
    
    This function applies food/product review data-specific quality issues to the chocolate
    bar ratings dataset. The issues are designed to reflect common problems in product review
    and food industry data collection.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean chocolate bar ratings dataset with columns:
        - id, manufacturer, company_location, year_reviewed, bean_origin, bar_name,
          cocoa_percent, num_ingredients, ingredients, rating
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues introduced
        - issues: List of strings describing each issue introduced
    
    Issues Introduced:
    ------------------
    1. Missing values: manufacturer, bean_origin, ingredients, rating
    2. Inconsistent categorical: company_location with mixed case and abbreviations
    3. Invalid values: cocoa_percent outside 0-100, rating outside 0-5, negative num_ingredients
    4. Data type issues: cocoa_percent and num_ingredients as strings with formatting
    5. Text formatting: Extra whitespace in bar_name, manufacturer
    6. Ingredient formatting: Mix of formats (B,S,C vs ['B','S','C'] vs B, S, C)
    7. Year inconsistencies: Mix of formats and invalid years
    8. Duplicates: 2% duplicate rows
    9. Noise columns: review_timestamp, reviewer_id, data_source
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['manufacturer', 'bean_origin'], 
                                       missing_rate=0.08, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['ingredients'], 
                                       missing_rate=0.05, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['rating'], 
                                       missing_rate=0.03, pattern='MCAR')
    issues.append("Missing values: 8% manufacturer and bean_origin, 5% ingredients, 3% rating")
    
    # Inconsistent categorical - company_location
    if 'company_location' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.15)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'company_location']):
                val = str(df_dirty.loc[idx, 'company_location'])
                # Create variations: U.S.A. vs USA vs United States
                if 'U.S.A.' in val or 'USA' in val.upper():
                    df_dirty.loc[idx, 'company_location'] = random.choice(['USA', 'U.S.A.', 'United States'])
                else:
                    df_dirty.loc[idx, 'company_location'] = random.choice([val.lower(), val.upper(), val.capitalize()])
    issues.append("Inconsistent categorical: company_location with mixed case and abbreviations (U.S.A./USA/United States)")
    
    # Invalid values
    invalid_rules = {
        'cocoa_percent': {'range': (0, 100), 'rate': 0.03},
        'rating': {'range': (0, 5), 'rate': 0.02},
        'num_ingredients': {'negative': True, 'rate': 0.01}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: cocoa_percent outside 0-100, rating outside 0-5, negative num_ingredients")
    
    # Data type issues
    df_dirty = introduce_data_type_issues(df_dirty, ['cocoa_percent', 'num_ingredients'], target_type='string')
    issues.append("Data type issues: cocoa_percent and num_ingredients as strings with formatting (commas, units)")
    
    # Text formatting
    text_cols = ['bar_name', 'manufacturer']
    df_dirty = introduce_text_issues(df_dirty, text_cols)
    issues.append("Text formatting: Extra whitespace in bar_name, manufacturer")
    
    # Ingredient formatting inconsistencies
    if 'ingredients' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.20)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'ingredients']):
                val = str(df_dirty.loc[idx, 'ingredients'])
                # Create variations: "B,S,C" vs "['B','S','C']" vs "B, S, C"
                if ',' in val and '[' not in val:
                    if ' ' in val:
                        df_dirty.loc[idx, 'ingredients'] = val.replace(' ', '')
                    else:
                        # Convert "B,S,C" to "['B','S','C']"
                        parts = val.split(',')
                        df_dirty.loc[idx, 'ingredients'] = "['" + "','".join(parts) + "']"
    issues.append("Ingredient formatting: Mix of formats (B,S,C vs ['B','S','C'] vs B, S, C)")
    
    # Year inconsistencies
    if 'year_reviewed' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.10)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'year_reviewed']):
                val = df_dirty.loc[idx, 'year_reviewed']
                # Convert to string with different formats or invalid years
                if isinstance(val, (int, float)):
                    if random.random() < 0.5:
                        df_dirty.loc[idx, 'year_reviewed'] = f"{int(val)}-01-01"  # Date format
                    else:
                        df_dirty.loc[idx, 'year_reviewed'] = int(val) + random.choice([-50, 50, 100])  # Invalid year
    issues.append("Year inconsistencies: Mix of formats (YYYY vs YYYY-MM-DD) and invalid years")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate rows")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added review_timestamp, reviewer_id, data_source")
    
    return df_dirty, issues

def dirty_flight_rating(df):
    """
    Create dirty version of Flight Rating dataset.
    
    This function applies airline/customer service data-specific quality issues to the flight
    rating dataset. The issues are designed to reflect common problems in customer feedback
    and airline operations data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Clean flight rating dataset with columns:
        - ID, Gender, Age, Customer_Type, Type_of_Travel, Class, Flight_Distance,
          Departure_Delay, Arrival_Delay, Rating
    
    Returns:
    --------
    tuple (pandas.DataFrame, list)
        - df_dirty: Dataframe with data quality issues introduced
        - issues: List of strings describing each issue introduced
    
    Issues Introduced:
    ------------------
    1. Missing values: Customer_Type, Age, Rating
    2. Inconsistent categorical: Gender (Male/male/M/MALE), Type_of_Travel, Class
    3. Invalid values: Age outside 0-120, negative delays, Rating outside 0-5, negative Flight_Distance
    4. Data type issues: Age, Flight_Distance, delays as strings with formatting
    5. Text formatting: Extra whitespace in categorical columns
    6. Customer_Type inconsistencies: First-time vs First time vs FirstTime
    7. Duplicates: 3% duplicate rows
    8. Noise columns: booking_id, flight_number, system_timestamp
    """
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['Customer_Type'], 
                                       missing_rate=0.05, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['Age'], 
                                       missing_rate=0.08, pattern='MCAR')
    df_dirty = introduce_missing_values(df_dirty, ['Rating'], 
                                       missing_rate=0.03, pattern='MCAR')
    issues.append("Missing values: 5% Customer_Type, 8% Age, 3% Rating")
    
    # Inconsistent categorical - Gender
    if 'Gender' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.15)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'Gender']):
                val = str(df_dirty.loc[idx, 'Gender']).lower()
                if 'male' in val:
                    df_dirty.loc[idx, 'Gender'] = random.choice(['Male', 'male', 'M', 'MALE'])
                elif 'female' in val:
                    df_dirty.loc[idx, 'Gender'] = random.choice(['Female', 'female', 'F', 'FEMALE'])
    issues.append("Inconsistent categorical: Gender (Male/male/M/MALE), Type_of_Travel, Class with mixed case")
    
    # Inconsistent categorical - Type_of_Travel and Class
    categorical_cols = ['Type_of_Travel', 'Class']
    for col in categorical_cols:
        if col in df_dirty.columns:
            n_inconsistent = int(len(df_dirty) * 0.12)
            indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
            for idx in indices:
                if pd.notna(df_dirty.loc[idx, col]):
                    val = str(df_dirty.loc[idx, col])
                    df_dirty.loc[idx, col] = random.choice([val.lower(), val.upper(), val.capitalize()])
    
    # Invalid values
    invalid_rules = {
        'Age': {'range': (0, 120), 'rate': 0.03},
        'Rating': {'range': (0, 5), 'rate': 0.02},
        'Departure_Delay': {'negative': True, 'rate': 0.01},
        'Arrival_Delay': {'negative': True, 'rate': 0.01},
        'Flight_Distance': {'negative': True, 'rate': 0.01}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: Age outside 0-120, negative delays, Rating outside 0-5, negative Flight_Distance")
    
    # Data type issues
    df_dirty = introduce_data_type_issues(df_dirty, ['Age', 'Flight_Distance', 'Departure_Delay', 'Arrival_Delay'], target_type='string')
    issues.append("Data type issues: Age, Flight_Distance, delays as strings with formatting (commas, units)")
    
    # Text formatting
    text_cols = ['Customer_Type', 'Type_of_Travel', 'Class']
    df_dirty = introduce_text_issues(df_dirty, text_cols)
    issues.append("Text formatting: Extra whitespace in categorical columns")
    
    # Customer_Type inconsistencies
    if 'Customer_Type' in df_dirty.columns:
        n_inconsistent = int(len(df_dirty) * 0.10)
        indices = np.random.choice(df_dirty.index, n_inconsistent, replace=False)
        for idx in indices:
            if pd.notna(df_dirty.loc[idx, 'Customer_Type']):
                val = str(df_dirty.loc[idx, 'Customer_Type'])
                if 'first' in val.lower():
                    df_dirty.loc[idx, 'Customer_Type'] = random.choice(['First-time', 'First time', 'FirstTime'])
                elif 'returning' in val.lower():
                    df_dirty.loc[idx, 'Customer_Type'] = random.choice(['Returning', 'returning', 'RETURNING'])
    issues.append("Customer_Type inconsistencies: First-time vs First time vs FirstTime")
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.03)
    issues.append("Duplicates: 3% duplicate rows")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=3)
    issues.append("Noise columns: Added booking_id, flight_number, system_timestamp")
    
    return df_dirty, issues

def read_clean_readme(clean_readme_path, dataset_file_name=None):
    """
    Read and parse the clean README to extract overview, data description, features, and use cases.
    
    Parameters:
    -----------
    clean_readme_path : Path
        Path to the clean README.md file
    dataset_file_name : str, optional
        If provided, extracts features for a specific file (for multi-file datasets)
        
    Returns:
    --------
    dict
        Dictionary with keys: overview, data_description, features, use_cases, notes
    """
    try:
        with open(clean_readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'overview': '',
            'data_description': '',
            'features': '',
            'use_cases': '',
            'notes': ''
        }
        
        # Extract overview (between # Title and ## Data Description)
        overview_match = re.search(r'## Overview\s*\n(.*?)(?=\n## )', content, re.DOTALL)
        if overview_match:
            result['overview'] = overview_match.group(1).strip()
        
        # Extract data description section
        data_desc_match = re.search(r'## Data Description\s*\n(.*?)(?=\n## )', content, re.DOTALL)
        if data_desc_match:
            full_data_desc = data_desc_match.group(1).strip()
            
            # For multi-file datasets, extract specific file section if requested
            if dataset_file_name:
                # Try to find section for specific file (e.g., "### application_record.csv")
                file_pattern = rf'### {re.escape(dataset_file_name)}.*?\n(.*?)(?=\n### |\n## |$)'
                file_section_match = re.search(file_pattern, full_data_desc, re.DOTALL)
                if file_section_match:
                    file_section = file_section_match.group(1)
                    # Extract features for this file
                    features_match = re.search(r'#### Features\s*\n(.*?)(?=\n#### |\n### |\n## |$)', file_section, re.DOTALL)
                    if features_match:
                        result['features'] = features_match.group(1).strip()
                    # Use the file-specific section as data description
                    result['data_description'] = f"### {dataset_file_name}\n{file_section.strip()}"
                else:
                    # Fall back to full description
                    result['data_description'] = full_data_desc
            else:
                # Use full data description
                result['data_description'] = full_data_desc
        
        # If no specific file features found, get general features
        if not result['features']:
            # Try to find features in the data description
            features_match = re.search(r'### Features.*?\n(.*?)(?=\n\*\*Note:|\n## |$)', content, re.DOTALL)
            if features_match:
                result['features'] = features_match.group(1).strip()
            # Also try #### Features (for multi-file datasets)
            if not result['features']:
                features_match = re.search(r'#### Features\s*\n(.*?)(?=\n#### |\n### |\n## |$)', content, re.DOTALL)
                if features_match:
                    result['features'] = features_match.group(1).strip()
        
        # Extract use cases
        use_cases_match = re.search(r'## Use Cases\s*\n(.*?)(?=\n## |$)', content, re.DOTALL)
        if use_cases_match:
            result['use_cases'] = use_cases_match.group(1).strip()
        
        # Extract notes (if any)
        notes_match = re.search(r'\*\*Note:\*\*(.*?)(?=\n## |$)', content, re.DOTALL)
        if notes_match:
            result['notes'] = notes_match.group(1).strip()
        
        return result
    except Exception as e:
        # If reading fails, return empty dict
        return {
            'overview': '',
            'data_description': '',
            'features': '',
            'use_cases': '',
            'notes': ''
        }

def create_practice_readme(dataset_name, clean_readme_path, dataset_file_name):
    """
    Generate a practice README.md file for datasets/ folder (no answer keys).
    
    This creates a README without revealing data quality issues or cleaning steps,
    suitable for students to practice data cleaning.
    
    Parameters:
    -----------
    dataset_name : str
        Name of the dataset
    clean_readme_path : Path
        Path to the clean README to extract information from
    dataset_file_name : str
        Name of the dataset CSV file
        
    Returns:
    --------
    str
        Complete markdown content for the practice README
    """
    # For practice README, get full description (not file-specific)
    clean_info = read_clean_readme(clean_readme_path)
    
    # Get dataset title from clean README
    try:
        with open(clean_readme_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            title = first_line.replace('# ', '') if first_line.startswith('#') else dataset_name
    except:
        title = dataset_name
    
    readme_content = f"""# {title}

## Overview
This directory contains the {title} dataset. This dataset has been intentionally modified to include various data quality issues commonly encountered in real-world data engineering and machine learning projects. Your task is to identify and resolve these issues through exploratory data analysis and data cleaning.

{clean_info['overview']}

## Data Description
{clean_info['data_description']}"""
    
    if clean_info['features']:
        readme_content += f"""

### Features
{clean_info['features']}"""
    
    if clean_info['notes']:
        readme_content += f"""

**Note:** {clean_info['notes']}"""
    
    readme_content += f"""

## Exercise Objective
This dataset contains intentional data quality problems that need to be identified and resolved. Use your data cleaning and preprocessing skills to prepare this dataset for analysis.

## Use Cases
{clean_info['use_cases']}

## Files
- `{dataset_file_name}` - The dataset file containing data with various data quality issues

---
*This dataset was programmatically generated for educational purposes.*
"""
    
    return readme_content

def create_solution_readme(issues, dataset_name, description, clean_readme_path, dataset_file_name=None):
    """
    Generate a solution README.md file for solutions/{dataset}/dirty/ folder (with answer keys).
    
    This creates a comprehensive README with all data quality issues and cleaning steps,
    serving as an answer key for instructors and students after practice.
    
    Parameters:
    -----------
    issues : list of str
        List of strings describing each data quality issue introduced
    dataset_name : str
        Name of the dataset
    description : str
        Brief description of the original clean dataset
    clean_readme_path : Path
        Path to the clean README to extract additional information
    dataset_file_name : str, optional
        Name of the dataset file (for multi-file datasets to extract specific features)
        
    Returns:
    --------
    str
        Complete markdown content for the solution README
    """
    # For solution README, get file-specific info if provided
    clean_info = read_clean_readme(clean_readme_path, dataset_file_name)
    
    # Get dataset title from clean README
    try:
        with open(clean_readme_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            title = first_line.replace('# ', '') if first_line.startswith('#') else dataset_name
    except:
        title = dataset_name
    
    readme_content = f"""# {title} - Dirty Dataset

## Overview
This is the "dirty" version of the {title} dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

{clean_info['overview']}

## Data Description
{clean_info['data_description']}"""
    
    if clean_info['features']:
        readme_content += f"""

### Features
{clean_info['features']}"""
    
    if clean_info['notes']:
        readme_content += f"""

**Note:** {clean_info['notes']}"""
    
    readme_content += f"""

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

"""
    
    for i, issue in enumerate(issues, 1):
        readme_content += f"{i}. {issue}\n"
    
    readme_content += f"""

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
{clean_info['use_cases']}

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
"""
    
    return readme_content

def create_readme(issues, dataset_name, description):
    """
    Generate a README.md file documenting all data quality issues introduced.
    
    This function creates a comprehensive markdown document that serves as an "answer key"
    for the dirty dataset. It lists all issues, provides cleaning recommendations, and
    explains how to use the dataset for practice.
    
    Parameters:
    -----------
    issues : list of str
        List of strings describing each data quality issue introduced.
        Each string should be a clear, concise description (e.g., "Missing values: 12% in age").
    dataset_name : str
        Name of the dataset (e.g., "Heart Failure", "Titanic").
        Used in the README title and headers.
    description : str
        Brief description of the original clean dataset (rows, columns, purpose).
        This is included in the README to provide context.
    
    Returns:
    --------
    str
        Complete markdown content for the README.md file.
    
    Examples:
    ---------
    >>> issues = ["Missing values: 10% in age", "Duplicates: 2% of rows"]
    >>> readme = create_readme(issues, "Test Dataset", "100 rows, 5 columns")
    >>> len(readme) > 0
    True
    
    Notes:
    ------
    - The README includes:
      * Overview and original dataset description
      * Numbered list of all issues
      * Usage recommendations
      * Step-by-step cleaning guide
      * Notes about issue interdependencies
    - The README is designed to be educational and help users understand what
      to look for when cleaning the data
    - Issues are numbered automatically in the order provided
    """
    readme_content = f"""# {dataset_name} - Dirty Dataset

## Overview
This is the "dirty" version of the {dataset_name} dataset, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. This dataset contains intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

## Original Dataset Description
{description}

## Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

"""
    
    for i, issue in enumerate(issues, 1):
        readme_content += f"{i}. {issue}\n"
    
    readme_content += f"""

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

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*
"""
    
    return readme_content

# ============================================================================
# Main execution
# ============================================================================

def main():
    """
    Main execution function that processes all datasets and creates dirty versions.
    
    This function:
    1. Defines configuration for all datasets (paths, functions, descriptions)
    2. Iterates through each dataset configuration
    3. Reads the clean dataset from solutions/[dataset_name]/clean/ folder
    4. Applies dataset-specific dirtying function
    5. Saves dirty dataset to datasets/[dataset_name]/ folder
    6. Generates README.md with issue documentation
    
    Special Handling:
    ------------------
    - Boston Housing: Reads space-separated file without headers, adds column names,
      saves without headers to maintain original format
    
    Output:
    -------
    Creates files in datasets/[dataset_name]/:
    - [dataset_file].csv - Dirty dataset with issues
    - README.md - Documentation of all issues (answer key)
    
    Error Handling:
    ---------------
    - Continues processing other datasets if one fails
    - Prints error messages with traceback for debugging
    - Reports success/failure status for each dataset
    
    Notes:
    ------
    - Uses fixed random seeds (set at module level) for reproducibility
    - All file paths are relative to the script's location
    - Creates datasets/[dataset_name]/ directories if they don't exist
    """
    solutions_path = Path("solutions")
    datasets_path = Path("datasets")
    
    datasets_config = [
        {
            'name': 'Heart Failure',
            'clean_path': solutions_path / 'heart_failure' / 'clean' / 'heart_failure_clinical_records_dataset.csv',
            'clean_readme_path': solutions_path / 'heart_failure' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'heart_failure' / 'heart_failure_clinical_records_dataset.csv',
            'practice_readme_path': datasets_path / 'heart_failure' / 'README.md',
            'solution_readme_path': solutions_path / 'heart_failure' / 'dirty' / 'README.md',
            'function': dirty_heart_failure,
            'description': 'Unbalanced binary classification dataset with 299 rows and 13 columns. Used for predicting death events based on clinical features.',
            'dataset_file_name': 'heart_failure_clinical_records_dataset.csv'
        },
        {
            'name': 'Titanic',
            'clean_path': solutions_path / 'titantic' / 'clean' / 'Titanic-Dataset.csv',
            'clean_readme_path': solutions_path / 'titantic' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'titantic' / 'Titanic-Dataset.csv',
            'practice_readme_path': datasets_path / 'titantic' / 'README.md',
            'solution_readme_path': solutions_path / 'titantic' / 'dirty' / 'README.md',
            'function': dirty_titanic,
            'description': 'Classic binary classification dataset with 891 rows and 12 columns. Used for predicting passenger survival.',
            'dataset_file_name': 'Titanic-Dataset.csv'
        },
        {
            'name': 'Boston Housing',
            'clean_path': solutions_path / 'boston_housing' / 'clean' / 'housing.csv',
            'clean_readme_path': solutions_path / 'boston_housing' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'boston_housing' / 'housing.csv',
            'practice_readme_path': datasets_path / 'boston_housing' / 'README.md',
            'solution_readme_path': solutions_path / 'boston_housing' / 'dirty' / 'README.md',
            'function': dirty_boston_housing,
            'description': 'Classic regression dataset with 506 rows and 14 columns. Used for predicting median house values in Boston suburbs.',
            'dataset_file_name': 'housing.csv'
        },
        {
            'name': 'Spam vs Ham',
            'clean_path': solutions_path / 'spam_ham' / 'clean' / 'spam_ham_dataset.csv',
            'clean_readme_path': solutions_path / 'spam_ham' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'spam_ham' / 'spam_ham_dataset.csv',
            'practice_readme_path': datasets_path / 'spam_ham' / 'README.md',
            'solution_readme_path': solutions_path / 'spam_ham' / 'dirty' / 'README.md',
            'function': dirty_spam_ham,
            'description': 'Text classification dataset with 5,171 rows and 4 columns. Used for classifying emails as spam or ham based on text content.',
            'dataset_file_name': 'spam_ham_dataset.csv'
        },
        {
            'name': 'Credit Card Approval - Application',
            'clean_path': solutions_path / 'credit_card_approval' / 'clean' / 'application_record.csv',
            'clean_readme_path': solutions_path / 'credit_card_approval' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'credit_card_approval' / 'application_record.csv',
            'practice_readme_path': datasets_path / 'credit_card_approval' / 'README.md',
            'solution_readme_path': solutions_path / 'credit_card_approval' / 'dirty' / 'README.md',
            'function': dirty_credit_card_approval_application,
            'description': 'Application records dataset with 438,557 rows and 18 columns. Contains applicant demographic and financial information.',
            'dataset_file_name': 'application_record.csv'
        },
        {
            'name': 'Credit Card Approval - Credit',
            'clean_path': solutions_path / 'credit_card_approval' / 'clean' / 'credit_record.csv',
            'clean_readme_path': solutions_path / 'credit_card_approval' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'credit_card_approval' / 'credit_record.csv',
            'practice_readme_path': None,  # Will use main README for credit_card_approval
            'solution_readme_path': solutions_path / 'credit_card_approval' / 'dirty' / 'credit_record_README.md',
            'function': dirty_credit_card_approval_credit,
            'description': 'Credit payment history dataset with 1,048,575 rows and 3 columns. Contains monthly credit payment history for applicants.',
            'dataset_file_name': 'credit_record.csv'
        },
        {
            'name': 'Spotify - Clean Data',
            'clean_path': solutions_path / 'spotify' / 'clean' / 'spotify_data clean.csv',
            'clean_readme_path': solutions_path / 'spotify' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'spotify' / 'spotify_data clean.csv',
            'practice_readme_path': datasets_path / 'spotify' / 'README.md',
            'solution_readme_path': solutions_path / 'spotify' / 'dirty' / 'spotify_data_clean_README.md',
            'function': lambda df: dirty_spotify(df, is_clean_file=True),
            'description': 'Recent and contemporary Spotify tracks dataset with 8,582 rows and 15 columns. Contains tracks mainly from 2025.',
            'dataset_file_name': 'spotify_data clean.csv'
        },
        {
            'name': 'Spotify - Track Data Final',
            'clean_path': solutions_path / 'spotify' / 'clean' / 'track_data_final.csv',
            'clean_readme_path': solutions_path / 'spotify' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'spotify' / 'track_data_final.csv',
            'practice_readme_path': None,  # Will use main README for spotify
            'solution_readme_path': solutions_path / 'spotify' / 'dirty' / 'track_data_final_README.md',
            'function': lambda df: dirty_spotify(df, is_clean_file=False),
            'description': 'Popular Spotify tracks from 2009-2023 dataset with 8,778 rows and 15 columns. Contains tracks from well-known artists.',
            'dataset_file_name': 'track_data_final.csv'
        },
        {
            'name': 'Chocolate Bar Ratings',
            'clean_path': solutions_path / 'chocolate_bars' / 'clean' / 'chocolate_bar_ratings.csv',
            'clean_readme_path': solutions_path / 'chocolate_bars' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'chocolate_bars' / 'chocolate_bar_ratings.csv',
            'practice_readme_path': datasets_path / 'chocolate_bars' / 'README.md',
            'solution_readme_path': solutions_path / 'chocolate_bars' / 'dirty' / 'README.md',
            'function': dirty_chocolate_bars,
            'description': 'Regression dataset with 2,530 rows and 10 columns. Used for predicting chocolate bar ratings based on characteristics.',
            'dataset_file_name': 'chocolate_bar_ratings.csv'
        },
        {
            'name': 'Flight Rating',
            'clean_path': solutions_path / 'flight_rating' / 'clean' / 'flight_rating.csv',
            'clean_readme_path': solutions_path / 'flight_rating' / 'clean' / 'README.md',
            'dirty_path': datasets_path / 'flight_rating' / 'flight_rating.csv',
            'practice_readme_path': datasets_path / 'flight_rating' / 'README.md',
            'solution_readme_path': solutions_path / 'flight_rating' / 'dirty' / 'README.md',
            'function': dirty_flight_rating,
            'description': 'Regression/classification dataset with 10,000 rows and 10 columns. Used for predicting flight ratings based on customer and flight characteristics.',
            'dataset_file_name': 'flight_rating.csv'
        }
    ]
    
    print("Creating dirty datasets...")
    print("=" * 60)
    
    for config in datasets_config:
        try:
            print(f"\nProcessing: {config['name']}")
            
            # Read clean dataset
            if config['name'] == 'Boston Housing':
                # Boston Housing has no headers and is space-separated
                df = pd.read_csv(config['clean_path'], sep=r'\s+', header=None)
                # Add column names
                columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                          'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
                df.columns = columns
            else:
                df = pd.read_csv(config['clean_path'])
            
            # Create dirty version
            df_dirty, issues = config['function'](df)
            
            # Ensure output directory exists
            config['dirty_path'].parent.mkdir(parents=True, exist_ok=True)
            
            # Save dirty dataset
            if config['name'] == 'Boston Housing':
                # Save without headers for Boston Housing
                df_dirty.to_csv(config['dirty_path'], sep=' ', header=False, index=False)
            else:
                df_dirty.to_csv(config['dirty_path'], index=False)
            
            # Create practice README (for datasets/ folder - no answer keys)
            if config.get('practice_readme_path'):
                practice_readme_content = create_practice_readme(
                    config['name'], 
                    config['clean_readme_path'], 
                    config['dataset_file_name']
                )
                config['practice_readme_path'].parent.mkdir(parents=True, exist_ok=True)
                with open(config['practice_readme_path'], 'w', encoding='utf-8') as f:
                    f.write(practice_readme_content)
                print(f"  [OK] Created practice README: {config['practice_readme_path']}")
            
            # Create solution README (for solutions/{dataset}/dirty/ folder - with answer keys)
            if config.get('solution_readme_path'):
                solution_readme_content = create_solution_readme(
                    issues, 
                    config['name'], 
                    config['description'],
                    config['clean_readme_path'],
                    config.get('dataset_file_name')
                )
                config['solution_readme_path'].parent.mkdir(parents=True, exist_ok=True)
                with open(config['solution_readme_path'], 'w', encoding='utf-8') as f:
                    f.write(solution_readme_content)
                print(f"  [OK] Created solution README: {config['solution_readme_path']}")
            
            print(f"  [OK] Created: {config['dirty_path']}")
            print(f"  [OK] Issues introduced: {len(issues)}")
            
        except Exception as e:
            print(f"  [ERROR] Error processing {config['name']}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Done! All dirty datasets and README files have been created.")
    print("\nREADME files created:")
    print("- Practice READMEs: datasets/{dataset}/README.md (no answer keys)")
    print("- Solution READMEs: solutions/{dataset}/dirty/README.md (with answer keys)")
    print("\nNext steps:")
    print("1. Review the dirty datasets in the 'datasets/' folders")
    print("2. Students can practice with datasets/ READMEs (no spoilers)")
    print("3. Check solutions/ READMEs for answer keys after practice")
    print("4. Practice cleaning the datasets to match the clean versions")

if __name__ == "__main__":
    main()

