# -*- coding: utf-8 -*-
import json
import os


def registrar_producto(productos, nombre, precio, stock):
    nombre = nombre.strip()
    if buscar_producto(productos, nombre) is not None:
        return False, "Ya existe un producto con ese nombre."
    p = {"nombre": nombre, "precio": precio, "stock": stock, "vendidos": 0}
    productos.append(p)
    return True, "Producto registrado correctamente."


def buscar_producto(productos, nombre):
    nombre = nombre.strip().lower()
    for p in productos:
        if p["nombre"].lower() == nombre:
            return p
    return None


def distancia(a, b):
    filas = len(a) + 1
    columnas = len(b) + 1
    m = [[0] * columnas for _ in range(filas)]
    for i in range(filas):
        m[i][0] = i
    for j in range(columnas):
        m[0][j] = j
    for i in range(1, filas):
        for j in range(1, columnas):
            costo = 0 if a[i - 1] == b[j - 1] else 1
            m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1,
                          m[i - 1][j - 1] + costo)
    return m[filas - 1][columnas - 1]


def sugerir_producto(productos, nombre):
    if len(productos) == 0:
        return ""
    mejor = ""
    menor = 9999
    for p in productos:
        d = distancia(nombre.lower(), p["nombre"].lower())
        if d < menor:
            menor = d
            mejor = p["nombre"]
    return mejor


def mostrar_productos(productos):
    if len(productos) == 0:
        print("No hay productos registrados.")
        return
    print("N | Nombre | Precio | Stock | Vendidos")
    print("----------------------------------------")
    i = 1
    for p in productos:
        print(i, "|", p["nombre"], "| S/", p["precio"], "|",
              p["stock"], "|", p["vendidos"])
        i = i + 1


def producto_mas_vendido(productos):
    if len(productos) == 0:
        return None
    mejor = productos[0]
    for p in productos:
        if p["vendidos"] > mejor["vendidos"]:
            mejor = p
    return mejor


def cargar_productos(ruta):
    """
    Lee la lista de productos desde el archivo JSON de ejemplo (clave
    "productos"). Si el archivo no existe, esta corrupto, o algun
    producto tiene un formato invalido, ese o esos registros se ignoran
    y se informa por mensaje en vez de romper el programa.
    """
    productos = []

    if not os.path.exists(ruta):
        return productos, (
            "Aviso: no se encontro el archivo de datos (" + ruta +
            "). Se inicia sin productos."
        )

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError) as error:
        return productos, (
            "Aviso: no se pudo leer el archivo de datos (" + str(error) +
            "). Se inicia sin productos."
        )

    invalidos = 0
    for item in datos.get("productos", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("nombre"), str) and item["nombre"].strip() != ""
            and isinstance(item.get("precio"), (int, float)) and item["precio"] > 0
            and isinstance(item.get("stock"), (int, float)) and item["stock"] >= 0
        ):
            productos.append({
                "nombre": item["nombre"].strip(),
                "precio": float(item["precio"]),
                "stock": int(item["stock"]),
                "vendidos": int(item.get("vendidos", 0)),
            })
        else:
            invalidos += 1

    mensaje = "Se cargaron " + str(len(productos)) + " producto(s) de ejemplo."
    if invalidos > 0:
        mensaje += (" Se ignoraron " + str(invalidos) +
                    " producto(s) del JSON por formato invalido.")
    return productos, mensaje
