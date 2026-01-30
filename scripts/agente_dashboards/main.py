#Este script es el encargado de ser el main pricipal

#-->Importar librerias
import asyncio
import json
import re
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agente_analizador_csv import agente_analizador
from agente_generador_dashboard import dashboard_agent

#-->Creacion de variables y cargar .env para el script
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

APP_NAME = "eda_dashboards"
USER_ID = "leonardo_test"
SESSION_EDA = "eda_session_001"
SESSION_DASHBOARD = "dashboard_session_001"
CSV_PATH = "data/Diabetes.csv"
OUTPUT_DIR = "resultado"
EDA_PATH = os.path.join(OUTPUT_DIR, "informe_eda.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

#-->Funcion que se encarga de extraer JSON limpio de un texto para posteriormente ser usado
def extract_json(text: str):
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        return json_match.group(1).strip()

    try:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return text[start:end + 1]
    except Exception:
        pass

    return None

#-->Funcion que se encarga de ejecutar los agentes de manera asíncrona y manejar la sesión
async def run_agent(runner, session_service, session_id, query):
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    if session is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state={}
        )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    final_text = ""

    #-->Contador de tokens
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message
    ):
        #-->Texto del agente
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    final_text += part.text.strip()

        #-->Metadatos de uso para el conteo de tokens
        if hasattr(event, "usage_metadata") and event.usage_metadata:
            prompt_tokens += event.usage_metadata.prompt_token_count or 0
            completion_tokens += event.usage_metadata.candidates_token_count or 0
            total_tokens += event.usage_metadata.total_token_count or 0

    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens
    }

    return final_text, usage

#-->Main principal que tiene la funcion de orquestar el pipeline completo
async def main():
    print("=== PIPELINE EDA --> DASHBOARD ===\n")
    session_service = InMemorySessionService()

    #-->Ejecutando Agente Analizador CSV
    print("-->Ejecutando Agente Analizador CSV")
    print(f"Archivo: {CSV_PATH}\n")

    eda_runner = Runner(
        agent=agente_analizador,
        app_name=APP_NAME,
        session_service=session_service
    )

    eda_query = f"""
Tienes acceso TOTAL al archivo CSV ubicado en:

{CSV_PATH}

La tool disponible te entregará TODO el contenido del dataset sin procesar.
Decide libremente qué análisis realizar.

Genera un informe EDA COMPLETO en formato JSON.
"""

    eda_resultado, eda_usage = await run_agent(
        eda_runner,
        session_service,
        SESSION_EDA,
        eda_query
    )

    if not eda_resultado:
        print("El agente EDA no devolvió contenido.")
        return

    clean_json = extract_json(eda_resultado)

    if not clean_json:
        print("No se pudo extraer JSON del EDA")
        print(eda_resultado)
        return

    try:
        parsed = json.loads(clean_json)
    except json.JSONDecodeError as e:
        print("-->JSON inválido")
        print(e)
        return

    with open(EDA_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    print("-->Informe EDA generado")
    print(f"Guardado en: {EDA_PATH}")

    print("\n-->CONSUMO DE TOKENS – AGENTE ANALIZADOR")
    print("-" * 40)
    print(f"Prompt tokens     : {eda_usage['prompt_tokens']}")
    print(f"Completion tokens : {eda_usage['completion_tokens']}")
    print(f"Total tokens      : {eda_usage['total_tokens']}")
    print("-" * 40)

    #-->Ejecutando Agente Generador de Dashboard
    print("\n-->Ejecutando Agente Generador de Dashboard\n")

    dashboard_runner = Runner(
        agent=dashboard_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    dashboard_query = f"""
Ya existe un informe EDA en:

{EDA_PATH}

Léelo usando tus tools disponibles.
Interpreta TODA la información.
Genera un dashboard en React que represente el análisis.
"""

    dashboard_resultado, dash_usage = await run_agent(
        dashboard_runner,
        session_service,
        SESSION_DASHBOARD,
        dashboard_query
    )

    if not dashboard_resultado:
        print("El agente de dashboard no devolvió contenido.")
        return

    print("-->Dashboard generado correctamente")

    print("\n-->CONSUMO DE TOKENS – AGENTE DASHBOARD")
    print("-" * 40)
    print(f"Prompt tokens     : {dash_usage['prompt_tokens']}")
    print(f"Completion tokens : {dash_usage['completion_tokens']}")
    print(f"Total tokens      : {dash_usage['total_tokens']}")
    print("-" * 40)

    print("\n-->Pipeline finalizado con éxito")

if __name__ == "__main__":
    asyncio.run(main())
