# pages/nfl_stats.py
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.query_engine import query_parquet

dash.register_page(__name__, path="/nfl-stats", name="NFL Statistics")

layout = html.Div(
    [
        html.H1("NFL Play-by-Play Analysis"),
        html.Div(
            [
                html.Label("Select Season:"),
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[
                        {"label": str(year), "value": year}
                        for year in range(2020, 2025)
                    ],
                    value=2024,
                ),
                html.Label("Select Team:"),
                dcc.Dropdown(id="team-dropdown"),
            ],
            style={"width": "50%"},
        ),
        dcc.Graph(id="passing-yards-chart"),
        dcc.Graph(id="play-type-distribution"),
    ]
)


@callback(Output("team-dropdown", "options"), Input("season-dropdown", "value"))
def update_teams(season):
    df = query_parquet(
        f"""
        SELECT DISTINCT posteam as team 
        FROM 'nfl_plays_{season}.parquet' 
        WHERE posteam IS NOT NULL
        ORDER BY team
    """
    )
    return [{"label": team, "value": team} for team in df["team"]]


@callback(
    [
        Output("passing-yards-chart", "figure"),
        Output("play-type-distribution", "figure"),
    ],
    [Input("season-dropdown", "value"), Input("team-dropdown", "value")],
)
def update_charts(season, team):
    if not team:
        return {}, {}

    # Query data
    df = query_parquet(
        f"""
        SELECT week, play_type, yards_gained, air_yards
        FROM 'nfl_plays_{season}.parquet'
        WHERE posteam = ?
    """,
        [team],
    )

    # Chart 1: Passing yards by week
    passing = (
        df[df["play_type"] == "pass"].groupby("week")["air_yards"].sum().reset_index()
    )
    fig1 = px.line(
        passing, x="week", y="air_yards", title=f"{team} Passing Air Yards by Week"
    )

    # Chart 2: Play type distribution
    play_dist = df["play_type"].value_counts().reset_index()
    fig2 = px.pie(
        play_dist,
        names="play_type",
        values="count",
        title=f"{team} Play Type Distribution",
    )

    return fig1, fig2
