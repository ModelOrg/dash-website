"""
Template for creating new analysis pages.

To create a new page:
1. Copy this file to pages/your_page_name.py
2. Update the path and name in dash.register_page()
3. Build your layout
4. Add callbacks for interactivity
5. The page will automatically appear in the navigation!
"""

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

# Register this page - UPDATE THESE VALUES
dash.register_page(
    __name__,
    path="/template",  # URL path: /template
    name="Template",  # Name in navigation menu
)

# Page layout
layout = html.Div(
    [
        html.H1("Your Page Title Here"),
        html.P("Describe what this page does."),
        html.Div(
            [
                html.Label("Select a filter:"),
                dcc.Dropdown(
                    id="template-dropdown",
                    options=[
                        {"label": "Option 1", "value": "opt1"},
                        {"label": "Option 2", "value": "opt2"},
                        {"label": "Option 3", "value": "opt3"},
                    ],
                    value="opt1",
                ),
            ],
            style={"width": "50%", "margin-bottom": "20px"},
        ),
        dcc.Graph(id="template-graph"),
    ]
)


# Callbacks for interactivity
@callback(Output("template-graph", "figure"), Input("template-dropdown", "value"))
def update_graph(selected_option):
    # Create sample data (replace with your actual data query)
    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 6, 8, 10] if selected_option == "opt1" else [1, 3, 5, 7, 9],
        }
    )

    # Create visualization
    fig = px.scatter(
        df,
        x="x",
        y="y",
        title=f"Analysis for {selected_option}",
        labels={"x": "X Axis Label", "y": "Y Axis Label"},
    )

    return fig
