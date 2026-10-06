from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

df1 = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app = Dash(__name__)

app.layout = html.Div(className="dashboard-container", children=[

    html.Div(className="sidebar", children=[
        html.H2("DAHSBOARD Indicadores", className="logo"),
        html.Ul(className="menu", children=[
            html.Li("Dashboard", className="menu-item active"),
            html.Li("Tables", className="menu-item"),
            html.Li("Reservations", className="menu-item"),
            html.Li("Waiters", className="menu-item"),
            html.Li("Menu", className="menu-item"),
            html.Li("Customers", className="menu-item"),
            html.Li("Reports", className="menu-item"),
        ]),
        html.Div(className="user-section", children=[
            html.Img(src="/assets/jv.png", className="avatar"),
            html.Div([
                html.Div("Jorge Victorino", className="user-name"),
                html.Div("Diseñador", className="user-role")
            ])
        ])
    ]),

    html.Div(className="main-content", children=[
        html.Div(className="header", children=[
            html.H1("Indicadores socio-económicos por país"),
            html.Div(className="header-tools", children=[
                dcc.Input(type="text", placeholder="Search", className="search-input"),
                html.Div("Monday, July 2", className="date-display")
            ])
        ]),

        html.Div(className="kpi-row", id='kpi-row-container'),

        html.Div(className="content-grid", children=[

            # Columna izquierda
            html.Div(className="left-panel", children=[
                html.Div(className="content-card", children=[
                    dcc.Dropdown(df1['Indicator Name'].unique(), 'Fertility rate, total (births per woman)', id='crossfilter-xaxis-column',),
                    dcc.RadioItems(['Linear', 'Log'], 'Linear', id='crossfilter-xaxis-type', labelStyle={'display': 'inline-block', 'marginTop': '5px'}),
                    dcc.Graph(id='crossfilter-indicator-scatter', hoverData={'points': [{'customdata': 'Japan'}]}),
                    dcc.Slider(df1['Year'].min(), df1['Year'].max(), step=None, id='crossfilter-year--slider', value=df1['Year'].max(), marks={str(y):str(y) for y in df1['Year'].unique()})
                ]),
            ]),

            # Columna derecha
            html.Div(className="right-panel", children=[
                html.Div(className="content-card", children=[
                    dcc.Dropdown(df1['Indicator Name'].unique(), 'Life expectancy at birth, total (years)', id='crossfilter-yaxis-column'),
                    dcc.RadioItems(['Linear', 'Log'], 'Linear', id='crossfilter-yaxis-type', labelStyle={'display': 'inline-block', 'marginTop': '5px'}),
                    html.Div("Series de tiempo por País", className="section-title"),
                    dcc.Graph(id='x-time-series'),
                    dcc.Graph(id='y-time-series'),
                ]),
            ])
        ])
    ])
])

@callback(
    Output('kpi-row-container', 'children'),
    Input('crossfilter-year--slider', 'value')
)
def update_kpis(year_value):
    indicadores_kpi = {
        'GDP growth (annual %)': 'Crecimiento del Ingreso - Mediana ',
        'Population density (people per sq. km of land area)': 'Densidad de problación - Mediana ',
        'Life expectancy at birth, total (years)': 'Expectativa de vida - Mediana ',
        'Fertility rate, total (births per woman)': 'Tasa de fertilidad - Mediana '
    }
    
    cards = []
    prev_year = 1962 if year_value==1962 else year_value - 5

    for ind_full, nombre_corto in indicadores_kpi.items():
        df_ind = df1[df1['Indicator Name'] == ind_full]
        
        val_actual = df_ind[df_ind['Year'] == year_value]['Value'].median()
        val_previo = df_ind[df_ind['Year'] == prev_year]['Value'].median()
        
        # Cálculo de cambio relativo
        if pd.notna(val_previo) and val_previo != 0 and pd.notna(val_actual):
            cambio = ((val_actual - val_previo) / val_previo) * 100
            clase_cambio = "positive" if cambio >= 0 else "negative"
            texto_cambio = f"{'+' if cambio > 0 else ''}{cambio:.2f}%"
        else:
            texto_cambio = "N/A"
            clase_cambio = ""

        # Crear el componente HTML para la tarjeta
        card = html.Div(className="kpi-card", children=[
            html.Div(nombre_corto + str(year_value), className="kpi-title"),
            html.Div(f"{val_actual:.2f}" if pd.notna(val_actual) else "0.00", className="kpi-value"),
            html.Div(texto_cambio, className=f"kpi-change {clase_cambio}")
        ])
        cards.append(card)
        
    return cards

@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    dff = df1[df1['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'], template='plotly_white',
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'], marginal_x='rug', marginal_y='box', 
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log', showgrid=False)
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title_text='', selector=lambda x: x.anchor != 'y')
    fig.update_yaxes(title_text='', selector=lambda x: x.anchor != 'x')    
    return fig

def create_time_series(dff, axis_type, title):
    fig = px.scatter(dff, x='Year', y='Value', template='plotly_white')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
    fig.add_annotation(
        x=1, y=0.95, xanchor='right', yanchor='bottom', xref='paper', yref='paper', showarrow=False, align='left',
        bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

@callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df1[df1['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b>:{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df1[df1['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run(debug=True)

