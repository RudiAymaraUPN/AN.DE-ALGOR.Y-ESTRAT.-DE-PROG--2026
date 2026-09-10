# -*- coding: utf-8 -*-
"""
ordenamiento.py - Algoritmos de ordenamiento vistos en clase
(burbuja descendente y quicksort) y las funciones que los usan para
ordenar la lista de productos.
"""


def burbuja_descendente(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] < lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort(menores) + iguales + quicksort(mayores)


def acomodar(productos, valores, clave):
    """Reordena la lista de productos siguiendo el orden ya calculado
    en 'valores' para el campo 'clave' (precio o vendidos)."""
    ordenados = []
    copia = list(productos)
    for v in valores:
        for p in copia:
            if p[clave] == v:
                ordenados.append(p)
                copia.remove(p)
                break
    return ordenados


def ordenar_por_precio(productos, ascendente):
    precios = [p["precio"] for p in productos]
    if ascendente:
        precios = quicksort(precios)
    else:
        precios = burbuja_descendente(precios)
    return acomodar(productos, precios, "precio")


def ordenar_por_vendidos(productos):
    vendidos = burbuja_descendente([p["vendidos"] for p in productos])
    return acomodar(productos, vendidos, "vendidos")
