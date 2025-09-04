Aquí tienes una versión reescrita del README, más clara, estructurada y completa, manteniendo toda la información y agregando un poco más de contexto y detalle para cada sección:

---

# Mapas Interactivos con Folium para Gestión Pesquera

Este repositorio tiene como objetivo **aprender, comprender y aplicar** la librería [Folium](https://python-visualization.github.io/folium/) para la creación de **mapas interactivos y animados** enfocados en la **gestión pesquera**.

Se incluyen ejemplos prácticos con datos reales o simulados para:

* Visualizar **rectángulos estadísticos** de zonas de pesca.
* Crear **mapas dinámicos y animados** de la trayectoria de los buques.
* Representar **capturas y esfuerzo pesquero** en diferentes regiones.
* Generar **mapas temáticos** por especie, temporada o zona de interés.

El repositorio está pensado para **investigadores, gestores pesqueros y programadores** que quieran aprender a integrar datos espaciales en visualizaciones interactivas.

---

## Estructura del repositorio

```
folium-gestion-pesquera/  
│  
├── README.md                   # Explicación general del proyecto  
├── requirements.txt            # Librerías y dependencias necesarias  
├── Q&A's                       # Preguntas y respuestas sobre el proyecto
├── data/                       # Datos de ejemplo (GeoJSON, CSV, shapefiles)  
├── notebooks/                  # Jupyter Notebooks con ejemplos prácticos  
│   ├── 01_basicos_folium.ipynb  
│   ├── 02_capas_y_controles_folium.ipynb  
│   ├── 03_mapas_avanzados.ipynb  
│   └── 04_Actividades_prácticas.ipynb  
├── scripts/                    # Scripts Python reutilizables  
│   ├── dashboard.py  
│   ├── tidy_functions.py  
│   ├── geo_functions.py  
│   └── folium_utils.py   
└── img/                        # Capturas de ejemplo para el README y mapas
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/folium-gestion-pesquera.git
cd folium-gestion-pesquera
```

### 2. Crear un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Contenido de aprendizaje

| Notebook                              | Tema                     | Descripción                                                                    |
| ------------------------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| 01\_basicos\_folium.ipynb             | Mapa base                | Creación de mapas, selección de tiles, centrado en coordenadas.                |
| 02\_capas\_y\_controles\_folium.ipynb | Capas vectoriales        | Añadir polígonos y líneas, colorearlos según atributos, controlar visibilidad. |
| 03\_mapas\_avanzados.ipynb            | Mapas temáticos          | Visualización de capturas, biomasa y esfuerzo por especie, temporada o zona.   |
| 04\_Actividades\_prácticas.ipynb      | Interactividad y filtros | Añadir `LayerControl`, popups, leyendas y filtros dinámicos.                   |

---

## Tecnologías y librerías utilizadas

* [Folium](https://python-visualization.github.io/folium/) – creación de mapas interactivos.
* [GeoPandas](https://geopandas.org/) – manejo de datos geoespaciales.
* [Pandas](https://pandas.pydata.org/) – manipulación de datos tabulares.
* [Shapely](https://shapely.readthedocs.io/) – geometría y análisis espacial.
* [Jupyter Notebook](https://jupyter.org/) – documentación interactiva y pruebas de código.

---

## Uso recomendado

1. Revisar los **notebooks en orden** para entender desde conceptos básicos hasta mapas avanzados.
2. Probar los **scripts reutilizables** para automatizar tareas y generar mapas personalizados.
3. Modificar los **datos de ejemplo** o incorporar datos propios para análisis específicos de gestión pesquera.
