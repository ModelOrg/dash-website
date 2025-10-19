"""
Team Offense Trends page using nflreadpy data (port for "nflverse" R package).

First run: python utils/load_nfl_data.py
Then this page will query the Parquet files.
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from utils.query_engine import query_parquet, list_available_datasets

dash.register_page(__name__, path="/team-offense-trends", name="Team Offense Trends")


def get_available_teams():
    """Get list of teams from the data"""
    try:
        teams_df = query_parquet(
            "SELECT DISTINCT posteam FROM 'nfl_team_games.parquet' WHERE posteam IS NOT NULL ORDER BY posteam"
        )
        return [{"label": team, "value": team} for team in teams_df["posteam"].tolist()]
    except:
        return [{"label": "Run load_nfl_data.py first", "value": "NONE"}]


def get_available_seasons():
    """Get available seasons"""
    try:
        seasons_df = query_parquet(
            "SELECT DISTINCT season FROM 'nfl_team_games.parquet' ORDER BY season DESC"
        )
        return [
            {"label": str(year), "value": year}
            for year in seasons_df["season"].tolist()
        ]
    except:
        return [{"label": "2024", "value": 2024}]


layout = html.Div(
    [
        html.H1("🏈 Team Offense Trends"),
        html.P(
            "Interactive dashboard using NFL offense data since 2022. "
            "Data is pulled using `nflreadpy` which is built on top of the `nflverse` R package."
        ),
        # Check if data exists
        html.Div(id="data-check", style={"margin-bottom": "20px"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select Season:"),
                        dcc.Dropdown(
                            id="nfl-season-dropdown",
                            options=get_available_seasons(),
                            value=2024,
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "margin-right": "3%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Team:"),
                        dcc.Dropdown(
                            id="nfl-team-dropdown",
                            options=get_available_teams(),
                            value=None,
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "margin-right": "3%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Stat:"),
                        dcc.Dropdown(
                            id="nfl-stat-dropdown",
                            options=[
                                {"label": "Total Yards", "value": "total_yards"},
                                {"label": "Passing Yards", "value": "passing_yards"},
                                {"label": "Rushing Yards", "value": "rushing_yards"},
                                {"label": "Points Scored", "value": "points"},
                            ],
                            value="total_yards",
                        ),
                    ],
                    style={"width": "30%", "display": "inline-block"},
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        dcc.Graph(id="nfl-weekly-trend"),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="nfl-stat-distribution")],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [html.H4("Season Summary"), html.Div(id="nfl-summary-cards")],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "padding-left": "2%",
                    },
                ),
            ]
        ),
    ]
)


@callback(Output("data-check", "children"), Input("nfl-season-dropdown", "value"))
def check_data(season):
    """Check if NFL data is available"""
    datasets = list_available_datasets()

    if "nfl_team_games.parquet" in datasets:
        return html.Div(
            [
                html.Span(
                    "✅ Data loaded successfully!",
                    style={"color": "green", "font-weight": "bold"},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.Span(
                    "⚠️ No data found. ",
                    style={"color": "orange", "font-weight": "bold"},
                ),
                html.Span("Run: "),
                html.Code("python utils/load_nfl_data.py"),
                html.Span(" to load data."),
            ],
            style={
                "padding": "10px",
                "background-color": "#fff3cd",
                "border-radius": "5px",
            },
        )


@callback(Output("nfl-team-dropdown", "options"), Input("nfl-season-dropdown", "value"))
def update_teams(season):
    """Update team list based on selected season"""
    try:
        teams_df = query_parquet(
            f"""
            SELECT DISTINCT posteam 
            FROM 'nfl_team_games.parquet' 
            WHERE season = {season} AND posteam IS NOT NULL
            ORDER BY posteam
        """
        )
        return [{"label": team, "value": team} for team in teams_df["posteam"].tolist()]
    except Exception:
        return [{"label": "Error loading teams", "value": "NONE"}]


@callback(
    [
        Output("nfl-weekly-trend", "figure"),
        Output("nfl-stat-distribution", "figure"),
        Output("nfl-summary-cards", "children"),
    ],
    [
        Input("nfl-season-dropdown", "value"),
        Input("nfl-team-dropdown", "value"),
        Input("nfl-stat-dropdown", "value"),
    ],
)
def update_dashboard(season, team, stat):
    """Update all visualizations"""

    # Default empty figures
    empty_fig = go.Figure()
    empty_fig.add_annotation(
        text="Select a team to see data",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16),
    )

    if not team or team == "NONE":
        return empty_fig, empty_fig, html.P("Select a team to see stats")

    try:
        # Get team's game data
        team_data = query_parquet(
            f"""
            SELECT 
                week, 
                {stat},
                passing_yards,
                rushing_yards,
                points,
                total_yards,
                turnovers,
                first_downs
            FROM 'nfl_team_games.parquet'
            WHERE season = {season} AND posteam = '{team}'
            ORDER BY week
        """
        )

        if team_data.empty:
            return empty_fig, empty_fig, html.P("No data available for this selection")

        # Chart 1: Weekly trend
        stat_labels = {
            "total_yards": "Total Yards",
            "passing_yards": "Passing Yards",
            "rushing_yards": "Rushing Yards",
            "points": "Points Scored",
        }

        fig1 = px.line(
            team_data,
            x="week",
            y=stat,
            title=f"{team} - {stat_labels[stat]} by Week ({season})",
            markers=True,
        )
        fig1.update_traces(line=dict(width=3))
        fig1.update_layout(
            xaxis_title="Week",
            yaxis_title=stat_labels[stat],
            hovermode="x unified",
            plot_bgcolor="white",
        )

        # Chart 2: Distribution of selected stat
        fig2 = px.histogram(
            team_data, x=stat, nbins=15, title=f"{stat_labels[stat]} Distribution"
        )
        fig2.update_layout(
            xaxis_title=stat_labels[stat],
            yaxis_title="Frequency",
            showlegend=False,
            plot_bgcolor="white",
        )

        # Summary stats
        total_stat = team_data[stat].sum()
        avg_stat = team_data[stat].mean()
        max_stat = team_data[stat].max()
        min_stat = team_data[stat].min()

        avg_points = team_data["points"].mean()
        total_turnovers = team_data["turnovers"].sum()

        summary = html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            f"{total_stat:,.0f}",
                            style={"margin": "5px 0", "color": "#1f77b4"},
                        ),
                        html.P(
                            f"Total {stat_labels[stat]}",
                            style={"margin": "0", "color": "#666"},
                        ),
                    ],
                    style={"margin-bottom": "20px"},
                ),
                html.Div(
                    [
                        html.H3(
                            f"{avg_stat:,.1f}",
                            style={"margin": "5px 0", "color": "#2ca02c"},
                        ),
                        html.P(
                            f"Avg {stat_labels[stat]}/Game",
                            style={"margin": "0", "color": "#666"},
                        ),
                    ],
                    style={"margin-bottom": "20px"},
                ),
                html.Div(
                    [
                        html.H3(
                            f"{max_stat:,.0f}",
                            style={"margin": "5px 0", "color": "#ff7f0e"},
                        ),
                        html.P("Best Game", style={"margin": "0", "color": "#666"}),
                    ],
                    style={"margin-bottom": "20px"},
                ),
                html.Hr(),
                html.Div(
                    [
                        html.P([html.Strong("Avg Points/Game: "), f"{avg_points:.1f}"]),
                        html.P(
                            [
                                html.Strong("Total Turnovers: "),
                                f"{int(total_turnovers)}",
                            ]
                        ),
                        html.P([html.Strong("Games Played: "), f"{len(team_data)}"]),
                    ]
                ),
            ],
            style={
                "padding": "20px",
                "background-color": "#f8f9fa",
                "border-radius": "5px",
            },
        )

        return fig1, fig2, summary

    except Exception as e:
        error_fig = go.Figure()
        error_fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return error_fig, error_fig, html.P(f"Error: {str(e)}")
