import csv
import re
import unicodedata

DATASET_FILE = "dataset.csv"


def leer_dataset(archivo=DATASET_FILE):
    """Carga el dataset de países desde un archivo CSV."""
    paises = []
    try:
        with open(archivo, encoding="utf-8", newline="") as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                paises.append({
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip(),
                })
    except FileNotFoundError:
        print(f"Advertencia: no se encontró {archivo}. Se devolverá una lista vacía.")
    return paises


def guardar_dataset(paises, archivo=DATASET_FILE):
    """Guarda el dataset de países en un archivo CSV."""
    with open(archivo, mode="w", encoding="utf-8", newline="") as csvfile:
        campos = ["nombre", "poblacion", "superficie", "continente"]
        escritor = csv.DictWriter(csvfile, fieldnames=campos)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow({
                "nombre": pais["nombre"],
                "poblacion": pais["poblacion"],
                "superficie": pais["superficie"],
                "continente": pais["continente"],
            })


def validar_entero(valor, nombre_campo):
    """Convierte un valor a entero o lanza ValueError con mensaje claro."""
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{nombre_campo} no puede quedar vacío.")
    if not valor.isdigit():
        raise ValueError(f"{nombre_campo} debe ser un número entero válido.")
    return int(valor)


def normalize_text(text):
    """Normaliza un texto a Title Case por token, preservando guiones y apóstrofes.

    Ejemplo: "argentina" -> "Argentina", "países bajos" -> "Países Bajos"
    """
    text = text.strip()
    if not text:
        return text
    parts = re.split("([ -'])", text)
    normalized_parts = []
    for part in parts:
        if part in " -'":
            normalized_parts.append(part)
        else:
            # capitalize preserves unicode correctly when using lower()/upper()
            normalized_parts.append(part[0].upper() + part[1:].lower() if len(part) > 0 else part)
    return "".join(normalized_parts)


def validar_formato_nombre(nombre):
    """Valida que el nombre contenga sólo letras (Unicode), espacios, guiones o apóstrofes
    y que cada token empiece con mayúscula seguido de minúsculas.
    """
    if not nombre:
        return False
    # Permitir letras unicode, espacios, guiones y apóstrofes
    for ch in nombre:
        if not (ch.isalpha() or ch in " -'"):
            return False

    tokens = re.split("[ -']", nombre)
    for t in tokens:
        if not t:
            continue
        if not t[0].isupper():
            return False
        if len(t) > 1 and not t[1:].islower():
            return False
    return True


def validar_formato_continente(continente):
    """Validación específica para continentes: reutiliza validar_formato_nombre."""
    return validar_formato_nombre(continente)


def strip_accents(text):
    """Elimina acentos/tildes de un texto para comparaciones insensibles a diacríticos."""
    if not text:
        return text
    nfkd = unicodedata.normalize('NFD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


def normalize_continent(continente):
    """Normaliza variantes de nombre de continente a la forma canónica con tildes.

    Maneja entradas como 'america', 'AMERICA', 'america del sur', etc. devolviendo 'América'.
    """
    clave = strip_accents(continente).lower()
    # Mapear por presencia de palabras clave
    if 'america' in clave:
        return 'América'
    if 'africa' in clave:
        return 'África'
    if 'oceania' in clave or 'ocean' in clave:
        return 'Oceanía'
    if 'europa' in clave:
        return 'Europa'
    if 'asia' in clave:
        return 'Asia'
    if 'antart' in clave:
        return 'Antártida'
    # Si no se reconoce, devolver la versión normalizada tal cual
    return continente


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

        # Normalizar continente a forma canónica (con tildes cuando corresponda)
        continente = normalize_continent(continente)

        if not validar_formato_continente(continente):
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


def ordenar_paises(paises, criterio, descendente=False):
    """Devuelve una lista de países ordenados por el criterio especificado."""
    if criterio not in {"nombre", "poblacion", "superficie"}:
        raise ValueError("Criterio de orden no válido.")
    if criterio == "nombre":
        return sorted(paises, key=get_nombre_key, reverse=descendente)
    if criterio == "poblacion":
        return sorted(paises, key=get_poblacion_key, reverse=descendente)
    return sorted(paises, key=get_superficie_key, reverse=descendente)


def get_nombre_key(pais):
    return pais["nombre"].lower()


def get_poblacion_key(pais):
    return pais["poblacion"]


def get_superficie_key(pais):
    return pais["superficie"]


def ordenar_por_nombre(paises, descendente=False):
    return ordenar_paises(paises, "nombre", descendente)


def ordenar_por_poblacion(paises, descendente=False):
    return ordenar_paises(paises, "poblacion", descendente)


def ordenar_por_superficie(paises, descendente=False):
    return ordenar_paises(paises, "superficie", descendente)


def mostrar_estadisticas(paises):
    """Muestra estadísticas del dataset de países."""
    if not paises:
        print("No hay datos de países para mostrar estadísticas.")
        return

    mayor_poblacion = max(paises, key=get_poblacion_key)
    menor_poblacion = min(paises, key=get_poblacion_key)
    promedio_poblacion = sum(get_poblacion_key(p) for p in paises) / len(paises)
    promedio_superficie = sum(get_superficie_key(p) for p in paises) / len(paises)

    print("Estadísticas del dataset de países:")
    print(f"- País con mayor población: {mayor_poblacion['nombre']} ({mayor_poblacion['poblacion']})")
    print(f"- País con menor población: {menor_poblacion['nombre']} ({menor_poblacion['poblacion']})")
    print(f"- Promedio de población: {promedio_poblacion:.2f}")
    print(f"- Promedio de superficie: {promedio_superficie:.2f}")


def imprimir_paises(paises):
    """Imprime una lista de países en formato tabular simple."""
    if not paises:
        print("No hay países para mostrar.")
        return

    print(f"{'Nombre':<25} {'Población':>12} {'Superficie':>12} {'Continente':>15}")
    print("-" * 70)
    for pais in paises:
        print(f"{pais['nombre']:<25} {pais['poblacion']:>12} {pais['superficie']:>12} {pais['continente']:>15}")


def main():
    paises = leer_dataset()
    while True:
        print("""\nMenú de opciones:
1. Agregar país
2. Ordenar por nombre ascendente
3. Ordenar por nombre descendente
4. Ordenar por población ascendente
5. Ordenar por población descendente
6. Ordenar por superficie ascendente
7. Ordenar por superficie descendente
8. Mostrar estadísticas
0. Salir""")
        opcion = input("Seleccione una opción: ").strip()
        match opcion:
            case "1":
                agregar_pais()
                paises = leer_dataset()
            case "2":
                imprimir_paises(ordenar_por_nombre(paises, descendente=False))
            case "3":
                imprimir_paises(ordenar_por_nombre(paises, descendente=True))
            case "4":
                imprimir_paises(ordenar_por_poblacion(paises, descendente=False))
            case "5":
                imprimir_paises(ordenar_por_poblacion(paises, descendente=True))
            case "6":
                imprimir_paises(ordenar_por_superficie(paises, descendente=False))
            case "7":
                imprimir_paises(ordenar_por_superficie(paises, descendente=True))
            case "8":
                mostrar_estadisticas(paises)
            case "0":
                print("Saliendo...")
                break
            case _:
                print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
