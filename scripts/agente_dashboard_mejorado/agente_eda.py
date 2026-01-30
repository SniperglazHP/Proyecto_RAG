#Script que tiene la funcion de crear un agente analizador asi como configurar su herramienta

#-->Importar librerias
import json
import pandas as pd
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

#-->Funcion principal de la tool donde tiene el objetivo de generar
def inspect_google_sheet(spreadsheet_id: str, sheet_name: str) -> str:

    csv_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    )

    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        return json.dumps({
            "error": "No se pudo cargar el Google Sheet",
            "detalle": str(e)
        }, ensure_ascii=False)

    numeric_cols = df.select_dtypes(include="number").columns.tolist() #Aqui se toma en cuenta
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    #-->En esta parte se calculan las estadísticas, outliers, datos faltantes y columnas de baja varianza
    stats = {}
    outliers = {}
    missing_data = {}
    low_variance = []

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        mask_outliers = (df[col] < lower) | (df[col] > upper)
        outlier_rows = df.loc[mask_outliers, col]

        variance = df[col].var()

        stats[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "std": float(df[col].std()),
            "q1": float(q1),
            "q3": float(q3),
            "skewness": float(df[col].skew()),
            "kurtosis": float(df[col].kurtosis()),
            "unique_values": int(df[col].nunique())
        }

        outliers[col] = {
            "cantidad": int(mask_outliers.sum()),
            "porcentaje": round(mask_outliers.sum() / len(df) * 100, 2),
            "valores_exactos": outlier_rows.round(4).tolist(),
            "indices_fila": outlier_rows.index.tolist()
        }

        missing_data[col] = {
            "faltantes": int(df[col].isna().sum()),
            "porcentaje": round(df[col].isna().mean() * 100, 2)
        }

        if variance < 0.01:
            low_variance.append(col)

    corr_matrix = df[numeric_cols].corr().round(2)

    strong_correlations = []
    for i in corr_matrix.columns:
        for j in corr_matrix.columns:
            if i != j and abs(corr_matrix.loc[i, j]) >= 0.8:
                strong_correlations.append({
                    "var_1": i,
                    "var_2": j,
                    "correlation": float(corr_matrix.loc[i, j])
                })

    return json.dumps({
        "dataset": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        },
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "statistics": stats,
        "outliers": outliers,
        "missing_data": missing_data,
        "low_variance_columns": low_variance,
        "correlations": corr_matrix.to_dict(),
        "strong_correlations": strong_correlations
    }, ensure_ascii=False, indent=2)

inspect_tool = FunctionTool(inspect_google_sheet)

eda_agent = LlmAgent(
    name="eda_google_sheets_agent",
    model="gemini-2.5-flash",
    description="Agente EDA avanzado con control total del dataset y razonamiento analítico.",
    instruction="""
REGLAS CLAVE:
- Usa inspect_google_sheet SOLO para obtener datos.
- NO copies el JSON literalmente.
- Justifica todo con números reales.

GENERA un INFORME EDA AVANZADO que incluya:

1. Resumen general del dataset
2. Tipos de variables y estructura
3. Calidad de los datos (faltantes, variabilidad)
4. Estadísticas descriptivas avanzadas
5. Análisis de distribuciones (asimetría y curtosis)
6. Outliers (mostrar valores exactos y su impacto)
7. Correlaciones fuertes y riesgos de multicolinealidad
8. Interpretación analítica profunda
9. Riesgos y limitaciones del dataset
10. Aplicaciones reales del dataset:
   - Salud
   - Modelos predictivos
   - Apoyo a decisiones
   - Investigación y política pública
11. Conclusiones finales claras y defendibles

FORMATO:
Devuelve SOLO JSON con raíz "informe_eda".
""",
    tools=[inspect_tool]
)
