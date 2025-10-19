# Setting Up nflverse Data

## Quick Setup (3 steps)

### 1. Install R Packages

Open R or RStudio and run:

```r
install.packages(c("nflverse", "arrow", "dplyr"))
```

This might take a few minutes.

### 2. Create the R Scripts Directory

```bash
mkdir r_scripts
```

### 3. Run the Fetch Script

```bash
Rscript r_scripts/fetch_nflverse.R
```

**This will download 2022-2024 NFL data** (takes 2-5 minutes depending on internet speed).

You'll see output like:
```
Starting nflverse data fetch...
Fetching play-by-play data...
✓ Saved: nfl_pbp_raw.parquet
✓ Saved: nfl_team_games.parquet
✓ Saved: nfl_weekly_stats.parquet
✓ Saved: nfl_teams.parquet
✅ All data exported successfully!
```

### 4. Refresh Your Dash App

The NFL Stats page will now show real data!

## What Data Gets Loaded?

- **nfl_pbp_raw.parquet** - Every play from 2022-2024 (~1M+ rows)
- **nfl_team_games.parquet** - Team stats per game (easier to query)
- **nfl_weekly_stats.parquet** - Weekly aggregates
- **nfl_teams.parquet** - Team info (names, colors, divisions)

## Updating Data

Just run the script again:
```bash
Rscript r_scripts/fetch_nflverse.R
```

It will overwrite with fresh data.

## Customizing

### Want Different Seasons?

Edit `fetch_nflverse.R` line 14:
```r
pbp <- load_pbp(seasons = 2020:2024)  # Change years here
```

### Want More Stats?

Add to the summarise() section in the R script. Available columns:
- `yards_gained`, `pass_attempt`, `rush_attempt`
- `touchdown`, `interception`, `fumble_lost`
- `sack`, `complete_pass`, `air_yards`
- `epa` (expected points added)
- And 200+ more!

See: https://nflverse.nflverse.com/articles/dictionary_pbp.html

## Troubleshooting

**"command not found: Rscript"**
- Install R: https://cran.r-project.org/

**"there is no package called 'nflverse'"**
- Run: `install.packages("nflverse")` in R

**"Error in load_pbp()"**
- Check internet connection
- Try: `options(timeout = 300)` in R before running script

**Data files are empty/missing**
- Check `data/parquet/` directory exists
- Verify R script completed without errors