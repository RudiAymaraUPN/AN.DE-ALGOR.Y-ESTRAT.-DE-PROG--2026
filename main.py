# -*- coding: utf-8 -*-
import os
from datetime import datetime

from src.productos import (registrar_producto,buscar_producto,sugerir_producto,mostrar_productos,producto_mas_vendido,cargar_productos)
from src.ventas import (registrar_venta,generar_boleta,mostrar_historial_ventas,total_recaudado,cargar_historial_ventas,aplicar_descuento,obtener_venta_activa,anular_venta)
from src.ordenamiento import (ordenar_por_precio,ordenar_por_vendidos)
from src.almacenamiento import guardar_datos
from src.validaciones import (pausar,leer_texto_no_vacio,leer_entero,leer_decimal,leer_si_no)
from src.backtracking import mostrar_opciones_compra
from src.vuelto import procesar_vuelto
from src.formato import formatear_moneda
from src.interfaz import (pintar,encabezado,imprimir_menu,pedir_opcion,mensaje_ok,mensaje_error,mensaje_aviso,mensaje_info)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "tests", "datos.json")

# Secciones del menu
MENU_PRINCIPAL = [
    ("PRODUCTOS", "cian", [
        ("1", "Registrar producto"),
        ("2", "Ver productos"),
        ("3", "Buscar producto"),
        ("4", "Ordenar productos"),
    ]),
    ("VENTAS", "verde", [
        ("5", "Registrar una venta"),
        ("6", "Anular una venta"),
        ("7", "Historial de ventas"),
        ("8", "Reporte de ventas"),
    ]),
    ("CAJA", "magenta", [
        ("9", "Que puedo comprar con un monto"),
        ("10", "Calcular vuelto"),
    ]),
]

MENU_ORDENAR = [
    ("Elija como ordenar", "amarillo", [
        ("1", "Por precio: de menor a mayor"),
        ("2", "Por precio: de mayor a menor"),
        ("3", "Por mas vendidos"),
    ]),
]

# Se "consumen" los datos de ejemplo una sola vez, al iniciar.
productos, mensaje_productos = cargar_productos(RUTA_DATOS)
historial_ventas, mensaje_ventas = cargar_historial_ventas(RUTA_DATOS)
mensaje_info(mensaje_productos)
mensaje_info(mensaje_ventas)


def guardar():
    ok_guardado, mensaje_guardado = guardar_datos(RUTA_DATOS, productos, historial_ventas)
    if not ok_guardado:
        mensaje_aviso(mensaje_guardado)


while True:
    imprimir_menu("SISTEMA DE VENTAS", MENU_PRINCIPAL, [("0", "Salir", "rojo")])
    opcion = pedir_opcion()

    try:
        if opcion == "1":
            encabezado("Registrar producto")
            nombre = leer_texto_no_vacio("Nombre: ")
            precio = leer_decimal("Precio: S/ ", minimo=0, incluir_minimo=False)
            stock = leer_entero("Stock: ", minimo=0)
            exito, mensaje = registrar_producto(productos, nombre, precio, stock)
            if exito:
                mensaje_ok(mensaje)
                guardar()
            else:
                mensaje_error(mensaje)
            pausar()

        elif opcion == "2":
            encabezado("Lista de productos")
            mostrar_productos(productos)
            pausar()

        elif opcion == "3":
            encabezado("Buscar producto")
            nombre = leer_texto_no_vacio("Producto a buscar: ")
            p = buscar_producto(productos, nombre)
            if p is None:
                sugerido = sugerir_producto(productos, nombre)
                if sugerido != "":
                    mensaje_aviso("No existe. Quizas quiso decir: " + sugerido)
                else:
                    mensaje_aviso("No se encontraron productos.")
            else:
                print("Nombre:", p["nombre"], "| Precio:", formatear_moneda(p["precio"]),
                      "| Stock:", p["stock"], "| Vendidos:", p["vendidos"])
            pausar()

        elif opcion == "4":
            if len(productos) == 0:
                encabezado("Ordenar productos")
                mensaje_aviso("No hay productos.")
                pausar()
            else:
                criterio = ""
                while criterio not in ("0", "1", "2", "3"):
                    imprimir_menu("ORDENAR PRODUCTOS", MENU_ORDENAR,
                                  [("0", "Volver al menu principal", "rojo")])
                    criterio = pedir_opcion()
                    if criterio not in ("0", "1", "2", "3"):
                        mensaje_error("Opcion no valida.")
                if criterio != "0":
                    if criterio == "1":
                        encabezado("Productos por precio: menor a mayor")
                        productos = ordenar_por_precio(productos, True)
                    elif criterio == "2":
                        encabezado("Productos por precio: mayor a menor")
                        productos = ordenar_por_precio(productos, False)
                    else:
                        encabezado("Productos mas vendidos")
                        productos = ordenar_por_vendidos(productos)
                    mostrar_productos(productos)
                    pausar()

        elif opcion == "5":
            encabezado("Registrar venta")
            if len(productos) == 0:
                mensaje_aviso("Primero registre productos.")
            else:
                mostrar_productos(productos)
                nombre = leer_texto_no_vacio("Producto a vender: ")
                if buscar_producto(productos, nombre) is None:
                    sugerido = sugerir_producto(productos, nombre)
                    if sugerido != "":
                        mensaje_aviso("No existe. Quizas quiso decir: " + sugerido)
                        if leer_si_no("Usar esa sugerencia? (s/n): "):
                            nombre = sugerido
                cantidad = leer_entero("Cantidad: ", minimo=0, incluir_minimo=False)
                detalle, mensaje = registrar_venta(productos, nombre, cantidad)
                if detalle is None:
                    mensaje_error(mensaje)
                else:
                    mensaje_ok(mensaje)
                    porcentaje = leer_decimal(
                        "Descuento en % (0 si no tiene): ", minimo=0, maximo=100
                    )
                    total_final, _ = aplicar_descuento(detalle["total"], porcentaje)
                    print(generar_boleta(detalle, porcentaje))
                    historial_ventas.append({
                        "nombre": detalle["nombre"],
                        "cantidad": detalle["cantidad"],
                        "precio": detalle["precio"],
                        "total": round(total_final, 2),
                        "descuento": porcentaje,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "anulada": False,
                    })
                    guardar()
                    if leer_si_no("Desea calcular el vuelto? (s/n): "):
                        procesar_vuelto(total_final)
            pausar()

        elif opcion == "6":
            encabezado("Anular una venta")
            hay_activas = False
            for v in historial_ventas:
                if not v.get("anulada", False):
                    hay_activas = True
            if not hay_activas:
                mensaje_aviso("No hay ventas para anular.")
            else:
                mostrar_historial_ventas(historial_ventas, solo_activas=True)
                numero = leer_entero("Numero (N) de la venta a anular (0 para cancelar): ", minimo=0)
                if numero == 0:
                    mensaje_aviso("Operacion cancelada.")
                else:
                    venta, error = obtener_venta_activa(historial_ventas, numero)
                    if venta is None:
                        mensaje_error(error)
                    else:
                        print("Venta N", numero, ":", venta["cantidad"], "x", venta["nombre"],
                              "por", formatear_moneda(venta["total"]))
                        if leer_si_no("Confirma anular esta venta? (s/n): "):
                            mensaje_ok(anular_venta(productos, venta))
                            guardar()
                        else:
                            mensaje_aviso("Operacion cancelada.")
            pausar()

        elif opcion == "7":
            encabezado("Historial de ventas")
            mostrar_historial_ventas(historial_ventas)
            pausar()

        elif opcion == "8":
            encabezado("Reporte de ventas")
            if len(productos) == 0:
                mensaje_aviso("No hay datos.")
            else:
                mejor = producto_mas_vendido(productos)
                if mejor["vendidos"] > 0:
                    print("Mas vendido:", pintar(mejor["nombre"], "negrita"), "-",
                          mejor["vendidos"], "unidades")
                else:
                    print("Aun no hay ventas.")
                print("Total recaudado:", pintar(formatear_moneda(total_recaudado(productos)),
                                                 "negrita", "verde"))
                anuladas = 0
                for v in historial_ventas:
                    if v.get("anulada", False):
                        anuladas = anuladas + 1
                print("Ventas anuladas:", anuladas)
            pausar()

        elif opcion == "9":
            encabezado("Que puedo comprar con un monto")
            if len(productos) == 0:
                mensaje_aviso("No hay productos registrados.")
            else:
                monto = leer_decimal("Monto que tiene el cliente: S/ ", minimo=0, incluir_minimo=False)
                mostrar_opciones_compra(productos, monto)
            pausar()

        elif opcion == "10":
            encabezado("Calcular vuelto")
            total = leer_decimal("Total a cobrar: S/ ", minimo=0, incluir_minimo=False)
            procesar_vuelto(total)
            pausar()

        elif opcion == "0":
            print(pintar("\nHasta pronto.", "negrita", "cian"))
            break

        else:
            mensaje_error("Opcion no valida.")
            pausar()

    except Exception as error:
        mensaje_error("Ocurrio un error inesperado: " + str(error))
        pausar()
