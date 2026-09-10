# -*- coding: utf-8 -*-

def pausar():
    input("\nPresione ENTER para continuar...")


def leer_texto_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Este campo no puede estar vacio. Intente de nuevo.")


def leer_entero(mensaje, minimo=None, incluir_minimo=True):
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
        except ValueError:
            print("Debe ingresar un numero entero valido.")
            continue
        if minimo is not None:
            if incluir_minimo and valor < minimo:
                print("El valor debe ser mayor o igual a", minimo)
                continue
            if not incluir_minimo and valor <= minimo:
                print("El valor debe ser mayor a", minimo)
                continue
        return valor


def leer_decimal(mensaje, minimo=None, maximo=None, incluir_minimo=True):
    while True:
        entrada = input(mensaje)
        try:
            valor = float(entrada)
        except ValueError:
            print("Debe ingresar un numero valido (ejemplo: 10.5).")
            continue
        if minimo is not None:
            if incluir_minimo and valor < minimo:
                print("El valor debe ser mayor o igual a", minimo)
                continue
            if not incluir_minimo and valor <= minimo:
                print("El valor debe ser mayor a", minimo)
                continue
        if maximo is not None and valor > maximo:
            print("El valor debe ser menor o igual a", maximo)
            continue
        return valor


def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respuesta no valida. Escriba 's' o 'n'.")
