"""
Fantasy Value Dashboard

This page helps determine fantasy football value for specific players.
The user selects a year, team, and position (RB, WR, TE), then a player.
It visualizes player usage, efficiency, and yardage trends.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# --- Load data ---
DATA_PATH = "data/parquet"
pbp = pd.read_parquet(os.path.join(DATA_PATH, "nfl_pbp_raw.parquet"))
rosters = pd.read_parquet(os.path.join(DATA_PATH, "nfl_rosters.parquet"))
team_games = pd.read_parquet(os.path.join(DATA_PATH, "nfl_team_games.parquet"))
teams = pd.read_parquet(os.path.join(DATA_PATH, "nfl_teams.parquet"))

# --- Page registration ---
dash.register_page(
    __name__,
    path="/fantasy_value",
    name="Fantasy Value",
)

# --- Filterable layout ---
layout = html.Div(
    [
        html.H1("Fantasy Value Dashboard"),
        html.P("Analyze player usage, efficiency, and yardage trends by week."),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select Year:"),
                        dcc.Dropdown(
                            id="fantasy-year",
                            options=[
                                {"label": str(y), "value": y}
                                for y in sorted(
                                    rosters["season"].unique(), reverse=True
                                )
                            ],
                            value=sorted(rosters["season"].unique(), reverse=True)[0],
                        ),
                    ],
                    style={
                        "width": "20%",
                        "display": "inline-block",
                        "margin-right": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Team:"),
                        dcc.Dropdown(
                            id="fantasy-team",
                            options=[
                                {"label": t, "value": t}
                                for t in sorted(rosters["team"].unique())
                            ],
                        ),
                    ],
                    style={
                        "width": "20%",
                        "display": "inline-block",
                        "margin-right": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Position:"),
                        dcc.Dropdown(
                            id="fantasy-pos",
                            options=[
                                {"label": p, "value": p} for p in ["RB", "WR", "TE"]
                            ],
                        ),
                    ],
                    style={
                        "width": "20%",
                        "display": "inline-block",
                        "margin-right": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Player:"),
                        dcc.Dropdown(id="fantasy-player"),
                    ],
                    style={"width": "30%", "display": "inline-block"},
                ),
            ],
            style={"margin-bottom": "25px"},
        ),
        html.Hr(),
        html.H3("Usage Overview"),
        dcc.Graph(id="usage-graph"),
        html.H3("Rushing Efficiency"),
        dcc.Graph(id="rushing-efficiency-graph"),
        html.H3("Receiving Efficiency"),
        dcc.Graph(id="receiving-efficiency-graph"),
        html.H3("Total Yardage"),
        dcc.Graph(id="yardage-graph"),
    ]
)


# --- Callbacks ---


@callback(
    Output("fantasy-player", "options"),
    Input("fantasy-year", "value"),
    Input("fantasy-team", "value"),
    Input("fantasy-pos", "value"),
)
def update_player_dropdown(year, team, pos):
    if not (year and team and pos):
        return []

    # Use the correct name column(s)
    name_col = "full_name" if "full_name" in rosters.columns else "football_name"

    players = rosters.query("season == @year and team == @team and position == @pos")[
        [name_col, "gsis_id"]
    ].drop_duplicates()

    # Build dropdown options
    return [
        {"label": n, "value": pid}
        for n, pid in zip(players[name_col], players["gsis_id"])
    ]


# Main graph callback
@callback(
    Output("usage-graph", "figure"),
    Output("rushing-efficiency-graph", "figure"),
    Output("receiving-efficiency-graph", "figure"),
    Output("yardage-graph", "figure"),
    Input("fantasy-player", "value"),
)
def update_player_viz(player_id):
    if not player_id:
        empty_fig = go.Figure().update_layout(title="Select a player to view data")
        return empty_fig, empty_fig, empty_fig, empty_fig

    # Filter player-level data
    df = pbp.query("rusher_id == @player_id or receiver_id == @player_id").copy()
    if df.empty:
        empty_fig = go.Figure().update_layout(
            title="No data available for this player."
        )
        return empty_fig, empty_fig, empty_fig, empty_fig

    df["week"] = df["week"].astype(int)
    df.sort_values("week", inplace=True)

    # === USAGE GRAPH ===
    # (for simplicity, use dummy "snap" data approximation)
    usage = (
        df.groupby("week")
        .agg(
            total_targets=("pass_attempt", "sum"),
            total_rushes=("rush_attempt", "sum"),
            total_snaps=("play_id", "count"),
        )
        .reset_index()
    )

    fig_usage = go.Figure()
    fig_usage.add_trace(
        go.Scatter(x=usage["week"], y=usage["total_snaps"], name="Snaps")
    )
    fig_usage.add_trace(
        go.Scatter(x=usage["week"], y=usage["total_targets"], name="Targets")
    )
    fig_usage.add_trace(
        go.Scatter(x=usage["week"], y=usage["total_rushes"], name="Rushes")
    )
    fig_usage.update_layout(
        title="Player Usage by Week",
        xaxis_title="Week",
        yaxis_title="Count",
        template="plotly_white",
    )

    # === RUSHING EFFICIENCY ===
    rush_df = df[df["rush_attempt"] == 1]
    fig_rush = px.box(
        rush_df,
        x="week",
        y="yards_gained",
        points="all",
        title="Rushing Efficiency (Yards per Rush)",
    )
    fig_rush.update_layout(template="plotly_white")

    # === RECEIVING EFFICIENCY ===
    rec_df = df[df["pass_attempt"] == 1]
    if not rec_df.empty:
        rec_week = (
            rec_df.groupby("week")
            .agg(
                targets=("pass_attempt", "sum"),
                completions=("complete_pass", "sum"),
            )
            .reset_index()
        )
        rec_week["incompletions"] = rec_week["targets"] - rec_week["completions"]
        rec_week["catch_pct"] = rec_week["completions"] / rec_week["targets"] * 100

        fig_rec = go.Figure()
        fig_rec.add_trace(
            go.Bar(
                x=rec_week["week"],
                y=rec_week["completions"],
                name="Completions",
                marker_color="green",
            )
        )
        fig_rec.add_trace(
            go.Bar(
                x=rec_week["week"],
                y=rec_week["incompletions"],
                name="Incompletions",
                marker_color="red",
            )
        )
        fig_rec.add_trace(
            go.Scatter(
                x=rec_week["week"],
                y=rec_week["catch_pct"],
                name="Catch %",
                mode="lines+markers",
                yaxis="y2",
            )
        )
        fig_rec.update_layout(
            title="Receiving Efficiency (Targets and Catch %)",
            xaxis_title="Week",
            yaxis_title="Targets",
            yaxis2=dict(
                title="Catch %",
                overlaying="y",
                side="right",
                range=[0, 100],
            ),
            barmode="stack",
            template="plotly_white",
        )
    else:
        fig_rec = go.Figure().update_layout(title="No receiving data.")

    # === TOTAL YARDAGE (fixed) ===
    # Use play-level yards_gained and filter by rush/pass plays
    # If your pbp uses different column names, adjust the filters/columns accordingly.

    # Ensure week is integer and sorted earlier in the function
    # df["week"] = df["week"].astype(int)
    # df.sort_values("week", inplace=True)

    # Rushing yards: sum yards_gained on rush attempts
    if "rush_attempt" in df.columns and "yards_gained" in df.columns:
        rush_week = (
            df[df["rush_attempt"] == 1]
            .groupby("week")["yards_gained"]
            .sum()
            .rename("rush_yards")
        )
    else:
        rush_week = pd.Series(name="rush_yards", dtype=float)

    # Receiving yards: typically sum yards_gained for completed passes
    # (change condition if you want targets including incompletions)
    if "complete_pass" in df.columns and "yards_gained" in df.columns:
        rec_week = (
            df[df["complete_pass"] == 1]
            .groupby("week")["yards_gained"]
            .sum()
            .rename("rec_yards")
        )
    else:
        rec_week = pd.Series(name="rec_yards", dtype=float)

    # Combine into one DataFrame, fill missing weeks with 0
    yard_df = pd.concat([rush_week, rec_week], axis=1).fillna(0).reset_index()
    yard_df["total_yards"] = yard_df["rush_yards"] + yard_df["rec_yards"]

    # Now build the figure
    fig_yards = go.Figure()
    fig_yards.add_trace(
        go.Bar(x=yard_df["week"], y=yard_df["rush_yards"], name="Rushing Yards")
    )
    fig_yards.add_trace(
        go.Bar(x=yard_df["week"], y=yard_df["rec_yards"], name="Receiving Yards")
    )
    fig_yards.update_layout(
        title="Total Yardage by Week",
        xaxis_title="Week",
        yaxis_title="Yards",
        barmode="stack",
        template="plotly_white",
    )

    return fig_usage, fig_rush, fig_rec, fig_yards
