import pandas as pd
from google.adk.tools import FunctionTool


def load_dataset(file_path: str) -> dict:
    """
    Carga un dataset CSV o Excel y devuelve:
    - columnas
    - número de filas
    - vista previa de los primeros registros
    """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        return {"error": "Formato no soportado"}

    return {
        "columns": list(df.columns),
        "rows": len(df),
        "preview": df.head(5).to_dict()
    }


# ADK infiere nombre y descripción desde la función
load_dataset_tool = FunctionTool(load_dataset)
