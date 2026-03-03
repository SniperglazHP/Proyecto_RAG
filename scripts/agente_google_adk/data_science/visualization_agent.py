#Script que tiene la funcion de generar visualizaciones a partir de datos

#-->Librerias
from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_visualizador
from .plot_tool import grafica_tool

#-->Agente visualizador
def get_visualization_agent():
    return LlmAgent(
        name="visualization_agent",
        model="gemini-2.5-flash",
        instruction=instrucciones_agente_visualizador(),
        tools=[grafica_tool],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.0
        )
    )
