import os

# Definir la ruta al archivo JSON dentro del paquete `config`
config_path_exp = os.path.join(os.path.dirname(__file__), "./conf_global/app-config-exp.json")
config_path_prod = os.path.join(os.path.dirname(__file__), "./conf_global/app-config-prod.json")
config_path_fempa = os.path.join(os.path.dirname(__file__), "./conf_global/app-config-fempa.json")
config_path_server = os.path.join(os.path.dirname(__file__), "./conf_global/server-config.json")
