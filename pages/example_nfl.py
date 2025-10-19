"""
Example NFL stats page showing how to build an interactive dashboard.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/nfl-example", name="NFL Example")


# Sample data (replace with real data queries later)
def get_sample_data(team, stat_type):
    """Generate sample data - replace with actual DuckDB queries"""
    weeks = list(range(1, 18))

    if stat_type == "passing":
        values = [250 + (i * 20) + (hash(team) % 50) for i in weeks]
        label = "Passing Yards"
    elif stat_type == "rushing":
        values = [100 + (i * 10) + (hash(team) % 30) for i in weeks]
        label = "Rushing Yards"
    else:
        values = [30 + (i * 2) + (hash(team) % 10) for i in weeks]
        label = "Points Scored"

    return pd.DataFrame({"Week": weeks, label: values, "Team": team})


layout = html.Div(
    [
        html.H1("🏈 NFL Statistics Dashboard"),
        html.P("Example page showing interactive controls and visualizations"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select Team:"),
                        dcc.Dropdown(
                            id="nfl-team-dropdown",
                            options=[
                                {"label": "Kansas City Chiefs", "value": "KC"},
                                {"label": "San Francisco 49ers", "value": "SF"},
                                {"label": "Buffalo Bills", "value": "BUF"},
                                {"label": "Philadelphia Eagles", "value": "PHI"},
                                {"label": "Dallas Cowboys", "value": "DAL"},
                            ],
                            value="KC",
                        ),
                    ],
                    style={
                        "width": "45%",
                        "display": "inline-block",
                        "margin-right": "5%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Stat Type:"),
                        dcc.Dropdown(
                            id="nfl-stat-dropdown",
                            options=[
                                {"label": "Passing Yards", "value": "passing"},
                                {"label": "Rushing Yards", "value": "rushing"},
                                {"label": "Points Scored", "value": "points"},
                            ],
                            value="passing",
                        ),
                    ],
                    style={"width": "45%", "display": "inline-block"},
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        dcc.Graph(id="nfl-trend-chart"),
        html.Hr(),
        html.Div([html.H4("Season Summary"), html.Div(id="nfl-summary-stats")]),
    ]
)


@callback(
    [Output("nfl-trend-chart", "figure"), Output("nfl-summary-stats", "children")],
    [Input("nfl-team-dropdown", "value"), Input("nfl-stat-dropdown", "value")],
)
def update_nfl_dashboard(team, stat_type):
    # Get data (replace with real query)
    df = get_sample_data(team, stat_type)

    # Create line chart
    stat_col = df.columns[1]  # The stat column
    fig = px.line(
        df, x="Week", y=stat_col, title=f"{team} - {stat_col} by Week", markers=True
    )
    fig.update_layout(hovermode="x unified", plot_bgcolor="white")

    # Calculate summary stats
    total = df[stat_col].sum()
    avg = df[stat_col].mean()
    max_val = df[stat_col].max()

    summary = html.Div(
        [
            html.Div(
                [html.H5(f"Total: {total:,.0f}"), html.P("Season Total")],
                style={"display": "inline-block", "margin-right": "40px"},
            ),
            html.Div(
                [html.H5(f"Average: {avg:,.1f}"), html.P("Per Game")],
                style={"display": "inline-block", "margin-right": "40px"},
            ),
            html.Div(
                [html.H5(f"Best: {max_val:,.0f}"), html.P("Single Game")],
                style={"display": "inline-block"},
            ),
        ]
    )

    return fig, summary
