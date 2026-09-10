# -*- coding: utf-8 -*-
import json
import os

from .productos import buscar_producto


def registrar_venta(productos, nombre, cantidad):
    if cantidad <= 0:
        return None, "La cantidad debe ser mayor a 0."
    p = buscar_producto(productos, nombre)
    if p is None:
        return None, "El producto no existe."
    if cantidad > p["stock"]:
        return None, "No hay stock suficiente. Stock disponible: " + str(p["stock"])
    p["stock"] = p["stock"] - cantidad
    p["vendidos"] = p["vendidos"] + cantidad
    total = p["precio"] * cantidad
    detalle = {"nombre": p["nombre"], "cantidad": cantidad,
               "precio": p["precio"], "total": total}
    return detalle, "Venta registrada"


def aplicar_descuento(total, porcentaje):
    if porcentaje < 0:
        porcentaje = 0
    elif porcentaje > 100:
        porcentaje = 100
    descuento = total * porcentaje / 100
    return total - descuento, descuento


def generar_boleta(detalle, porcentaje):
    total_final, descuento = aplicar_descuento(detalle["total"], porcentaje)
    b = "==============================\n"
    b = b + "        BOLETA DE VENTA\n"
    b = b + "==============================\n"
    b = b + "Producto : " + detalle["nombre"] + "\n"
    b = b + "Cantidad : " + str(detalle["cantidad"]) + "\n"
    b = b + "Precio   : S/ " + str(detalle["precio"]) + "\n"
    b = b + "Subtotal : S/ " + str(detalle["total"]) + "\n"
    b = b + "Descuento: S/ " + str(descuento) + "\n"
    b = b + "------------------------------\n"
    b = b + "TOTAL    : S/ " + str(total_final) + "\n"
    b = b + "==============================\n"
    return b


def mostrar_historial_ventas(historial_ventas):
    if len(historial_ventas) == 0:
        print("No hay ventas registradas.")
        return
    print("N | Fecha | Producto | Cantidad | Precio | Descuento % | Total")
    print("--------------------------------------------------------------")
    i = 1
    for v in historial_ventas:
        print(i, "|", v["fecha"], "|", v["nombre"], "|", v["cantidad"], "|",
              "S/", v["precio"], "|", v["descuento"], "|", "S/", v["total"])
        i = i + 1


def total_recaudado(productos):
    total = 0
    for p in productos:
        total = total + p["precio"] * p["vendidos"]
    return total


def cargar_historial_ventas(ruta):
    historial_ventas = []

    if not os.path.exists(ruta):
        return historial_ventas, (
            "Aviso: no se encontro el archivo de datos (" + ruta +
            "). Se inicia sin historial de ventas."
        )

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError) as error:
        return historial_ventas, (
            "Aviso: no se pudo leer el archivo de datos (" + str(error) +
            "). Se inicia sin historial de ventas."
        )

    invalidos = 0
    for item in datos.get("ventas", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("producto"), str)
            and isinstance(item.get("cantidad"), (int, float))
            and isinstance(item.get("precio_unitario"), (int, float))
            and isinstance(item.get("total"), (int, float))
        ):
            historial_ventas.append({
                "nombre": item["producto"],
                "cantidad": item["cantidad"],
                "precio": item["precio_unitario"],
                "total": item["total"],
                "descuento": item.get("descuento", 0),
                "fecha": item.get("fecha", "sin fecha"),
            })
        else:
            invalidos += 1

    mensaje = "Se cargaron " + str(len(historial_ventas)) + " venta(s) de ejemplo."
    if invalidos > 0:
        mensaje += (" Se ignoraron " + str(invalidos) +
                    " venta(s) del JSON por formato invalido.")
    return historial_ventas, mensaje
