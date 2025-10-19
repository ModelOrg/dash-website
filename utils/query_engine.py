"""
Query engine for Parquet files using DuckDB.

This module provides simple functions to query your analytics data
without loading entire files into memory.
"""

import duckdb
import pandas as pd
from pathlib import Path

# Data directory - adjust this path as needed
DATA_DIR = Path(__file__).parent.parent / "data" / "parquet"


def query_parquet(sql: str, params: list = None) -> pd.DataFrame:
    """
    Execute SQL query on Parquet files using DuckDB.

    Args:
        sql: SQL query string. Can reference parquet files directly.
        params: Optional list of parameters for parameterized queries.

    Returns:
        DataFrame with query results

    Examples:
        # Query a single file
        df = query_parquet("SELECT * FROM 'nfl_plays.parquet' WHERE season = 2024")

        # Parameterized query
        df = query_parquet("SELECT * FROM 'nfl_plays.parquet' WHERE team = ?", ["KC"])

        # Query all parquet files in a directory
        df = query_parquet("SELECT * FROM 'data/parquet/*.parquet'")

        # Join multiple files
        df = query_parquet('''
            SELECT p.*, t.team_name
            FROM 'plays.parquet' p
            JOIN 'teams.parquet' t ON p.team_id = t.id
        ''')
    """
    conn = duckdb.connect(database=":memory:")

    # Set data directory for relative paths
    if DATA_DIR.exists():
        conn.execute(f"SET file_search_path='{DATA_DIR}'")

    try:
        if params:
            result = conn.execute(sql, params).fetchdf()
        else:
            result = conn.execute(sql).fetchdf()
    finally:
        conn.close()

    return result


def list_available_datasets() -> list:
    """
    List all available Parquet files in the data directory.

    Returns:
        List of filenames
    """
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return []

    return [f.name for f in DATA_DIR.glob("*.parquet")]


def get_table_info(filename: str) -> dict:
    """
    Get schema information for a Parquet file.

    Args:
        filename: Name of the parquet file

    Returns:
        Dictionary with column names and types
    """
    conn = duckdb.connect(database=":memory:")

    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {"error": f"File {filename} not found"}

    try:
        result = conn.execute(f"DESCRIBE SELECT * FROM '{file_path}'").fetchdf()
        return result.to_dict("records")
    finally:
        conn.close()


def create_sample_data():
    """
    Create sample Parquet files for testing.
    Call this once to set up example data.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Sample NFL data
    sample_nfl = pd.DataFrame(
        {
            "game_id": range(1, 101),
            "season": [2024] * 100,
            "week": [i % 17 + 1 for i in range(100)],
            "team": ["KC", "SF", "BUF", "PHI", "DAL"] * 20,
            "points": [24, 27, 21, 30, 17] * 20,
            "yards": [350, 400, 320, 380, 290] * 20,
        }
    )

    sample_nfl.to_parquet(DATA_DIR / "sample_nfl_games.parquet", index=False)
    print(f"Sample data created at {DATA_DIR / 'sample_nfl_games.parquet'}")


if __name__ == "__main__":
    # Test the query engine
    print("Testing query engine...")

    # Create sample data if needed
    if not list_available_datasets():
        print("No data found. Creating sample data...")
        create_sample_data()

    # Test query
    print("\nAvailable datasets:", list_available_datasets())

    print("\nRunning test query...")
    df = query_parquet("SELECT * FROM 'sample_nfl_games.parquet' LIMIT 5")
    print(df)
