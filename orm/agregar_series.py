import csv
import os
from sqlalchemy.orm import sessionmaker
from modelo import engine, Serie, Plataforma, Pais

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 2. Obtener la ruta del archivo CSV
dir_actual = os.path.dirname(__file__)
ruta_csv = os.path.abspath(os.path.join(dir_actual, "..", "data", "series.csv"))

try:
    # Cargar países, plataformas y series existentes en memoria (Idioma Python)
    paises = {p.nombre: p for p in session.query(Pais).all()}
    plataformas = {p.nombre: p for p in session.query(Plataforma).all()}
    series_existentes = {s.titulo for s in session.query(Serie).all()}

    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_serie = int(fila["id"])
            titulo = fila["titulo"]
            genero = fila["genero"]
            anio_estreno = int(fila["anio_estreno"])
            temporadas = int(fila["temporadas"])
            nombre_plataforma = fila["plataforma"]
            nombre_pais = fila["pais"]

            # Buscar la plataforma correspondiente en memoria
            plataforma_obj = plataformas.get(nombre_plataforma)
            if not plataforma_obj and nombre_plataforma:
                print(f"Advertencia: No se encontró la plataforma '{nombre_plataforma}' en memoria.")

            # Buscar el país correspondiente en memoria
            pais_obj = paises.get(nombre_pais)
            if not pais_obj and nombre_pais:
                print(f"Advertencia: No se encontró el país '{nombre_pais}' en memoria.")

            # Verificar si ya existe la serie en memoria para evitar duplicados
            if titulo not in series_existentes:
                nueva_serie = Serie(
                    id=id_serie,
                    titulo=titulo,
                    genero=genero,
                    anio_estreno=anio_estreno,
                    temporadas=temporadas,
                    plataforma=plataforma_obj,
                    pais=pais_obj
                )
                session.add(nueva_serie)
                series_existentes.add(titulo)
                print(f"Agregando serie: {titulo} (Plataforma: {nombre_plataforma}, País: {nombre_pais})")
            else:
                print(f"La serie ya existe: {titulo}")

        session.commit()
        print("Carga de series completada con éxito.")
except Exception as e:
    session.rollback()
    print(f"Error al cargar series: {e}")
finally:
    session.close()

def __repr__(self):
    return f"Serie: {self.nombre}"

def obtener_edad_actores(self):
    edades = [e.edad for e in self.actores]
    if len(edades) > 0:
        suma = sum(edades)
        promedio = suma / len(edades)
        return promedio
    else:
        return 0

def obtener_premios_series(self):
    premios = [p.numero_premios for p in self.premios]
    if len(premios) > 0:
        suma = sum(premios)
        promedio = suma / len(premios)
        return promedio
    else:
        return 0