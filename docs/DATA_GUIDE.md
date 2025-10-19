6. Data Storage Strategy
6.1 What Goes Where
PostgreSQL (Small, relational data):

User accounts/permissions
Page metadata
Lookup tables (team names, player IDs)
Application configuration

Parquet Files (Large tabular data):

Play-by-play data
Player statistics (season-level)
Historical game logs
Model outputs/predictions

6.2 Parquet File Naming Convention
{sport}_{data_type}_{time_period}.parquet

Examples:
- nfl_plays_2024.parquet
- nba_shots_2023_2024.parquet
- mlb_batting_career.parquet
6.3 Data Refresh Strategy
Option A: Full Replace
pythondf.to_parquet("data/parquet/nfl_plays_2024.parquet")
Option B: Partitioned (for large datasets)
pythondf.to_parquet(
    "data/parquet/nfl_plays/",
    partition_cols=["season", "week"]
)
Query partitioned data:
sqlSELECT * FROM 'data/parquet/nfl_plays/**/*.parquet' 
WHERE season = 2024

10.2 Data Loading Best Practices

Use DuckDB's ability to query Parquet files directly (no full load into memory)
Filter early in SQL queries (push filtering down)
Use columnar storage advantages (only read needed columns)
Consider partitioning large datasets by season/date