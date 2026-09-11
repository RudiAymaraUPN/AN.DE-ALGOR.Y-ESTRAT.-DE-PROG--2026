# -*- coding: utf-8 -*-

def imprimir_tabla(encabezados, filas, alineaciones=None):
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
    print(linea_encabezado)
    print("-" * len(linea_encabezado))
    for fila in filas:
        print(formatear_fila(fila))


def formatear_fecha(fecha):
    fecha = str(fecha)
    if " " not in fecha:
        fecha = fecha + " 00:00"
    return fecha


def formatear_moneda(valor):
    """Formatea un monto con 2 decimales fijos, ej. 'S/ 5.50'."""
    return "S/ {:.2f}".format(valor)
