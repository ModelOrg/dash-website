import dash
from dash import Dash, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

# Sidebar with navigation links
sidebar = html.Div(
    [
        html.H2("Dashboards", className="text-center mb-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span(page["name"])],
                    href=page["path"],
                    active="exact",
                    className="mb-2",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    className="sidebar",
)

# Hamburger button for mobile
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Button(
                html.I(className="fas fa-bars"),
                id="sidebar-toggle",
                className="me-2",
                color="primary",
                outline=True,
            ),
            dbc.NavbarBrand("Sports Analytics Platform", className="ms-2"),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    className="navbar-mobile",
)

# Main content area
content = html.Div(dash.page_container, id="page-content")

# App layout
app.layout = html.Div([navbar, sidebar, content])


# Callback to toggle sidebar
@callback(
    Output("sidebar", "className"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "className"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, current_class):
    if n_clicks:
        if "collapsed" in current_class:
            return "sidebar"
        else:
            return "sidebar collapsed"
    return current_class


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
