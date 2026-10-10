# PROGRAMACIÓN I - Buffet: arrays paralelos (catálogo), matriz ventas[día][producto] y archivos.
import os
CANT_PRODUCTOS = 6
CANT_DIAS = 5
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

def leer_numero(mensaje):
    texto = input(mensaje)
    while not texto.isdigit():
        texto = input("Error, ingrese un número entero: ")
    return int(texto)
def buscar_producto(codigos, codigo):
    for i in range(CANT_PRODUCTOS):
        if codigos[i] == codigo:
            return i          # sale apenas lo encuentra
    return -1
def total_producto(ventas, p):
    total = 0
    for d in range(CANT_DIAS):
        total = total + ventas[d][p]
    return total
def recaudacion_dia(ventas, precios, d):
    total = 0
    for p in range(CANT_PRODUCTOS):
        total = total + ventas[d][p] * precios[p]
    return total

def guardar_datos(codigos, nombres, precios, ventas):
    archivo = open("productos.txt", "w", encoding="utf-8")
    for i in range(CANT_PRODUCTOS):
        archivo.write(str(codigos[i]) + ";" + nombres[i] + ";" + str(precios[i]) + "\n")
    archivo.close()
    archivo = open("ventas.txt", "w", encoding="utf-8")
    for d in range(CANT_DIAS):
        for p in range(CANT_PRODUCTOS):
            archivo.write(str(ventas[d][p]) + ";")
        archivo.write("\n")
    archivo.close()
def cargar_datos(codigos, nombres, precios, ventas):
    if not (os.path.exists("productos.txt") and os.path.exists("ventas.txt")):
        print("Primera vez: todavía no hay datos guardados.")
        return
    lineas = open("productos.txt", "r", encoding="utf-8").readlines()
    for i in range(CANT_PRODUCTOS):
        partes = lineas[i].strip().split(";")
        codigos[i] = int(partes[0])
        nombres[i] = partes[1]
        precios[i] = int(partes[2])
    lineas = open("ventas.txt", "r", encoding="utf-8").readlines()
    for d in range(CANT_DIAS):
        partes = lineas[d].strip().split(";")
        for p in range(CANT_PRODUCTOS):
            ventas[d][p] = int(partes[p])
def cargar_catalogo(codigos, nombres, precios, ventas):
    if 0 not in codigos:
        print("El catálogo ya está cargado.")
        return
    for i in range(CANT_PRODUCTOS):
        codigo = leer_numero("Código del producto " + str(i + 1) + ": ")
        while codigo == 0 or buscar_producto(codigos, codigo) != -1:
            codigo = leer_numero("Código inválido o repetido. Otro código: ")
        codigos[i] = codigo
        nombres[i] = input("Nombre: ").replace(";", ",")
        precios[i] = leer_numero("Precio: ")
    guardar_datos(codigos, nombres, precios, ventas)
def registrar_venta(codigos, nombres, precios, ventas):
    dia = leer_numero("Día (1 = lunes ... 5 = viernes): ")
    p = buscar_producto(codigos, leer_numero("Código del producto: "))
    cantidad = leer_numero("Cantidad: ")
    if dia < 1 or dia > CANT_DIAS or p == -1 or cantidad == 0:
        print("Error: día, código o cantidad inválidos.")
        return
    ventas[dia - 1][p] = ventas[dia - 1][p] + cantidad    # si ya había, se suma
    guardar_datos(codigos, nombres, precios, ventas)
def mostrar_informes(nombres, precios, ventas):
    maximo = 0
    for p in range(CANT_PRODUCTOS):
        if total_producto(ventas, p) > maximo:
            maximo = total_producto(ventas, p)
    if maximo == 0:
        print("Todavía no hay ventas cargadas.")
        return
    for p in range(CANT_PRODUCTOS):
        print(nombres[p], ":", total_producto(ventas, p), "unidades")
        if total_producto(ventas, p) == maximo:
            print("   ^ el más vendido")
        if total_producto(ventas, p) == 0:
            print("   ^ no se vendió")
    mejor = 0
    total = 0
    for d in range(CANT_DIAS):
        print(DIAS[d], ": $", recaudacion_dia(ventas, precios, d))
        total = total + recaudacion_dia(ventas, precios, d)
        if recaudacion_dia(ventas, precios, d) > recaudacion_dia(ventas, precios, mejor):
            mejor = d
    print("Mayor recaudación:", DIAS[mejor], "\nTotal de la semana: $", total)

def main():
    codigos = [0] * CANT_PRODUCTOS
    nombres = [""] * CANT_PRODUCTOS
    precios = [0] * CANT_PRODUCTOS
    ventas = []
    for d in range(CANT_DIAS):
        ventas.append([0] * CANT_PRODUCTOS)
    cargar_datos(codigos, nombres, precios, ventas)
    opcion = 0
    while opcion != 4:
        print("\n1. Cargar catálogo\n2. Registrar venta\n3. Ver informes\n4. Salir")
        opcion = leer_numero("Opción: ")
        if opcion == 1:
            cargar_catalogo(codigos, nombres, precios, ventas)
        elif opcion == 2:
            registrar_venta(codigos, nombres, precios, ventas)
        elif opcion == 3:
            mostrar_informes(nombres, precios, ventas)
        elif opcion != 4:
            print("Opción inválida.")

main()
