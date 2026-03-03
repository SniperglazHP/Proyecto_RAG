import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.orchestrator_agent import orchestrator_agent
from .config import APP_NAME, USER_ID

# Servicio de sesión (vive mientras el backend está activo)
session_service = InMemorySessionService()

async def handle_chat_async(message: str) -> str:
    runner = Runner(
        agent=orchestrator_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    session_id = "chat_session"

    # Crear mensaje del usuario
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=message)]
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
                    final_text += part.text

    return final_text.strip()


def handle_chat(message: str) -> str:
    return asyncio.run(handle_chat_async(message))
