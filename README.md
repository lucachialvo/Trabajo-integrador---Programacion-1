# Sistema de Gestión de Países

## Descripción

Este proyecto fue desarrollado como Trabajo Integrador Final de Programación 1 utilizando Python. La aplicación permite gestionar información de distintos países a partir de un archivo CSV, aplicando conceptos fundamentales de programación como listas, diccionarios, funciones, estructuras de control, ordenamientos y estadísticas.

El sistema funciona mediante un menú interactivo en consola que permite realizar operaciones de consulta, modificación y análisis sobre un conjunto de datos de países.

---

## Objetivos

* Implementar estructuras de datos utilizando listas y diccionarios.
* Modularizar el código mediante funciones con responsabilidades específicas.
* Leer y procesar información desde archivos CSV.
* Aplicar técnicas de búsqueda, filtrado y ordenamiento.
* Generar estadísticas básicas a partir de los datos almacenados.
* Validar entradas y manejar errores comunes de ejecución.

---

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

---

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

---

## Validaciones implementadas

* Control de campos vacíos.
* Verificación de tipos numéricos.
* Manejo de errores durante la lectura del CSV.
* Control de búsquedas sin resultados.
* Validación de filtros ingresados por el usuario.
* Mensajes informativos de éxito y error.

---

## Tecnologías utilizadas

* Python 3.x
* Archivos CSV
* Listas
* Diccionarios
* Funciones
* Estructuras condicionales
* Estructuras repetitivas

---

## Estructura general del programa

1. Carga de datos desde archivo CSV.
2. Presentación del menú principal.
3. Selección de operaciones por parte del usuario.
4. Procesamiento de información.
5. Visualización de resultados.
6. Actualización de datos cuando corresponde.

---

## Integrantes

* Nombre Apellido
* Nombre Apellido

---

## Materia

**Programación 1**

Trabajo Integrador Final.
