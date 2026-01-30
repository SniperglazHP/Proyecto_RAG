#Script main que tiene la funcion de ejecutar los agentes con sus respectivas herramientas

#-->Importar librerias
import asyncio
import json
import re
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agente_eda import eda_agent

#-->Configuracion basica
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
APP_NAME = "eda_dashboard_mejorado"
USER_ID = "leonardo_test"

#-->Funcion que se encarga de hacer una extraccion de JSON desde texto para evitar errores de formato
def extract_json(text):
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        return json_match.group(1).strip()
    try:
        start_idx = text.find('{')
        if start_idx != -1:
            end_idx = text.rfind('}')
            if end_idx != -1:
                return text[start_idx:end_idx + 1]
    except Exception:
        pass
    return None

#-->Funcion que tiene la funcion de configurar 
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
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    final_text += part.text.strip()
    return final_text

#-->Funcion que se encarga de ejecutar el agente con sesiones
async def main():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=eda_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    spreadsheet_id = "1D-ipQVMfcNCGHPsP7oeRVrR4VCcUCy081n2doPuuBug"
    sheet_name = "Diabetes"

    output_dir = "resultado"
    output_path = os.path.join(output_dir, "informe_eda.json")
    os.makedirs(output_dir, exist_ok=True)

    print("=== INICIANDO ANÁLISIS EDA ===")
    print(f"Spreadsheet ID: {spreadsheet_id}")
    print(f"Hoja: {sheet_name}\n")
    query = f"""
Realiza un análisis exploratorio completo (EDA) del dataset almacenado en Google Sheets.

SPREADSHEET_ID: {spreadsheet_id}
SHEET_NAME: {sheet_name}

Sigue todas tus instrucciones internas y genera el informe estructurado.
"""
    resultado = await run_agent(
        runner,
        session_service,
        "eda_session_001",
        query
    )
    if not resultado:
        print("El agente no devolvió contenido.")
        return

    clean_json = extract_json(resultado)

    if not clean_json:
        print("No se pudo extraer JSON del resultado")
        print(resultado)
        return
    try:
        parsed = json.loads(clean_json)
    except json.JSONDecodeError as e:
        print("JSON inválido tras limpieza")
        print(e)
        print(clean_json)
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    print("Informe EDA generado correctamente")
    print(f"Guardado en: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())