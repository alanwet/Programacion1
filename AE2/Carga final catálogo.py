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
