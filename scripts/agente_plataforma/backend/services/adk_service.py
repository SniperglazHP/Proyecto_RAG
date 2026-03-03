from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.agents import orquestador_agent
from config import APP_NAME, USER_ID


# Servicio de sesiones (memoria del agente)
session_service = InMemorySessionService()

# Runner CORRECTAMENTE inicializado
runner = Runner(
    agent=orquestador_agent,
    session_service=session_service
)


async def run_orchestrator(session_id: str, user_message: str) -> dict:
    """
    Ejecuta el agente orquestador con una sesión activa.
    """
    # Obtener o crear sesión
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    # Ejecutar el agente
    result = await runner.run(
        session=session,
        input=user_message
    )

    return {
        "response": result.output_text,
        "events": [e.type for e in result.events]
    }
