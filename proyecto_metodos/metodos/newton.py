def diferencias_divididas(x, y):
    n = len(x)
    coef = y.copy()
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    return coef

def evaluar_newton(x, coef, x_eval):
    n = len(coef)
    resultado = coef[-1]
    for i in range(n - 2, -1, -1):
        resultado = resultado * (x_eval - x[i]) + coef[i]
    return resultado

def interpolar_newton(puntos_x, puntos_y, x_faltante):
    # Eliminar puntos vacíos
    puntos_validos = [(xi, yi) for xi, yi in zip(puntos_x, puntos_y) if yi is not None]
    x = [p[0] for p in puntos_validos]
    y = [p[1] for p in puntos_validos]

    coef = diferencias_divididas(x, y)
    y_estimado = evaluar_newton(x, coef, x_faltante)
    return y_estimado
