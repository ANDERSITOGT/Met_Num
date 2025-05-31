import numpy as np

def generar_tabla_diferencias(x, y):
    n = len(x)
    tabla = [[0 for _ in range(n)] for _ in range(n)]
    pasos = []

    for i in range(n):
        tabla[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            num = tabla[i + 1][j - 1] - tabla[i][j - 1]
            den = x[i + j] - x[i]
            tabla[i][j] = num / den
            paso = f"Δ^{j}[{i}] = ({tabla[i + 1][j - 1]:.4f} - {tabla[i][j - 1]:.4f}) / ({x[i + j]:.1f} - {x[i]:.1f}) = {tabla[i][j]:.4f}"
            pasos.append(paso)

    salida_tabla = "Tabla de Diferencias Divididas:\n\n"
    encabezado = ["f[x]"] + [f"Δ^{j}" for j in range(1, n)]
    salida_tabla += "\t".join(encabezado) + "\n"

    for i in range(n):
        fila = [f"{tabla[i][j]:.4f}" if j <= n - i - 1 else "" for j in range(n)]
        salida_tabla += "\t".join(fila) + "\n"

    resultado = salida_tabla + "\n\nCálculos paso a paso:\n\n" + "\n".join(pasos)
    return resultado

def generar_procedimiento_minimos(x, y, grado=2):
    n = len(x)
    procedimiento = "Procedimiento del Método de Mínimos Cuadrados (grado 2):\n\n"
    
    procedimiento += "Paso 1: Crear sistema normal de ecuaciones (matriz A y vector b)\n"
    A = np.zeros((grado + 1, grado + 1))
    b = np.zeros(grado + 1)

    for i in range(grado + 1):
        for j in range(grado + 1):
            A[i][j] = sum(xi**(i + j) for xi in x)
        b[i] = sum((xi**i) * yi for xi, yi in zip(x, y))

    procedimiento += "\nMatriz A (coeficientes):\n"
    for fila in A:
        procedimiento += "  " + "  ".join(f"{v:.4f}" for v in fila) + "\n"

    procedimiento += "\nVector b (términos independientes):\n"
    for i, val in enumerate(b):
        procedimiento += f"  b{i} = {val:.4f}\n"

    procedimiento += "\nPaso 2: Resolver sistema A·a = b para encontrar los coeficientes [a0, a1, a2]\n"
    try:
        coef = np.linalg.solve(A, b)
        procedimiento += "\nSolución del sistema:\n"
        for i, c in enumerate(coef):
            procedimiento += f"  a{i} = {c:.4f}\n"

        procedimiento += "\nPaso 3: Polinomio ajustado:\n"
        pol = "y = " + " + ".join([
            f"{coef[i]:.4f}" if i == 0 else
            f"{coef[i]:.4f}·x" if i == 1 else
            f"{coef[i]:.4f}·x^{i}"
            for i in range(len(coef))
        ])
        procedimiento += pol + "\n"

    except np.linalg.LinAlgError:
        procedimiento += "\nError: sistema de ecuaciones no tiene solución única."

    return procedimiento
