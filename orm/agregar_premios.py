import csv
import os
from sqlalchemy.orm import sessionmaker
from modelo import engine, Premio, Serie

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 2. Obtener la ruta del archivo CSV
dir_actual = os.path.dirname(__file__)
ruta_csv = os.path.abspath(os.path.join(dir_actual, "..", "data", "premios.csv"))

try:
    # Cargar series y premios existentes en memoria (Idioma Python)
    series = {s.titulo: s for s in session.query(Serie).all()}
    # Clave compuesta (nombre_premio, categoria, anio, serie_id) para verificar existentes en memoria
    premios_existentes = {(p.nombre_premio, p.categoria, p.anio, p.serie_id) for p in session.query(Premio).all()}

    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_premio = int(fila["id"])
            nombre_premio = fila["nombre_premio"]
            categoria = fila["categoria"]
            anio = int(fila["anio"])
            titulo_serie = fila["serie"]

            # Buscar la serie correspondiente en memoria
            serie_obj = series.get(titulo_serie)
            if not serie_obj and titulo_serie:
                print(f"Advertencia: No se encontró la serie '{titulo_serie}' en memoria.")
            serie_id = serie_obj.id if serie_obj else None

            # Verificar si ya existe el premio en memoria para evitar duplicados
            if (nombre_premio, categoria, anio, serie_id) not in premios_existentes:
                nuevo_premio = Premio(
                    id=id_premio,
                    nombre_premio=nombre_premio,
                    categoria=categoria,
                    anio=anio,
                    serie=serie_obj
                )
                session.add(nuevo_premio)
                premios_existentes.add((nombre_premio, categoria, anio, serie_id))
                print(f"Agregando premio: {nombre_premio} ({categoria}) para la serie '{titulo_serie}'")
            else:
                print(f"El premio ya existe: {nombre_premio} en '{titulo_serie}'")

        session.commit()
        print("Carga de premios completada con éxito.")
except Exception as e:
    session.rollback()
    print(f"Error al cargar premios: {e}")
finally:
    session.close()
