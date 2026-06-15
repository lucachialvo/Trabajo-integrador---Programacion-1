"""Lógica de cada opción del menú de países."""

from utils import (
    leer_dataset, guardar_dataset, validar_entero, strip_accents,
    normalize_text, normalize_continent, validar_formato_nombre,
    filtrar_paises, imprimir_paises
)


def agregar_pais():
    """Solicita los datos de un país desde input y lo agrega al dataset."""
    paises = leer_dataset()

    while True:
        try:
            nombre_raw = input("Nombre: ")
            if nombre_raw is None:
                raise ValueError("El nombre es obligatorio.")
            nombre = normalize_text(nombre_raw)
            if not nombre:
                raise ValueError("El nombre es obligatorio.")
            if not validar_formato_nombre(nombre):
                raise ValueError("Formato de nombre inválido después de normalizar.")
            if any(strip_accents(existente["nombre"].strip()).lower() == strip_accents(nombre.strip()).lower() for existente in paises):
                print(f"El país '{nombre}' ya existe en el dataset. Ingrese otro nombre.")
                continue
            break
        except ValueError as error:
            print(f"Error: {error}")

    try:
        poblacion = validar_entero(input("Población: "), "Población")
        superficie = validar_entero(input("Superficie: "), "Superficie")
        continente_raw = input("Continente: ")
        if continente_raw is None:
            raise ValueError("El continente es obligatorio.")
        continente = normalize_text(continente_raw)
        if not continente:
            raise ValueError("El continente es obligatorio.")

        continente = normalize_continent(continente)

        if not validar_formato_nombre(continente):
            raise ValueError("Formato de continente inválido después de normalizar.")
    except ValueError as error:
        print(f"Error: {error}")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    guardar_dataset(paises)
    print(f"País '{nombre}' agregado correctamente.")


def actualizar_pais():
    """Busca un país por nombre y actualiza su población y superficie."""
    paises = leer_dataset()

    nombre_raw = input("Nombre del país a actualizar: ").strip()
    if not nombre_raw:
        print("Error: el nombre no puede estar vacío.")
        return

    nombre_normalizado = normalize_text(nombre_raw)

    pais_encontrado = None
    for pais in paises:
        if strip_accents(pais["nombre"].strip()).lower() == strip_accents(nombre_normalizado.strip()).lower():
            pais_encontrado = pais
            break

    if pais_encontrado is None:
        print(f"No se encontró ningún país con el nombre '{nombre_raw}'.")
        return

    print(f"País encontrado: {pais_encontrado['nombre']}")
    print(f"Población actual: {pais_encontrado['poblacion']}")
    print(f"Superficie actual: {pais_encontrado['superficie']}")

    try:
        poblacion = validar_entero(input("Nueva población: "), "Población")
        superficie = validar_entero(input("Nueva superficie: "), "Superficie")
    except ValueError as error:
        print(f"Error: {error}")
        return

    pais_encontrado["poblacion"] = poblacion
    pais_encontrado["superficie"] = superficie

    guardar_dataset(paises)
    print(f"Datos del país '{pais_encontrado['nombre']}' actualizados correctamente.")


def buscar_paises(paises):
    """Busca países por nombre (coincidencia parcial o exacta)."""
    termino = input("Ingrese el nombre a buscar: ").strip()
    if not termino:
        print("Debe ingresar un término de búsqueda.")
        return

    termino_normalizado = strip_accents(termino.lower())
    resultados = [
        pais for pais in paises
        if strip_accents(pais["nombre"].lower()) == termino_normalizado
        or termino_normalizado in strip_accents(pais["nombre"].lower())
    ]

    if resultados:
        imprimir_paises(resultados)
    else:
        print(f"No se encontraron países que coincidan con '{termino}'.")


def filtrar_por_continente(paises):
    """Filtra países por continente."""
    continente_raw = input("Continente: ").strip()
    if not continente_raw:
        print("El continente no puede estar vacío.")
        return
    continente = normalize_text(continente_raw)
    continente = normalize_continent(continente)
    if not validar_formato_nombre(continente):
        print("Formato de continente inválido.")
        return
    resultados = filtrar_paises(paises, continente=continente)
    if resultados:
        print(f"Países en {continente}:")
        imprimir_paises(resultados)
    else:
        print(f"No se encontraron países en {continente}.")


def filtrar_por_poblacion(paises):
    """Filtra países por rango de población."""
    print("Rango de población (ingrese valores enteros, deje vacío para omitir):")
    poblacion_min = None
    poblacion_max = None
    try:
        min_raw = input("  Mínimo: ").strip()
        if min_raw:
            poblacion_min = validar_entero(min_raw, "Población mínima")
        max_raw = input("  Máximo: ").strip()
        if max_raw:
            poblacion_max = validar_entero(max_raw, "Población máxima")
        if poblacion_min is not None and poblacion_max is not None and poblacion_min > poblacion_max:
            print("El valor mínimo no puede ser mayor que el máximo.")
            return
    except ValueError as error:
        print(f"Error: {error}")
        return
    resultados = filtrar_paises(paises, poblacion_min=poblacion_min, poblacion_max=poblacion_max)
    if resultados:
        print(f"Países con población entre {poblacion_min or 0} y {poblacion_max or 'inf'}:")
        imprimir_paises(resultados)
    else:
        print("No se encontraron países en ese rango de población.")


def filtrar_por_superficie(paises):
    """Filtra países por rango de superficie."""
    print("Rango de superficie (ingrese valores enteros, deje vacío para omitir):")
    superficie_min = None
    superficie_max = None
    try:
        min_raw = input("  Mínimo: ").strip()
        if min_raw:
            superficie_min = validar_entero(min_raw, "Superficie mínima")
        max_raw = input("  Máximo: ").strip()
        if max_raw:
            superficie_max = validar_entero(max_raw, "Superficie máxima")
        if superficie_min is not None and superficie_max is not None and superficie_min > superficie_max:
            print("El valor mínimo no puede ser mayor que el máximo.")
            return
    except ValueError as error:
        print(f"Error: {error}")
        return
    resultados = filtrar_paises(paises, superficie_min=superficie_min, superficie_max=superficie_max)
    if resultados:
        print(f"Países con superficie entre {superficie_min or 0} y {superficie_max or 'inf'}:")
        imprimir_paises(resultados)
    else:
        print("No se encontraron países en ese rango de superficie.")
