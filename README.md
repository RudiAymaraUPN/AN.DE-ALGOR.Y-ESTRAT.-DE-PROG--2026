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
│   └── validaciones.py    # Lectura segura de datos por consola (sin crashear)
└── tests/
    └── datos.json         # Datos de ejemplo: 5 productos y 5 ventas
```

## Como ejecutar

```
python main.py
```

Ejecutar desde la carpeta raiz del proyecto (donde esta `main.py`),
para que las importaciones `from src...` funcionen.

Al iniciar, el programa carga los productos y el historial de ventas
de ejemplo desde `tests/datos.json`. Todo lo que se registre despues
durante la ejecucion (productos nuevos, ventas nuevas) queda solo en
memoria: el archivo JSON no se modifica.

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

## Datos de ejemplo

`tests/datos.json` contiene 5 productos y 5 ventas de ejemplo, para
que el sistema no arranque vacio al presentarlo. Si el archivo no
existe o esta mal formado, el programa avisa por consola y arranca
vacio en vez de caerse.

## Requisitos

Solo biblioteca estandar de Python (3.8+). Ver `requirements.txt`.
