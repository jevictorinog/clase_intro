import dash
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__)

df = px.data.gapminder()
dlab = {"gdpPercap": "Ingreso per cápita (USD, escala log)", "lifeExp": "Expectativa de vida (años)", "continent": "Continente"}
fig = px.scatter(df, x='gdpPercap', y='lifeExp', size='pop', color='continent', animation_frame='year', size_max=60, hover_name='country', 
                 animation_group='country', template='plotly_white', width=720, labels=dlab)
fig.update_traces(marker_sizemin=3)
fig.update_yaxes(range=[20, 90])
fig.update_xaxes(range=[-500, 50000])

layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=fig)
])
