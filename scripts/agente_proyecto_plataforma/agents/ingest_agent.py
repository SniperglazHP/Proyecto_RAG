from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_ingestador


ingest_agent = LlmAgent(
    name="agente_ingestador",
    model="gemini-2.5-flash",
    instruction=instrucciones_agente_ingestador(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0
    )
)
