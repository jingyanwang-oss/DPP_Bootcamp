# Spotify - Dirty Datasets

## Overview
This directory contains the "dirty" versions of the Spotify datasets, created to simulate real-world data quality issues commonly encountered in data engineering and machine learning projects. These datasets contain intentional data quality problems that need to be identified and resolved during exploratory data analysis and preprocessing.

Well-structured dataset containing Spotify track information suitable for time series analysis or higher-level exploratory data analysis. The dataset consists of two files: one with recent/contemporary tracks and another with popular tracks from 2009-2023 by well-known artists. Excellent for analyzing musical trends, artist popularity, and audio feature relationships.

## Data Description

### 1. Spotify Clean Data Dataset (`spotify_data clean.csv`)

- **Rows:** 8,582
- **Columns:** 15
- **Description:** Data for recent and contemporary Spotify tracks, mainly from 2025. Each row represents a single track with its artist, album, and popularity data.

#### Features
- **track_id:** Unique Spotify track identifier
- **track_name:** Name of the track
- **track_number:** Track number on the album
- **track_popularity:** Track popularity score (0-100)
- **explicit:** Whether the track contains explicit content (TRUE/FALSE)
- **artist_name:** Name of the artist
- **artist_popularity:** Artist popularity score
- **artist_followers:** Number of artist followers
- **artist_genres:** List of artist genres
- **album_id:** Unique Spotify album identifier
- **album_name:** Name of the album
- **album_release_date:** Album release date
- **album_total_tracks:** Total number of tracks on the album
- **album_type:** Type of album (album, single, compilation, etc.)
- **track_duration_min:** Track duration in minutes

#### Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 12% artist_genres, 5% album_release_date, 3% explicit
2. Inconsistent explicit: Mix of TRUE/True/1/yes and FALSE/False/0/no
3. Date format inconsistencies: Mix of YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
4. Invalid values: track_popularity outside 0-100, negative duration values
5. Genre formatting: Mix of list format ['pop'] and comma-separated 'pop'
6. Text formatting: Extra whitespace in track_name, artist_name, album_name
7. Data type issues: Numeric columns as strings in 10% of rows
8. Inconsistent album_type: Mixed casing (Album/album/ALBUM)
9. Duplicates: 2% duplicate tracks
10. Noise columns: Added scraped_timestamp, data_source, playlist_id

### 2. Track Data Final Dataset (`track_data_final.csv`)

- **Rows:** 8,778
- **Columns:** 15
- **Description:** Popular and timeless Spotify songs from 2009-2023 from well-known singers including Taylor Swift, Billie Eilish, Rihanna, and others. This collection aids in analyzing long-term shifts in musical style, song length, and artist fame.

#### Features
- **track_id:** Unique Spotify track identifier
- **track_name:** Name of the track
- **track_number:** Track number on the album
- **track_popularity:** Track popularity score (0-100)
- **track_duration_ms:** Track duration in milliseconds
- **explicit:** Whether the track contains explicit content (TRUE/FALSE)
- **artist_name:** Name of the artist
- **artist_popularity:** Artist popularity score
- **artist_followers:** Number of artist followers
- **artist_genres:** List of artist genres
- **album_id:** Unique Spotify album identifier
- **album_name:** Name of the album
- **album_release_date:** Album release date
- **album_total_tracks:** Total number of tracks on the album
- **album_type:** Type of album (album, single, compilation, etc.)

**Note:** The main difference between the two files is the duration field (minutes vs milliseconds) and the time period covered.

#### Data Quality Issues Introduced

The following data quality issues have been intentionally introduced to this dataset:

1. Missing values: 12% artist_genres, 5% album_release_date, 3% explicit
2. Inconsistent explicit: Mix of TRUE/True/1/yes and FALSE/False/0/no
3. Date format inconsistencies: Mix of YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
4. Invalid values: track_popularity outside 0-100, negative duration values
5. Genre formatting: Mix of list format ['pop'] and comma-separated 'pop'
6. Text formatting: Extra whitespace in track_name, artist_name, album_name
7. Data type issues: Numeric columns as strings in 10% of rows
8. Inconsistent album_type: Mixed casing (Album/album/ALBUM)
9. Duplicates: 2% duplicate tracks
10. Noise columns: Added scraped_timestamp, data_source, playlist_id

## How to Use These Datasets

These dirty datasets are designed for:
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
- Time series analysis: Analyze trends in music popularity over time
- Exploratory data analysis: Understand relationships between popularity, genres, and artist metrics
- Regression: Predict track popularity based on features
- Clustering: Group tracks by genre, artist, or audio features
- Trend analysis: Compare musical characteristics across different time periods
- Artist analysis: Study artist popularity and follower growth patterns

## Notes

- The issues introduced are realistic and commonly found in real-world datasets
- Some issues may be interdependent (e.g., missing values and data type issues)
- The severity of issues varies to provide a range of cleaning challenges
- Always validate your cleaning steps against domain knowledge

---
*This dirty dataset was programmatically generated for educational purposes.*

