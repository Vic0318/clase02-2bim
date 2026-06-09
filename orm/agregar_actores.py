import csv
import os
from sqlalchemy.orm import sessionmaker
from modelo import engine, Actor, Serie, Pais

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 2. Obtener la ruta del archivo CSV
dir_actual = os.path.dirname(__file__)
ruta_csv = os.path.abspath(os.path.join(dir_actual, "..", "data", "actores.csv"))

try:
    # Cargar países, series y actores existentes en memoria (Idioma Python)
    paises = {p.nombre: p for p in session.query(Pais).all()}
    series = {s.titulo: s for s in session.query(Serie).all()}
    # Clave compuesta (nombre, serie_id) para verificar existentes en memoria
    actores_existentes = {(a.nombre, a.serie_id) for a in session.query(Actor).all()}

    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_actor = int(fila["id"])
            nombre = fila["nombre"]
            edad = int(fila["edad"]) if fila["edad"] else None
            nombre_pais = fila["pais"]
            titulo_serie = fila["serie"]

            # Buscar el país correspondiente en memoria
            pais_obj = paises.get(nombre_pais)
            if not pais_obj and nombre_pais:
                print(f"Advertencia: No se encontró el país '{nombre_pais}' en memoria.")

            # Buscar la serie correspondiente en memoria
            serie_obj = series.get(titulo_serie)
            if not serie_obj and titulo_serie:
                print(f"Advertencia: No se encontró la serie '{titulo_serie}' en memoria.")
            serie_id = serie_obj.id if serie_obj else None

            # Verificar si ya existe el actor en memoria para evitar duplicados
            if (nombre, serie_id) not in actores_existentes:
                nuevo_actor = Actor(
                    id=id_actor,
                    nombre=nombre,
                    edad=edad,
                    pais=pais_obj,
                    serie=serie_obj
                    # 'rol' queda como None (NULL) ya que no está en el CSV
                )
                session.add(nuevo_actor)
                actores_existentes.add((nombre, serie_id))
                print(f"Agregando actor: {nombre} (Serie: {titulo_serie})")
            else:
                print(f"El actor ya existe: {nombre} en la serie '{titulo_serie}'")

        session.commit()
        print("Carga de actores completada con éxito.")
except Exception as e:
    session.rollback()
    print(f"Error al cargar actores: {e}")
finally:
    session.close()
