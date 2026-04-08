# Spotify Dataset

## Overview
Well-structured dataset containing Spotify track information suitable for time series analysis or higher-level exploratory data analysis. The dataset consists of two files: one with recent/contemporary tracks and another with popular tracks from 2009-2023 by well-known artists. Excellent for analyzing musical trends, artist popularity, and audio feature relationships.

## Data Description

### spotify_data clean.csv
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

### track_data_final.csv
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

## Use Cases
- Time series analysis: Analyze trends in music popularity over time
- Exploratory data analysis: Understand relationships between popularity, genres, and artist metrics
- Regression: Predict track popularity based on features
- Clustering: Group tracks by genre, artist, or audio features
- Trend analysis: Compare musical characteristics across different time periods
- Artist analysis: Study artist popularity and follower growth patterns

