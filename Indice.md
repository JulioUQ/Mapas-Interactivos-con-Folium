# **Índice**

  

<ul style="list-style-type:none">

  

<li><a href="#1-capas-y-controles">1. Capas y Controles</a></li>

  <ul style="list-style-type:none">

    <li><a href="#1-1-capas-de-marcadores-folium-featuregroup">1.1. Capas de marcadores (<em>folium.FeatureGroup</em>)</a></li>

    <li><a href="#1-2-capas-de-poligonos-y-lineas-folium-polygon-y-folium-polyline">1.2. Capas de polígonos y líneas (<em>folium.Polygon</em>, <em>folium.PolyLine</em>)</a></li>

    <li><a href="#1-3-control-de-capas-y-visibilidad-folium-layercontrol">1.3. Control de capas y visibilidad (<em>folium.LayerControl</em>)</a></li>

  </ul>

  

<li><a href="#2-integracion-con-datos">2. Integración con Datos</a></li>

  <ul style="list-style-type:none">

    <li><a href="#2-1-importar-datos-desde-csv-con-pandas">2.1. Importar datos desde CSV con Pandas</a></li>

    <li><a href="#2-2-visualizacion-de-datos-con-geojson">2.2. Visualización de datos con GeoJSON</a></li>

    <li><a href="#2-3-mapas-coropleticos-folium-choropleth">2.3. Mapas coropléticos (<em>folium.Choropleth</em>)</a></li>

  </ul>

  

<li><a href="#3-personalizacion-avanzada">3. Personalización Avanzada</a></li>

  <ul style="list-style-type:none">

    <li><a href="#3-1-colores-y-estilos-dinamicos">3.1. Colores y estilos dinámicos</a></li>

  </ul>

  

</ul>


Modifica el indice anterior asi como sus enlaces con el titulo de los apartados, por los apartados siguientes:

<a id="1-capas-y-controles"></a>

<a id="1-capas-y-controles"></a>

# 1. Capas en mapas interactivos con Folium

<a id="1-1-capas-de-marcadores-folium-featuregroup"></a>

## 1.1. Capas agrupadas: Clase [folium.FeatureGroup](https://python-visualization.github.io/folium/latest/user_guide/plugins/featuregroup_subgroup.html)

## 1.2 Segmentación temporal de las posiciones de captura
## 1.3 Creación de capas temáticas con `FeatureGroup`

<a id="1-2-control-de-capas-y-visibilidad-folium-layercontrol"></a>

# 2. Control de capas e interactividad del mapa - Clase [LayerControl](https://python-visualization.github.io/folium/modules.html#folium.map.LayerControl)

<a id="1-3-1-lineas-folium-polyline"></a>

# 3. Líneas - Clase [`folium.PolyLine`](https://python-visualization.github.io/folium/latest/user_guide/vector_layers/polyline.html)

## 3.1. Representación de geometrías tipo `LineString` - [Linea base recta (LBR)](https://centrodedescargas.cnig.es/CentroDescargas/lineas-base-rectas)

## 3.2 Representación de rutas de pesca

### 3.2.1 Construcción de la geometría lineal con `folium.PolyLine`

### 3.2.2. `PolyLine` como elemento informativo interactivo

### 3.2.3. Combinación de líneas y puntos: lectura completa de la trayectoria

### 3.2.4. Integración de la ruta en una capa (`FeatureGroup`)

# 4. Polígonos - Clase [`folium.Polygon`](https://python-visualization.github.io/folium/latest/user_guide/vector_layers/polygon.html)

## 4.1. Zonas de veda espacial en el Golfo de Cádiz

# 5. Geometrías GeoJSON - Clase [`folium.GeoJson`](https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html)

## 5.1. Representación de geometrías tipo `MultiPolygon` - Zonas FAO

## 5.2. Etiquetas e iconos en el mapa - Clase `folium.Marker`