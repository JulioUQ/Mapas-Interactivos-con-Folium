# =========================================================
# Actividad 3: CONTROL AVANZADO DE CAPAS CON LAYERCONTROL
# =========================================================

# === Carga de librerías ===
import pandas as pd
import geopandas as gpd
import folium
from folium import CircleMarker, FeatureGroup, LayerControl
import os


# =============================================================================
# 1. CONFIGURACIÓN DE RUTAS (WINDOWS)
# =============================================================================
ruta_excel = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\DatosPosicionamiento\Redmine 8258_v2.xlsx"

ruta_lbr = r"P:\Proyectos\CALCULO_CIERRES\CONTROL CALIDAD\TeoríaSIPE\Programacion\Directorio GIS con QGIS\GIS_2.0\Líneas de base\LBR.shp"
ruta_reservas = r"P:\Proyectos\CALCULO_CIERRES\CONTROL CALIDAD\TeoríaSIPE\Programacion\Directorio GIS con QGIS\GIS_2.0\Capas especiales\Reservas marinas\RESERVAS MARINAS.shp"

ruta_as = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\AreasSensiblesyCriticas\8258_AC.shp"
ruta_ac = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\AreasSensiblesyCriticas\8258_AS.shp"

ruta_salida = r"C:\Users\jubeda2\Documents\git\Mapas-Interactivos-con-Folium\data\Actividades\mapa_interactivo_multicapas_Act3.html"

# =============================================================================
# 2. CARGA Y LIMPIEZA DE DATOS (EXCEL)
# =============================================================================
print("Cargando Excel de datos...")
df = pd.read_excel(ruta_excel)

# Asegurar que las coordenadas sean números
for col in ["Latitud", "Longitud"]:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

df = df.dropna(subset=["Latitud", "Longitud"])

# Convertir Fecha a string
if pd.api.types.is_datetime64_any_dtype(df["Fecha"]):
    df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")
else:
    df["Fecha"] = df["Fecha"].astype(str)

# Rellenar nulos para tooltips
campos_texto = ["CFR", "NombreBuque", "Zona", "Censo"]
for c in campos_texto:
    if c in df.columns:
        df[c] = df[c].fillna("-")

# =============================================================================
# 3. CARGA DE SHAPEFILES 
# =============================================================================
def import_shp_as_gpd(shapefile: str) -> gpd.GeoDataFrame:
    """
    Importa shapefile como GeoDataFrame en CRS EPSG:4326
    y lo deja preparado para usar en Folium (sin errores JSON).
    
    Ejemplo:
        gdf = import_shp_as_gpd("/ruta/archivo.shp")
    """
    
    # 1️ Leer shapefile
    print(f"Cargando shapefile: {os.path.basename(shapefile)}...")
    gdf = gpd.read_file(shapefile)

    # 2️ Asegurar CRS WGS84 (EPSG:4326)
    if gdf.crs:
        gdf = gdf.to_crs(epsg=4326)
    else:
        gdf = gdf.set_crs(epsg=4326)

    # 3️ Limpiar columnas para evitar error JSON en Folium
    for col in gdf.columns:
        if col != "geometry":
            
            # Convertir datetime a string
            if pd.api.types.is_datetime64_any_dtype(gdf[col]):
                gdf[col] = gdf[col].astype(str)
            
            # Convertir posibles Timestamp sueltos
            elif gdf[col].apply(lambda x: isinstance(x, pd.Timestamp)).any():
                gdf[col] = gdf[col].astype(str)

            # Reemplazar NaN / NaT por None (JSON compatible)
            gdf[col] = gdf[col].where(gdf[col].notnull(), None)

    return gdf


gdf_lbr = import_shp_as_gpd(ruta_lbr)
gdf_reservas = import_shp_as_gpd(ruta_reservas)
gdf_as = import_shp_as_gpd(ruta_as)
gdf_ac = import_shp_as_gpd(ruta_ac)

# =============================================================================
# 4. INICIALIZACIÓN DEL MAPA Y TILES
# =============================================================================
print("Generando mapa...")
centro_mapa = [df["Latitud"].mean(), df["Longitud"].mean()]
m = folium.Map(location=centro_mapa, zoom_start=6, tiles=None)

# --- Añadiendo Tiles ---
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles © Esri', name='Esri World Ocean Base', overlay=False
).add_to(m)

# =============================================================================
# 5. AÑADIR SHAPEFILES AL MAPA
# =============================================================================
print("Añadiendo shapefiles al mapa...")
if gdf_lbr is not None:
    folium.GeoJson(gdf_lbr, name="Líneas de Base (LBR)",
                   style_function=lambda x: {'color': '#003366', 'weight': 2, 'fillOpacity': 0}).add_to(m)

if gdf_reservas is not None:
    folium.GeoJson(gdf_reservas, name="Reservas Marinas",
                   style_function=lambda x: {'color': 'green', 'weight': 1, 'fillOpacity': 0.3},
                   tooltip=folium.GeoJsonTooltip(fields=list(gdf_reservas.columns.drop('geometry'))) if not gdf_reservas.empty else None
                   ).add_to(m)

if gdf_as is not None:
    folium.GeoJson(gdf_as, name="Áreas Sensibles (AS)",
                   style_function=lambda x: {'color': 'orange', 'weight': 2, 'fillOpacity': 0.2},
                   tooltip=folium.GeoJsonTooltip(fields=list(gdf_as.columns.drop('geometry'))) if not gdf_as.empty else None
                   ).add_to(m)

if gdf_ac is not None:
    folium.GeoJson(gdf_ac, name="Áreas Críticas (AC)",
                   style_function=lambda x: {'color': 'red', 'weight': 2, 'fillOpacity': 0.2},
                   tooltip=folium.GeoJsonTooltip(fields=list(gdf_ac.columns.drop('geometry'))) if not gdf_ac.empty else None
                   ).add_to(m)

# =============================================================================
# 6. LOGICA DE COLORES Y CAPAS (PUNTOS)
# =============================================================================
print("Generando capas de puntos...")

colores_hex = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

unique_years = sorted(df["Año"].unique())
color_dict = {year: colores_hex[i % len(colores_hex)] for i, year in enumerate(unique_years)}

grupos = df.groupby(["Año", "Censo"])

for (anio, censo), data_grupo in grupos:
    nombre_capa = f"{anio} - {censo}"
    fg = FeatureGroup(name=nombre_capa, show=False)
    
    color_punto = color_dict.get(anio, "blue")
    
    for _, row in data_grupo.iterrows():
        tooltip_html = f"""
        <div style="font-family: Arial; font-size: 12px; min-width: 200px;">
            <b>Buque:</b> {row['NombreBuque']}<br>
            <b>CFR:</b> {row['CFR']}<br>
            <b>Fecha:</b> {row['Fecha']}<br>
            <b>Censo:</b> {row['Censo']}<br>
            <b>Zona:</b> {row['Zona']}<br>
            <b>Velocidad:</b> {row['Velocidad']} kn<br>
            <b>Coords:</b> {round(row['Latitud'], 4)}, {round(row['Longitud'], 4)}
        </div>
        """
        
        CircleMarker(
            location=[row["Latitud"], row["Longitud"]],
            radius=2,
            color=color_punto,
            fill=True,
            fill_color=color_punto,
            fill_opacity=0.7,
            weight=1,
            tooltip=tooltip_html
        ).add_to(fg)
    
    fg.add_to(m)

# =============================================================================
# 7. CONTROL DE CAPAS Y GUARDADO
# =============================================================================
LayerControl(collapsed=False).add_to(m)

print(f"Guardando mapa en: {ruta_salida}")
m.save(ruta_salida)
