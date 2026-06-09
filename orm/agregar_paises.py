import csv
import os
from sqlalchemy.orm import sessionmaker
from modelo import engine, Pais

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 2. Obtener la ruta del archivo CSV
dir_actual = os.path.dirname(__file__)
ruta_csv = os.path.abspath(os.path.join(dir_actual, "..", "data", "paises.csv"))

try:
    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_pais = int(fila["id"])
            nombre = fila["nombre"]
            continente = fila["continente"]

            # Verificar si ya existe para evitar duplicados en re-ejecuciones
            pais_existente = session.query(Pais).filter_by(nombre=nombre).first()
            if not pais_existente:
                nuevo_pais = Pais(id=id_pais, nombre=nombre, continente=continente)
                session.add(nuevo_pais)
                print(f"Agregando país: {nombre}")
            else:
                print(f"El país ya existe: {nombre}")

        session.commit()
        print("Carga de países completada con éxito.")
except Exception as e:
    session.rollback()
    print(f"Error al cargar países: {e}")
finally:
    session.close()
