from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_generador


generation_agent = LlmAgent(
    name="agente_generador",
    model="gemini-2.5-flash",
    instruction=instrucciones_agente_generador(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1
    )
)
