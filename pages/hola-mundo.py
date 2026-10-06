import dash
from dash import Dash, html

dash.register_page(__name__)

layout = html.Div([
    html.Div(children='Hello World')
])
