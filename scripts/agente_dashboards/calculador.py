#Script que se encarga de calcular los resultados del agente analizador (todavia hay que hacer mas pruebas)

#-->Importar librerias
import json
import pandas as pd
import numpy as np
import os

#-->Variables que se usaran en este script
CSV_PATH = "data/Diabetes.csv"
OUTPUT_DIR = "resultado"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "estadisticas_calculadas.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

#-->Funcion principal de calculo estadistico
def calcular_estadisticas(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    stats = {
        "dataset": {
            "filas": int(df.shape[0]),
            "columnas": int(df.shape[1]),
            "column_names": list(df.columns)
        },
        "tipos_de_datos": {
            col: str(df[col].dtype) for col in df.columns
        },
        "estadisticas_descriptivas": {},
        "distribuciones_categoricas": {},
        "skewness": {},
        "kurtosis": {},
        "correlacion_con_Y": {}
    }

    #-->Estadísticas descriptivas
    for col in numeric_cols:
        stats["estadisticas_descriptivas"][col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "media": float(df[col].mean()),
            "mediana": float(df[col].median()),
            "std": float(df[col].std()),
            "q1": float(df[col].quantile(0.25)),
            "q3": float(df[col].quantile(0.75))
        }

        stats["skewness"][col] = float(df[col].skew())
        stats["kurtosis"][col] = float(df[col].kurtosis())

    #-->Distribuciones categóricas
    for col in categorical_cols:
        stats["distribuciones_categoricas"][col] = (
            df[col].value_counts().to_dict()
        )

    #-->Correlación con variable objetivo (Y)
    if "Y" in df.columns:
        corr = df[numeric_cols].corr()["Y"].drop("Y")
        stats["correlacion_con_Y"] = corr.round(6).to_dict()

    return stats

#-->Ejecución directa
if __name__ == "__main__":
    print("=== CALCULANDO ESTADÍSTICAS DEL DATASET ===")

    resultado = calcular_estadisticas(CSV_PATH)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("Estadísticas calculadas correctamente")
    print(f"Archivo generado en: {OUTPUT_PATH}")
