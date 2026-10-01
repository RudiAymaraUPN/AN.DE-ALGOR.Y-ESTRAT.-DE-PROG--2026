# -*- coding: utf-8 -*-
# Vuelto con algoritmo voraz
from .formato import imprimir_tabla, formatear_moneda
from .interfaz import pintar, mensaje_ok, mensaje_error, mensaje_aviso
from .validaciones import leer_decimal, leer_si_no

# (centimos, tipo, texto)
DENOMINACIONES = [
    (20000, "Billete", "S/ 200"),
    (10000, "Billete", "S/ 100"),
    (5000, "Billete", "S/ 50"),
    (2000, "Billete", "S/ 20"),
    (1000, "Billete", "S/ 10"),
    (500, "Moneda", "S/ 5"),
    (200, "Moneda", "S/ 2"),
    (100, "Moneda", "S/ 1"),
    (50, "Moneda", "S/ 0.50"),
    (20, "Moneda", "S/ 0.20"),
    (10, "Moneda", "S/ 0.10"),
    (5, "Moneda", "S/ 0.05"),
]


def a_centimos(valor):
    return int(round(valor * 100))


def calcular_vuelto(monto_centimos):
    # Algoritmo voraz
    desglose = []
    restante = monto_centimos
    for valor, tipo, texto in DENOMINACIONES:
        cantidad = restante // valor
        if cantidad > 0:
            desglose.append((tipo, texto, valor, cantidad))
            restante -= cantidad * valor
    return desglose, restante


def procesar_vuelto(total):
    # Calcula y muestra vuelto
    total_c = a_centimos(total)
    print("Total a cobrar:", pintar(formatear_moneda(total), "negrita", "cian"))

    while True:
        pago = leer_decimal("Monto recibido del cliente: S/ ", minimo=0, incluir_minimo=False)
        pago_c = a_centimos(pago)
        if pago_c >= total_c:
            break
        mensaje_error("El monto no cubre el total. Faltan " +
                      formatear_moneda((total_c - pago_c) / 100) + ".")
        if not leer_si_no("Intentar con otro monto? (s/n): "):
            return

    vuelto_c = pago_c - total_c
    if vuelto_c == 0:
        mensaje_ok("Pago exacto. No hay vuelto que entregar.")
        return

    print("\nVUELTO A ENTREGAR:", pintar(formatear_moneda(vuelto_c / 100), "negrita", "verde"))
    desglose, sobrante = calcular_vuelto(vuelto_c)
    filas = []
    for tipo, texto, valor, cantidad in desglose:
        filas.append([tipo + " de " + texto, str(cantidad), formatear_moneda(valor * cantidad / 100)])
    imprimir_tabla(["Entregar", "Cantidad", "Subtotal"], filas, alineaciones=["izq", "der", "der"])
    piezas = sum(cantidad for _, _, _, cantidad in desglose)
    print(pintar("Total de piezas: " + str(piezas), "tenue"))
    if sobrante > 0:
        mensaje_aviso("Quedan " + formatear_moneda(sobrante / 100) +
                      " que no se pueden entregar (no hay monedas menores a 5 centimos).")
