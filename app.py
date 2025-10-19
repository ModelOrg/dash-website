import dash
from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
                for page in dash.page_registry.values()
            ],
            brand="Sports Analytics Platform",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-4",
        ),
        dash.page_container,
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
