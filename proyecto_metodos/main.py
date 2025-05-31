import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from utilidades.archivo import cargar_csv
from metodos.newton import interpolar_newton
from metodos.minimos_cuadrados import ajustar_minimos_cuadrados
from utilidades.procedimiento import generar_tabla_diferencias, generar_procedimiento_minimos
from utilidades.graficador import mostrar_grafica_ajuste
import os

COLOR_FONDO = "#E3F2FD"
COLOR_HEADER = "#1976D2"
COLOR_HEADER_TEXTO = "white"
COLOR_ZEBRA_1 = "#FFFFFF"
COLOR_ZEBRA_2 = "#F0F8FF"
FUENTE_NORMAL = ("Arial", 11)
FUENTE_NEGRITA = ("Arial", 11, "bold")

datos_actuales = None
tipo_metodo_actual = None
procedimiento_generado = ""
tiempos_estimados = []

ventana = tk.Tk()
ventana.title("Recuperación de Datos - Métodos Numéricos")
ventana.geometry("900x750")
ventana.configure(bg=COLOR_FONDO)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", background=COLOR_HEADER, foreground=COLOR_HEADER_TEXTO, font=FUENTE_NEGRITA)
style.configure("Treeview", font=FUENTE_NORMAL, rowheight=25, background=COLOR_ZEBRA_1, fieldbackground=COLOR_ZEBRA_1)
style.map("Treeview", background=[('selected', '#BBDEFB')])

frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
frame_tabla.pack(pady=10)

tabla = ttk.Treeview(frame_tabla, columns=("Tiempo", "Temperatura"), show="headings", height=15)
tabla.heading("Tiempo", text="Tiempo")
tabla.heading("Temperatura", text="Temperatura")
tabla.column("Tiempo", anchor=tk.CENTER, width=100)
tabla.column("Temperatura", anchor=tk.CENTER, width=150)
tabla.pack(side="left")

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")

etiqueta_resultados = tk.Label(ventana, text="", font=FUENTE_NORMAL, fg="red", bg=COLOR_FONDO, justify="left")
etiqueta_resultados.pack()

texto_procedimiento = tk.Text(ventana, height=12, width=100, font=("Courier New", 10), bg="#fefefe")

# Contenedor de botones agrupados
frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

btn_procedimiento = tk.Button(frame_botones, text="Ver procedimiento", font=FUENTE_NEGRITA,
                               bg="#9C27B0", fg="white", activebackground="#7B1FA2",
                               command=lambda: mostrar_procedimiento(), width=25)

btn_grafica = tk.Button(frame_botones, text="Mostrar gráfica del ajuste", font=FUENTE_NORMAL,
                         bg="#607D8B", fg="white", activebackground="#455A64",
                         command=lambda: mostrar_grafica_ajuste(datos_actuales, tipo_metodo_actual, tiempos_estimados), width=25)

btn_exportar_csv = tk.Button(frame_botones, text="Exportar CSV", font=FUENTE_NORMAL,
                              bg="#03A9F4", fg="white", activebackground="#0288D1",
                              command=lambda: exportar_csv(datos_actuales), width=25)

btn_exportar_txt = tk.Button(frame_botones, text="Exportar procedimiento", font=FUENTE_NORMAL,
                              bg="#FF5722", fg="white", activebackground="#E64A19",
                              command=lambda: exportar_procedimiento(procedimiento_generado), width=25)

btn_reset = tk.Button(frame_botones, text="Nuevo ejercicio", font=FUENTE_NEGRITA,
                      bg="#009688", fg="white", activebackground="#00796B",
                      command=lambda: reiniciar_interfaz(), width=52)

btn_cargar = tk.Button(ventana, text="Cargar archivo CSV", font=FUENTE_NEGRITA,
                       bg="#FF9800", fg="white", activebackground="#FB8C00",
                       command=lambda: cargar_datos())
btn_cargar.pack(pady=5)

btn_newton = tk.Button(ventana, text="Aplicar Interpolación de Newton", font=FUENTE_NORMAL,
                       bg="#4CAF50", fg="white", activebackground="#45a049",
                       command=lambda: aplicar_metodo("newton"))

btn_minimos = tk.Button(ventana, text="Aplicar Mínimos Cuadrados", font=FUENTE_NORMAL,
                        bg="#2196F3", fg="white", activebackground="#1E88E5",
                        command=lambda: aplicar_metodo("minimos"))

def mostrar_botones_finales():
    btn_procedimiento.grid(row=0, column=0, padx=10, pady=5)
    btn_grafica.grid(row=0, column=1, padx=10, pady=5)
    btn_exportar_csv.grid(row=1, column=0, padx=10, pady=5)
    btn_exportar_txt.grid(row=1, column=1, padx=10, pady=5)
    btn_reset.grid(row=2, column=0, columnspan=2, pady=10)

def mostrar_en_tabla(datos):
    for fila in tabla.get_children():
        tabla.delete(fila)
    for i, (_, fila) in enumerate(datos.iterrows()):
        tiempo = fila["Tiempo"]
        temp = round(fila["Temperatura"], 3) if pd.notnull(fila["Temperatura"]) else "NaN"
        bg_color = COLOR_ZEBRA_1 if i % 2 == 0 else COLOR_ZEBRA_2
        tabla.insert("", tk.END, values=(tiempo, temp), tags=(f'fila{i}',))
        tabla.tag_configure(f'fila{i}', background=bg_color)

def cargar_datos():
    global datos_actuales
    datos = cargar_csv()
    if datos is not None:
        datos_actuales = datos
        mostrar_en_tabla(datos)

        tiempos = datos[datos.isnull().any(axis=1)]["Tiempo"].tolist()
        mensaje = "Datos faltantes detectados en:\n" + "\n".join([f"- Tiempo = {t}" for t in tiempos])
        etiqueta_resultados.config(text=mensaje if tiempos else "No se detectaron datos faltantes.")

        btn_newton.pack(pady=5)
        btn_minimos.pack(pady=5)
        ocultar_secundarios()
        messagebox.showinfo("Carga exitosa", "Archivo cargado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo cargar el archivo.")

def aplicar_metodo(tipo):
    global datos_actuales, tipo_metodo_actual, procedimiento_generado, tiempos_estimados

    datos = datos_actuales.copy()
    resultados = []
    tiempos_estimados = []

    for index, fila in datos.iterrows():
        if pd.isnull(fila["Temperatura"]):
            datos_validos = datos.dropna().reset_index(drop=True)
            if len(datos_validos) < 2:
                resultados.append(f"No hay suficientes datos para calcular en Tiempo = {fila['Tiempo']}")
                continue

            x = datos_validos["Tiempo"].tolist()
            y = datos_validos["Temperatura"].tolist()
            x_faltante = fila["Tiempo"]

            try:
                if tipo == "newton":
                    y_estimado = interpolar_newton(x, y, x_faltante)
                    metodo = "Newton"
                    procedimiento_generado = generar_tabla_diferencias(x, y)
                else:
                    y_estimado, _ = ajustar_minimos_cuadrados(x, y, grado=2, x_eval=x_faltante)
                    metodo = "Mínimos Cuadrados"
                    procedimiento_generado = generar_procedimiento_minimos(x, y, grado=2)

                datos.at[index, "Temperatura"] = y_estimado
                tiempos_estimados.append(x_faltante)
                resultados.append(f"{metodo} → Tiempo = {x_faltante} → Estimado: {round(y_estimado, 3)}")

            except Exception as e:
                resultados.append(f"Error en Tiempo = {x_faltante}: {e}")

    datos_actuales = datos
    mostrar_en_tabla(datos)
    etiqueta_resultados.config(text=f"{metodo} aplicado:\n\n" + "\n".join(resultados))

    tipo_metodo_actual = tipo

    btn_cargar.pack_forget()
    btn_newton.pack_forget()
    btn_minimos.pack_forget()
    texto_procedimiento.pack_forget()

    mostrar_botones_finales()

def mostrar_procedimiento():
    texto_procedimiento.delete("1.0", tk.END)
    texto_procedimiento.insert(tk.END, procedimiento_generado)
    texto_procedimiento.pack(pady=5)
    btn_procedimiento.grid_remove()

def reiniciar_interfaz():
    global datos_actuales, tipo_metodo_actual, procedimiento_generado, tiempos_estimados

    datos_actuales = None
    tipo_metodo_actual = None
    procedimiento_generado = ""
    tiempos_estimados = []

    for fila in tabla.get_children():
        tabla.delete(fila)

    etiqueta_resultados.config(text="")
    texto_procedimiento.delete("1.0", tk.END)
    texto_procedimiento.pack_forget()

    for widget in frame_botones.winfo_children():
        widget.grid_remove()

    btn_newton.pack_forget()
    btn_minimos.pack_forget()

    btn_cargar.pack(pady=5)

def exportar_csv(datos):
    ruta = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivos CSV", "*.csv")],
        title="Guardar archivo de resultados"
    )
    if ruta:
        datos.to_csv(ruta, index=False)

def exportar_procedimiento(contenido):
    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")],
        title="Guardar procedimiento"
    )
    if ruta:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)

def ocultar_secundarios():
    texto_procedimiento.pack_forget()
    for widget in frame_botones.winfo_children():
        widget.grid_remove()

ventana.mainloop()
