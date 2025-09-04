# dashboard.py

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import folium
import os

# Carpeta donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta absoluta al CSV
posiciones_path = os.path.join(script_dir, "..", "data", "LIC INTERMARES", "Posiciones_LIC_BancoGalicia.csv")
posiciones_path = os.path.abspath(posiciones_path)

# Leer CSV
df_posiciones = pd.read_csv(
    posiciones_path,
    sep=";",        
    decimal=",",    
)

df = df_posiciones.copy()

# ==================================
# 2) Crear gráfico Plotly
# ==================================
conteo = df["HojaMarea"].value_counts().reset_index()
conteo.columns = ["HojaMarea", "NumPuntos"]
fig = px.bar(conteo, x="HojaMarea", y="NumPuntos", title="Número de puntos por marea")

# ==================================
# 3) Crear o importa un mapa Folium
# ==================================
map_html = os.path.join(script_dir, "..", "img", "mapa_mareas_js_featuregroups.html")
map_html = os.path.abspath(map_html)


# ==================================
# 4) Crear app Dash
# ==================================
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Mareas", style={"textAlign": "center"}),

    html.Div([
        html.Iframe(
            id="map",
            srcDoc=open(map_html, "r", encoding="utf-8").read(),
            width="100%",
            height="500"
        ),
    ], style={"flex": "1", "padding": "10px"}),

    html.Div([
        dcc.Graph(figure=fig, style={"height": "500px"})
    ], style={"flex": "1", "padding": "10px"}),

], style={"display": "flex", "flexDirection": "column"})

# ==================================
# 5) Ejecutar app
# ==================================
if __name__ == "__main__":
    # Abre automáticamente en el navegador si se puede
    app.run(debug=True, use_reloader=False)
