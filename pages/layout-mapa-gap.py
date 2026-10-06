import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

df = px.data.gapminder()

df_2007 = df[df['year'] == 2007].copy()

etiquet = ['1. Muy Bajo', '2. Bajo', '3. Medio-Bajo', '4. Medio-Alto', '5. Alto', '6. Muy Alto']
df_2007['Rango Ingresos'] = pd.qcut(df_2007['gdpPercap'], q=6, labels=etiquet)
kol = ['deepskyblue', 'limegreen', 'yellowgreen', 'gold', 'orange', 'salmon', 'tomato']

fig_mapa = px.choropleth(df_2007, locations="iso_alpha", color="Rango Ingresos", hover_name="country", projection="orthographic", color_discrete_sequence=kol, category_orders={"Rango Ingresos": etiquet})
fig_mapa.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor="rgba(0,0,0,0)", height=550)


layout = html.Div([        
    html.Div(className="main-content", children=[
        html.Div(className="header", children=[
            html.H2("Tablero de Análisis Demográfico y Económico", style={'margin': '0'}),
            html.Div(className="date-display", children="Datos basados en Gapminder (2007)")
        ]),
        html.Div(className="kpi-row", children=[
            html.Div(className="kpi-card", children=[
                html.Div("Ingreso Per Cápita", className="kpi-title"),
                html.Div(id="kpi-1-value", className="kpi-value"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Div("% Ingreso Total del Continente", className="kpi-title"),
                html.Div(id="kpi-2-value", className="kpi-value"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Div("% Exp. Vida vs Media del Continente", className="kpi-title"),
                html.Div(id="kpi-3-value", className="kpi-value"),
            ]),
            html.Div(className="kpi-card", children=[
                html.Div("% Población del Continente", className="kpi-title"),
                html.Div(id="kpi-4-value", className="kpi-value"),
            ]),
        ]),
        
        html.Div(className="content-grid", children=[
            html.Div(className="content-card left-panel", children=[
                html.Div("Distribución Global de Ingresos", className="section-title", style={'padding': '15px', 'paddingBottom': '0px'}),
                dcc.Graph(id="mapa-interactivo", figure=fig_mapa, clear_on_unhover=False)
            ], style={'backgroundColor': 'rgba(0,0,0,0)', 'boxShadow': 'none', 'border': 'none'}),
            html.Div(className="content-card", children=[
                html.Div("Evolución Histórica", className="section-title"),
                dcc.Graph(id="grafica-ingreso"),
                dcc.Graph(id="grafica-exp-vida")
            ], style={'backgroundColor': 'rgba(0,0,0,0)', 'boxShadow': 'none', 'border': 'none'})
        ])
    ])
])

@callback(
    Output("kpi-1-value", "children"),
    Output("kpi-2-value", "children"),
    Output("kpi-3-value", "children"),
    Output("kpi-4-value", "children"),
    Output("grafica-ingreso", "figure"),
    Output("grafica-exp-vida", "figure"),
    Input("mapa-interactivo", "hoverData")
)
def actualizar_tablero(hoverData):
    pais_seleccionado = "Colombia" 
    
    if hoverData:
        pais_seleccionado = hoverData["points"][0]["hovertext"]

    datos_pais_2007 = df_2007[df_2007['country'] == pais_seleccionado].iloc[0]
    continente = datos_pais_2007['continent']
    
    df_continente = df_2007[df_2007['continent'] == continente]
    
    ingreso_percapita = datos_pais_2007['gdpPercap']
    poblacion = datos_pais_2007['pop']
    exp_vida = datos_pais_2007['lifeExp']
    ingreso_total_pais = ingreso_percapita * poblacion
    
    poblacion_continente = df_continente['pop'].sum()
    ingreso_total_continente = (df_continente['gdpPercap'] * df_continente['pop']).sum()
    exp_vida_media_continente = df_continente['lifeExp'].mean()
    
    kpi_1 = f"${ingreso_percapita:,.0f}"
    kpi_2 = f"{(ingreso_total_pais / ingreso_total_continente) * 100:.2f}%"
    kpi_3 = f"{(exp_vida / exp_vida_media_continente) * 100:.2f}%"
    kpi_4 = f"{(poblacion / poblacion_continente) * 100:.2f}%"
    
    df_historico_pais = df[df['country'] == pais_seleccionado]
    
    fig_ingreso = px.line(df_historico_pais, x="year", y="gdpPercap", title=f"Ingreso (GDP) - {pais_seleccionado}", markers=True, color_discrete_sequence=['crimson'])
    fig_ingreso.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=230, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.02)", xaxis=dict(tickmode='array',tickvals=list(range(1952,2008,10))))
    
    #fig_exp_vida = px.line(df_historico_pais, x="year", y="lifeExp", title=f"Expectativa de Vida - {pais_seleccionado}", markers=True, color_discrete_sequence=['#27ae60'])
    fig_exp_vida =  px.bar(df_historico_pais, x='year', y='lifeExp', text_auto='.1f', color_discrete_sequence=['#2a9d8f'], title=f"Expectativa de Vida - {pais_seleccionado}")
    fig_exp_vida.update_traces(marker=dict(cornerradius=10))
    fig_exp_vida.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=230, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.02)", xaxis=dict(tickmode='array',tickvals=list(range(1952,2008,5))))

    return kpi_1, kpi_2, kpi_3, kpi_4, fig_ingreso, fig_exp_vida
