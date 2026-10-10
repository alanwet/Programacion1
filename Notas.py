
alumnos = [
    {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
    {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
    {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
    {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85}
]

def esta_regular(alumno):
    promedio = sum(alumno["notas"]) / len(alumno["notas"])

    if promedio >= 6 and alumno["asistencia"] >= 75:
        return True
    else:
        return False


nombre = input("Ingrese el nombre del alumno: ")

encontrado = False

for alumno in alumnos:
    if alumno["nombre"].lower() == nombre.lower():
        encontrado = True

        if esta_regular(alumno):
            print(nombre, "esta regular")
        else:
            print(nombre, "no esta regular")

if encontrado == False:
    print("Alumno no encontrado")
