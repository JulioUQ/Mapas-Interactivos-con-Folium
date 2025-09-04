"""
folium_utils.py
Funciones para inicializar y enriquecer mapas base en Folium de forma genérica.
"""

import folium
from folium.features import DivIcon
import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon


def crear_mapa(lat=None, lon=None, gdf=None, zoom=10, tiles="CartoDB positron", 
               control_scale=True, prefer_canvas=True, archivo=None):
    """
    Crea un mapa interactivo en Folium, ya sea a partir de coordenadas o de un GeoDataFrame.

    Parámetros:
    - lat (float, opcional): Latitud del centro del mapa (usar junto con lon).
    - lon (float, opcional): Longitud del centro del mapa (usar junto con lat).
    - gdf (GeoDataFrame, opcional): Objeto GeoDataFrame para centrar el mapa en su centroide.
    - zoom (int, opcional): Nivel inicial de zoom (por defecto 10).
    - tiles (str, opcional): Estilo de mapa base. Ejemplos: 
        "OpenStreetMap", "Stamen Terrain", "Stamen Toner", 
        "CartoDB positron", "CartoDB dark_matter".
    - control_scale (bool, opcional): Mostrar escala en el mapa (por defecto True).
    - prefer_canvas (bool, opcional): Optimiza renderizado si hay muchos objetos (por defecto True).
    - archivo (str, opcional): Si se proporciona, guarda el mapa en un archivo HTML.

    Retorna:
    - folium.Map
    """

    if gdf is not None:
        centro = gdf.geometry.union_all().centroid
        location = [centro.y, centro.x]
    elif lat is not None and lon is not None:
        location = [lat, lon]
    else:
        raise ValueError("Debes proporcionar (lat, lon) o un GeoDataFrame (gdf).")

    # Crear el mapa con todos los parámetros relevantes
    mapa = folium.Map(
        location=location,
        zoom_start=zoom,
        tiles=tiles,
        control_scale=control_scale,
        prefer_canvas=prefer_canvas
    )

    # Guardar si se proporciona archivo
    if archivo:
        mapa.save(archivo)

    return mapa

def añadir_puntos(
    m,
    gdf,
    lat_col="Latitud",
    lon_col="Longitud",
    color_col=None,
    tooltip_text=None,
    cmap_name="tab10",
    color_dict=None
):
    """
    Añade puntos al mapa, creando un FeatureGroup por categoría si se indica color_col.
    Funciona con columna 'geometry' o columnas de latitud/longitud.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame o DataFrame): Datos con coordenadas.
        lat_col (str): Columna de latitud.
        lon_col (str): Columna de longitud.
        color_col (str): Columna que define el color/categoría.
        tooltip_text (str o lista): Columnas para tooltip.
        cmap_name (str): Nombre de colormap (solo si no se pasa color_dict).
        color_dict (dict): Diccionario {categoria: color_hex} opcional.
    """
    
    # Preparar colores
    if color_col:
        categorias = gdf[color_col].unique()
        if color_dict is not None:
            internal_color_dict = color_dict
        else:
            colormap = mcm.get_cmap(cmap_name, len(categorias))
            internal_color_dict = {cat: mcolors.rgb2hex(colormap(i)) for i, cat in enumerate(categorias)}
    else:
        internal_color_dict = {None: "blue"}
        categorias = [None]

    # Crear FeatureGroup por categoría
    for cat in categorias:
        fg_name = str(cat) if cat is not None else "Puntos"
        fg_color = internal_color_dict.get(cat, "blue")
        fg = folium.FeatureGroup(name=f'<span style="color:{fg_color}">{fg_name}</span>', show=True)
        
        subset = gdf[gdf[color_col] == cat] if color_col else gdf

        for _, row in subset.iterrows():
            # Coordenadas
            if "geometry" in gdf.columns and row.geometry is not None:
                lat, lon = row.geometry.y, row.geometry.x
            else:
                lat, lon = row[lat_col], row[lon_col]

            # Tooltip
            if isinstance(tooltip_text, list):
                tooltip_html = "<br>".join(f"{col}: {row[col]}" for col in tooltip_text)
            elif isinstance(tooltip_text, str):
                tooltip_html = row[tooltip_text] if tooltip_text in gdf.columns else tooltip_text
            else:
                tooltip_html = None

            folium.CircleMarker(
                location=[lat, lon],
                radius=2,
                color=fg_color,
                fill=True,
                fill_color=fg_color,
                fill_opacity=0.7,
                tooltip=folium.Tooltip(tooltip_html, sticky=True) if tooltip_html else None
            ).add_to(fg)
        
        fg.add_to(m)




def añadir_poligonos_por_valor(
    m,
    gdf,
    columna_nombre=None,
    tooltip_fields=None,
    tooltip_aliases=None,
    cmap_name="tab20",
    fill_opacity=0.4,
    default_color="#3388ff"
):
    """
    Añade polígonos coloreados por un valor único de columna, o con un color por defecto si no se indica.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna_nombre (str, opcional): Columna que define las categorías.
        tooltip_fields (list): Columnas para tooltip.
        tooltip_aliases (list): Alias para tooltip.
        cmap_name (str): Nombre del colormap de Matplotlib.
        fill_opacity (float): Opacidad del relleno.
        default_color (str): Color por defecto si no se especifica columna de categorías.
    """
    
    if columna_nombre:
        nombres_unicos = gdf[columna_nombre].dropna().unique()
        cmap = plt.colormaps[cmap_name].resampled(len(nombres_unicos))
        colores = [cmap(i) for i in range(len(nombres_unicos))]
        color_map = {
            nombre: f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            for nombre, (r, g, b, _) in zip(nombres_unicos, colores)
        }

        for nombre in nombres_unicos:
            sub_gdf = gdf[gdf[columna_nombre] == nombre]
            color = color_map[nombre]

            folium.GeoJson(
                sub_gdf,
                name=f'<span style="color:{color}">{nombre}</span>',
                style_function=lambda x, col=color: {
                    "fillColor": col,
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": fill_opacity
                },
                tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases) if tooltip_fields else None
            ).add_to(m)
    else:
        # Si no hay columna de categorías, todos los polígonos con color por defecto
        folium.GeoJson(
            gdf,
            style_function=lambda x: {
                "fillColor": default_color,
                "color": "black",
                "weight": 1,
                "fillOpacity": fill_opacity
            },
            tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases) if tooltip_fields else None
        ).add_to(m)


def añadir_contornos(m, gdf, columna_grupo, color_map=None, emoji_map=None, tooltip_fields=None, tooltip_aliases=None):
    """
    Añade contornos agrupados por un valor de columna.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna_grupo (str): Columna por la que agrupar.
        color_map (dict): Diccionario valor → color.
        emoji_map (dict): Diccionario valor → emoji.
        tooltip_fields (list): Columnas para tooltip.
        tooltip_aliases (list): Alias de las columnas para tooltip.

    Ejemplo:
        color_map = {"Zona A": "red", "Zona B": "blue"}
        emoji_map = {"Zona A": "🅰️", "Zona B": "🅱️"}
        tooltip_fields = ["IdRectangu", "Descripcio"]
        añadir_contornos(mapa, gdf, "TipoZona", color_map=color_map, emoji_map=emoji_map, tooltip_fields=tooltip_fields)
    """
    for valor, grupo in gdf.groupby(columna_grupo):
        color = color_map.get(valor, "#999999") if color_map else "#999999"
        emoji = emoji_map.get(valor, "") if emoji_map else ""

        folium.GeoJson(
            data=grupo,
            name=f"{emoji} {valor}" if emoji else str(valor),
            style_function=lambda x, col=color: {
                "fillColor": col,
                "color": col,
                "weight": 2,
                "fillOpacity": 0
            },
            tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases) if tooltip_fields else None
        ).add_to(m)


def añadir_etiquetas_por_poligono(m, gdf, columna, color_texto="black"):
    """
    Añade etiquetas de texto en el centroide de cada polígono.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna (str): Columna cuyo valor se mostrará como etiqueta.
        color_texto (str): Color del texto.

    Ejemplo:
    añadir_etiquetas_por_poligono(
            m=mapa,
            gdf=gdf_zonas,
            columna="Descripcio",
            color_texto="darkblue"
            )
    """
    for _, row in gdf.iterrows():
        valor = row[columna]
        geom = row["geometry"]

        geoms = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom] if isinstance(geom, Polygon) else []
        for poly in geoms:
            centroide = poly.centroid
            folium.Marker(
                location=[centroide.y, centroide.x],
                icon=DivIcon(
                    icon_size=(100, 20),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 11pt; font-weight: bold; color: {color_texto}">{valor}</div>',
                )
            ).add_to(m)


def crear_ruta(
    gdf_puntos, 
    mapa=None,
    lat_col="Latitud", 
    lon_col="Longitud", 
    fecha_col="Fecha", 
    hora_col="Hora", 
    vel_col="Velocidad", 
    rumbo_col="Rumbo",
    buque_col="Buque", 
    marea_col="HojaMarea"
):
    """
    Añade a un mapa folium la ruta de una marea (línea + puntos de inicio/fin).
    
    Parámetros
    ----------
    gdf_puntos : GeoDataFrame
        GeoDataFrame con los puntos de la marea seleccionada.
    mapa : folium.Map, optional
        Mapa de folium sobre el que añadir la ruta. Si None, se crea uno centrado en la marea.
    lat_col, lon_col : str
        Nombre de las columnas con latitud y longitud.
    fecha_col, hora_col : str
        Columnas de fecha y hora.
    vel_col, rumbo_col : str
        Columnas de velocidad y rumbo.
    buque_col, marea_col : str
        Columnas de identificación del buque y marea.
    
    Retorna
    -------
    folium.Map
        Mapa con la ruta añadida.
    """
    
    # Ordenar puntos por tiempo
    gdf_marea = gdf_puntos.dropna(subset=[lat_col, lon_col]).copy()
    gdf_marea = gdf_marea.sort_values(by=[fecha_col, hora_col])

    # Crear mapa base si no se pasa uno
    if mapa is None:
        mapa = folium.Map(
            location=[gdf_marea[lat_col].mean(), gdf_marea[lon_col].mean()],
            zoom_start=8,
            tiles="CartoDB positron"
        )

    # Coordenadas de la ruta
    coords = gdf_marea[[lat_col, lon_col]].values.tolist()

    # Tooltip resumen para la línea
    fecha_min = gdf_marea[fecha_col].min()
    fecha_max = gdf_marea[fecha_col].max()
    tooltip_text = (
        f"<b>Buque:</b> {gdf_marea[buque_col].iloc[0]} <br>"
        f"<b>Hoja de Marea</b>: {gdf_marea[marea_col].iloc[0]} <br>"
        f"<b>Número de puntos</b>: {len(gdf_marea)} <br>"
        f"<b>Fecha inicio</b>: {fecha_min} <br>"
        f"<b>Fecha fin</b>: {fecha_max}"
    )

    # Dibujar la ruta
    folium.PolyLine(
        locations=coords,
        color="blue",
        weight=3,
        opacity=0.8,
        tooltip=tooltip_text
    ).add_to(mapa)

    # Marcar inicio y fin
    primer_punto = gdf_marea.iloc[0]
    ultimo_punto = gdf_marea.iloc[-1]

    folium.Marker(
        location=[primer_punto[lat_col], primer_punto[lon_col]],
        popup=(f"<b>Inicio</b><br>"
               f"Vel: {primer_punto[vel_col]} nudos<br>"
               f"Rumbo: {primer_punto[rumbo_col]}"),
        icon=folium.Icon(color="green", icon="play"),
        tooltip="Inicio"
    ).add_to(mapa)

    folium.Marker(
        location=[ultimo_punto[lat_col], ultimo_punto[lon_col]],
        popup=(f"<b>Fin</b><br>"
               f"Vel: {ultimo_punto[vel_col]} nudos<br>"
               f"Rumbo: {ultimo_punto[rumbo_col]}"),
        icon=folium.Icon(color="red", icon="flag"),
        tooltip="Fin"
    ).add_to(mapa)

    return mapa
