#Script que tiene la funcion de analizar un archivo CSV y generar un informe EDA en formato JSON

#-->Importar librerias
import json
import pandas as pd
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from prompts import eda_analyzer_prompt

#-->Funcion tool que carga un CSV completo y devuelve su contenido para que el agente analizador genere un informe para dashboards
def load_csv_full(file_path: str) -> str:
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return json.dumps({
            "error": "No se pudo cargar el CSV",
            "detalle": str(e)
        }, ensure_ascii=False)

    return json.dumps({
        "file_path": file_path,
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "data": df.to_dict(orient="records")
    }, ensure_ascii=False)

#-->Funcion tool que vamos a utilizar y creamos arriba
load_csv_tool = FunctionTool(load_csv_full)

#-->Agente analizador
agente_analizador = LlmAgent(
    name="eda_full_control_agent",
    model="gemini-2.5-flash",
    description="Agente EDA con control total sobre un dataset CSV completo.",
    tools=[load_csv_tool],
    instruction=eda_analyzer_prompt()
)
