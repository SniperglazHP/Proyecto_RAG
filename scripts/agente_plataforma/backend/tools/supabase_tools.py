from google.adk.tools import FunctionTool


def save_dataset_metadata(filename: str, storage_path: str) -> dict:
    """
    Guarda metadata del dataset en Supabase.

    Parámetros:
    - filename: nombre original del archivo
    - storage_path: ruta en Supabase Storage
    """
    # Aquí después conectaremos Supabase real
    return {
        "status": "saved",
        "filename": filename,
        "storage_path": storage_path
    }


save_dataset_metadata_tool = FunctionTool(save_dataset_metadata)
