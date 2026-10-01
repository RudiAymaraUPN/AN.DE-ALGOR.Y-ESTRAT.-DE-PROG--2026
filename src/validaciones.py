# -*- coding: utf-8 -*-
from .interfaz import pintar, mensaje_error


def pausar():
    input(pintar("\nPresione ENTER para volver al menu principal...", "negrita", "amarillo"))


def leer_texto_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        mensaje_error("Este campo no puede estar vacio. Intente de nuevo.")


def leer_entero(mensaje, minimo=None, incluir_minimo=True):
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
        except ValueError:
            mensaje_error("Debe ingresar un numero entero valido.")
            continue
        if minimo is not None:
            if incluir_minimo and valor < minimo:
                mensaje_error("El valor debe ser mayor o igual a " + str(minimo))
                continue
            if not incluir_minimo and valor <= minimo:
                mensaje_error("El valor debe ser mayor a " + str(minimo))
                continue
        return valor


def leer_decimal(mensaje, minimo=None, maximo=None, incluir_minimo=True):
    while True:
        entrada = input(mensaje)
        try:
            valor = float(entrada)
        except ValueError:
            mensaje_error("Debe ingresar un numero valido (ejemplo: 10.5).")
            continue
        if minimo is not None:
            if incluir_minimo and valor < minimo:
                mensaje_error("El valor debe ser mayor o igual a " + str(minimo))
                continue
            if not incluir_minimo and valor <= minimo:
                mensaje_error("El valor debe ser mayor a " + str(minimo))
                continue
        if maximo is not None and valor > maximo:
            mensaje_error("El valor debe ser menor o igual a " + str(maximo))
            continue
        return valor


def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        mensaje_error("Respuesta no valida. Escriba 's' o 'n'.")
