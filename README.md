# Sistema de Ventas

Sistema de ventas por consola (proyecto academico: UPN, Analisis de
Algoritmos y Estrategias de Programacion). Permite registrar
productos, registrar ventas, generar boletas con descuento, ordenar
productos (quicksort / burbuja descendente), buscar productos con
autocorrector (distancia de edicion) y ver reportes e historial de
ventas.

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

1. Registrar producto
2. Ver productos
3. Registrar una venta
4. Ordenar por precio
5. Ordenar por mas vendidos
6. Reporte de ventas
7. Buscar producto
8. Historial de ventas
0. Salir

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
