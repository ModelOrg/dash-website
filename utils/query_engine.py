import duckdb
from pathlib import Path

DATA_DIR = Path("data/parquet")


def query_parquet(sql: str, params: list = None):
    """
    Execute SQL query on Parquet files using DuckDB.

    Example:
        df = query_parquet("SELECT * FROM 'nfl_plays.parquet' WHERE season = ?", [2024])
    """
    conn = duckdb.connect(database=":memory:")

    # Set data directory for relative paths
    conn.execute(f"SET file_search_path='{DATA_DIR}'")

    if params:
        result = conn.execute(sql, params).fetchdf()
    else:
        result = conn.execute(sql).fetchdf()

    conn.close()
    return result


def list_available_datasets():
    """Return list of available Parquet files."""
    return [f.name for f in DATA_DIR.glob("*.parquet")]
