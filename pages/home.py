import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Home")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "🏈 Sports Analytics Platform", className="text-center mt-5"
                        ),
                        html.Hr(),
                        html.P(
                            "Welcome! This is your collaborative sports analytics workspace.",
                            className="lead text-center",
                        ),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Getting Started"),
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "Add Your First Page",
                                            className="card-title",
                                        ),
                                        html.P(
                                            [
                                                "Copy ",
                                                html.Code("pages/_template.py"),
                                                " to create a new analysis page. It will automatically appear in the navigation menu!",
                                            ]
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Each page is a Python file in the pages/ folder"
                                                ),
                                                html.Li(
                                                    "Use Plotly for interactive visualizations"
                                                ),
                                                html.Li(
                                                    "Query data with DuckDB from Parquet files"
                                                ),
                                                html.Li(
                                                    "No frontend experience needed - just Python!"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            className="mb-3",
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Available Features"),
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "What You Can Build", className="card-title"
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Interactive dashboards with dropdowns and filters"
                                                ),
                                                html.Li(
                                                    "Complex Bayesian model visualizations"
                                                ),
                                                html.Li(
                                                    "Real-time statistics and metrics"
                                                ),
                                                html.Li(
                                                    "Custom sports analytics pages"
                                                ),
                                            ]
                                        ),
                                        html.P(
                                            "Check out the example pages in the navigation!",
                                            className="mt-3",
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    width=6,
                ),
            ],
            className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Alert(
                            [
                                html.H5("📚 Documentation", className="alert-heading"),
                                html.P(
                                    "For detailed setup and contribution guidelines, see:"
                                ),
                                html.Ul(
                                    [
                                        html.Li(html.Code("docs/CONTRIBUTING.md")),
                                        html.Li(html.Code("docs/DATA_GUIDE.md")),
                                        html.Li(html.Code("README.md")),
                                    ]
                                ),
                            ],
                            color="info",
                        )
                    ]
                )
            ],
            className="mt-4",
        ),
    ]
)
