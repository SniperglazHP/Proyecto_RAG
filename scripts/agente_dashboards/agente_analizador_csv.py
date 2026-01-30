#Script que tiene la funcion de analizar un archivo CSV y generar un informe EDA en formato JSON

#-->Importar librerias
import json
import pandas as pd
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

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
    instruction="""
REGLAS CLAVE:
- Usa la tool SOLO para obtener el dataset completo.
- NO copies el contenido crudo del CSV en la respuesta.
- El análisis, selección de métricas y conclusiones deben ser decisiones del agente.
- Usa valores numéricos reales y explícitos.
- El resultado será consumido posteriormente por un AGENTE GENERADOR DE DASHBOARDS.

OBJETIVO:
Generar un INFORME EDA AVANZADO, estructurado y orientado a visualización,
que sirva como contrato de datos para la construcción de dashboards interactivos.

INCLUYE LAS SIGUIENTES SECCIONES EN EL JSON:

1. Resumen general del dataset
   - Dimensiones
   - Tipos de datos
   - Descripción semántica de columnas

2. Calidad de datos
   - Valores nulos
   - Rangos, dispersión y estabilidad
   - Problemas potenciales de interpretación

3. Análisis estadístico relevante
   - Distribuciones
   - Sesgo (skewness) y curtosis
   - Estadísticas descriptivas clave

4. Relaciones importantes
   - Variables más influyentes sobre la variable objetivo
   - Relaciones fuertes entre características
   - Variables redundantes o altamente correlacionadas

5. KPIs sugeridos para dashboards
   - Métricas clave que deberían mostrarse como indicadores
   - Valores promedio, máximos, mínimos o porcentajes relevantes

6. Segmentaciones recomendadas
   - Segmentaciones útiles (edad, sexo, rangos de riesgo, etc.)
   - Justificación analítica de cada segmentación

7. Recomendaciones de visualización
   - Tipo de gráfico recomendado por análisis
   - Variables sugeridas para eje X / eje Y
   - Objetivo analítico de cada visualización

8. Insights accionables del mundo real
   - Salud pública
   - Atención clínica
   - Investigación
   - Educación / prevención

9. Casos de uso analíticos y predictivos
   - Modelos potenciales
   - Clustering
   - Simulación de escenarios

10. Conclusiones finales

FORMATO:
- Devuelve SOLO JSON
- Raíz del documento: "informe_eda"
- Usa claves claras y estructuradas
- Piensa en que otro agente automatizado consumirá este JSON
"""
)
