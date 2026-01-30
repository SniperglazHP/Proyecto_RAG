"""
Este script se encarga de crear un agente y subagente utilizando Google ADK
"""

#-->Importar librerias
import os
import json
import asyncio
import pandas as pd
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

#-->Cargar el contenido de .env
load_dotenv()

#-->Constantes de configuración
APP_NAME = "dashboard_adk"
AGENT_NAME = "dashboard_agent"
USER_ID = "user_dashboard"
SESSION_ID = "session_dashboard_001"
MODEL = "gemini-2.5-flash"

#-->Rutas de salida del resultado del agente y subagente
BASE_PATH = os.path.dirname(__file__)
OUTPUT_JSON = os.path.join(BASE_PATH, "resultado_agente_adk.json")

#-->Subagente que se encarga de análisis y planeación
def subagente_planner(df: pd.DataFrame) -> dict:
    """
    Subagente unificado tipo PLANNER:
    - Analiza datos
    - Genera KPIs
    - Sugiere visualizaciones
    """

    total_registros = len(df)
    columnas = list(df.columns)
    nulos = df.isnull().sum().to_dict()

    columnas_vacias = [
        col for col, count in nulos.items() if count == total_registros
    ]

    porcentaje_nulos = round(
        (sum(nulos.values()) / (total_registros * len(columnas))) * 100, 2
    )

    calidad = "Alta"
    if porcentaje_nulos > 30:
        calidad = "Media"
    if porcentaje_nulos > 60:
        calidad = "Baja"

    return {
        "descripcion": "Subagente Planner (análisis + planeación)",
        "resumen_tecnico": {
            "total_registros": total_registros,
            "total_columnas": len(columnas),
            "columnas": columnas,
            "nulos_por_columna": nulos,
            "columnas_completamente_vacias": columnas_vacias,
            "porcentaje_nulos": f"{porcentaje_nulos}%",
            "calidad_datos": calidad,
        },
        "kpis": [
            {
                "nombre": "Total de registros",
                "valor": total_registros,
                "descripcion": "Número total de filas del dataset"
            },
            {
                "nombre": "Total de columnas",
                "valor": len(columnas),
                "descripcion": "Número total de columnas del CSV"
            },
            {
                "nombre": "Porcentaje de nulos",
                "valor": f"{porcentaje_nulos}%",
                "descripcion": "Proporción de datos faltantes"
            }
        ],
        "visualizaciones_sugeridas": [
            {
                "tipo": "KPI",
                "descripcion": "Indicador del tamaño del dataset"
            },
            {
                "tipo": "Tabla",
                "descripcion": "Vista general de columnas y estructura"
            },
            {
                "tipo": "Barras",
                "descripcion": "Valores nulos por columna"
            }
        ]
    }

#-->Agente principal que se encarga de generar dashboards ejecutivos
dashboard_agent = LlmAgent(
    name=AGENT_NAME,
    model=MODEL,
    instruction="""
Eres un agente experto en análisis de datos y diseño de dashboards ejecutivos.

A partir de un análisis técnico previo:
- Genera hallazgos claros
- Propón decisiones estratégicas
- Da recomendaciones orientadas a dashboards y gestión de datos

Responde en texto claro y estructurado.
""",
    description="Agente principal de análisis y dashboards"
)

#-->En esta parte se configura el runner (el runner sirve para ejecutar el agente) y el servicio de sesiones (el servicio de sesiones sirve para manejar las sesiones de los usuarios)
session_service = InMemorySessionService()
runner = Runner(
    agent=dashboard_agent,
    app_name=APP_NAME,
    session_service=session_service
)

#-->Función para ejecutar el agente principal con el subagente planner
async def ejecutar_agente(ruta_csv: str):
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    df = pd.read_csv(ruta_csv)
    resultado_planner = subagente_planner(df)
    prompt = f"""
ANÁLISIS TÉCNICO Y PLANNER:

{json.dumps(resultado_planner, indent=2)}

Genera:
1. Hallazgos ejecutivos
2. Decisiones estratégicas
3. Recomendaciones para dashboards
"""

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
    respuesta_final = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                respuesta_final = event.content.parts[0].text

    resultado = {
        "agente_principal": {
            "nombre": AGENT_NAME,
            "rol": "Orquestador y generador de insights",
            "modelo": MODEL
        },
        "subagente_planner": resultado_planner,
        "resultado_llm": respuesta_final
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print("Resultado guardado en:", OUTPUT_JSON)

#-->Ejecutar el agente si se corre este script directamente
if __name__ == "__main__":
    asyncio.run(
        ejecutar_agente("scripts/agentes/Diabetes.csv")
    )
