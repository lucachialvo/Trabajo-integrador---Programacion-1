# Sistema de Gestión de Países

## Integrantes

* **Luca** — Creación del repositorio e implementación de estructura básica. Encargado de las funcionalidades de agregar país, ordenar países y mostrar estadísticas.
* **Ignacio** — Encargado de las funcionalidades de actualizar país, buscar país por nombre y filtrar países. Actualización del README.md y reorganización del código en tres archivos .py.


## Descripción

Este proyecto fue desarrollado como Trabajo Integrador Final de Programación 1 utilizando Python. La aplicación permite gestionar información de distintos países a partir de un archivo CSV, aplicando conceptos fundamentales de programación como listas, diccionarios, funciones, estructuras de control, ordenamientos y estadísticas.

El sistema funciona mediante un menú interactivo en consola que permite realizar operaciones de consulta, modificación y análisis sobre un conjunto de datos de países.

Link al video explicativo: https://youtu.be/wcThJTcLZ7I


## Materia

**Programación 1**

Trabajo Integrador Final.

## Objetivos

* Implementar estructuras de datos utilizando listas y diccionarios.
* Modularizar el código mediante funciones con responsabilidades específicas.
* Leer y procesar información desde archivos CSV.
* Aplicar técnicas de búsqueda, filtrado y ordenamiento.
* Generar estadísticas básicas a partir de los datos almacenados.
* Validar entradas y manejar errores comunes de ejecución.


## Estructura general del programa

1. Carga de datos desde archivo CSV.
2. Presentación del menú principal.
3. Selección de operaciones por parte del usuario.
4. Procesamiento de información.
5. Visualización de resultados.
6. Actualización de datos cuando corresponde.


## Datos gestionados

Cada país contiene la siguiente información:

| Campo            | Tipo    |
| ---------------- | ------- |
| Nombre           | String  |
| Población        | Integer |
| Superficie (km²) | Integer |
| Continente       | String  |

### Ejemplo de registro

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
Brasil,213993437,8515767,América
Alemania,83149300,357022,Europa
```


## Funcionalidades

### Gestión de países

* Agregar nuevos países.
* Actualizar población y superficie de un país existente.
* Buscar países por nombre (coincidencia exacta o parcial).

### Filtros

* Filtrar por continente.
* Filtrar por rango de población.
* Filtrar por rango de superficie.

### Ordenamientos

* Ordenar por nombre.
* Ordenar por población.
* Ordenar por superficie.
* Orden ascendente y descendente.

### Estadísticas

* País con mayor población.
* País con menor población.
* Promedio de población.
* Promedio de superficie.
* Cantidad de países por continente.


## Arquitectura del código

El programa está modularizado en tres archivos Python:

| Archivo | Responsabilidad |
|---------|-----------------|
| `main.py` | Punto de entrada. Contiene el bucle principal y el menú interactivo. |
| `operaciones.py` | Lógica de negocio. Implementa las operaciones del menú (agregar, actualizar, buscar, filtrar). |
| `utils.py` | Utilidades y funciones auxiliares. Lectura/escritura de CSV, validaciones, normalización, ordenamiento, filtrado e impresión. |

### Diagrama de dependencias

```
main.py
  ├── utils.py (leer_dataset, ordenar_paises, imprimir_paises, mostrar_estadisticas)
  └── operaciones.py
        └── utils.py (leer_dataset, guardar_dataset, validar_entero, strip_accents, normalize_text, normalize_continent, validar_formato_nombre, filtrar_paises, imprimir_paises)
```

---

## Flujo de ejecución

```
main()
│
├── leer_dataset()          → Carga países desde dataset.csv
│
└── Bucle while True
    │
    ├── mostrar_menu()      → Imprime opciones del menú
    │
    ├── input()             → Lee opción del usuario
    │
    └── Selección por opción (0-13)
        │
        ├── Opción 1: agregar_pais()
        │   └── operations.py → utils.py (validación, guardar_dataset)
        │
        ├── Opción 2: actualizar_pais()
        │
        ├── Opción 3: buscar_paises()
        │
        ├── Opción 4: filtrar_por_continente()
        │
        ├── Opción 5: filtrar_por_poblacion()
        │
        ├── Opción 6: filtrar_por_superficie()
        │
        ├── Opciones 7-12: ordenar_paises() + imprimir_paises()
        │
        ├── Opción 13: mostrar_estadisticas()
        │
        └── Opción 0: Salir
```

---

## Estructura del dataset (CSV)

El archivo `dataset.csv` contiene una fila por país con los campos:

```csv
nombre,poblacion,superficie,continente
```

Cada registro se representa internamente como un diccionario:

```python
{
    "nombre": "Argentina",
    "poblacion": 45376763,
    "superficie": 2780400,
    "continente": "América"
}
```


## Ejemplos de uso

### Menú principal

```python
"""
Menú de opciones:
  1. Agregar país
  2. Actualizar país
  3. Buscar país por nombre
  4. Filtrar por continente
  5. Filtrar por rango de población
  6. Filtrar por rango de superficie
  7. Ordenar por nombre ascendente
  8. Ordenar por nombre descendente
  9. Ordenar por población ascendente
 10. Ordenar por población descendente
 11. Ordenar por superficie ascendente
 12. Ordenar por superficie descendente
 13. Mostrar estadísticas
  0. Salir
"""
```

### Agregar un país

```python
# En operaciones.py → agregar_pais()
paises = leer_dataset()

# Validación del nombre (normalización + formato)
nombre = normalize_text(nombre_raw)           # "argentina" → "Argentina"
if not validar_formato_nombre(nombre):        # Verifica "Argentina" tiene mayúscula inicial
    raise ValueError("Formato de nombre inválido")

# Validación de continente (normalización con tildes)
continente = normalize_continent(continente)  # "america" → "América"

# Estructura del nuevo país
paises.append({
    "nombre": nombre,
    "poblacion": poblacion,
    "superficie": superficie,
    "continente": continente,
})

guardar_dataset(paises)
```

### Buscar países

```python
# En operaciones.py → buscar_paises()
termino_normalizado = strip_accents(termino.lower())

resultados = [
    pais for pais in paises
    if strip_accents(pais["nombre"].lower()) == termino_normalizado
    or termino_normalizado in strip_accents(pais["nombre"].lower())
]
# Coincide con "argentina", "Argentina", "ARGENTINA", etc.
```

### Filtrar por rango de población

```python
# En operaciones.py → filtrar_por_poblacion()
poblacion_min = validar_entero(min_raw, "Población mínima")
poblacion_max = validar_entero(max_raw, "Población máxima")

resultados = filtrar_paises(
    paises,
    poblacion_min=poblacion_min,
    poblacion_max=poblacion_max
)
```

### Ordenar países

```python
# En utils.py → ordenar_paises()
def ordenar_paises(paises, criterio, descendente=False):
    keys = {
        "nombre": get_nombre_key,      # pais["nombre"].lower()
        "poblacion": get_poblacion_key, # pais["poblacion"]
        "superficie": get_superficie_key # pais["superficie"]
    }
    return sorted(paises, key=keys[criterio], reverse=descendente)

# Uso:
ordenar_paises(paises, "poblacion", descendente=True)  # Mayor a menor
ordenar_paises(paises, "nombre", descendente=False)    # A a Z
```

### Mostrar estadísticas

```python
# En utils.py → mostrar_estadisticas()
mayor_poblacion = max(paises, key=get_poblacion_key)
menor_poblacion = min(paises, key=get_poblacion_key)
promedio_poblacion = sum(get_poblacion_key(p) for p in paises) / len(paises)
promedio_superficie = sum(get_superficie_key(p) for p in paises) / len(paises)
```

### Impresión tabular

```python
# En utils.py → imprimir_paises()
print(f"{'Nombre':<25} {'Población':>12} {'Superficie':>12} {'Continente':>15}")
print("-" * 70)
for pais in paises:
    print(f"{pais['nombre']:<25} {pais['poblacion']:>12} {pais['superficie']:>12} {pais['continente']:>15}")
```

**Resultado:**
```
Nombre                     Población   Superficie      Continente
----------------------------------------------------------------------
Argentina                45376763      2780400         América
Japón                  125800000       377975            Asia
Brasil                 213993437      8515767         América
```

---

## Validaciones implementadas

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `validar_entero()` | Verifica que el valor sea numérico entero | `"abc"` → Error |
| `strip_accents()` | Elimina acentos para comparaciones insensibles | `"México"` → `"Mexico"` |
| `normalize_text()` | Convierte a Title Case | `"argentina"` → `"Argentina"` |
| `normalize_continent()` | Normaliza nombres de continentes con tildes | `"america"` → `"América"` |
| `validar_formato_nombre()` | Verifica formato "Título" con mayúscula inicial | `"argentina"` → False |

### Ejemplo de validación de nombre

```python
# normalize_text() → Title Case
normalize_text("argentina")           # "Argentina"
normalize_text("paises bajos")        # "Países Bajos"
normalize_text(" republica CHENA ")  # "Republica Chena"

# validar_formato_nombre() → Verifica formato
validar_formato_nombre("Argentina")   # True
validar_formato_nombre("ARGENTINA")   # False (debe ser Title Case)
validar_formato_nombre("Argentina2")  # False (caracteres inválidos)
```

### Ejemplo de validación de continente

```python
normalize_continent("america")       # "América"
normalize_continent("AMERICA")       # "América"
normalize_continent("america del sur") # "América"
normalize_continent("europa")        # "Europa"
normalize_continent("asia")          # "Asia"
```

---

## Tecnologías utilizadas

* Python 3.x
* Archivos CSV
* Listas
* Diccionarios
* Funciones
* Estructuras condicionales
* Estructuras repetitivas
