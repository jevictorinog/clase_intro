import dash
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import plotly.express as px

dash.register_page(__name__)

df = px.data.gapminder()

layout = html.Div([
    html.Div(children='Distribución interactiva de variables demográficas'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph')
]) 
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.box(df, x='continent', y=col_chosen, color='continent', points=False, template='simple_white')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.5)')
    return fig
