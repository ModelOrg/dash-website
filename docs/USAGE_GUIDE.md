# Usage Guide

Complete guide to building dashboards with Dash.

## Table of Contents

1. [Layout Components](#layout-components)
2. [Interactive Controls](#interactive-controls)
3. [Charts & Visualizations](#charts--visualizations)
4. [Callbacks](#callbacks)
5. [Styling](#styling)

---

## Layout Components

### Basic Structure

```python
from dash import html

layout = html.Div([
    html.H1("Page Title"),
    html.H2("Section Header"),
    html.P("Paragraph text"),
    html.Hr(),  # Horizontal line
    html.Br(),  # Line break
])
```

### Divs and Containers

```python
# Simple div
html.Div([...], style={"margin": "20px"})

# Columns (side by side)
html.Div([
    html.Div([...], style={"width": "48%", "display": "inline-block"}),
    html.Div([...], style={"width": "48%", "display": "inline-block"})
])

# Bootstrap components (better styling)
import dash_bootstrap_components as dbc

dbc.Container([
    dbc.Row([
        dbc.Col([...], width=6),
        dbc.Col([...], width=6)
    ])
])
```

### Text Formatting

```python
html.P([
    "Some text with ",
    html.Strong("bold"),
    " and ",
    html.Em("italic"),
    " and ",
    html.Code("code"),
])
```

---

## Interactive Controls

### Dropdown

```python
from dash import dcc

dcc.Dropdown(
    id="my-dropdown",
    options=[
        {"label": "Option 1", "value": "opt1"},
        {"label": "Option 2", "value": "opt2"}
    ],
    value="opt1",           # Default value
    multi=False,            # Single selection
    clearable=True,         # Can clear selection
    searchable=True         # Can type to search
)
```

### Slider

```python
dcc.Slider(
    id="my-slider",
    min=0,
    max=100,
    step=5,
    value=50,
    marks={0: '0', 50: '50', 100: '100'}
)

# Range slider
dcc.RangeSlider(
    id="range-slider",
    min=0,
    max=100,
    value=[25, 75]
)
```

### Radio Buttons

```python
dcc.RadioItems(
    id="radio",
    options=[
        {"label": "Option A", "value": "a"},
        {"label": "Option B", "value": "b"}
    ],
    value="a"
)
```

### Checkboxes

```python
dcc.Checklist(
    id="checklist",
    options=[
        {"label": "Item 1", "value": "1"},
        {"label": "Item 2", "value": "2"}
    ],
    value=["1"]  # Pre-checked items
)
```

### Date Picker

```python
dcc.DatePickerSingle(
    id="date-picker",
    date="2024-01-01"
)

dcc.DatePickerRange(
    id="date-range",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Input Box

```python
dcc.Input(
    id="text-input",
    type="text",      # or "number", "email", etc.
    placeholder="Enter text...",
    value=""
)
```

---

## Charts & Visualizations

### Line Chart

```python
import plotly.express as px

df = query_parquet("SELECT * FROM 'nfl_team_games.parquet' WHERE posteam = 'KC'")

fig = px.line(
    df, 
    x="week", 
    y="points",
    title="Points by Week",
    markers=True,           # Show points
    labels={"week": "Week", "points": "Points Scored"}
)

dcc.Graph(figure=fig)
```

### Bar Chart

```python
fig = px.bar(
    df,
    x="team",
    y="total_yards",
    color="team",           # Color by category
    title="Total Yards by Team"
)
```

### Scatter Plot

```python
fig = px.scatter(
    df,
    x="passing_yards",
    y="points",
    size="rushing_yards",   # Bubble size
    color="team",           # Color by category
    hover_data=["week"],    # Extra info on hover
    title="Passing vs Points"
)
```

### Histogram

```python
fig = px.histogram(
    df,
    x="points",
    nbins=20,
    title="Points Distribution"
)
```

### Box Plot

```python
fig = px.box(
    df,
    x="team",
    y="points",
    title="Points Distribution by Team"
)
```

### Heatmap

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
    z=[[1, 2, 3], [4, 5, 6]],
    x=["A", "B", "C"],
    y=["Row 1", "Row 2"],
    colorscale="Viridis"
))
```

### Multiple Traces

```python
fig = go.Figure()

fig.add_trace(go.Scatter(x=df["week"], y=df["passing_yards"], name="Passing"))
fig.add_trace(go.Scatter(x=df["week"], y=df["rushing_yards"], name="Rushing"))

fig.update_layout(title="Yards by Type", xaxis_title="Week", yaxis_title="Yards")
```

### Styling Charts

```python
fig.update_layout(
    title="My Chart Title",
    xaxis_title="X Axis",
    yaxis_title="Y Axis",
    hovermode="x unified",      # Unified hover
    plot_bgcolor="white",       # Background color
    font=dict(size=14),
    showlegend=True
)

fig.update_traces(
    line=dict(width=3),         # Line width
    marker=dict(size=10)        # Marker size
)
```

---

## Callbacks

### Basic Callback

```python
from dash import callback, Input, Output

@callback(
    Output("output-id", "figure"),
    Input("input-id", "value")
)
def update_chart(selected_value):
    df = query_parquet(f"SELECT * FROM data WHERE category = '{selected_value}'")
    fig = px.line(df, x="x", y="y")
    return fig
```

### Multiple Inputs

```python
@callback(
    Output("chart", "figure"),
    [Input("dropdown1", "value"),
     Input("dropdown2", "value"),
     Input("slider", "value")]
)
def update(val1, val2, val3):
    # Use all three inputs
    df = query_parquet(...)
    fig = px.bar(...)
    return fig
```

### Multiple Outputs

```python
@callback(
    [Output("chart1", "figure"),
     Output("chart2", "figure"),
     Output("summary", "children")],
    Input("filter", "value")
)
def update_all(filter_val):
    df = query_parquet(...)
    
    fig1 = px.line(df, x="x", y="y1")
    fig2 = px.bar(df, x="x", y="y2")
    summary = html.P(f"Showing data for {filter_val}")
    
    return fig1, fig2, summary
```

### Chained Callbacks

```python
# Callback 1: Update dropdown options based on season
@callback(
    Output("team-dropdown", "options"),
    Input("season-dropdown", "value")
)
def update_teams(season):
    teams = query_parquet(f"SELECT DISTINCT team FROM data WHERE season = {season}")
    return [{"label": t, "value": t} for t in teams["team"]]

# Callback 2: Update chart based on team
@callback(
    Output("chart", "figure"),
    Input("team-dropdown", "value")
)
def update_chart(team):
    df = query_parquet(f"SELECT * FROM data WHERE team = '{team}'")
    return px.line(df, x="week", y="points")
```

### Prevent Initial Call

```python
@callback(
    Output("chart", "figure"),
    Input("button", "n_clicks"),
    prevent_initial_call=True  # Don't run on page load
)
def update(n_clicks):
    ...
```

---

## Styling

### Inline Styles

```python
html.Div(
    [...],
    style={
        "margin": "20px",
        "padding": "10px",
        "background-color": "#f0f0f0",
        "border-radius": "5px",
        "width": "50%"
    }
)
```

### Common Style Properties

```python
{
    # Spacing
    "margin": "20px",
    "margin-top": "10px",
    "padding": "15px",
    
    # Size
    "width": "50%",
    "height": "400px",
    
    # Display
    "display": "inline-block",
    "display": "flex",
    "vertical-align": "top",
    
    # Colors
    "background-color": "#ffffff",
    "color": "#333333",
    
    # Text
    "font-size": "16px",
    "font-weight": "bold",
    "text-align": "center",
    
    # Border
    "border": "1px solid #ddd",
    "border-radius": "5px"
}
```

### Bootstrap Components

```python
import dash_bootstrap_components as dbc

# Cards
dbc.Card([
    dbc.CardHeader("Header"),
    dbc.CardBody([
        html.H4("Title"),
        html.P("Content")
    ])
], className="mb-3")

# Alerts
dbc.Alert("This is an alert!", color="info")

# Buttons
dbc.Button("Click Me", id="btn", color="primary")
```

---

## Tips & Tricks

### Loading States

```python
dcc.Loading(
    id="loading",
    type="default",  # or "circle", "dot", "cube"
    children=dcc.Graph(id="chart")
)
```

### Tabs

```python
dcc.Tabs([
    dcc.Tab(label="Tab 1", children=[...]),
    dcc.Tab(label="Tab 2", children=[...]),
])
```

### Markdown

```python
dcc.Markdown("""
## Markdown Title
This supports **bold** and *italic* text.

- Bullet points
- Work too!
""")
```

### Conditional Display

```python
@callback(
    Output("chart", "style"),
    Input("toggle", "value")
)
def toggle_visibility(show):
    if show:
        return {"display": "block"}
    else:
        return {"display": "none"}
```

---

## Example: Complete Dashboard

```python
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.query_engine import query_parquet

dash.register_page(__name__, path="/example", name="Example")

layout = html.Div([
    html.H1("My Dashboard"),
    
    # Filters
    html.Div([
        html.Label("Select Team:"),
        dcc.Dropdown(id="team-dd", options=[...], value="KC"),
        
        html.Label("Select Season:"),
        dcc.Dropdown(id="season-dd", options=[...], value=2024)
    ], style={"width": "50%", "margin-bottom": "30px"}),
    
    # Charts
    dcc.Loading(
        children=[
            dcc.Graph(id="trend-chart"),
            dcc.Graph(id="distribution-chart")
        ]
    ),
    
    # Summary
    html.Div(id="summary")
])

@callback(
    [Output("trend-chart", "figure"),
     Output("distribution-chart", "figure"),
     Output("summary", "children")],
    [Input("team-dd", "value"),
     Input("season-dd", "value")]
)
def update_dashboard(team, season):
    df = query_parquet(f"""
        SELECT * FROM 'nfl_team_games.parquet'
        WHERE posteam = '{team}' AND season = {season}
    """)
    
    fig1 = px.line(df, x="week", y="points", title="Points Trend")
    fig2 = px.histogram(df, x="points", title="Points Distribution")
    
    summary = html.Div([
        html.H4(f"Season Stats for {team}"),
        html.P(f"Average Points: {df['points'].mean():.1f}"),
        html.P(f"Games Played: {len(df)}")
    ])
    
    return fig1, fig2, summary
```

---

For more examples, check out `pages/example_nfl.py` in the repo!