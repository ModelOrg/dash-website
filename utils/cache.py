# 10.1 Caching Strategy
# Use Case 1: Expensive Queries
# pythonfrom functools import lru_cache


@lru_cache(maxsize=100)
def get_season_stats(season, team):
    return query_parquet(f"SELECT * FROM stats WHERE season={season} AND team='{team}'")


# Use Case 2: Page-Level Caching
# pythonfrom flask_caching import Cache

# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'simple',
#     'CACHE_DEFAULT_TIMEOUT': 300
# })

# @cache.memoize(timeout=600)
# def expensive_computation():
#     # ...
