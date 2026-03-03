#Script que define una herramienta para generar gráficas a partir de archivos CSV

#-->Librerias
import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid
from google.adk.tools import FunctionTool

#-->Ruta de las graficas a guardar
ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

#-->Funcion tool que genera una gráfica a partir de la informacion adjuntada
def generar_grafica(
    csv_path: str,
    tipo: str,
    columna_x: str = None,
    columna_y: str = None
) -> str:
    df = pd.read_csv(csv_path)

    plt.figure(figsize=(8, 5))

    if tipo == "barras":
        df.mean(numeric_only=True).plot(kind="bar")
        plt.title("Gráfica de barras - promedios")

    elif tipo == "dispersion":
        plt.scatter(df[columna_x], df[columna_y])
        plt.xlabel(columna_x)
        plt.ylabel(columna_y)
        plt.title(f"Dispersión: {columna_x} vs {columna_y}")

    elif tipo == "pastel":
        conteo = df[columna_x].value_counts()
        plt.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
        plt.title(f"Distribución de {columna_x}")

    elif tipo == "histograma":
        plt.hist(df[columna_x], bins=20)
        plt.xlabel(columna_x)
        plt.ylabel("Frecuencia")
        plt.title(f"Histograma de {columna_x}")

    else:
        return "Tipo de gráfica no soportado."

    plt.tight_layout()

    filename = f"grafica_{uuid.uuid4().hex}.png"
    path = os.path.join(ARTIFACTS_DIR, filename)
    plt.savefig(path)
    plt.close()

    return f"Gráfica generada correctamente: {path}"

grafica_tool = FunctionTool(generar_grafica)
