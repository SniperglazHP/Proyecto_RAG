import pandas as pd
from io import BytesIO

def load_csv(file_bytes):
    return pd.read_csv(BytesIO(file_bytes))

def load_excel(file_bytes):
    return pd.read_excel(BytesIO(file_bytes))

def basic_eda(df):
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "nulls": df.isnull().sum().to_dict(),
        "describe": df.describe(include="all").to_dict()
    }
