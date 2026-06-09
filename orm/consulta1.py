from sqlalchemy.orm import sessionmaker
from modelo import engine, Serie

# 1. Crear sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("==================================================")
    print("PROMEDIO DE EDADES DE ACTORES POR SERIE")
    print("==================================================")
    
    # Consultamos todas las series
    series = session.query(Serie).all()
    
    for s in series:
        promedio = s.obtener_edad_actores()
        if promedio > 0:
            print(f"Serie: {s.titulo:<35} | Promedio de Edad: {promedio:.2f} años")
        else:
            print(f"Serie: {s.titulo:<35} | Promedio de Edad: N/A (Sin actores con edad registrada)")
            
    print("==================================================")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
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
