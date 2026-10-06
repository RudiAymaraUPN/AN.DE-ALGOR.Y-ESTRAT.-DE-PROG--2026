# -*- coding: utf-8 -*-
# Comparacion de rapidez entre algoritmos (solo para la clase)
import random
import time

from .backtracking import combinaciones_posibles
from .formato import imprimir_tabla
from .interfaz import mensaje_info
from .ordenamiento import burbuja_descendente, quicksort
from .vuelto import calcular_vuelto

REPETICIONES = 3  # Se mide varias veces y se toma el mejor tiempo


def _medir_ms(funcion):
    # Tiempo en milisegundos de la mejor corrida
    mejor = None
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        funcion()
        tiempo = time.perf_counter() - inicio
        if mejor is None or tiempo < mejor:
            mejor = tiempo
    return mejor * 1000


def comparar_algoritmos(n_datos, n_productos):
    # Devuelve [(algoritmo, entrada, ms, complejidad)] ordenado del mas rapido al mas lento
    datos = [random.randint(1, 100000) for _ in range(n_datos)]
    productos = [{"nombre": "P" + str(i), "precio": float(i + 1), "stock": 1, "vendidos": 0}
                 for i in range(n_productos)]
    monto = sum(p["precio"] for p in productos) / 2

    resultados = [
        ("Quicksort", str(n_datos) + " datos",
         _medir_ms(lambda: quicksort(list(datos))), "O(n log n)"),
        ("Burbuja", str(n_datos) + " datos",
         _medir_ms(lambda: burbuja_descendente(list(datos))), "O(n^2)"),
        ("Backtracking", str(n_productos) + " productos",
         _medir_ms(lambda: combinaciones_posibles(productos, monto)), "O(2^n)"),
        ("Voraz (vuelto)", "S/ 1234.55",
         _medir_ms(lambda: calcular_vuelto(123455)), "O(k)"),
    ]
    resultados.sort(key=lambda r: r[2])
    return resultados


def mostrar_comparacion(n_datos, n_productos):
    mensaje_info("Midiendo (mejor de " + str(REPETICIONES) + " corridas por algoritmo)...")
    resultados = comparar_algoritmos(n_datos, n_productos)
    mas_rapido = resultados[0][2]

    filas = []
    estilos = []
    for puesto, (nombre, entrada, ms, complejidad) in enumerate(resultados, start=1):
        veces = "mas rapido" if puesto == 1 else "x{:.1f} mas lento".format(ms / max(mas_rapido, 1e-9))
        filas.append([str(puesto), nombre, entrada, "{:.3f} ms".format(ms), complejidad, veces])
        estilos.append(("verde", "negrita") if puesto == 1 else ())
    print()
    imprimir_tabla(["Puesto", "Algoritmo", "Entrada", "Tiempo", "Complejidad", "Comparacion"],
                   filas, alineaciones=["der", "izq", "izq", "der", "izq", "izq"],
                   estilos_filas=estilos)
