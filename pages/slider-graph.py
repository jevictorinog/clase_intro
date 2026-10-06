import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px

dash.register_page(__name__)

df = px.data.gapminder()

layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])

@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55, range_x=[200, 80000], range_y=[30, 90])
    fig.update_layout(transition_duration=500, template='plotly_white')

    return fig
