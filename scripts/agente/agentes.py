import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ===============================
# CARGAR VARIABLES DE ENTORNO
# ===============================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY no encontrada")

# ADK usa esta variable internamente
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# ===============================
# CONFIGURACIÓN
# ===============================
MODEL = "gemini-2.5-flash"
APP_NAME = "dashboard-agente"
USER_ID = "usuario-demo"
SESSION_ID = "dashboard-session"

# ===============================
# AGENTE 1: ANALISTA
# ===============================
analista_agent = LlmAgent(
    name="agente_analista_diabetes",
    model=MODEL,
    instruction="""
Eres un analista de datos médicos.

Analiza un dataset de diabetes y produce SOLO JSON con:
- total_pacientes
- promedio_y
- promedio_bmi
- promedio_bp
"""
)

# ===============================
# AGENTE 2: DASHBOARD UI
# ===============================
dashboard_agent = LlmAgent(
    name="agente_dashboard_ui",
    model=MODEL,
    instruction="""
Eres un experto en dashboards web con React + Tailwind CSS.

Devuelve SOLO JSON con esta estructura:

{
  "title": "Dashboard de Diabetes",
  "kpis": [{ "label": "...", "value": number }],
  "charts": [
    {
      "type": "bar | scatter | line",
      "title": "...",
      "x": [...],
      "y": [...]
    }
  ]
}

Hazlo vistoso y profesional.
"""
)

# ===============================
# PIPELINE
# ===============================
def ejecutar_pipeline(ruta_csv: str, ruta_salida: str):

    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(ruta_csv)

    # ---- SESIÓN (AQUÍ ESTABA EL ERROR) ----
    session_service = InMemorySessionService()
    session_service.create_session_sync(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner_analista = Runner(
        agent=analista_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    runner_dashboard = Runner(
        agent=dashboard_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # -------- MENSAJE AL AGENTE 1 --------
    msg_analisis = types.Content(
        role="user",
        parts=[types.Part(
            text=f"Analiza el dataset de diabetes ubicado en: {ruta_csv}"
        )]
    )

    analisis_texto = ""

    for event in runner_analista.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=msg_analisis
    ):
        if event.is_final_response():
            analisis_texto = event.content.parts[0].text

    if not analisis_texto.strip():
        raise RuntimeError("❌ El agente analista no devolvió nada")

    # -------- MENSAJE AL AGENTE 2 --------
    msg_dashboard = types.Content(
        role="user",
        parts=[types.Part(text=analisis_texto)]
    )

    dashboard_texto = ""

    for event in runner_dashboard.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=msg_dashboard
    ):
        if event.is_final_response():
            dashboard_texto = event.content.parts[0].text

    if not dashboard_texto.strip():
        raise RuntimeError("❌ El agente dashboard no devolvió nada")

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(dashboard_texto)

    print("✅ Dashboard generado correctamente")
