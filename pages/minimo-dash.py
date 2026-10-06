import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

df = px.data.gapminder()

layout = [
    html.H1(children='Evolución de población por País', style={'color':'crimson'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country.isin([value,'Colombia'])]
    fig = px.line(dff, x='year', y='pop', color='country', markers='lines+markers+text')
    fig.update_layout(transition_duration=800, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)')
    return fig
