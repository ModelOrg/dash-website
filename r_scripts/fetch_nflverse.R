#!/usr/bin/env Rscript

# Fetch data from nflverse and export to Parquet
# Run this script: Rscript r_scripts/fetch_nflverse.R

library(nflverse)
library(arrow)
library(dplyr)

cat("Starting nflverse data fetch...\n")

# Create data directory if it doesn't exist
dir.create("data/parquet", recursive = TRUE, showWarnings = FALSE)

# 1. Load play-by-play data (last 3 seasons)
cat("Fetching play-by-play data...\n")
pbp <- load_pbp(seasons = 2022:2024)

# Export full play-by-play
write_parquet(pbp, "data/parquet/nfl_pbp_raw.parquet")
cat("✓ Saved: nfl_pbp_raw.parquet\n")

# 2. Create aggregated team stats by game
cat("Creating team game stats...\n")
team_games <- pbp %>%
  filter(!is.na(posteam)) %>%
  group_by(game_id, season, week, posteam) %>%
  summarise(
    total_yards = sum(yards_gained, na.rm = TRUE),
    passing_yards = sum(yards_gained[pass == 1], na.rm = TRUE),
    rushing_yards = sum(yards_gained[rush == 1], na.rm = TRUE),
    points = max(posteam_score, na.rm = TRUE),
    turnovers = sum(interception == 1 | fumble_lost == 1, na.rm = TRUE),
    first_downs = sum(first_down == 1, na.rm = TRUE),
    plays = n(),
    .groups = 'drop'
  ) %>%
  arrange(season, week, posteam)

write_parquet(team_games, "data/parquet/nfl_team_games.parquet")
cat("✓ Saved: nfl_team_games.parquet\n")

# 3. Create weekly team stats
cat("Creating weekly team aggregates...\n")
weekly_stats <- team_games %>%
  group_by(season, week, posteam) %>%
  summarise(
    games = n(),
    avg_points = mean(points, na.rm = TRUE),
    avg_yards = mean(total_yards, na.rm = TRUE),
    avg_pass_yards = mean(passing_yards, na.rm = TRUE),
    avg_rush_yards = mean(rushing_yards, na.rm = TRUE),
    total_turnovers = sum(turnovers, na.rm = TRUE),
    .groups = 'drop'
  )

write_parquet(weekly_stats, "data/parquet/nfl_weekly_stats.parquet")
cat("✓ Saved: nfl_weekly_stats.parquet\n")

# 4. Get team info for lookups
cat("Fetching team info...\n")
teams <- load_teams() %>%
  select(team_abbr, team_name, team_conf, team_division, team_color, team_color2)

write_parquet(teams, "data/parquet/nfl_teams.parquet")
cat("✓ Saved: nfl_teams.parquet\n")

cat("\n✅ All data exported successfully!\n")
cat("\nFiles created:\n")
cat("  - nfl_pbp_raw.parquet (play-by-play data)\n")
cat("  - nfl_team_games.parquet (team stats per game)\n")
cat("  - nfl_weekly_stats.parquet (weekly aggregates)\n")
cat("  - nfl_teams.parquet (team reference data)\n")
cat("\nYou can now query these files in Python!\n")