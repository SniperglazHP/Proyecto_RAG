#Script que tiene la funcion de analizar datos para obtener insights y demas

#-->Librerias
from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_analitico

#-->Agente analizador
analytics_agent = LlmAgent(
    name="agente_analitico",
    model="gemini-2.5-flash",
    instruction=instrucciones_agente_analitico(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.01
    )
)
