library(nflverse)
library(arrow)

# Load play-by-play data
pbp <- load_pbp(seasons = 2024)

# Write to Parquet
write_parquet(pbp, "data/parquet/nfl_plays_2024.parquet")

print("Data exported successfully!")