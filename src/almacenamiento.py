# -*- coding: utf-8 -*-
import json


def _bloque_lista(clave, lista):
    if not lista:
        return '  "' + clave + '": []'
    lineas = ['  "' + clave + '": [']
    for i, item in enumerate(lista):
        coma = "," if i < len(lista) - 1 else ""
        lineas.append("    " + json.dumps(item, ensure_ascii=False) + coma)
    lineas.append("  ]")
    return "\n".join(lineas)


def guardar_datos(ruta, productos, historial_ventas):
    productos_json = [
        {
            "nombre": p["nombre"],
            "precio": p["precio"],
            "stock": p["stock"],
            "vendidos": p["vendidos"],
        }
        for p in productos
    ]
    ventas_json = [
        {
            "producto": v["nombre"],
            "cantidad": v["cantidad"],
            "precio_unitario": v["precio"],
            "descuento": v["descuento"],
            "total": v["total"],
            "fecha": v["fecha"],
        }
        for v in historial_ventas
    ]

    contenido = (
        "{\n"
        + _bloque_lista("productos", productos_json) + ",\n"
        + _bloque_lista("ventas", ventas_json) + "\n"
        + "}\n"
    )

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        return True, "Datos guardados en " + ruta
    except OSError as error:
        return False, "Aviso: no se pudo guardar en el archivo JSON (" + str(error) + ")."
