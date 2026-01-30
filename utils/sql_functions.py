# ================================
# sql_functions.py
# Funciones para manipular datos desde SQL Server
# ================================

import sys
import os
import warnings
import json
import pyodbc
import pandas as pd
from pandas._typing import MergeHow
import geopandas as gpd
from shapely.geometry import Point
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from typing import Literal, Optional

# Ruta de configuración por defecto
from config import config_path_exp

# Añadir directorio raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=UserWarning)

# ================================
# CONFIGURACIÓN Y CONEXIÓN A BBDD
# ================================

def cargar_configuracion_json(config_file: str = config_path_exp) -> dict:
    """Carga un archivo JSON de configuración y lo convierte en diccionario.

    Ejemplo:
        conf = cargar_configuracion_json()
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_file}")
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_configuracion_conexion(database_key: str, ruta_config: str = config_path_exp) -> dict:
    """Obtiene configuración combinada 'common' + específica desde JSON.

    Ejemplo:
        conf = obtener_configuracion_conexion("SGP_SIPE_EXPLOTACION")
    """
    confs = cargar_configuracion_json(ruta_config)
    if "common" not in confs or database_key not in confs:
        raise ValueError(f"Faltan claves en la configuración: 'common' o '{database_key}'")
    return {**confs["common"], **confs[database_key]}

def crear_cadena_conexion_odbc(conf: dict) -> str:
    """Genera una cadena de conexión ODBC a SQL Server.

    Ejemplo:
        conn_str = crear_cadena_conexion_odbc(conf)
    """
    return (
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={conf['Server']};"
        f"DATABASE={conf['Database']};"
        f"UID={conf['UID']};"
        f"PWD={conf['PWD']}"
    )

def ejecutar_consulta_sql(query: str, database_key: str = "SGP_SIPE_EXPLOTACION", ruta_config: str = config_path_exp):
    """Ejecuta una consulta SQL y retorna los resultados en un DataFrame.

    Ejemplo:
        df_resultado = ejecutar_consulta_sql("SELECT * FROM tabla")
    """
    all_confs = cargar_configuracion_json(ruta_config)

    if "common" not in all_confs:
        raise KeyError("No se encontró la sección 'common' en la configuración.")
    if database_key not in all_confs:
        raise KeyError(f"No se encontró la base de datos '{database_key}' en la configuración.")

    conf = {**all_confs["common"], **all_confs[database_key]}

    conn_str = (
        f"DRIVER={conf['Driver']};"
        f"SERVER={conf['Server']};"
        f"DATABASE={conf['Database']};"
        f"UID={conf['UID']};"
        f"PWD={conf['PWD']}"
    )
    conn_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"
    engine = create_engine(conn_url)

    return pd.read_sql_query(query, con=engine)



def importar_shapefile_a_sqlserver(
        ruta_shapefile: str, 
        nombre_tabla: str, 
        database_key: str, 
        ruta_config: str = config_path_exp):
    """Importa un shapefile o GeoJSON a una tabla de SQL Server con geometría."""
    gdf = gpd.read_file(ruta_shapefile)
    gdf = gdf.to_crs(epsg=4326)
    gdf["geometry_WKT"] = gdf.geometry.apply(lambda geom: geom.wkt if geom else None)
    df = gdf.drop(columns='geometry')

    conf = obtener_configuracion_conexion(database_key, ruta_config)
    conn_str = crear_cadena_conexion_odbc(conf)
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    schema = "dbo"
    cursor.execute(f"IF OBJECT_ID('{schema}.{nombre_tabla}', 'U') IS NOT NULL DROP TABLE {schema}.{nombre_tabla};")
    conn.commit()

    # Mejorar la detección de tipos de datos
    definicion_columnas = []
    for col in df.columns:
        dtype = df[col].dtype
        
        if pd.api.types.is_datetime64_any_dtype(dtype):
            # Columnas de fecha/hora
            definicion_columnas.append(f"[{col}] DATETIME2")
        elif pd.api.types.is_integer_dtype(dtype):
            # Columnas enteras
            definicion_columnas.append(f"[{col}] BIGINT")
        elif pd.api.types.is_float_dtype(dtype):
            # Columnas decimales
            definicion_columnas.append(f"[{col}] FLOAT")
        elif pd.api.types.is_bool_dtype(dtype):
            # Columnas booleanas
            definicion_columnas.append(f"[{col}] BIT")
        else:
            # Por defecto, texto
            definicion_columnas.append(f"[{col}] NVARCHAR(MAX)")
    
    definicion_columnas_str = ",\n    ".join(definicion_columnas)
    cursor.execute(f"CREATE TABLE {schema}.{nombre_tabla} (\n    {definicion_columnas_str}\n);")
    conn.commit()

    # Convertir fechas a formato compatible y reemplazar NaN/NaT con None
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(lambda x: x if pd.notna(x) else None)
        else:
            df[col] = df[col].where(pd.notna(df[col]), None) # type: ignore

    columnas = ', '.join(f"[{col}]" for col in df.columns)
    placeholders = ', '.join('?' for _ in df.columns)
    insert_sql = f"INSERT INTO {schema}.{nombre_tabla} ({columnas}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cursor.execute(insert_sql, row)
    conn.commit()

    cursor.execute(f"ALTER TABLE {schema}.{nombre_tabla} ADD geometry_GEOM geometry;")
    cursor.execute(f"""
        UPDATE {schema}.{nombre_tabla}
        SET geometry_GEOM = geometry::STGeomFromText(REPLACE(geometry_WKT, ' Z', ''), 4326)
        WHERE geometry_WKT IS NOT NULL;
    """)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Shapefile cargado correctamente en la tabla [{schema}].[{nombre_tabla}].")

def importar_dataframe_a_sqlserver(
    df: pd.DataFrame,
    nombre_tabla: str,
    database_key: str,
    esquema: str = "dbo",
    if_exists: Literal["replace", "fail", "append"] = "replace",
    ruta_config: str = config_path_exp
):
    """
    Importa un DataFrame de pandas a una tabla en SQL Server.

    La conexión se obtiene a partir de una configuración definida externamente
    (clave de base de datos y fichero de configuración). La tabla se crea o
    actualiza según el parámetro `if_exists`.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que se desea importar a SQL Server.
    nombre_tabla : str
        Nombre de la tabla destino en la base de datos.
    database_key : str
        Clave identificadora de la base de datos en el fichero de configuración.
    esquema : str, optional
        Esquema de la tabla en SQL Server (por defecto "dbo").
    if_exists : {"replace", "fail", "append"}, optional
        Comportamiento si la tabla ya existe:
        - "replace": elimina la tabla y la vuelve a crear (por defecto)
        - "append": añade los datos a la tabla existente
        - "fail": lanza un error si la tabla existe
    ruta_config : str, optional
        Ruta al fichero de configuración de la conexión.

    Returns
    -------
    None

    Examples
    --------
    >>> importar_dataframe_a_sqlserver(
    ...     df=df_buques,
    ...     nombre_tabla="buques_12_15m_sin_vms",
    ...     database_key="sqlserver_produccion",
    ...     esquema="dbo",
    ...     if_exists="replace"
    ... )
    """
    conf = obtener_configuracion_conexion(database_key, ruta_config)
    conn_str = quote_plus(crear_cadena_conexion_odbc(conf))
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={conn_str}",
        fast_executemany=True
    )

    # Reemplazar NaN por None para compatibilidad con SQL Server
    df = df.where(pd.notnull(df), None)

    print(f"Importando a {conf['Database']}.{esquema}.{nombre_tabla} ...")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    df.to_sql(nombre_tabla, engine, schema=esquema, if_exists=if_exists, index=False)
    print("Importación completada con éxito.")
