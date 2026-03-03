from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_orquestador


orchestrator_agent = LlmAgent(
    name="agente_orquestador",
    model="gemini-2.5-flash",
    instruction=instrucciones_agente_orquestador(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0
    )
)
