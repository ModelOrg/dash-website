import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.query_engine import query_parquet

# Register this page
dash.register_page(__name__, path="/template", name="Template Page")

# Page layout
layout = html.Div(
    [
        html.H1("Your Page Title"),
        html.Div(
            [
                html.Label("Select a filter:"),
                dcc.Dropdown(
                    id="template-dropdown",
                    options=[
                        {"label": "Option 1", "value": "opt1"},
                        {"label": "Option 2", "value": "opt2"},
                    ],
                    value="opt1",
                ),
            ]
        ),
        dcc.Graph(id="template-graph"),
    ]
)


# Callbacks for interactivity
@callback(Output("template-graph", "figure"), Input("template-dropdown", "value"))
def update_graph(selected_option):
    # Query your data
    df = query_parquet("SELECT * FROM my_data WHERE category = ?", [selected_option])

    # Create visualization
    fig = px.scatter(df, x="x_col", y="y_col", title=f"Analysis for {selected_option}")
    return fig
