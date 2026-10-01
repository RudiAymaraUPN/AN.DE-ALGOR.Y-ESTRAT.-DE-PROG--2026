# -*- coding: utf-8 -*-
# Compras con backtracking
from .formato import imprimir_tabla, formatear_moneda
from .interfaz import pintar, mensaje_aviso
from .ordenamiento import ordenar_por_precio

LIMITE_BUSQUEDA = 5000  # Tope de combinaciones


def _centimos(valor):
    # Evita errores decimales
    return int(round(valor * 100))


def productos_asequibles(productos, monto):
    # Productos que alcanzan
    presupuesto = _centimos(monto)
    asequibles = [p for p in productos
                  if p["stock"] > 0 and _centimos(p["precio"]) <= presupuesto]
    return ordenar_por_precio(asequibles, True)


def combinaciones_posibles(productos, monto, limite=LIMITE_BUSQUEDA):
    # Combinaciones con backtracking
    disponibles = [p for p in productos if p["stock"] > 0 and _centimos(p["precio"]) > 0]
    # Mas caros primero
    disponibles = ordenar_por_precio(disponibles, False)
    precios = [_centimos(p["precio"]) for p in disponibles]
    n = len(disponibles)
    presupuesto = _centimos(monto)
    cantidades = [0] * n
    resultados = []
    estado = {"truncado": False}

    def se_puede_agregar(i, restante):
        return precios[i] <= restante and cantidades[i] < disponibles[i]["stock"]

    def explorar(inicio, restante):
        if len(resultados) >= limite:
            estado["truncado"] = True
            return
        # Caso base
        if not any(se_puede_agregar(i, restante) for i in range(n)):
            if sum(cantidades) > 0:
                partes = [(disponibles[i], cantidades[i]) for i in range(n) if cantidades[i] > 0]
                resultados.append((presupuesto - restante, sum(cantidades), partes))
            return
        # Elegir y explorar
        for i in range(inicio, n):
            if se_puede_agregar(i, restante):
                cantidades[i] += 1
                explorar(i, restante - precios[i])
                cantidades[i] -= 1  # Deshacer

    explorar(0, presupuesto)
    # Mejores primero
    resultados.sort(key=lambda c: (-c[0], c[1]))
    return resultados, estado["truncado"]


def mostrar_opciones_compra(productos, monto, mostrar=10):
    presupuesto = _centimos(monto)
    print("Monto disponible:", pintar(formatear_moneda(monto), "negrita", "verde"))

    asequibles = productos_asequibles(productos, monto)
    if len(asequibles) == 0:
        con_stock = [p for p in productos if p["stock"] > 0]
        if len(con_stock) == 0:
            mensaje_aviso("No hay productos con stock.")
        else:
            barato = ordenar_por_precio(con_stock, True)[0]
            mensaje_aviso("Con " + formatear_moneda(monto) + " no alcanza para ningun producto. "
                          "El mas barato es " + barato["nombre"] + " (" +
                          formatear_moneda(barato["precio"]) + ").")
        return

    print(pintar("\nProductos que cuestan " + formatear_moneda(monto) + " o menos:", "negrita"))
    filas = []
    estilos = []
    for i, p in enumerate(asequibles, start=1):
        justo = _centimos(p["precio"]) == presupuesto
        filas.append([str(i), p["nombre"], formatear_moneda(p["precio"]), str(p["stock"]),
                      "Precio justo" if justo else "Sobra " + formatear_moneda(monto - p["precio"])])
        estilos.append(("verde",) if justo else ())
    imprimir_tabla(["N", "Nombre", "Precio", "Stock", "Detalle"], filas,
                   alineaciones=["der", "izq", "der", "der", "izq"], estilos_filas=estilos)

    combinaciones, truncado = combinaciones_posibles(productos, monto)
    print(pintar("\nCombinaciones posibles (backtracking):", "negrita"))
    for numero, (gasto, unidades, partes) in enumerate(combinaciones[:mostrar], start=1):
        detalle = " + ".join(str(cant) + " x " + p["nombre"] for p, cant in partes)
        sobra = presupuesto - gasto
        resumen = "Total " + formatear_moneda(gasto / 100) + " | Sobra " + formatear_moneda(sobra / 100)
        estilo = ("verde",) if sobra == 0 else ()
        print(pintar(str(numero).rjust(3) + ") " + detalle, *estilo))
        print(pintar("       " + resumen, "tenue"))
    if len(combinaciones) > mostrar:
        print(pintar("\nSe muestran las " + str(mostrar) + " mejores de " +
                     str(len(combinaciones)) + " combinaciones encontradas.", "tenue"))
    if truncado:
        mensaje_aviso("Hay demasiadas combinaciones: se revisaron solo las primeras " +
                      str(LIMITE_BUSQUEDA) + ".")
