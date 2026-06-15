"""Funciones auxiliares del dataset de países."""


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


def strip_accents(text):
    """Elimina acentos/tildes de un texto para comparaciones insensibles a diacríticos."""
    if not text:
        return text
    nfkd = unicodedata.normalize('NFD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


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
            normalized_parts.append(part[0].upper() + part[1:].lower() if len(part) > 0 else part)
    return "".join(normalized_parts)


def validar_formato_nombre(nombre):
    """Valida que el nombre contenga sólo letras (Unicode), espacios, guiones o apóstrofes
    y que cada token empiece con mayúscula seguido de minúsculas.
    """
    if not nombre:
        return False
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


def normalize_continent(continente):
    """Normaliza variantes de nombre de continente a la forma canónica con tildes.

    Maneja entradas como 'america', 'AMERICA', 'america del sur', etc. devolviendo 'América'.
    """
    clave = strip_accents(continente).lower()
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
    return continente


def get_nombre_key(pais):
    """Key function para ordenamiento por nombre."""
    return pais["nombre"].lower()


def get_poblacion_key(pais):
    """Key function para ordenamiento por población."""
    return pais["poblacion"]


def get_superficie_key(pais):
    """Key function para ordenamiento por superficie."""
    return pais["superficie"]


def ordenar_paises(paises, criterio, descendente=False):
    """Devuelve una lista de países ordenados por el criterio especificado."""
    keys = {
        "nombre": get_nombre_key,
        "poblacion": get_poblacion_key,
        "superficie": get_superficie_key,
    }
    if criterio not in keys:
        raise ValueError("Criterio de orden no válido.")
    return sorted(paises, key=keys[criterio], reverse=descendente)


def filtrar_paises(paises, continente=None, poblacion_min=None, poblacion_max=None, superficie_min=None, superficie_max=None):
    """Devuelve países que cumplen TODOS los filtros activos."""
    resultado = paises
    if continente:
        resultado = [p for p in resultado if p["continente"] == continente]
    if poblacion_min is not None:
        resultado = [p for p in resultado if p["poblacion"] >= poblacion_min]
    if poblacion_max is not None:
        resultado = [p for p in resultado if p["poblacion"] <= poblacion_max]
    if superficie_min is not None:
        resultado = [p for p in resultado if p["superficie"] >= superficie_min]
    if superficie_max is not None:
        resultado = [p for p in resultado if p["superficie"] <= superficie_max]
    return resultado


def imprimir_paises(paises):
    """Imprime una lista de países en formato tabular simple."""
    if not paises:
        print("No hay países para mostrar.")
        return

    print(f"{'Nombre':<25} {'Población':>12} {'Superficie':>12} {'Continente':>15}")
    print("-" * 70)
    for pais in paises:
        print(f"{pais['nombre']:<25} {pais['poblacion']:>12} {pais['superficie']:>12} {pais['continente']:>15}")


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
