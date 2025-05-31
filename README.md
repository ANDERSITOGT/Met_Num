Proyecto Final de Métodos Numéricos

Este proyecto implementa un programa en Python con interfaz gráfica que permite recuperar datos faltantes en archivos CSV utilizando métodos numéricos clásicos, como la Interpolación de Newton y el Método de Mínimos Cuadrados. También incluye una visualización gráfica del ajuste y funciones de exportación.

Estructura del proyecto:

main.py: archivo principal del programa

utilidades/: contiene los módulos auxiliares

graficador.py: genera la gráfica del ajuste

interpolacion_newton.py: contiene el método de interpolación de Newton

minimos_cuadrados.py: contiene el método de mínimos cuadrados

datos/: contiene archivos CSV de ejemplo

exportaciones/: guarda los resultados generados

Características principales:

Carga de archivos CSV con datos y tiempos

Detección automática de valores faltantes

Aplicación de métodos numéricos para recuperar datos

Visualización paso a paso del procedimiento

Exportación de resultados a archivos CSV y TXT

Gráfica del ajuste comparando valores reales y estimados

Requisitos del sistema:

Python 3.8 o superior

Librerías necesarias:
matplotlib
numpy
pandas

Para instalar las dependencias, se puede ejecutar el siguiente comando:

pip install matplotlib numpy pandas

Instrucciones de uso:

Abrir una terminal o consola en la carpeta del proyecto

Ejecutar el siguiente comando:

python main.py

Esto abrirá la interfaz gráfica donde se puede cargar un archivo CSV, aplicar los métodos numéricos y visualizar los resultados.
