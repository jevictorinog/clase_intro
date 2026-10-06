import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div([
    html.Div(className="dashboard-container", children=[        
        html.Aside(className="sidebar", children=[
            html.Div([
                html.Img(src="/assets/logo-ucentral.png", height="50px"),
                html.Div("DASHBORADS Indicadores", className="logo"),
                html.Nav(className="menu", children=[
                    dcc.Link(html.Div([html.Span("🏠"), "Inicio"], className="menu-item active"), href="/"),
                    dcc.Link(html.Div("Hola Mundo", className="menu-item"), href="/hola-mundo"),
                    dcc.Link(html.Div("Población VS", className="menu-item"), href="/minimo-dash"),
                    dcc.Link(html.Div("Tabla y Scatter", className="menu-item"), href="/tabla-datos"),
                    dcc.Link(html.Div("Box Plots", className="menu-item"), href="/simple-callback"),
                    dcc.Link(html.Div("Slider Tiempo", className="menu-item"), href="/slider-graph"),
                    dcc.Link(html.Div("Mapa Ingresos", className="menu-item"), href="/layout-mapa-gap"),
                    dcc.Link(html.Div("Scatter vars", className="menu-item"), href="/layout-scater"),
                ])
            ]),
            
            html.Div(className="user-section", children=[
                html.Img(src="/assets/jv.png", className="avatar"),
                html.Div([
                    html.Div("Jorge Victorino", className="user-name"),
                    html.Div("Diseñador", className="user-role")
                ])
            ])
        ]),

        # CONTENIDO DINÁMICO (Derecha)
        html.Main(className="main-content", children=[
            dash.page_container
        ])
    ])
])

#     html.Footer([
#         html.Div(className="user-section", children=[
#             html.Img(src="/assets/jv.png", className="avatar"),
#             html.Div([
#                 html.Div("Jorge Victorino", className="user-name"),
#                 html.Div("Diseñador", className="user-role")
#             ]),
#             html.Img(src="/assets/torres.webp", height="80px"),
#         ]),
        
#         #html.P("© 2023 Contratista de transporte de energia")
#     ])
# ])

if __name__ == '__main__':
    app.run(debug=True) 
