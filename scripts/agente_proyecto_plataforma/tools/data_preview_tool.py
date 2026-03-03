import pandas as pd


def get_data_preview(file_path: str, rows: int = 10) -> dict:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Formato de archivo no soportado")

    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "sample": df.head(rows).to_dict(orient="records")
    }
