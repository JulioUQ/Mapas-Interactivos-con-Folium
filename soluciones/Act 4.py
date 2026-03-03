# =========================================================
# Actividad 4: EXPLORACIÓN DE PLUGINS EN FOLIUM
# =========================================================

# === 1. Carga de librerías ===
import pandas as pd
import geopandas as gpd
import folium
from folium import FeatureGroup, LayerControl
from folium.plugins import (
    MiniMap,
    Fullscreen,
    MousePosition,
    MeasureControl,
    MarkerCluster,
    Draw
)
import os


# =============================================================================
# 2. CONFIGURACIÓN DE RUTAS
# =============================================================================
ruta_excel = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\DatosPosicionamiento\Redmine 8258_v2.xlsx"

ruta_salida = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\mapa_plugins_Act4.html"


# =============================================================================
# 3. CARGA Y LIMPIEZA DE DATOS
# =============================================================================
print("Cargando datos Excel...")

df = pd.read_excel(ruta_excel)

# Asegurar formato numérico correcto en coordenadas
for col in ["Latitud", "Longitud"]:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

df = df.dropna(subset=["Latitud", "Longitud"])

# Convertir Fecha a string si es datetime
if "Fecha" in df.columns:
    if pd.api.types.is_datetime64_any_dtype(df["Fecha"]):
        df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")
    else:
        df["Fecha"] = df["Fecha"].astype(str)

# Rellenar posibles nulos
for col in ["CFR", "NombreBuque", "Zona", "Censo"]:
    if col in df.columns:
        df[col] = df[col].fillna("-")


# =============================================================================
# 4. INICIALIZACIÓN DEL MAPA BASE
# =============================================================================
print("Inicializando mapa...")

centro_mapa = [df["Latitud"].mean(), df["Longitud"].mean()]

m = folium.Map(
    location=centro_mapa,
    zoom_start=6,
    tiles=None
)

# Tile base profesional
folium.TileLayer(
    tiles="CartoDB positron",
    name="CartoDB Positron",
    overlay=False
).add_to(m)


# =============================================================================
# 5. PLUGIN 1: MARKERCLUSTER (visualización avanzada)
# =============================================================================
print("Añadiendo MarkerCluster...")

fg_cluster = FeatureGroup(name="Posiciones VMS (Cluster)", show=True)
marker_cluster = MarkerCluster().add_to(fg_cluster)

for _, row in df.iterrows():

    tooltip_html = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <b>Buque:</b> {row.get('NombreBuque','-')}<br>
        <b>CFR:</b> {row.get('CFR','-')}<br>
        <b>Fecha:</b> {row.get('Fecha','-')}<br>
        <b>Censo:</b> {row.get('Censo','-')}<br>
        <b>Zona:</b> {row.get('Zona','-')}
    </div>
    """

    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=3,
        fill=True,
        fill_opacity=0.7,
        tooltip=tooltip_html
    ).add_to(marker_cluster)

fg_cluster.add_to(m)


# =============================================================================
# 6. PLUGINS DE INTERACCIÓN
# =============================================================================
print("Añadiendo plugins de interacción...")

# MiniMapa
MiniMap(toggle_display=True).add_to(m)

# Pantalla completa
Fullscreen(position="topright").add_to(m)

# Mostrar coordenadas del cursor
MousePosition(
    position="bottomright",
    separator=" | ",
    prefix="Coords:"
).add_to(m)

# Herramienta de medición
MeasureControl(
    position="topleft",
    primary_length_unit="kilometers"
).add_to(m)

# Herramienta de dibujo
Draw(
    export=True,
    filename="geometrias_dibujadas.geojson",
    position="topleft"
).add_to(m)


# =============================================================================
# 7. CONTROL DE CAPAS
# =============================================================================
LayerControl(collapsed=False).add_to(m)


# =============================================================================
# 8. GUARDADO DEL MAPA
# =============================================================================
print(f"Guardando mapa en: {ruta_salida}")

m.save(ruta_salida)

print("Proceso finalizado correctamente.")