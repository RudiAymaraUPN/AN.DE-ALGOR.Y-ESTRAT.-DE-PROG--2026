# -*- coding: utf-8 -*-
import json
import os

from .productos import buscar_producto
from .formato import imprimir_tabla, formatear_fecha, formatear_moneda
from .interfaz import pintar, mensaje_aviso


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


def obtener_venta_activa(historial_ventas, numero):
    # Busca venta activa
    if numero < 1 or numero > len(historial_ventas):
        return None, "No existe una venta con ese numero."
    venta = historial_ventas[numero - 1]
    if venta.get("anulada", False):
        return None, "Esa venta ya fue anulada."
    return venta, ""


def anular_venta(productos, venta):
    # Anula y repone stock
    venta["anulada"] = True
    p = buscar_producto(productos, venta["nombre"])
    if p is None:
        return ("Venta anulada. Aviso: el producto '" + venta["nombre"] +
                "' ya no existe, no se pudo devolver al stock.")
    cantidad = int(venta["cantidad"])
    p["stock"] = p["stock"] + cantidad
    p["vendidos"] = max(0, p["vendidos"] - cantidad)
    return ("Venta anulada. Se devolvieron " + str(cantidad) +
            " unidad(es) de " + p["nombre"] + " al stock.")


def generar_boleta(detalle, porcentaje):
    total_final, descuento = aplicar_descuento(detalle["total"], porcentaje)
    doble = pintar("=" * 30, "cian") + "\n"
    b = doble
    b = b + pintar("        BOLETA DE VENTA", "negrita", "cian") + "\n"
    b = b + doble
    b = b + "Producto : " + detalle["nombre"] + "\n"
    b = b + "Cantidad : " + str(detalle["cantidad"]) + "\n"
    b = b + "Precio   : " + formatear_moneda(detalle["precio"]) + "\n"
    b = b + "Subtotal : " + formatear_moneda(detalle["total"]) + "\n"
    b = b + "Descuento: " + formatear_moneda(descuento) + "\n"
    b = b + pintar("-" * 30, "tenue") + "\n"
    b = b + pintar("TOTAL    : " + formatear_moneda(total_final), "negrita", "verde") + "\n"
    b = b + doble
    return b


def mostrar_historial_ventas(historial_ventas, solo_activas=False, fecha=None):
    # fecha = "AAAA-MM-DD" para ver solo ese dia (None = todas). El N conserva el numero real
    filas = []
    estilos = []
    for i, v in enumerate(historial_ventas, start=1):
        anulada = v.get("anulada", False)
        if solo_activas and anulada:
            continue
        if fecha is not None and str(v["fecha"])[:10] != fecha:
            continue
        filas.append([
            str(i),
            formatear_fecha(v["fecha"]),
            v["nombre"],
            str(v["cantidad"]),
            formatear_moneda(v["precio"]),
            "{:.1f}".format(v["descuento"]),
            formatear_moneda(v["total"]),
            "ANULADA" if anulada else "Activa",
        ])
        estilos.append(("rojo", "tenue") if anulada else ())
    if len(filas) == 0:
        if fecha is not None:
            mensaje_aviso("No hay ventas registradas el " + fecha + ".")
        else:
            mensaje_aviso("No hay ventas registradas.")
        return
    imprimir_tabla(
        ["N", "Fecha", "Producto", "Cantidad", "Precio", "Descuento %", "Total", "Estado"],
        filas,
        alineaciones=["der", "izq", "izq", "der", "der", "der", "der", "izq"],
        estilos_filas=estilos,
    )


def resumen_del_dia(historial_ventas, fecha):
    # Calcula solo las ventas de un dia (ventas activas y anuladas)
    ventas = 0
    unidades = 0
    total = 0
    anuladas = 0
    por_producto = {}
    for v in historial_ventas:
        if str(v["fecha"])[:10] != fecha:
            continue
        if v.get("anulada", False):
            anuladas = anuladas + 1
            continue
        ventas = ventas + 1
        unidades = unidades + v["cantidad"]
        total = total + v["total"]
        por_producto[v["nombre"]] = por_producto.get(v["nombre"], 0) + v["cantidad"]
    mas_vendido = None
    for nombre, cantidad in por_producto.items():
        if mas_vendido is None or cantidad > mas_vendido[1]:
            mas_vendido = (nombre, cantidad)
    return {"ventas": ventas, "unidades": unidades, "total": total,
            "anuladas": anuladas, "mas_vendido": mas_vendido}


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
                "anulada": bool(item.get("anulada", False)),
            })
        else:
            invalidos += 1

    mensaje = "Se cargaron " + str(len(historial_ventas)) + " venta(s) de ejemplo."
    if invalidos > 0:
        mensaje += (" Se ignoraron " + str(invalidos) +
                    " venta(s) del JSON por formato invalido.")
    return historial_ventas, mensaje
