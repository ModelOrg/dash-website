# Data Guide

Guide to available datasets and how to query them.

## Available Datasets

### NFL Play-by-Play Data

**File:** `nfl_pbp_raw.parquet`  
**Source:** nflreadpy  
**Seasons:** 2022-2024  
**Size:** ~1M+ rows

Every play from NFL games with detailed information.

**Key Columns:**
- `game_id` - Unique game identifier
- `season`, `week` - When the game occurred
- `posteam`, `defteam` - Offensive and defensive teams
- `play_type` - "pass", "run", "punt", "kickoff", etc.
- `yards_gained` - Yards on the play
- `touchdown`, `interception`, `fumble_lost` - Scoring events
- `first_down` - Whether play resulted in first down
- `epa` - Expected Points Added (advanced metric)
- `air_yards` - Yards ball traveled in air (passing)
- `qb_hit`, `sack` - Pass rush events

**Example Query:**
```python
df = query_parquet("""
    SELECT posteam, COUNT(*) as plays, AVG(epa) as avg_epa
    FROM 'nfl_pbp_raw.parquet'
    WHERE season = 2024 AND play_type = 'pass'
    GROUP BY posteam
    ORDER BY avg_epa DESC
""")
```

---

### NFL Team Game Stats

**File:** `nfl_team_games.parquet`  
**Source:** Aggregated from play-by-play  
**Seasons:** 2022-2024

Team statistics per game (easier to query than raw play-by-play).

**Columns:**
- `game_id` - Game identifier
- `season`, `week` - When the game occurred
- `posteam` - Team abbreviation (e.g., "KC", "SF")
- `total_yards` - Total offensive yards
- `passing_yards` - Passing yards
- `rushing_yards` - Rushing yards
- `points` - Points scored
- `turnovers` - Interceptions + fumbles lost
- `first_downs` - Total first downs
- `pass_attempts`, `rush_attempts` - Number of plays

**Example Query:**
```python
df = query_parquet("""
    SELECT posteam, AVG(points) as avg_points, AVG(total_yards) as avg_yards
    FROM 'nfl_team_games.parquet'
    WHERE season = 2024
    GROUP BY posteam
    ORDER BY avg_points DESC
""")
```

---

### NFL Teams Reference

**File:** `nfl_teams.parquet`  
**Source:** nflreadpy

Team information and metadata.

**Columns:**
- `team_abbr` - Team abbreviation ("KC", "SF", etc.)
- `team_name` - Full team name
- `team_conf` - Conference (AFC/NFC)
- `team_division` - Division (North, South, East, West)
- `team_color`, `team_color2` - Team colors (hex codes)

**Example Query:**
```python
teams = query_parquet("SELECT * FROM 'nfl_teams.parquet'")
```

---

### NFL Rosters

**File:** `nfl_rosters.parquet`  
**Source:** nflreadpy  
**Season:** 2024

Player roster information.

**Key Columns:**
- `player_id`, `player_name` - Player identifiers
- `team` - Current team
- `position` - Player position
- `jersey_number` - Jersey number
- `status` - Active/Injured/etc.
- `height`, `weight` - Physical stats
- `birth_date` - Date of birth
- `college` - College attended

**Example Query:**
```python
qbs = query_parquet("""
    SELECT player_name, team, college
    FROM 'nfl_rosters.parquet'
    WHERE position = 'QB'
    ORDER BY team
""")
```

---

## Querying Data

### Basic Queries

```python
from utils.query_engine import query_parquet

# Select all columns
df = query_parquet("SELECT * FROM 'nfl_team_games.parquet'")

# Filter rows
df = query_parquet("SELECT * FROM 'nfl_team_games.parquet' WHERE season = 2024")

# Select specific columns
df = query_parquet("SELECT posteam, points, total_yards FROM 'nfl_team_games.parquet'")
```

### Filtering

```python
# Single condition
df = query_parquet("SELECT * FROM 'nfl_team_games.parquet' WHERE posteam = 'KC'")

# Multiple conditions (AND)
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    WHERE season = 2024 AND posteam = 'KC'
""")

# Multiple conditions (OR)
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    WHERE posteam = 'KC' OR posteam = 'SF'
""")

# IN clause
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    WHERE posteam IN ('KC', 'SF', 'BUF')
""")

# Ranges
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    WHERE points BETWEEN 20 AND 30
""")

# NULL checks
df = query_parquet("""
    SELECT * FROM 'nfl_pbp_raw.parquet' 
    WHERE posteam IS NOT NULL
""")
```

### Aggregations

```python
# Count
df = query_parquet("SELECT COUNT(*) as total_plays FROM 'nfl_pbp_raw.parquet'")

# Average
df = query_parquet("SELECT AVG(points) as avg_points FROM 'nfl_team_games.parquet'")

# Sum, Min, Max
df = query_parquet("""
    SELECT 
        SUM(points) as total_points,
        MIN(points) as min_points,
        MAX(points) as max_points
    FROM 'nfl_team_games.parquet'
    WHERE posteam = 'KC'
""")

# Group by
df = query_parquet("""
    SELECT posteam, AVG(points) as avg_points
    FROM 'nfl_team_games.parquet'
    GROUP BY posteam
    ORDER BY avg_points DESC
""")

# Multiple aggregations
df = query_parquet("""
    SELECT 
        season,
        COUNT(*) as games,
        AVG(points) as avg_points,
        SUM(total_yards) as total_yards
    FROM 'nfl_team_games.parquet'
    WHERE posteam = 'KC'
    GROUP BY season
""")
```

### Sorting

```python
# Sort ascending
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    ORDER BY points ASC
""")

# Sort descending
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    ORDER BY points DESC
""")

# Multiple columns
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    ORDER BY season DESC, week ASC
""")
```

### Limiting Results

```python
# Top 10 results
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    ORDER BY points DESC 
    LIMIT 10
""")

# Skip first 10, get next 10
df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    ORDER BY points DESC 
    LIMIT 10 OFFSET 10
""")
```

### Joins

```python
# Join team games with team info
df = query_parquet("""
    SELECT 
        g.posteam,
        t.team_name,
        g.points,
        g.total_yards
    FROM 'nfl_team_games.parquet' g
    JOIN 'nfl_teams.parquet' t ON g.posteam = t.team_abbr
    WHERE g.season = 2024
""")
```

### Parameterized Queries

```python
# Use parameters for safety (prevents SQL injection)
team = "KC"
season = 2024

df = query_parquet("""
    SELECT * FROM 'nfl_team_games.parquet' 
    WHERE posteam = ? AND season = ?
""", [team, season])
```

---

## Common Patterns

### Team Season Stats

```python
def get_team_season_stats(team, season):
    return query_parquet(f"""
        SELECT 
            COUNT(*) as games_played,
            AVG(points) as avg_points,
            AVG(total_yards) as avg_yards,
            SUM(turnovers) as total_turnovers
        FROM 'nfl_team_games.parquet'
        WHERE posteam = '{team}' AND season = {season}
    """)
```

### Weekly Trends

```python
def get_weekly_stats(team, season, stat):
    return query_parquet(f"""
        SELECT week, {stat}
        FROM 'nfl_team_games.parquet'
        WHERE posteam = '{team}' AND season = {season}
        ORDER BY week
    """)
```

### Team Comparisons

```python
def compare_teams(teams, season):
    team_list = "', '".join(teams)
    return query_parquet(f"""
        SELECT 
            posteam,
            AVG(points) as avg_points,
            AVG(total_yards) as avg_yards,
            SUM(turnovers) as turnovers
        FROM 'nfl_team_games.parquet'
        WHERE poste