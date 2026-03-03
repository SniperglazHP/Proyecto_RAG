#Script de una tool que tiene la funcion de cargar archivos CSV y generar un resumen    

#-->Librerias
import pandas as pd
from google.adk.tools import FunctionTool

#-->Funcion tool que carga un archivo CSV y guarda su contenido para posteriormente ser usado
def cargar_csv(path: str) -> str:
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"Error al cargar el archivo: {e}"
    resumen = {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "nombres_columnas": list(df.columns),
        "tipos": {c: str(df[c].dtype) for c in df.columns},
        "describe": df.describe(include="all").to_string()
    }
    return str(resumen)

cargar_csv_tool = FunctionTool(cargar_csv)
