import os
import json
import re
import pandas as pd
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# =====================
# CONFIGURACIÓN
# =====================
load_dotenv()

MODEL = "gemini-2.5-flash"
APP_NAME = "dashboard_agente"
USER_ID = "usuario_dashboard"
SESSION_ID = "session_dashboard"

# =====================
# RUTA BASE PROYECTO
# =====================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

# =====================
# UTILIDAD: EXTRAER JSON
# =====================
def extraer_json(texto: str) -> dict:
    """
    Extrae el primer bloque JSON válido desde un texto LLM.
    """
    if not texto or not texto.strip():
        raise ValueError("Respuesta del agente vacía")

    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if not match:
        raise ValueError(f"No se encontró JSON en la respuesta:\n{texto}")

    return json.loads(match.group())

# =====================
# AGENTE 1: ANALIZADOR
# =====================
analizador_agent = LlmAgent(
    name="agente_analizador_csv",
    model=MODEL,
    instruction="""
Responde EXCLUSIVAMENTE en JSON válido.
NO agregues texto, markdown ni explicaciones.

Estructura requerida:
{
  "descripcion": "",
  "columnas": {},
  "calidad_datos": [],
  "observaciones": []
}
""",
    description="Analiza estructura y calidad de datos CSV"
)

# =====================
# AGENTE 2: DASHBOARD
# =====================
dashboard_agent = LlmAgent(
    name="agente_generador_dashboard",
    model=MODEL,
    instruction="""
Responde EXCLUSIVAMENTE en JSON válido.
NO agregues texto, markdown ni comentarios.

Estructura requerida:
{
  "kpis": [],
  "graficas": [],
  "layout": {}
}
""",
    description="Genera especificación de dashboard"
)

# =====================
# FUNCIÓN PRINCIPAL
# =====================
def ejecutar_agente_dashboard(ruta_csv, ruta_salida):
    ruta_csv = os.path.join(BASE_DIR, ruta_csv)
    ruta_salida = os.path.join(BASE_DIR, ruta_salida)

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    # ---- carga CSV
    df = pd.read_csv(ruta_csv)

    resumen = {
        "columnas": list(df.columns),
        "tipos": df.dtypes.astype(str).to_dict(),
        "nulos": df.isnull().sum().to_dict(),
        "total_filas": len(df)
    }

    # ---- sesión ADK
    session_service = InMemorySessionService()
    session_service.create_session_sync(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner_analisis = Runner(
        agent=analizador_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    runner_dashboard = Runner(
        agent=dashboard_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # =====================
    # AGENTE 1
    # =====================
    mensaje_analisis = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps(resumen, ensure_ascii=False))]
    )

    analisis_texto = ""
    for event in runner_analisis.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=mensaje_analisis
    ):
        if event.is_final_response():
            analisis_texto = event.content.parts[0].text

    try:
        analisis_json = extraer_json(analisis_texto)
    except Exception as e:
        raise RuntimeError(f"❌ Error en agente analizador:\n{e}")

    # =====================
    # AGENTE 2
    # =====================
    mensaje_dashboard = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps(analisis_json, ensure_ascii=False))]
    )

    dashboard_texto = ""
    for event in runner_dashboard.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=mensaje_dashboard
    ):
        if event.is_final_response():
            dashboard_texto = event.content.parts[0].text

    try:
        dashboard_json = extraer_json(dashboard_texto)
    except Exception as e:
        raise RuntimeError(f"❌ Error en agente dashboard:\n{e}")

    # =====================
    # GUARDAR RESULTADO
    # =====================
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(dashboard_json, f, indent=2, ensure_ascii=False)

    print("✅ Dashboard generado correctamente")
    print(f"📁 Archivo: {ruta_salida}")
