import pandas as pd
from tkinter import filedialog

def cargar_csv():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if ruta:
        try:
            datos = pd.read_csv(ruta)
            return datos
        except Exception as e:
            print("❌ Error al cargar el archivo:", e)
            return None
    return None
