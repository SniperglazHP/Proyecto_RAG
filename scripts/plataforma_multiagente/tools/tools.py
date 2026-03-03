import pandas as pd
from google.adk.tools import FunctionTool


def load_csv(file_path: str) -> str:
    df = pd.read_csv(file_path)
    return f"Columnas: {list(df.columns)} | Filas: {len(df)}"


load_csv_tool = FunctionTool(load_csv)
