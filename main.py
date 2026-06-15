"""Módulo principal del gestor de países."""

from utils import (
    leer_dataset, ordenar_paises,
    imprimir_paises, mostrar_estadisticas
)
from operaciones import (
    agregar_pais, actualizar_pais, buscar_paises,
    filtrar_por_continente, filtrar_por_poblacion, filtrar_por_superficie
)


def mostrar_menu():
    """Imprime el menú de opciones."""
    print("""\nMenú de opciones:
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
  0. Salir""")


def main():
    """Bucle principal del programa."""
    paises = leer_dataset()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            agregar_pais()
            paises = leer_dataset()
        elif opcion == "2":
            actualizar_pais()
            paises = leer_dataset()
        elif opcion == "3":
            buscar_paises(paises)
        elif opcion == "4":
            filtrar_por_continente(paises)
        elif opcion == "5":
            filtrar_por_poblacion(paises)
        elif opcion == "6":
            filtrar_por_superficie(paises)
        elif opcion == "7":
            imprimir_paises(ordenar_paises(paises, "nombre", descendente=False))
        elif opcion == "8":
            imprimir_paises(ordenar_paises(paises, "nombre", descendente=True))
        elif opcion == "9":
            imprimir_paises(ordenar_paises(paises, "poblacion", descendente=False))
        elif opcion == "10":
            imprimir_paises(ordenar_paises(paises, "poblacion", descendente=True))
        elif opcion == "11":
            imprimir_paises(ordenar_paises(paises, "superficie", descendente=False))
        elif opcion == "12":
            imprimir_paises(ordenar_paises(paises, "superficie", descendente=True))
        elif opcion == "13":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
