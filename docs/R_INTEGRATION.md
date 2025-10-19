5. R Integration Strategy
5.1 MVP Approach: Scheduled Jobs
Workflow:

R script runs on schedule (cron job or Task Scheduler)
Fetches data from nflverse
Exports to Parquet format
Saves to data/parquet/ directory
Python apps query the Parquet files via DuckDB

Example R Script (r_scripts/fetch_nflverse.R):
rlibrary(nflverse)
library(arrow)

# Load play-by-play data
pbp <- load_pbp(seasons = 2024)

# Write to Parquet
write_parquet(pbp, "data/parquet/nfl_plays_2024.parquet")

print("Data exported successfully!")
Scheduling:

Linux/Mac: Add to crontab (crontab -e)

  0 3 * * * Rscript /path/to/r_scripts/fetch_nflverse.R

Windows: Use Task Scheduler

5.2 Future Enhancement: Plumber API
If real-time R queries become necessary:
r# api.R
library(plumber)
library(nflverse)

#* Get play-by-play data
#* @param season The NFL season
#* @get /pbp
function(season = 2024) {
  pbp <- load_pbp(seasons = as.integer(season))
  return(pbp)
}
Run: Rscript -e "plumber::plumb('api.R')$run(port=8000)"
Python calls via requests.get("http://localhost:8000/pbp?season=2024")

# Installation
install.packages(c(
  "nflverse",
  "arrow",        # For Parquet export
  "plumber",      # If building API
  "dplyr",
  "tidyverse"
))