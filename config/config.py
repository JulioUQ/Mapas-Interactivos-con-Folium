import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ruta al archivo de configuración
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path_exp = os.path.join(base_dir, "./conf_global/app-config-exp.json")

# Ruta a capas espaciales
paises = r"C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\WorldCountries\WorldCountries.shp"
fao = r"C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\ZonasFAO\ZonasFAO.shp"
gsa = r'C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\ZonasGSA\ZonasGSA.shp'
MarTerritorial = r'C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\ZonaMarTerritorial\ZonaMarTerritorial.shp'
ZEE = r'C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\ZonasZEE\ZonasZEE.shp'
rectices = r'C:\Users\jubeda2\Desktop\Programacion\GIS_2.0\Rectangulos Estadisticos ICES\RectangulosEstadisticosICES.shp'