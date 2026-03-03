# =========================================================
# Actividad 2: CREACIÓN DE HEATMAP CON LEYENDA HTML PERSONALIZADA
# =========================================================

# === 1. Carga de librerías ===
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from branca.element import Template, MacroElement


# === 2. Definición de rutas de archivos ===
ruta_datos = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\Puntos VMS.csv"      # Archivo Excel con columnas Latitud y Longitud
ruta_salida = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\mapa_heatmap_Act2.html"     # Archivo HTML de salida (opcional)

# === 3. Carga de datos ===
df = pd.read_csv(ruta_datos, sep=";", decimal = ',', nrows=100000)

# === 4. Creación del GeoDataFrame ===
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]),
    crs="EPSG:4326"
)


# === 5. Preparación de datos para HeatMap ===
# El HeatMap necesita una lista de listas con formato:
# [[lat, lon], [lat, lon], ...]
datos_heatmap = [[row.geometry.y, row.geometry.x] for _, row in gdf.iterrows()]


# === 6. Creación del mapa base ===
centro = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles='CartoDB positron',
    name='CartoDB Positron'
)


# === 7. Añadir HeatMap ===
HeatMap(
    datos_heatmap,
    radius=8,          # Radio de influencia de cada punto
    blur=12,           # Difuminado
    min_opacity=0.3,   # Opacidad mínima
    max_zoom=1
).add_to(m)


# === 8. Crear leyenda HTML personalizada ===
template = """
{% macro html(this, kwargs) %}

<div style="
position: fixed; 
bottom: 40px;
left: 40px;
width: 200px;
height: 120px;
z-index:9999;
font-size:14px;
background-color: white;
padding: 10px;
border-radius: 8px;
box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">

<b>Densidad de actividad</b><br><br>

<div style="width: 100%; height: 15px; 
background: linear-gradient(to right, 
blue, cyan, lime, yellow, orange, red);">
</div>

<br>
<span style="float:left;">Baja</span>
<span style="float:right;">Alta</span>

</div>

{% endmacro %}
"""


macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

# === 9. Guardar el mapa en HTML ===
m.save(ruta_salida)
print(f"Mapa guardado correctamente en: {ruta_salida}")
