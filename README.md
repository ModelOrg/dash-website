# Sports Analytics Platform

A collaborative sports analytics website built with Dash. Designed for Python developers who want to create analytics pages quickly without frontend experience.

## 🚀 Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd sports-analytics-platform

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Sample Data (Optional)

```bash
python utils/query_engine.py
```

This creates sample data files you can query.

### 3. Run the App

```bash
python app.py
```

Visit: **http://localhost:8050**

## 📁 Project Structure

```
sports-analytics-platform/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── pages/                    # All your analytics pages
│   ├── home.py              # Landing page
│   ├── _template.py         # Copy this to create new pages
│   └── example_nfl.py       # Example dashboard
├── utils/                    # Utilities
│   └── query_engine.py      # DuckDB query helpers
└── data/                     # Data storage
    └── parquet/             # Your Parquet files go here
```

## ✨ Adding a New Page

**Super easy - just 3 steps:**

1. **Copy the template:**
   ```bash
   cp pages/_template.py pages/my_analysis.py
   ```

2. **Edit `my_analysis.py`:**
   ```python
   dash.register_page(__name__, path="/my-analysis", name="My Analysis")
   ```

3. **Refresh your browser** - your page appears in the nav menu! 🎉

## 📊 Working with Data

### Query Parquet Files

```python
from utils.query_engine import query_parquet

# Simple query
df = query_parquet("SELECT * FROM 'my_data.parquet' WHERE season = 2024")

# Parameterized query
df = query_parquet("SELECT * FROM 'plays.parquet' WHERE team = ?", ["KC"])

# Aggregate data
df = query_parquet("""
    SELECT team, AVG(points) as avg_points
    FROM 'games.parquet'
    GROUP BY team
    ORDER BY avg_points DESC
""")
```

### Add Your Data

Just drop Parquet files into `data/parquet/` and query them!

```python
import pandas as pd

# Save your data as Parquet
df.to_parquet("data/parquet/my_data.parquet")
```

## 🎨 Building Dashboards

### Interactive Controls

```python
from dash import dcc

# Dropdown
dcc.Dropdown(
    id="my-dropdown",
    options=[{"label": "Option 1", "value": "opt1"}],
    value="opt1"
)

# Slider
dcc.Slider(min=0, max=100, value=50, id="my-slider")

# Date picker
dcc.DatePickerRange(id="date-picker")
```

### Callbacks (Make it Interactive)

```python
from dash import callback, Input, Output

@callback(
    Output("my-graph", "figure"),
    Input("my-dropdown", "value")
)
def update_graph(selected_value):
    df = query_parquet(f"SELECT * FROM data WHERE category = '{selected_value}'")
    fig = px.line(df, x="date", y="value")
    return fig
```

## 🔧 Tips for Your Team

### For Python Folks New to Dash:
- Each page is just a Python file
- Layout is built with Python objects (no HTML needed)
- Callbacks connect inputs to outputs
- Check `example_nfl.py` for a complete example

### For Data Scientists:
- Use pandas/polars as usual
- DuckDB queries are just SQL
- Plotly handles all your viz needs
- No need to learn JavaScript!

### Performance Tips:
- DuckDB only loads the columns you need
- Query Parquet files directly (no full load)
- Use `LIMIT` while developing
- Add caching for expensive queries

## 📚 Common Patterns

### Multiple Charts on One Page

```python
layout = html.Div([
    dcc.Graph(id="chart-1"),
    dcc.Graph(id="chart-2"),
    dcc.Graph(id="chart-3")
])

@callback(
    [Output("chart-1", "figure"),
     Output("chart-2", "figure"),
     Output("chart-3", "figure")],
    Input("filter", "value")
)
def update_all_charts(filter_val):
    # Return multiple figures
    return fig1, fig2, fig3
```

### Tabs for Organization

```python
from dash import dcc

layout = dcc.Tabs([
    dcc.Tab(label="Overview", children=[...]),
    dcc.Tab(label="Details", children=[...]),
    dcc.Tab(label="Trends", children=[...])
])
```

## 🔌 R Integration

### Option 1: Scheduled Jobs (Easiest)

```bash
# Run your R script to fetch data
Rscript r_scripts/fetch_nflverse.R

# It exports to data/parquet/
# Python queries it directly!
```

### Option 2: Real-time API (Advanced)

Set up Plumber API in R, call it from Python. See full specs doc for details.

## 🚢 Deployment

### Railway (Recommended)
1. Push to GitHub
2. Connect Railway to repo
3. Deploy! (Railway auto-detects Python)

### DigitalOcean
1. Create App Platform app
2. Point to your repo
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python app.py`

## 📖 Documentation

- `pages/_template.py` - Commented template to copy
- `example_nfl.py` - Full working example
- Technical specs doc - Complete architecture details

## 🤝 Getting Help

- Check existing pages for examples
- Run `python utils/query_engine.py` to test queries
- Ask in team chat!
- Dash docs: https://dash.plotly.com

## 🎯 Next Steps

1. ✅ Get the app running locally
2. ✅ Try creating a page from the template
3. ✅ Add your first dataset
4. ✅ Build your first visualization
5. ✅ Share with the team!

---

**Built with:** Dash, DuckDB, Plotly, Python ❤️