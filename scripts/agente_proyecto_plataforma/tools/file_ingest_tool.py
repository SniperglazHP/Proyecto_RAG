import pandas as pd


def process_uploaded_file(file_path: str) -> dict:
    """
    Lee un archivo CSV o Excel y devuelve metadata estructural
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Formato de archivo no soportado")

    metadata = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "preview": df.head(5).to_dict(orient="records")
    }

    return metadata
