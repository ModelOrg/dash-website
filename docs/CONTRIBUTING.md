# Contributing Guide

## Adding a New Page (3 Steps!)

### 1. Create a Dev Branch

```bash
git checkout -b my-analysis-name
```

### 2. Copy the Template

```bash
cp pages/_template.py pages/my_analysis.py
```

### 3. Edit Your Page

Open `pages/my_analysis.py` and update:

```python
# Change the path and name
dash.register_page(
    __name__, 
    path="/my-analysis",      # URL: localhost:8050/my-analysis
    name="My Analysis"         # Name in navigation menu
)

# Build your layout
layout = html.Div([
    html.H1("Your Title"),
    # Add your components...
])

# Add callbacks for interactivity
@callback(...)
def your_function(...):
    # Your logic here
```

### 4. Test Locally

```bash
python app.py
```

Visit `http://localhost:8050/my-analysis` to see your page!

### 5. Commit and Merge

```bash
git add pages/my_analysis.py
git commit -m "Add my analysis page"
git push origin my-analysis-name

# Create PR or merge to main
git checkout main
git merge my-analysis-name
```

## Best Practices

### Code Style

- Use descriptive variable names
- Add docstrings to functions
- Comment complex logic
- Keep callbacks focused (one purpose each)

### File Naming

- Use lowercase with underscores: `nfl_passing_analysis.py`
- Name should describe what the page does
- Avoid spaces or special characters

### Page Organization

```python
# Standard page structure:

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.query_engine import query_parquet

# 1. Register the page
dash.register_page(__name__, path="/...", name="...")

# 2. Define layout
layout = html.Div([...])

# 3. Add callbacks
@callback(...)
def update_chart(...):
    ...
```

### Data Queries

- Use `query_parquet()` from `utils/query_engine.py`
- Filter data in SQL when possible (faster)
- Test queries with small data first

```python
# Good: Filter in SQL
df = query_parquet("SELECT * FROM 'nfl_pbp_raw.parquet' WHERE season = 2024 LIMIT 100")

# Not ideal: Load everything then filter
df = query_parquet("SELECT * FROM 'nfl_pbp_raw.parquet'")
df = df[df['season'] == 2024]
```

## Common Patterns

### Multiple Filters

```python
layout = html.Div([
    dcc.Dropdown(id="season-filter"),
    dcc.Dropdown(id="team-filter"),
    dcc.Graph(id="my-chart")
])

@callback(
    Output("my-chart", "figure"),
    [Input("season-filter", "value"),
     Input("team-filter", "value")]
)
def update_chart(season, team):
    df = query_parquet(f"""
        SELECT * FROM 'nfl_team_games.parquet'
        WHERE season = {season} AND posteam = '{team}'
    """)
    fig = px.line(df, x="week", y="points")
    return fig
```

### Multiple Charts

```python
@callback(
    [Output("chart-1", "figure"),
     Output("chart-2", "figure")],
    Input("filter", "value")
)
def update_all(filter_val):
    df = query_parquet(...)
    fig1 = px.bar(...)
    fig2 = px.scatter(...)
    return fig1, fig2
```

### Loading States

```python
dcc.Loading(
    id="loading",
    type="default",
    children=dcc.Graph(id="my-chart")
)
```

## Getting Help

- Check `pages/example_nfl.py` for a complete working example
- Look at `pages/_template.py` for basic structure
- See [USAGE_GUIDE.md](USAGE_GUIDE.md) for component examples
- Ask the team in chat!

## What NOT to Commit

- Don't commit data files (`data/` is gitignored)
- Don't commit virtual environment files
- Don't commit `.env` files
- Don't commit IDE-specific files (`.vscode/`, `.idea/`)

## Troubleshooting

**Page doesn't appear in navigation**
- Check `dash.register_page()` is called
- Verify file is in `pages/` directory
- Restart the app

**Callback errors**
- Check Input/Output IDs match your layout
- Verify all Inputs are defined
- Look at console for error messages

**Data not loading**
- Run `python utils/load_nfl_data.py` first
- Check `data/parquet/` has files
- Verify query syntax with `utils/query_engine.py`