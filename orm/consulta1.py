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
        # Extraer las edades válidas (no nulas) de los actores de la serie
        edades = [actor.edad for actor in s.actores if actor.edad is not None]
        
        if edades:
            promedio = sum(edades) / len(edades)
            print(f"Serie: {s.titulo:<35} | Promedio de Edad: {promedio:.2f} años")
        else:
            print(f"Serie: {s.titulo:<35} | Promedio de Edad: N/A (Sin actores con edad registrada)")
            
    print("==================================================")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
finally:
    session.close()
