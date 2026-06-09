import csv
import os
from sqlalchemy.orm import sessionmaker
from modelo import engine, Plataforma, Pais

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 2. Obtener la ruta del archivo CSV
dir_actual = os.path.dirname(__file__)
ruta_csv = os.path.abspath(os.path.join(dir_actual, "..", "data", "plataformas.csv"))

try:
    # Cargar países y plataformas existentes en memoria (Idioma Python)
    paises = {p.nombre: p for p in session.query(Pais).all()}
    plataformas_existentes = {p.nombre for p in session.query(Plataforma).all()}

    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_plataforma = int(fila["id"])
            nombre = fila["nombre"]
            nombre_pais = fila["pais"]
            
            # Convertir suscriptores a entero (puede venir con decimal en el CSV)
            suscriptores_str = fila.get("suscriptores_millones")
            if suscriptores_str:
                suscriptores = int(round(float(suscriptores_str)))
            else:
                suscriptores = None

            # Buscar el país correspondiente en memoria
            pais_obj = paises.get(nombre_pais)
            if not pais_obj and nombre_pais:
                print(f"Advertencia: No se encontró el país '{nombre_pais}' en memoria.")

            # Verificar si ya existe la plataforma en memoria
            if nombre not in plataformas_existentes:
                nueva_plataforma = Plataforma(
                    id=id_plataforma,
                    nombre=nombre,
                    pais=pais_obj,
                    suscriptores_millones=suscriptores
                )
                session.add(nueva_plataforma)
                plataformas_existentes.add(nombre)
                print(f"Agregando plataforma: {nombre} (País: {nombre_pais})")
            else:
                print(f"La plataforma ya existe: {nombre}")

        session.commit()
        print("Carga de plataformas completada con éxito.")
except Exception as e:
    session.rollback()
    print(f"Error al cargar plataformas: {e}")
finally:
    session.close()
