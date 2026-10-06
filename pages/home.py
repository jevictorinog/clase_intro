import dash
from dash import html, dcc

dash.register_page(__name__, path='/') # Página raíz

layout = html.Div([
    html.H2("Seleccione un Tablero"),
    html.Div([
        dcc.Link("Ejemplo de Hola Mundo", href="/hola-mundo"),
        html.Br(),
        dcc.Link("Líneas de evolución de población paísX vs Colombia", href="/minimo-dash"),
        html.Br(),
        dcc.Link("Tabla de datos y scatter plot con animación", href="/tabla-datos"),
        html.Br(),
        dcc.Link("Box plots de variables población, ingreso, expectativa de vida", href="/simple-callback"),
        html.Br(),
        dcc.Link("Disersión de países con Slider de tiempo", href="/slider-graph"),
        html.Br(),
        dcc.Link("Globo interactivo de Ingresos por países", href="/layout-mapa-gap"),
        html.Br(),
        dcc.Link("Scatter plot interactivo y series de tiempo", href="/layout-mapa-gap"),
    ])
])

