# -*- coding: utf-8 -*-
# Colores y menus
import os
import sys

if os.name == "nt":
    os.system("")  # Activa colores ANSI
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

# Sin colores si se redirige
USAR_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

ANCHO = 58

_CODIGOS = {
    "negrita": "1",
    "tenue": "2",
    "rojo": "31",
    "verde": "32",
    "amarillo": "33",
    "azul": "34",
    "magenta": "35",
    "cian": "36",
    "blanco": "97",
    "fondo_azul": "44",
}


def pintar(texto, *estilos):
    # Aplica color ANSI
    if not USAR_COLOR or len(estilos) == 0:
        return str(texto)
    codigos = ";".join(_CODIGOS[e] for e in estilos)
    return "\033[" + codigos + "m" + str(texto) + "\033[0m"


def _fila(segmentos, ancho, borde="║"):
    # Fila de caja
    visible = sum(len(texto) for texto, _ in segmentos)
    relleno = " " * max(0, ancho - visible)
    cuerpo = "".join(pintar(texto, *estilos) for texto, estilos in segmentos)
    return pintar(borde, "cian") + cuerpo + relleno + pintar(borde, "cian")


def _fila_opcion(clave, texto, estilo_texto, ancho):
    return _fila([
        ("    [", ("tenue",)),
        (str(clave).rjust(2), ("negrita", "amarillo")),
        ("] ", ("tenue",)),
        (texto, (estilo_texto,)),
    ], ancho)


def imprimir_menu(titulo, secciones, opciones_finales=None, ancho=ANCHO):
    # Dibuja menu en caja
    print()
    print(pintar("╔" + "═" * ancho + "╗", "cian"))
    print(_fila([(titulo.center(ancho), ("negrita", "blanco", "fondo_azul"))], ancho))
    print(pintar("╠" + "═" * ancho + "╣", "cian"))

    for nombre, estilo, opciones in secciones:
        base = "  ── " + nombre + " "
        resto = ancho - len(base) - 2
        print(_fila([(base + "─" * max(0, resto), ("negrita", estilo))], ancho))
        for clave, texto in opciones:
            print(_fila_opcion(clave, texto, "blanco", ancho))
        print(_fila([("", ())], ancho))

    if opciones_finales:
        print(pintar("╠" + "═" * ancho + "╣", "cian"))
        for clave, texto, estilo in opciones_finales:
            print(_fila_opcion(clave, texto, estilo, ancho))

    print(pintar("╚" + "═" * ancho + "╝", "cian"))


def encabezado(texto, ancho=ANCHO):
    # Titulo de seccion
    print()
    print(pintar("┌" + "─" * ancho + "┐", "cian"))
    print(_fila([("  " + texto.upper(), ("negrita", "blanco"))], ancho, borde="│"))
    print(pintar("└" + "─" * ancho + "┘", "cian"))


def pedir_opcion(texto="Elija una opcion"):
    return input(pintar("  >> " + texto + ": ", "negrita", "verde")).strip()


def mensaje_ok(texto):
    print(pintar(" [OK] ", "negrita", "verde") + pintar(texto, "verde"))


def mensaje_error(texto):
    print(pintar(" [ERROR] ", "negrita", "rojo") + pintar(texto, "rojo"))


def mensaje_aviso(texto):
    print(pintar(" [AVISO] ", "negrita", "amarillo") + pintar(texto, "amarillo"))


def mensaje_info(texto):
    print(pintar(" [INFO] ", "negrita", "cian") + pintar(texto, "cian"))
