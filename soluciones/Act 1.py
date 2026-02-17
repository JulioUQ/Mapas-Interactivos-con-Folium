# =========================================================
# Actividad 1: Creación de un mapa interactivo con puntos y capas poligonales
# =========================================================

# === 1. Carga de librerías ===
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import os

# === 2. Definición de rutas de archivos ===
# Modifica las rutas según tu entorno de trabajo
ruta_datos = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\Act 1 - Puntos VMS.csv"       # Archivo csv con columnas Latitud y Longitud
ruta_gsa = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\ZonasGSA\ZonasGSA.shp"    # Capa poligonal
ruta_paises = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\WorldCountries\WorldCountries.shp"    # Capa poligonal
ruta_salida = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\mapa_interactivo_Act1.html"   # Archivo HTML de salida (opcional)


# === 3. Carga de datos ===
# Leemos los datos del csv con pandas
df = pd.read_csv(ruta_datos, sep=";", decimal = ',', nrows=100000)

# Leemos las capas poligonales con geopandas
capa_gsa = gpd.read_file(ruta_gsa)
capa_paises = gpd.read_file(ruta_paises)

# === 4. Creación del GeoDataFrame con los puntos ===
# Asegúrate de que el csv tenga las columnas "Latitud" y "Longitud"
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]),
    crs="EPSG:4326"   # Sistema de referencia geográfico (WGS84)
)

# === 5. Creación del mapa base ===
# Calculamos el centro del mapa a partir del promedio de coordenadas
centro = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]

# Creamos el mapa base
m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles=None
)

# Añadir la capa base manualmente y ocultarla del control
folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri — GEBCO, NOAA, Esri",
        name="Océano",
        overlay=False,
        control=False  
    ).add_to(m)


# === 6. Puntos con popup ===
for _, row in gdf.iterrows():
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 12px; padding: 4px 6px; max-width: 240px;">
        <table style="border-collapse: collapse; width: 100%;">
            <tr><td style="font-weight: bold;">CodigoCFR:</td><td>{row['CodigoCFR']}</td></tr>
            <tr><td style="font-weight: bold;">NombreBuque:</td><td>{row['NombreBuque']}</td></tr>
            <tr><td style="font-weight: bold;">Fecha:</td><td>{row['Fecha']}</td></tr>
            <tr><td style="font-weight: bold;">Hora:</td><td>{row['Hora']}</td></tr>
            <tr><td style="font-weight: bold;">GSA:</td><td>{row['GSA']}</td></tr>
            <tr><td style="font-weight: bold;">Velocidad:</td><td>{row['Velocidad']}</td></tr>
            <tr><td style="font-weight: bold;">Rumbo:</td><td>{row['Rumbo']}</td></tr>
        </table>
    </div>
    """
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        color="#1f78b4",
        fill=True,
        fill_color="#1f78b4",
        fill_opacity=0.6,
        popup=folium.Popup(popup_html, max_width=260)
    ).add_to(m)


# === 7. Capa GSA con tooltip ===
if capa_gsa.crs is None or capa_gsa.crs.to_string().upper() != "EPSG:4326":
    capa_gsa = capa_gsa.to_crs(epsg=4326)

folium.GeoJson(
    capa_gsa,
    name="Zonas GSA",
    style_function=lambda x: {
        "color": "red",
        "fillColor": "transparent",
        "weight": 1.5
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Descripcio", "NombreGSA", "FaoSubarea"],
        aliases=["Descripción:", "Nombre GSA:", "FAO Subarea:"],
        style="font-family: Arial; font-size: 11px;"
    )
).add_to(m)


# === 8. Capa países ===
if capa_paises.crs is None or capa_paises.crs.to_string().upper() != "EPSG:4326":
    capa_paises = capa_paises.to_crs(epsg=4326)

folium.GeoJson(
    capa_paises,
    name="Países",
    style_function=lambda x: {
        "color": "brown",
        "fillColor": "beige",
        "fillOpacity": 1
    }
).add_to(m)

# === 8. Guardar el mapa en HTML ===
m.save(ruta_salida)
print(f"Mapa guardado correctamente en: {ruta_salida}")
