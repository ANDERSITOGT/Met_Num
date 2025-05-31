import numpy as np

def ajustar_minimos_cuadrados(x, y, grado, x_eval):
    # Ajuste de un polinomio de grado n por mínimos cuadrados
    coeficientes = np.polyfit(x, y, grado)
    p = np.poly1d(coeficientes)
    y_estimado = p(x_eval)
    return y_estimado, coeficientes

