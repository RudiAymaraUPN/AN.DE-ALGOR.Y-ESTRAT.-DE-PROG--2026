# Sistema de Ventas

Sistema de ventas por consola (proyecto academico: UPN, Analisis de
Algoritmos y Estrategias de Programacion). Permite registrar
productos, registrar ventas, generar boletas con descuento, ordenar
productos (quicksort / burbuja descendente), buscar productos con
autocorrector (distancia de edicion), anular ventas, sugerir que se
puede comprar con un monto (backtracking), calcular el vuelto
(algoritmo voraz) y ver reportes e historial de ventas. El menu usa
colores y cajas para que sea facil de atender.

## Estructura del proyecto

```
sistema_ventas/
├── main.py              # Punto de entrada: el menu de consola
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── productos.py      # Registrar, buscar, sugerir y mostrar productos
│   ├── ventas.py          # Registrar venta, boleta, historial, recaudado
│   ├── ordenamiento.py    # quicksort, burbuja descendente, ordenar por precio/vendidos
│   ├── backtracking.py    # Que se puede comprar con un monto (backtracking)
│   ├── vuelto.py          # Calculo del vuelto con algoritmo voraz (greedy)
│   ├── interfaz.py        # Colores, cajas y menus de la consola
│   ├── formato.py         # Tablas y formato de moneda
│   ├── validaciones.py    # Lectura segura de datos por consola (sin crashear)
│   └── almacenamiento.py  # Guarda productos y ventas en el JSON (mini "base de datos")
└── tests/
    └── datos.json         # Datos de ejemplo / almacenamiento: productos y ventas
```

## Como ejecutar

```
python main.py
```

Ejecutar desde la carpeta raiz del proyecto (donde esta `main.py`),
para que las importaciones `from src...` funcionen.

Al iniciar, el programa carga los productos y el historial de ventas
desde `tests/datos.json`. Cada vez que se registra un producto o una
venta, el archivo se vuelve a escribir con los datos actualizados, asi
que `tests/datos.json` funciona como una mini "base de datos" de
prueba: lo registrado queda guardado entre una ejecucion y otra. Al
ser solo para pruebas, no se espera que supere los 10 registros por
tabla, por lo que reescribir el JSON completo en cada cambio es
suficiente (no hace falta un motor de base de datos real).

## Menu

```
PRODUCTOS
  1. Registrar producto
  2. Ver productos
  3. Buscar producto
  4. Ordenar productos      (submenu: precio menor a mayor,
                             precio mayor a menor, mas vendidos)
VENTAS
  5. Registrar una venta    (al final ofrece calcular el vuelto)
  6. Anular una venta       (devuelve las unidades al stock)
  7. Historial de ventas
  8. Reporte de ventas
CAJA
  9. Que puedo comprar con un monto   (backtracking)
 10. Calcular vuelto                  (algoritmo voraz)
  0. Salir
```

Despues de mostrar cada resultado el programa pide
"Presione ENTER para volver al menu principal..." antes de volver
a mostrar el menu.

### Anular una venta
Muestra las ventas activas, se elige el numero (N) y se confirma. La
venta queda marcada como `ANULADA` en el historial (no se borra), las
unidades vuelven al stock y se descuentan de "vendidos".

### Que puedo comprar con un monto (backtracking)
Se ingresa el monto que tiene el cliente (ej. S/ 2.00). El sistema
muestra los productos que cuestan ese monto o menos y las
combinaciones de productos que caben en el monto, respetando el
stock. Las combinaciones se buscan con backtracking: se agrega un
producto, se explora y, si no sirve, se deshace la eleccion.

### Calcular vuelto (algoritmo voraz)
Se ingresa el total y el monto recibido. En cada paso se entrega la
denominacion mas grande que quepa en el vuelto restante (billetes de
S/ 200, 100, 50, 20, 10 y monedas de S/ 5, 2, 1, 0.50, 0.20, 0.10 y
0.05).

## Datos de ejemplo y persistencia

`tests/datos.json` trae 5 productos y 5 ventas de ejemplo, para que
el sistema no arranque vacio al presentarlo. Si el archivo no existe
o esta mal formado, el programa avisa por consola y arranca vacio en
vez de caerse. Desde ahi, cada producto o venta que se registre en el
menu se agrega en memoria y tambien se guarda en ese mismo archivo
(`src/almacenamiento.py`), para que los cambios persistan la proxima
vez que se ejecute `main.py`.

## Requisitos

Solo biblioteca estandar de Python (3.8+). Ver `requirements.txt`.
