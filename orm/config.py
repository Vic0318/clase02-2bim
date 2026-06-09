import os

# Obtener la ruta absoluta a la raíz del proyecto para ubicar la base de datos
directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruta_db = os.path.join(directorio_raiz, "base_datos.db")

# Cadena de conexión para SQLite
cadena_base_datos = f"sqlite:///{ruta_db}"
