#Script de tools para los agentes de la plataforma de análisis de datos, incluyendo funciones para subir datasets a Supabase, cargar datasets desde Supabase y convertirlos en formatos adecuados para su análisis y visualización.

#-->Librerias
import io
import json
import os
from typing import Any
import pandas as pd
from dotenv import load_dotenv
from google.adk.tools import FunctionTool
from supabase import Client, create_client

#-->Carga de variables de entorno para Supabase
load_dotenv()
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "datasets")

#-->Tool interna para manejo de Supabase y procesamiento de datasets
def _get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Fallo con SUPABASE_URL or SUPABASE_SERVICE_KEY."
        )

    return create_client(url, key)

#-->Tool interna que se enacarga de leer el archivo enviado por el usuario a Supabase
def _read_dataframe_from_bytes(file_bytes: bytes, filename: str) -> pd.DataFrame:
    lower = filename.lower()
    buffer = io.BytesIO(file_bytes)

    if lower.endswith(".csv"):
        return pd.read_csv(buffer)

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(buffer)

    raise ValueError("Solo .csv, .xlsx, y .xls son soportados de momento.")

#-->Tool interna enfocada en convertir un DataFrame a un formato JSON serializable, con metadatos útiles para el análisis y la visualización.
def _serialize_df(df: pd.DataFrame) -> dict[str, Any]:
    df_clean = df.where(pd.notnull(df), None)
    return {
        "rows": int(df_clean.shape[0]),
        "columns": list(df_clean.columns),
        "dtypes": {col: str(dtype) for col, dtype in df_clean.dtypes.items()},
        "data": df_clean.to_dict(orient="records"),
    }

#-->Tool para subir archivos a Supabase, que también registra metadatos en una tabla "datasets" para facilitar su gestión y acceso posterior.
def upload_to_supabase(file_bytes: bytes, filename: str) -> str:
    client = _get_supabase_client()
    bucket = SUPABASE_BUCKET

    client.storage.from_(bucket).upload(
        path=filename,
        file=file_bytes,
        file_options={"content-type": "application/octet-stream", "upsert": "true"},
    )

    client.table("datasets").upsert(
        {
            "filename": filename,
            "storage_path": filename,
        }
    ).execute()

    return json.dumps({"status": "uploaded", "filename": filename})

#-->Tool para cargar un dataset desde Supabase, que se puede usar directamente en el agente de análisis para obtener los datos en formato JSON listo para su procesamiento.
def load_dataset_from_supabase(filename: str) -> dict[str, Any]:
    client = _get_supabase_client()
    bucket = SUPABASE_BUCKET

    raw_bytes = client.storage.from_(bucket).download(filename)
    df = _read_dataframe_from_bytes(raw_bytes, filename)
    return _serialize_df(df)

#-->Tool para cargar un dataset desde Supabase y devolverlo como JSON, que se puede usar directamente en el agente de análisis para obtener los datos en formato JSON listo para su procesamiento.
def load_csv_from_supabase(filename: str) -> str:
    dataset = load_dataset_from_supabase(filename)
    return json.dumps(dataset)

#-->Tools para los agentes, que permiten integrar las funciones de carga y análisis de datasets directamente en el flujo de trabajo de los agentes, facilitando la interacción con los datos y la generación de insights.
upload_tool = FunctionTool(upload_to_supabase)
load_dataset_tool = FunctionTool(load_dataset_from_supabase)
load_csv_tool = FunctionTool(load_csv_from_supabase)
