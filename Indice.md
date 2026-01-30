# **Índice**

  

<ul style="list-style-type:none">

  

<li><a href="#1-introduccion-a-folium">1. Introducción a Folium</a></li>

  <ul style="list-style-type:none">

    <li><a href="#1-1-que-es-folium">1.1. ¿Qué es Folium?</a></li>

    <li><a href="#1-2-instalacion-y-configuracion-inicial">1.2. Instalación y configuración inicial</a></li>

    <li><a href="#1-3-primer-mapa-con-folium-map">1.3. Primer mapa con <em>folium.Map</em></a></li>

  </ul>

  

<li><a href="#2-conceptos-fundamentales">2. Conceptos Fundamentales</a></li>

  <ul style="list-style-type:none">

    <li><a href="#2-1-estructura-basica-de-un-mapa">2.1. Estructura básica de un mapa</a></li>

    <li><a href="#2-2-guardado-y-visualizacion-de-mapas">2.2. Guardado y visualización de mapas</a></li>

  </ul>

  

<li><a href="#3-elementos-basicos-en-folium">3. Elementos Básicos en Folium</a></li>

  <ul style="list-style-type:none">

    <li><a href="#3-1-marcadores-simples-folium-marker">3.1. Marcadores simples (<em>folium.Marker</em>)</a></li>

    <li><a href="#3-2-marcadores-simples-folium-circlemarker">3.2. Marcadores simples (<em>folium.CircleMarker</em>)</a></li>

    <li><a href="#3-3-elementos-del-marcador-folium-tooltip">3.3. Elementos del marcador (<em>folium.Tooltip</em>)</a></li>

    <li><a href="#3-4-iconos-personalizados-folium-divicon">3.4. Iconos personalizados (<em>folium.DivIcon</em>)</a></li>

  </ul>

  

</ul>





Los encunciados de los apartados son:

<a id="1-introduccion-a-folium"></a>

<a id="1-introduccion-a-folium"></a>

# 1. Introducción a Folium
<a id="1-1-que-es-folium"></a>

## 1.1. ¿Qué es Folium?

<a id="1-2-instalacion-y-configuracion-inicial"></a>

## 1.2. Instalación y configuración inicial

## 1.3. Primer mapa con folium

### 1.3.1. Estructura básica de un mapa - Clase [Map](https://python-visualization.github.io/folium/modules.html#folium.folium.Map)

### 1.3.2. Añadir tile desde URL - Método [add_tile_layer()](https://python-visualization.github.io/folium/modules.html#folium.folium.Map.add_tile_layer)
### 1.3.3. Guardar el mapa en HTML - Método [save()](https://python-visualization.github.io/folium/modules.html#folium.folium.Map.save)

# 2. Importación y preparación de los datos

## 2.1. Importación de posiciones desde bases de datos (SQL)

## 2.2. Importación desde ficheros tabulares (CSV, Excel)

## 2.3. Importación de datos geoespaciales (Shapefile, GeoPackage, GeoJSON)

## 2.4. Creación manual de posiciones a partir de coordenadas

## 2.5. Estandarización de los datos para Folium

# 3. Visualización de posiciones de pesca

## 3.1. Seguimiento pesquero - Clase [CircleMarker](https://python-visualization.github.io/folium/modules.html#folium.vector_layers.CircleMarker)

## 3.2. Ajustar limites espaciales del mapa

## 3.2. Incluir posiciones en el mapa (usando Latitud y Longitud)

## 3.3. Incluir posiciones en el mapa (usando Geometria = POINT)

# 4. Información interactiva en mapas: Clase [popup](https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html) y [tooltip](https://juncotic.com/introduccion-a-los-marcadores-en-folium-iconos-colores-y-tooltips/)

## 4.1. Popup: información detallada bajo demanda

## 4.2. Tooltip: información rápida en contexto
