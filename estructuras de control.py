def contar_palabras(parrafo):
    """Cuenta las palabras de un párrafo. Se detiene en el primer punto."""
    cantidad = 0
    en_palabra = False  # indica si estoy "dentro" de una palabra

    for letra in parrafo:
        if letra == ".":
            break  # el párrafo termina con punto, no sigo leyendo

        if letra.isalpha() or letra.isdigit():
            if not en_palabra:
                cantidad = cantidad + 1  # empieza una palabra nueva
                en_palabra = True
        else:
            en_palabra = False  # espacio, coma, punto y coma, etc.

    return cantidad


texto = input("Ingresá el párrafo (terminado con punto): ")
print("Cantidad de palabras:", contar_palabras(texto))