import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from metodos.minimos_cuadrados import ajustar_minimos_cuadrados
from metodos.newton import interpolar_newton

def mostrar_grafica_ajuste(datos, metodo, tiempos_estimados=[]):
    if datos is None or metodo not in ["newton", "minimos"]:
        print("No hay datos o método inválido.")
        return

    datos_validos = datos.dropna()
    x_valid = datos_validos["Tiempo"].values
    y_valid = datos_validos["Temperatura"].values

    x_estimar = tiempos_estimados
    y_estimados = []

    if metodo == "minimos":
        coefs = np.polyfit(x_valid, y_valid, 2)
        x_graf = np.linspace(min(datos["Tiempo"]), max(datos["Tiempo"]), 200)
        y_graf = np.polyval(coefs, x_graf)

        for x in x_estimar:
            y_estimados.append(np.polyval(coefs, x))

    elif metodo == "newton":
        def calcular_pol_newton(x_base, y_base, x_eval):
            n = len(x_base)
            coef = y_base.copy()
            for j in range(1, n):
                for i in range(n - 1, j - 1, -1):
                    coef[i] = (coef[i] - coef[i - 1]) / (x_base[i] - x_base[i - j])

            resultado = coef[0]
            producto = 1.0
            for i in range(1, n):
                producto *= (x_eval - x_base[i - 1])
                resultado += coef[i] * producto
            return resultado

        x_graf = np.linspace(min(datos["Tiempo"]), max(datos["Tiempo"]), 200)
        y_graf = [calcular_pol_newton(x_valid, y_valid, xi) for xi in x_graf]

        for x in x_estimar:
            y_estimados.append(calcular_pol_newton(x_valid, y_valid, x))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_valid, y_valid, color='blue', label='Datos conocidos')
    plt.plot(x_graf, y_graf, color='green', label='Curva ajustada')

    if len(x_estimar) > 0:
        plt.scatter(x_estimar, y_estimados, color='orange', label='Valores estimados', marker='x', s=100)

    plt.title(f"Ajuste por el método de {'Mínimos Cuadrados' if metodo == 'minimos' else 'Newton'}")
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
