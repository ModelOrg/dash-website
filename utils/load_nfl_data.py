"""
Load NFL data using nflreadpy and save as Parquet files.

Run this script once to download data:
    python utils/load_nfl_data.py

Then query the Parquet files in your Dash pages!
"""

import nflreadpy as nfl
import polars as pl
from pathlib import Path

# Create data directory
DATA_DIR = Path("data/parquet")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_play_by_play(seasons=[2022, 2023, 2024, 2025]):
    """Load play-by-play data and save as Parquet"""
    print(f"Loading play-by-play data for seasons {seasons}...")

    pbp = nfl.load_pbp(seasons)

    # Save raw data (polars or pandas both work)
    output_path = DATA_DIR / "nfl_pbp_raw.parquet"
    if isinstance(pbp, pl.DataFrame):
        pbp.write_parquet(output_path)
    else:
        pbp.to_parquet(output_path, index=False)
    print(f"✓ Saved: {output_path} ({len(pbp):,} plays)")

    return pbp


def create_team_game_stats(pbp):
    """Aggregate play-by-play into team game stats"""
    print("Creating team game stats...")

    # Convert to pandas for groupby operations (easier syntax)
    if isinstance(pbp, pl.DataFrame):
        pbp = pbp.to_pandas()

    team_games = (
        pbp.groupby(["game_id", "season", "week", "posteam"])
        .agg(
            {
                "yards_gained": "sum",
                "pass_attempt": "sum",
                "rush_attempt": "sum",
                "first_down": "sum",
                "interception": "sum",
                "fumble_lost": "sum",
                "touchdown": "sum",
                "posteam_score": "max",
            }
        )
        .reset_index()
    )

    # Rename columns for clarity
    team_games = team_games.rename(
        columns={
            "yards_gained": "total_yards",
            "pass_attempt": "pass_attempts",
            "rush_attempt": "rush_attempts",
            "first_down": "first_downs",
            "posteam_score": "points",
        }
    )

    # Calculate passing and rushing yards separately
    passing = (
        pbp[pbp["pass_attempt"] == 1]
        .groupby(["game_id", "posteam"])["yards_gained"]
        .sum()
        .reset_index()
    )
    passing = passing.rename(columns={"yards_gained": "passing_yards"})

    rushing = (
        pbp[pbp["rush_attempt"] == 1]
        .groupby(["game_id", "posteam"])["yards_gained"]
        .sum()
        .reset_index()
    )
    rushing = rushing.rename(columns={"yards_gained": "rushing_yards"})

    # Merge
    team_games = team_games.merge(passing, on=["game_id", "posteam"], how="left")
    team_games = team_games.merge(rushing, on=["game_id", "posteam"], how="left")

    # Fill NaN with 0
    team_games["passing_yards"] = team_games["passing_yards"].fillna(0)
    team_games["rushing_yards"] = team_games["rushing_yards"].fillna(0)

    # Calculate turnovers
    team_games["turnovers"] = team_games["interception"] + team_games["fumble_lost"]

    # Sort
    team_games = team_games.sort_values(["season", "week", "posteam"])

    output_path = DATA_DIR / "nfl_team_games.parquet"
    team_games.to_parquet(output_path, index=False)
    print(f"✓ Saved: {output_path} ({len(team_games):,} games)")

    return team_games


def load_team_info():
    """Load team reference data"""
    print("Loading team info...")

    teams = nfl.load_teams()

    # Save (polars or pandas both work)
    output_path = DATA_DIR / "nfl_teams.parquet"
    if isinstance(teams, pl.DataFrame):
        teams.write_parquet(output_path)
    else:
        teams.to_parquet(output_path, index=False)
    print(f"✓ Saved: {output_path} ({len(teams)} teams)")

    return teams


def load_rosters(seasons=[2025]):
    """Load player rosters"""
    print(f"Loading rosters for {seasons}...")

    rosters = nfl.load_rosters(seasons)

    # Save (polars or pandas both work)
    output_path = DATA_DIR / "nfl_rosters.parquet"
    if isinstance(rosters, pl.DataFrame):
        rosters.write_parquet(output_path)
    else:
        rosters.to_parquet(output_path, index=False)
    print(f"✓ Saved: {output_path} ({len(rosters):,} players)")

    return rosters


def main():
    """Load all NFL data"""
    print("=" * 60)
    print("NFL Data Loader (nflreadpy)")
    print("=" * 60)

    try:
        # Load play-by-play
        pbp = load_play_by_play(seasons=[2022, 2023, 2024, 2025])

        # Create aggregated stats
        team_games = create_team_game_stats(pbp)

        # Load team info
        teams = load_team_info()

        # Load rosters
        rosters = load_rosters(seasons=[2025])

        print("\n" + "=" * 60)
        print("✅ All data loaded successfully!")
        print("=" * 60)
        print("\nFiles created in data/parquet/:")
        print("  - nfl_pbp_raw.parquet (play-by-play)")
        print("  - nfl_team_games.parquet (team game stats)")
        print("  - nfl_teams.parquet (team info)")
        print("  - nfl_rosters.parquet (player rosters)")
        print("\nYou can now run your Dash app and query this data!")

    except Exception as e:
        print(f"\n❌ Error loading data: {e}")
        print("\nMake sure you have nflreadpy installed:")
        print("  pip install nflreadpy")


if __name__ == "__main__":
    main()
