# -*- coding: utf-8 -*-
from .interfaz import pintar


def imprimir_tabla(encabezados, filas, alineaciones=None, estilos_filas=None):
    # Tabla con colores
    n_columnas = len(encabezados)
    if alineaciones is None:
        alineaciones = ["izq"] * n_columnas

    anchos = []
    for i in range(n_columnas):
        ancho = len(encabezados[i])
        for fila in filas:
            ancho = max(ancho, len(str(fila[i])))
        anchos.append(ancho)

    def formatear_fila(valores):
        celdas = []
        for i in range(n_columnas):
            texto = str(valores[i])
            if alineaciones[i] == "der":
                celdas.append(texto.rjust(anchos[i]))
            else:
                celdas.append(texto.ljust(anchos[i]))
        return " | ".join(celdas)

    linea_encabezado = formatear_fila(encabezados)
    print(pintar(linea_encabezado, "negrita", "cian"))
    print(pintar("-" * len(linea_encabezado), "tenue"))
    for indice, fila in enumerate(filas):
        estilos = estilos_filas[indice] if estilos_filas else ()
        print(pintar(formatear_fila(fila), *estilos))


def formatear_fecha(fecha):
    fecha = str(fecha)
    if " " not in fecha:
        fecha = fecha + " 00:00"
    return fecha


def formatear_moneda(valor):
    # Formato S/ 0.00
    return "S/ {:.2f}".format(valor)
