"""
Agente de postprocesamiento para mejorar respuestas generadas por el sistema RAG.
Usa OpenAI Agents SDK (oficial).
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

MODEL_NAME = os.getenv("LLM_MODEL", "gpt-5-mini")

# ===============================
# Crear el agente
# ===============================

agente_postprocesador = Agent(
    name="AgentePostprocesadorRAG",
    model=MODEL_NAME,
    instructions=(
        "Eres un agente encargado de mejorar respuestas generadas por un sistema RAG. "
        "Tu tarea es mejorar la claridad, coherencia y redacción de la respuesta, "
        "sin agregar información nueva ni inventar datos. "
        "Debes basarte únicamente en el contexto proporcionado."
    ),
)

# ===============================
# Ejecutar el agente (ASYNC)
# ===============================

async def ejecutar_agente_postprocesamiento(
    pregunta: str,
    contexto: str,
    respuesta_base: str
) -> str:
    """
    Ejecuta el agente de postprocesamiento y devuelve la respuesta mejorada.
    """

    prompt = (
        f"PREGUNTA:\n{pregunta}\n\n"
        f"CONTEXTO:\n{contexto}\n\n"
        f"RESPUESTA BASE:\n{respuesta_base}\n\n"
        "INSTRUCCIONES: Mejora la respuesta sin inventar información."
    )

    resultado = await Runner.run(
        agente_postprocesador,
        prompt
    )

    # 🔴 AQUÍ ESTABA EL ERROR
    texto_final = resultado.final_output

    if not texto_final or not isinstance(texto_final, str):
        return respuesta_base

    return f"Respuesta_Mejorada:\n{texto_final.strip()}"
