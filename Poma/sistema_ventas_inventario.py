"""
Sistema de Ventas e Inventario
Curso: Analisis de Algoritmos y Estrategias de Programacion
Tecnicas aplicadas:
    - Algoritmo VORAZ (greedy): calculo del vuelto con el minimo numero de
      billetes/monedas.
    - Algoritmo RECURSIVO: busqueda binaria recursiva de productos y calculo
      recursivo del subtotal del carrito de compras.
    - BACKTRACKING: generacion de combinaciones (combos) de productos del
      inventario cuyo precio total sea exactamente igual a un presupuesto
      dado por el cliente.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. MODELO DE DATOS
# ---------------------------------------------------------------------------

@dataclass
class Producto:
    codigo: str
    nombre: str
    precio: float
    stock: int


@dataclass
class ItemVenta:
    producto: Producto
    cantidad: int

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad


class Inventario:
    """Controla el registro, busqueda y stock de productos."""

    def __init__(self):
        self.productos = []          # lista de objetos Producto
        self._contador_boleta = 1000  # correlativo de boletas

    # -------------------- REGISTRO --------------------
    def registrar_producto(self, codigo, nombre, precio, stock):
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"El codigo '{codigo}' ya existe en el inventario.")
        self.productos.append(Producto(codigo, nombre, float(precio), int(stock)))

    # -------------------- BUSQUEDA (RECURSIVA) --------------------
    def _lista_ordenada_por_codigo(self):
        return sorted(self.productos, key=lambda p: p.codigo)

    def buscar_por_codigo(self, codigo):
        """Busqueda binaria RECURSIVA de un producto por su codigo.

        Caso base: sublista vacia -> no se encontro el producto.
        Caso recursivo: se compara el elemento central y se reduce el
        espacio de busqueda a la mitad izquierda o derecha.
        """
        lista = self._lista_ordenada_por_codigo()
        return self._busqueda_binaria_recursiva(lista, codigo, 0, len(lista) - 1)

    def _busqueda_binaria_recursiva(self, lista, codigo, inicio, fin):
        if inicio > fin:                     # caso base: no encontrado
            return None
        medio = (inicio + fin) // 2
        if lista[medio].codigo == codigo:    # caso base: encontrado
            return lista[medio]
        elif lista[medio].codigo > codigo:
            return self._busqueda_binaria_recursiva(lista, codigo, inicio, medio - 1)
        else:
            return self._busqueda_binaria_recursiva(lista, codigo, medio + 1, fin)

    def buscar_por_nombre(self, texto):
        texto = texto.lower()
        return [p for p in self.productos if texto in p.nombre.lower()]

    # -------------------- CONTROL DE STOCK --------------------
    def hay_stock_suficiente(self, codigo, cantidad):
        producto = self.buscar_por_codigo(codigo)
        return producto is not None and producto.stock >= cantidad

    def descontar_stock(self, codigo, cantidad):
        producto = self.buscar_por_codigo(codigo)
        if producto is None:
            raise ValueError("Producto no encontrado.")
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente para '{producto.nombre}'.")
        producto.stock -= cantidad

    def listar_productos(self):
        return list(self.productos)

    # -------------------- BACKTRACKING: COMBOS PROMOCIONALES --------------------
    def generar_combos_backtracking(self, presupuesto, max_items=4):
        """Genera, mediante BACKTRACKING, todas las combinaciones de productos
        distintos cuyo precio total sea EXACTAMENTE igual al presupuesto que
        indica el cliente (por ejemplo, para armar un combo/promocion).

        Se explora el espacio de soluciones probando incluir o no cada
        producto (poda cuando el acumulado supera el presupuesto o cuando ya
        se alcanzo el numero maximo de items permitido en un combo).
        """
        productos = self.listar_productos()
        soluciones = []
        combo_actual = []

        def backtrack(indice, acumulado):
            # Poda: combo valido encontrado
            if abs(acumulado - presupuesto) < 1e-9 and combo_actual:
                soluciones.append(list(combo_actual))
            # Poda: nos pasamos del presupuesto, del limite de items o
            # ya no quedan productos por evaluar -> se corta esta rama
            if indice == len(productos) or acumulado >= presupuesto or len(combo_actual) >= max_items:
                return

            producto = productos[indice]

            # Rama 1: SI se incluye el producto actual
            if acumulado + producto.precio <= presupuesto:
                combo_actual.append(producto)
                backtrack(indice + 1, acumulado + producto.precio)
                combo_actual.pop()          # retroceso (undo choice)

            # Rama 2: NO se incluye el producto actual
            backtrack(indice + 1, acumulado)

        backtrack(0, 0.0)
        return soluciones


# ---------------------------------------------------------------------------
# 2. VENTAS, DESCUENTOS Y BOLETA
# ---------------------------------------------------------------------------

class ModuloVentas:
    DENOMINACIONES = [200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1]  # S/ (soles)

    def __init__(self, inventario: Inventario):
        self.inventario = inventario

    # -------------------- CALCULO RECURSIVO DEL SUBTOTAL --------------------
    def calcular_subtotal(self, carrito):
        """Calcula el subtotal de un carrito de forma RECURSIVA.
        Caso base: carrito vacio -> subtotal 0.
        Caso recursivo: subtotal = primer item + subtotal(resto del carrito).
        """
        if not carrito:
            return 0.0
        primero, *resto = carrito
        return primero.subtotal + self.calcular_subtotal(resto)

    # -------------------- DESCUENTO --------------------
    @staticmethod
    def aplicar_descuento(monto, porcentaje):
        if not 0 <= porcentaje <= 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        descuento = monto * (porcentaje / 100)
        return round(monto - descuento, 2), round(descuento, 2)

    # -------------------- ALGORITMO VORAZ: VUELTO --------------------
    @classmethod
    def calcular_vuelto_voraz(cls, monto_pagado, total_a_pagar):
        """Calcula el vuelto usando un algoritmo VORAZ: en cada paso se
        entrega la denominacion mas alta posible sin excederse, hasta
        cubrir el vuelto total. Es la solucion clasica (localmente optima
        en cada paso) para el problema del cambio con las denominaciones
        del sistema monetario peruano.
        """
        vuelto = round(monto_pagado - total_a_pagar, 2)
        if vuelto < 0:
            raise ValueError("El monto pagado es menor al total a pagar.")

        detalle = {}
        restante = round(vuelto, 2)
        for denominacion in cls.DENOMINACIONES:
            cantidad = int(restante // denominacion)
            if cantidad > 0:
                detalle[denominacion] = cantidad
                restante = round(restante - cantidad * denominacion, 2)
        return vuelto, detalle

    # -------------------- REGISTRO DE VENTA + BOLETA --------------------
    def registrar_venta(self, carrito, porcentaje_descuento, monto_pagado):
        for item in carrito:
            if not self.inventario.hay_stock_suficiente(item.producto.codigo, item.cantidad):
                raise ValueError(f"Stock insuficiente para '{item.producto.nombre}'.")

        subtotal = self.calcular_subtotal(carrito)
        total, descuento = self.aplicar_descuento(subtotal, porcentaje_descuento)
        vuelto, detalle_vuelto = self.calcular_vuelto_voraz(monto_pagado, total)

        for item in carrito:
            self.inventario.descontar_stock(item.producto.codigo, item.cantidad)

        numero_boleta = self.inventario._contador_boleta
        self.inventario._contador_boleta += 1

        return {
            "numero_boleta": numero_boleta,
            "items": carrito,
            "subtotal": subtotal,
            "porcentaje_descuento": porcentaje_descuento,
            "descuento": descuento,
            "total": total,
            "monto_pagado": monto_pagado,
            "vuelto": vuelto,
            "detalle_vuelto": detalle_vuelto,
        }

    @staticmethod
    def emitir_boleta(venta):
        lineas = []
        lineas.append("=" * 46)
        lineas.append("           BOLETA DE VENTA ELECTRONICA")
        lineas.append("        Sistema de Ventas e Inventario")
        lineas.append("=" * 46)
        lineas.append(f"N. Boleta : B001-{venta['numero_boleta']}")
        lineas.append("-" * 46)
        lineas.append(f"{'CANT':<5}{'DESCRIPCION':<22}{'P.UNIT':>8}{'SUBT.':>8}")
        for item in venta["items"]:
            lineas.append(
                f"{item.cantidad:<5}{item.producto.nombre[:22]:<22}"
                f"{item.producto.precio:>8.2f}{item.subtotal:>8.2f}"
            )
        lineas.append("-" * 46)
        lineas.append(f"{'SUBTOTAL':>38}: S/ {venta['subtotal']:.2f}")
        lineas.append(f"{'DESCUENTO (' + str(venta['porcentaje_descuento']) + '%)':>38}: S/ {venta['descuento']:.2f}")
        lineas.append(f"{'TOTAL A PAGAR':>38}: S/ {venta['total']:.2f}")
        lineas.append(f"{'MONTO PAGADO':>38}: S/ {venta['monto_pagado']:.2f}")
        lineas.append(f"{'VUELTO':>38}: S/ {venta['vuelto']:.2f}")
        if venta["detalle_vuelto"]:
            lineas.append("-" * 46)
            lineas.append("Detalle del vuelto (algoritmo voraz):")
            for denom, cant in venta["detalle_vuelto"].items():
                etiqueta = f"S/ {denom:.2f}" if denom < 1 else f"S/ {int(denom)}"
                lineas.append(f"   {cant} x {etiqueta}")
        lineas.append("=" * 46)
        lineas.append("        Gracias por su compra")
        lineas.append("=" * 46)
        boleta_texto = "\n".join(lineas)
        print(boleta_texto)
        return boleta_texto


# ---------------------------------------------------------------------------
# 3. MENU DE CONSOLA (uso interactivo real de la aplicacion)
# ---------------------------------------------------------------------------

def menu():
    inventario = Inventario()
    ventas = ModuloVentas(inventario)

    # Datos iniciales de ejemplo
    inventario.registrar_producto("P001", "Arroz Costeno 5kg", 21.50, 40)
    inventario.registrar_producto("P002", "Aceite Primor 1L", 12.90, 30)
    inventario.registrar_producto("P003", "Azucar Rubia 1kg", 4.50, 60)
    inventario.registrar_producto("P004", "Leche Gloria 400g", 4.20, 80)
    inventario.registrar_producto("P005", "Fideos Don Vittorio 500g", 3.80, 50)

    while True:
        print("\n===== SISTEMA DE VENTAS E INVENTARIO =====")
        print("1. Registrar producto")
        print("2. Buscar producto por codigo (recursivo)")
        print("3. Buscar producto por nombre")
        print("4. Listar inventario")
        print("5. Registrar venta y emitir boleta")
        print("6. Generar combos por presupuesto (backtracking)")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                codigo = input("Codigo: ").strip()
                nombre = input("Nombre: ").strip()
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                inventario.registrar_producto(codigo, nombre, precio, stock)
                print("Producto registrado correctamente.")

            elif opcion == "2":
                codigo = input("Codigo a buscar: ").strip()
                producto = inventario.buscar_por_codigo(codigo)
                print(producto if producto else "Producto no encontrado.")

            elif opcion == "3":
                texto = input("Nombre o parte del nombre: ").strip()
                resultados = inventario.buscar_por_nombre(texto)
                for p in resultados:
                    print(p)
                if not resultados:
                    print("Sin resultados.")

            elif opcion == "4":
                for p in inventario.listar_productos():
                    print(f"{p.codigo} | {p.nombre:<25} | S/ {p.precio:>6.2f} | Stock: {p.stock}")

            elif opcion == "5":
                carrito = []
                while True:
                    codigo = input("Codigo del producto (enter para terminar): ").strip()
                    if codigo == "":
                        break
                    cantidad = int(input("Cantidad: "))
                    producto = inventario.buscar_por_codigo(codigo)
                    if producto is None:
                        print("Producto no encontrado.")
                        continue
                    carrito.append(ItemVenta(producto, cantidad))
                descuento = float(input("Porcentaje de descuento (0 si no aplica): "))
                pago = float(input("Monto con el que paga el cliente: "))
                venta = ventas.registrar_venta(carrito, descuento, pago)
                ventas.emitir_boleta(venta)

            elif opcion == "6":
                presupuesto = float(input("Presupuesto exacto del cliente (S/): "))
                combos = inventario.generar_combos_backtracking(presupuesto)
                if combos:
                    print(f"Se encontraron {len(combos)} combo(s) que suman exactamente S/ {presupuesto:.2f}:")
                    for i, combo in enumerate(combos, 1):
                        nombres = ", ".join(p.nombre for p in combo)
                        print(f"  Combo {i}: {nombres}")
                else:
                    print("No existe ninguna combinacion exacta para ese presupuesto.")

            elif opcion == "0":
                print("Gracias por usar el sistema.")
                break
            else:
                print("Opcion invalida.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu()
