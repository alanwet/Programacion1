
jugadores = []
categorias = []
parejas = []


cantidad = int(input("Cuantos jugadores van a participar? "))

while cantidad <= 0 or cantidad % 2 != 0:
    print("Debe ingresar una cantidad positiva y par de jugadores.")
    cantidad = int(input("Cuantos jugadores van a participar? "))


for i in range(cantidad):
    print("\nJugador", i + 1)

    nombre = input("Ingrese el nombre: ")
    categoria = input("Ingrese la categoria (4ta, 5ta, 6ta,8va,suma11): ")

    jugadores.append(nombre)
    categorias.append(categoria)

print("\n--- JUGADORES INSCRIPTOS ---")


for i in range(len(jugadores)):
    print(i + 1, "-", jugadores[i], "- Categoria:", categorias[i])


disponibles = list(range(len(jugadores)))


while len(disponibles) > 0:
    print("\n--- ARMADO DE PAREJAS ---")

    nombre_pareja = input("Ingrese el nombre de la pareja: ")

    print("Jugadores disponibles:")

    for i in disponibles:
        print(i + 1, "-", jugadores[i], "- Categoria:", categorias[i])

    
    num1 = int(input("Elija el numero del primer jugador: "))

    while num1 - 1 not in disponibles:
        print("Ese jugador no esta disponible.")
        num1 = int(input("Elija otro jugador: "))

    disponibles.remove(num1 - 1)

    
    num2 = int(input("Elija el numero del segundo jugador: "))

    while num2 - 1 not in disponibles:
        print("Ese jugador no esta disponible.")
        num2 = int(input("Elija otro jugador: "))

    disponibles.remove(num2 - 1)

   
    parejas.append([
        nombre_pareja,
        jugadores[num1 - 1],
        jugadores[num2 - 1]
    ])


print("\n--- PAREJAS DEL TORNEO ---")

for i in range(len(parejas)):
    print(
        parejas[i][0], ":",
        parejas[i][1], "y", parejas[i][2]
    )

print("\nInscripcion finalizada correctamente.")
