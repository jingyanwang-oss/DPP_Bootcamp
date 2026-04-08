# Dirty Dataset Creation Utility

## Overview

The `create_dirty_datasets.py` script programmatically introduces realistic data quality issues to clean datasets, creating "dirty" versions that simulate real-world data problems. This is designed for practicing data engineering, cleaning, and preprocessing skills, particularly for DPP (Databricks Preferred Partner) certification preparation.

## Purpose

Real-world datasets are rarely clean. This script helps create practice datasets with intentional data quality issues that data engineers and data scientists commonly encounter, including:

- Missing values (various patterns)
- Duplicate rows
- Inconsistent data types
- Invalid values and outliers
- Text encoding issues
- Categorical inconsistencies
- Irrelevant noise columns
- Formatting problems

## Script Location

`utils/create_dirty_datasets.py`

## Requirements

- Python 3.7+
- pandas
- numpy

Install dependencies:
```bash
pip install pandas numpy
```

Or use the project's virtual environment:
```bash
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Usage

### Basic Usage

From the project root directory:

```bash
python utils/create_dirty_datasets.py
```

The script will:
1. Read clean datasets from `datasets/[dataset_name]/clean/`
2. Apply data quality issues to each dataset
3. Save dirty versions to `datasets/[dataset_name]/dirty/`
4. Generate README.md files in each dirty folder documenting all issues

### Output Structure

```
datasets/
  └── [dataset_name]/
      ├── clean/
      │   ├── [dataset_file].csv
      │   └── README.md
      └── dirty/
          ├── [dataset_file].csv
          └── README.md          # Answer key with all issues listed
```

## How It Works

### Process Flow

1. **Read Clean Dataset**: Loads the clean CSV file from the `clean/` folder
2. **Apply Data Quality Issues**: Calls dataset-specific function to introduce issues
3. **Save Dirty Dataset**: Writes the modified dataset to the `dirty/` folder
4. **Generate Documentation**: Creates README.md listing all introduced issues

### Core Functions

The script provides reusable functions for introducing common data quality issues:

#### `introduce_missing_values(df, columns, missing_rate, pattern)`
- Introduces missing values (NaN) in specified columns
- Patterns: `MCAR` (Missing Completely At Random), `MAR` (Missing At Random), `MNAR` (Missing Not At Random)

#### `introduce_duplicates(df, duplicate_rate)`
- Adds duplicate rows with slight variations
- Creates near-duplicates to simulate real-world scenarios

#### `introduce_outliers(df, columns, outlier_rate)`
- Creates extreme outliers (10x-100x normal values)
- Useful for testing outlier detection and handling

#### `introduce_invalid_values(df, column_rules)`
- Introduces values outside acceptable ranges
- Can create negative values where they shouldn't exist
- Sets values outside specified min/max ranges

#### `introduce_inconsistent_categorical(df, column_mappings)`
- Creates variations in categorical values (e.g., "Male"/"male"/"M")
- Simulates inconsistent data entry

#### `introduce_data_type_issues(df, columns, target_type)`
- Converts numeric columns to strings with formatting
- Adds commas, units, or other formatting issues

#### `introduce_text_issues(df, text_columns)`
- Adds extra whitespace
- Simulates encoding problems (e.g., é → Ã©)
- Creates text formatting inconsistencies

#### `add_noise_columns(df, n_columns)`
- Adds irrelevant columns that don't contribute to analysis
- Simulates metadata or system columns

#### `introduce_column_name_issues(df)`
- Adds extra whitespace to column names
- Creates inconsistent casing (UPPER, lower, Mixed)

### Dataset-Specific Functions

Each dataset has a custom function (e.g., `dirty_heart_failure()`, `dirty_titanic()`) that:
1. Applies appropriate data quality issues for that dataset type
2. Maintains a list of all issues introduced
3. Returns the dirty dataframe and issues list

## Adding a New Dataset

To add a new dataset to the dirty dataset creation process:

### Step 1: Organize Your Dataset

Place your clean dataset in the proper structure:
```
datasets/
  └── [new_dataset_name]/
      └── clean/
          ├── [dataset_file].csv
          └── README.md
```

### Step 2: Create a Dataset-Specific Function

Add a new function in `create_dirty_datasets.py` following this pattern:

```python
def dirty_new_dataset(df):
    """Create dirty version of new dataset."""
    df_dirty = df.copy()
    issues = []
    
    # Missing values
    df_dirty = introduce_missing_values(df_dirty, ['column1', 'column2'], 
                                       missing_rate=0.10, pattern='MCAR')
    issues.append("Missing values: 10% missing in column1, column2")
    
    # Invalid values
    invalid_rules = {
        'numeric_column': {'range': (0, 100), 'rate': 0.02}
    }
    df_dirty = introduce_invalid_values(df_dirty, invalid_rules)
    issues.append("Invalid values: numeric_column outside 0-100 range")
    
    # Add more issues as needed...
    
    # Duplicates
    df_dirty = introduce_duplicates(df_dirty, duplicate_rate=0.02)
    issues.append("Duplicates: 2% duplicate rows")
    
    # Noise columns
    df_dirty = add_noise_columns(df_dirty, n_columns=2)
    issues.append("Noise columns: Added metadata columns")
    
    return df_dirty, issues
```

### Step 3: Add Configuration

Add your dataset to the `datasets_config` list in the `main()` function:

```python
{
    'name': 'New Dataset Name',
    'clean_path': base_path / 'new_dataset_name' / 'clean' / 'dataset_file.csv',
    'dirty_path': base_path / 'new_dataset_name' / 'dirty' / 'dataset_file.csv',
    'readme_path': base_path / 'new_dataset_name' / 'dirty' / 'README.md',
    'function': dirty_new_dataset,
    'description': 'Brief description of the dataset (rows, columns, purpose)'
}
```

### Step 4: Handle Special Cases

If your dataset has special requirements (like Boston Housing with no headers):

```python
# In main() function, add special handling:
if config['name'] == 'New Dataset Name':
    # Custom reading logic
    df = pd.read_csv(config['clean_path'], sep='\t', encoding='utf-8')
else:
    df = pd.read_csv(config['clean_path'])
```

### Step 5: Run the Script

```bash
python utils/create_dirty_datasets.py
```

The script will create:
- Dirty dataset in `datasets/[new_dataset_name]/dirty/`
- README.md with all issues documented

## Best Practices

### Issue Selection

When creating dirty datasets, consider:

1. **Realism**: Issues should reflect real-world problems
2. **Variety**: Include different types of issues (missing, invalid, formatting, etc.)
3. **Severity**: Mix mild (easy to detect) and severe (requires careful analysis) issues
4. **Interdependence**: Some issues can be related (e.g., missing values causing data type issues)
5. **Domain-Specific**: Consider what issues are common in that domain

### Issue Rates

Typical rates for different issue types:
- **Missing values**: 5-20% depending on column importance
- **Duplicates**: 2-5%
- **Invalid values**: 1-3%
- **Outliers**: 1-3%
- **Formatting issues**: 10-20% of affected columns
- **Categorical inconsistencies**: 10-20% of categorical values

### Performance Considerations

For large datasets (100K+ rows):
- Use vectorized operations when possible
- Process in batches for memory-intensive operations
- Avoid row-by-row loops for large datasets
- Consider sampling for very large datasets

Example optimization:
```python
# Slow (row-by-row):
for idx in indices:
    df_dirty.loc[idx, col] = process_value(df_dirty.loc[idx, col])

# Fast (vectorized):
df_dirty.loc[indices, col] = df_dirty.loc[indices, col].apply(process_value)
```

## Reproducibility

The script uses fixed random seeds for reproducibility:
```python
np.random.seed(42)
random.seed(42)
```

This ensures that running the script multiple times produces the same dirty datasets.

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Ensure clean datasets exist in the correct location
2. **MemoryError**: For very large datasets, consider processing in chunks
3. **TypeError**: Check that column types match expected types before operations
4. **UnicodeEncodeError**: Ensure proper encoding when reading/writing files

### Debugging

Add print statements to track progress:
```python
print(f"Processing {config['name']}...")
print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"  Issues introduced: {len(issues)}")
```

## Example: Complete Workflow

1. **Prepare clean dataset**:
   ```bash
   # Place dataset in datasets/new_dataset/clean/
   ```

2. **Create dirty function**:
   ```python
   def dirty_new_dataset(df):
       # ... implementation
   ```

3. **Add to config**:
   ```python
   datasets_config.append({
       'name': 'New Dataset',
       # ... configuration
   })
   ```

4. **Run script**:
   ```bash
   python utils/create_dirty_datasets.py
   ```

5. **Verify output**:
   - Check dirty dataset was created
   - Review README.md for issue list
   - Test cleaning the dirty dataset

## Maintenance

### Updating Existing Datasets

If you need to modify the issues for an existing dataset:

1. Edit the dataset-specific function (e.g., `dirty_heart_failure()`)
2. Run the script to regenerate
3. Update documentation if issue types change

### Version Control

- Commit clean datasets to version control
- Consider adding dirty datasets to `.gitignore` if they're large
- Keep the script in version control for reproducibility

## Related Documentation

- Main dataset documentation: `DPP_Practice_Datasets.md`
- Individual dataset READMEs: `datasets/[dataset_name]/clean/README.md`
- Dirty dataset answer keys: `datasets/[dataset_name]/dirty/README.md`

## Notes

- The script is designed to be educational and create realistic practice scenarios
- Issues are intentionally introduced and documented for learning purposes
- Always validate cleaning steps against domain knowledge
- Some issues may be interdependent, requiring careful cleaning order

---

*Last updated: 2025*
*Script version: 1.0*

