import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# Configuración de API
API_BASE_URL = "http://127.0.0.1:8000"

# Paleta de Colores: "Luxury Chocolate"
COLORS = {
    'bg': '#121212',           # Fondo neutro casi negro
    'card': '#1E1E1E',         # Tarjetas gris oscuro
    'accent': '#C5A059',       # Dorado Bronce (Elegancia)
    'text_main': '#E0E0E0',    # Gris claro (suave a la vista)
    'text_dim': '#A0A0A0',     # Gris apagado para etiquetas
    'palette': ['#3E2723', '#5D4037', '#8D6E63', '#D7CCC8', '#C5A059']
}

app = dash.Dash(__name__, title="Sales Analytics | Chocolate")

app.layout = html.Div(style={'backgroundColor': COLORS['bg'], 'color': COLORS['text_main'], 'minHeight': '100vh', 'padding': '2% 5%'}, children=[
    
    # Header minimalista
    html.Div([
        html.H1("CHOCOLATE SALES", 
                style={'letterSpacing': '6px', 'fontWeight': '300', 'color': COLORS['accent'], 'margin': '0'}),
        html.P("Data-Driven Insights for Sweet Success", 
               style={'letterSpacing': '2px', 'color': COLORS['text_dim'], 'fontSize': '14px'})
    ], style={'textAlign': 'left', 'marginBottom': '40px', 'borderLeft': f'4px solid {COLORS["accent"]}', 'paddingLeft': '20px'}),

    # Layout Grid
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 2fr', 'gap': '25px'}, children=[
        
        # Columna Izquierda: KPI Principal y Categorías
        html.Div(children=[
            # KPI 1: Revenue
            html.Div(id='rev-card', style={
                'backgroundColor': COLORS['card'], 'padding': '30px', 'borderRadius': '4px',
                'borderTop': f'3px solid {COLORS["accent"]}', 'marginBottom': '25px'
            }),
            
            # KPI 4: Category Sales (Treemap)
            html.Div([
                html.Label("Distribution by Category", style={'color': COLORS['text_dim'], 'fontSize': '20px', 'marginLeft': '10px'}),
                dcc.Graph(id='cat-tree', config={'displayModeBar': False}, style={'height': '400px'})
            ], style={'backgroundColor': COLORS['card'], 'padding': '10px', 'borderRadius': '4px'})
        ]),

        # Columna Derecha: Productos y Ciudades
        html.Div(children=[
            # KPI 2: Top Products (Bar Chart)
            html.Div([
                dcc.Graph(id='prod-bar', config={'displayModeBar': False}, style={'height': '350px'})
            ], style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '4px', 'marginBottom': '25px'}),

            # KPI 3: City Performance (Horizontal Bar)
            html.Div([
                dcc.Graph(id='city-bar', config={'displayModeBar': False}, style={'height': '350px'})
            ], style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '4px'})
        ])
    ]),

    dcc.Interval(id='refresh', interval=30000, n_intervals=0)
])

@app.callback(
    [Output('rev-card', 'children'),
     Output('prod-bar', 'figure'),
     Output('city-bar', 'figure'),
     Output('cat-tree', 'figure')],
    [Input('refresh', 'n_intervals')]
)
def update_view(n):
    # Configuración de fuentes y estilo
    base_layout = {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'family': 'Arial', 'color': COLORS['text_main']},
        'margin': {'t': 60, 'b': 50, 'l': 70, 'r': 20},
        'title_font_size': 22,  # Título de gráfica más grande
    }

    # 1. Revenue
    try:
        r = requests.get(f"{API_BASE_URL}/kpi/total-revenue").json()
        val = f"${r['total_revenue']:,.0f}"
    except: val = "$0"
    rev_content = [
        html.Small("TOTAL NET REVENUE", style={'color': COLORS['text_dim'], 'letterSpacing': '2px', 'fontSize': '20px'}),
        html.H2(val, style={'color': COLORS['accent'], 'fontSize': '52px', 'margin': '10px 0', 'fontWeight': 'bold'})
    ]

    # 2. Top Products
    try:
        df_p = pd.DataFrame(requests.get(f"{API_BASE_URL}/kpi/top-profitable-products").json())
        # labels={} renombra las etiquetas de los ejes automáticamente
        fig_p = px.bar(df_p, x='product_name', y='total_profit', 
                       title="Top Profit Contributors",
                       labels={'product_name': 'Product Name', 'total_profit': 'Total Profit'})
        
        fig_p.update_traces(
            marker_color=COLORS['accent'],
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>"
        )
        fig_p.update_layout(base_layout, bargap=0.4)
        # Ajuste de tamaño de fuente en ejes
        fig_p.update_xaxes(tickfont=dict(size=12), title_font=dict(size=14))
        fig_p.update_yaxes(tickfont=dict(size=12), title_font=dict(size=14))
    except: fig_p = {}

    # 3. City Performance
    try:
        df_ci = pd.DataFrame(requests.get(f"{API_BASE_URL}/kpi/performance-by-city").json())
        fig_ci = px.bar(df_ci, x='total_revenue', y='city', orientation='h', 
                        title="Revenue by Location",
                        labels={'total_revenue': 'Total Revenue', 'city': 'City'})
        
        fig_ci.update_traces(
            marker_color='#5D4037',
            hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>"
        )
        fig_ci.update_layout(base_layout)
        fig_ci.update_yaxes(autorange="reversed", tickfont=dict(size=12), title_font=dict(size=14))
        fig_ci.update_xaxes(tickfont=dict(size=12), title_font=dict(size=14))
    except: fig_ci = {}

    # 4. Category Sales
    try:
        df_ca = pd.DataFrame(requests.get(f"{API_BASE_URL}/kpi/category-sales").json())
        fig_ca = px.treemap(df_ca, path=['category'], values='total_units_sold',
                            title="Sales Volume by Category",
                            labels={'category': 'Category', 'total_units_sold': 'Units Sold'})
        
        fig_ca.update_traces(
            marker=dict(colors=COLORS['palette']),
            hovertemplate="<b>%{label}</b><br>Units Sold: %{value:,.0f}<extra></extra>"
        )
        # El título del Treemap suele ser pequeño, aquí lo agrandamos
        fig_ca.update_layout(base_layout, margin={'t': 50, 'b': 10, 'l': 10, 'r': 10})
    except: fig_ca = {}

    return rev_content, fig_p, fig_ci, fig_ca

if __name__ == '__main__':
    app.run(debug=True, port=8050)