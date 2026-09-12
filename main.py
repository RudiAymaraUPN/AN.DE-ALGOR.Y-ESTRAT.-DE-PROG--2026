# -*- coding: utf-8 -*-
import os
from datetime import datetime

from src.productos import (
    registrar_producto,
    buscar_producto,
    sugerir_producto,
    mostrar_productos,
    producto_mas_vendido,
    cargar_productos,
)
from src.ventas import (
    registrar_venta,
    generar_boleta,
    mostrar_historial_ventas,
    total_recaudado,
    cargar_historial_ventas,
)
from src.ordenamiento import (
    ordenar_por_precio,
    ordenar_por_vendidos,
)
from src.almacenamiento import guardar_datos
from src.validaciones import (
    pausar,
    leer_texto_no_vacio,
    leer_entero,
    leer_decimal,
    leer_si_no,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "tests", "datos.json")

# Se "consumen" los datos de ejemplo una sola vez, al iniciar.
productos, mensaje_productos = cargar_productos(RUTA_DATOS)
historial_ventas, mensaje_ventas = cargar_historial_ventas(RUTA_DATOS)
print(mensaje_productos)
print(mensaje_ventas)

while True:
    print("\n========== SISTEMA DE VENTAS ==========")
    print("1. Registrar producto")
    print("2. Ver productos")
    print("3. Registrar una venta")
    print("4. Ordenar por precio")
    print("5. Reporte de ventas")
    print("6. Producto más vendido")
    print("7. Buscar producto")
    print("8. Historial de ventas")
    print("0. Salir")
    opcion = input("Elija una opcion: ")

    try:
        if opcion == "1":
            print("\n--- Registrar producto ---")
            nombre = leer_texto_no_vacio("Nombre: ")
            precio = leer_decimal("Precio: S/ ", minimo=0, incluir_minimo=False)
            stock = leer_entero("Stock: ", minimo=0)
            exito, mensaje = registrar_producto(productos, nombre, precio, stock)
            print(mensaje)
            if exito:
                ok_guardado, mensaje_guardado = guardar_datos(
                    RUTA_DATOS, productos, historial_ventas
                )
                if not ok_guardado:
                    print(mensaje_guardado)
            pausar()

        elif opcion == "2":
            print("\n--- Lista de productos ---")
            mostrar_productos(productos)
            pausar()

        elif opcion == "3":
            print("\n--- Registrar venta ---")
            if len(productos) == 0:
                print("Primero registre productos.")
            else:
                mostrar_productos(productos)
                nombre = leer_texto_no_vacio("Producto a vender: ")
                if buscar_producto(productos, nombre) is None:
                    sugerido = sugerir_producto(productos, nombre)
                    if sugerido != "":
                        print("No existe. Quizas quiso decir:", sugerido)
                        if leer_si_no("Usar esa sugerencia? (s/n): "):
                            nombre = sugerido
                cantidad = leer_entero("Cantidad: ", minimo=0, incluir_minimo=False)
                detalle, mensaje = registrar_venta(productos, nombre, cantidad)
                print(mensaje)
                if detalle is not None:
                    porcentaje = leer_decimal(
                        "Descuento en % (0 si no tiene): ", minimo=0, maximo=100
                    )
                    print(generar_boleta(detalle, porcentaje))
                    historial_ventas.append({
                        "nombre": detalle["nombre"],
                        "cantidad": detalle["cantidad"],
                        "precio": detalle["precio"],
                        "total": detalle["total"],
                        "descuento": porcentaje,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    })
                    ok_guardado, mensaje_guardado = guardar_datos(
                        RUTA_DATOS, productos, historial_ventas
                    )
                    if not ok_guardado:
                        print(mensaje_guardado)
            pausar()

        elif opcion == "4":
            print("\n--- Ordenar por precio ---")
            if len(productos) == 0:
                print("No hay productos.")
            else:
                tipo = input("1) Menor a mayor  2) Mayor a menor: ")
                productos = ordenar_por_precio(productos, tipo == "1")
                mostrar_productos(productos)
            pausar()

        elif opcion == "5":
            print("\n--- Ordenar por mas vendidos ---")
            if len(productos) == 0:
                print("No hay productos.")
            else:
                productos = ordenar_por_vendidos(productos)
                mostrar_productos(productos)
            pausar()

        elif opcion == "6":
            print("\n--- Reporte de ventas ---")
            if len(productos) == 0:
                print("No hay datos.")
            else:
                mejor = producto_mas_vendido(productos)
                print("========== REPORTE ==========")
                if mejor["vendidos"] > 0:
                    print("Mas vendido:", mejor["nombre"], "-",
                          mejor["vendidos"], "unidades")
                else:
                    print("Aun no hay ventas.")
                print("Total recaudado: S/", total_recaudado(productos))
            pausar()

        elif opcion == "7":
            print("\n--- Buscar producto ---")
            nombre = leer_texto_no_vacio("Producto a buscar: ")
            p = buscar_producto(productos, nombre)
            if p is None:
                sugerido = sugerir_producto(productos, nombre)
                if sugerido != "":
                    print("No existe. Quizas quiso decir:", sugerido)
                else:
                    print("No se encontraron productos.")
            else:
                print("Nombre:", p["nombre"], "| Precio: S/", p["precio"],
                      "| Stock:", p["stock"], "| Vendidos:", p["vendidos"])
            pausar()

        elif opcion == "8":
            print("\n--- Historial de ventas ---")
            mostrar_historial_ventas(historial_ventas)
            pausar()

        elif opcion == "0":
            print("Hasta pronto.")
            break

        else:
            print("Opcion no valida.")
            pausar()

    except Exception as error:
        print("Ocurrio un error inesperado:", error)
        pausar()
