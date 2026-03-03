# =========================================================
# Actividad 2: HEATMAP POR DÍA DE LA SEMANA
# =========================================================

# === 1. Carga de librerías ===
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from branca.element import Template, MacroElement


# =========================================================
# 2. Definición de rutas
# =========================================================
ruta_datos = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\Puntos VMS.csv"
ruta_salida = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\mapa_heatmap_por_dia.html"


# =========================================================
# 3. Carga de datos
# =========================================================
df = pd.read_csv(ruta_datos, sep=";", decimal=",", nrows=100000)


# =========================================================
# 4. Creación del GeoDataFrame
# =========================================================
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]),
    crs="EPSG:4326"
)

# Convertir Fecha a datetime
gdf["Fecha"] = pd.to_datetime(gdf["Fecha"])

# Calcular día de la semana (0=Lunes, 6=Domingo)
gdf["NumeroDia"] = gdf["Fecha"].dt.weekday

dias_semana = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

gdf["NombreDia"] = gdf["NumeroDia"].map(dias_semana)


# =========================================================
# 5. Crear mapa base
# =========================================================
centro = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)


# =========================================================
# 6. Crear HeatMap por cada día
# =========================================================
for dia in dias_semana.values():

    gdf_dia = gdf[gdf["NombreDia"] == dia]

    # Evitar capas vacías
    if gdf_dia.empty:
        continue

    # Lista de coordenadas eficiente
    datos_heatmap = list(zip(gdf_dia.geometry.y, gdf_dia.geometry.x))

    # Crear grupo de capa
    fg = folium.FeatureGroup(name=f"HeatMap - {dia}", show=False)

    HeatMap(
        datos_heatmap,
        radius=8,
        blur=12,
        min_opacity=0.3,
        max_zoom=1
    ).add_to(fg)

    fg.add_to(m)


# =========================================================
# 7. Leyenda HTML personalizada
# =========================================================
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


# =========================================================
# 8. Añadir LayerControl
# =========================================================
folium.LayerControl(collapsed=False).add_to(m)


# =========================================================
# 9. Guardar mapa
# =========================================================
m.save(ruta_salida)

print(f"Mapa guardado correctamente en: {ruta_salida}")