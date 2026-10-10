ARCHIVO = "inscriptos.txt"


def crear_archivo():
    """Crea el archivo vacío si todavía no existe (no borra nada si ya existe)."""
    archivo = open(ARCHIVO, "a", encoding="utf-8")
    archivo.close()


def leer_inscriptos():
    """Lee el archivo y devuelve una lista de [nombre, categoria]."""
    inscriptos = []
    archivo = open(ARCHIVO, "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea != "":
            partes = linea.split(";")
            inscriptos.append([partes[0], partes[1]])
    archivo.close()
    return inscriptos


def guardar_inscriptos(inscriptos):
    """Escribe toda la lista en el archivo (reemplaza lo anterior)."""
    archivo = open(ARCHIVO, "w", encoding="utf-8")
    for jugador in inscriptos:
        archivo.write(jugador[0] + ";" + jugador[1] + "\n")
    archivo.close()


def agregar_inscripto():
    """ALTA: agrega un jugador nuevo al final del archivo."""
    nombre = input("Nombre del jugador: ").strip()
    categoria = input("Categoría: ").strip()

    if nombre == "" or categoria == "":
        print("El nombre y la categoría no pueden estar vacíos.")
        return

    archivo = open(ARCHIVO, "a", encoding="utf-8")
    archivo.write(nombre + ";" + categoria + "\n")
    archivo.close()
    print("Jugador inscripto correctamente.")


def mostrar_lista():
    """Muestra todos los inscriptos que hay en el archivo."""
    inscriptos = leer_inscriptos()

    if len(inscriptos) == 0:
        print("Todavía no hay jugadores inscriptos.")
        return

    print("\n--- LISTA DE INSCRIPTOS ---")
    numero = 1
    for jugador in inscriptos:
        print(str(numero) + ". " + jugador[0] + " - Categoría: " + jugador[1])
        numero = numero + 1
    print("Total:", len(inscriptos))


def buscar_jugador():
    """Busca un jugador por nombre y dice en qué categoría juega."""
    nombre = input("Nombre a buscar: ").strip().lower()
    inscriptos = leer_inscriptos()

    encontrado = False
    for jugador in inscriptos:
        if jugador[0].lower() == nombre:
            print(jugador[0] + " está inscripto en la categoría " + jugador[1])
            encontrado = True

    if not encontrado:
        print("Ese jugador NO está inscripto.")


def eliminar_jugador():
    """BAJA: saca a un jugador de la lista (por ejemplo, si se lesionó)."""
    nombre = input("Nombre del jugador a eliminar: ").strip().lower()
    inscriptos = leer_inscriptos()

    nueva_lista = []
    eliminado = False
    for jugador in inscriptos:
        if jugador[0].lower() == nombre:
            eliminado = True
        else:
            nueva_lista.append(jugador)

    if eliminado:
        guardar_inscriptos(nueva_lista)
        print("Jugador eliminado de la lista.")
    else:
        print("Ese jugador no está en la lista.")


def modificar_categoria():
    """MODIFICACIÓN: cambia la categoría de un jugador."""
    nombre = input("Nombre del jugador: ").strip().lower()
    inscriptos = leer_inscriptos()

    modificado = False
    for jugador in inscriptos:
        if jugador[0].lower() == nombre:
            nueva = input("Nueva categoría: ").strip()
            if nueva != "":
                jugador[1] = nueva
                modificado = True

    if modificado:
        guardar_inscriptos(inscriptos)
        print("Categoría modificada.")
    else:
        print("No se modificó nada.")


def menu():
    crear_archivo()
    opcion = ""
    while opcion != "6":
        print("\n===== TORNEO =====")
        print("1. Agregar inscripto")
        print("2. Ver lista completa")
        print("3. Buscar jugador")
        print("4. Eliminar jugador")
        print("5. Modificar categoría")
        print("6. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            agregar_inscripto()
        elif opcion == "2":
            mostrar_lista()
        elif opcion == "3":
            buscar_jugador()
        elif opcion == "4":
            eliminar_jugador()
        elif opcion == "5":
            modificar_categoria()
        elif opcion == "6":
            print("Hasta luego, los datos quedaron guardados.")
        else:
            print("Opción inválida.")


menu()