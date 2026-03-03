#Script que define el agente raíz para orquestar tareas de ciencia de datos

#-->Librerias 
from google.adk.agents import LlmAgent
from google.genai import types
from .prompts import instrucciones_agente_raiz
from .csv_tools import cargar_csv_tool
from .tools import analytics_agent_tool
from .tools import visualization_agent_tool

#-->Agente orquestador
def get_root_agent():
    return LlmAgent(
        name="data_science_root_agent",
        model="gemini-2.5-flash",
        instruction=instrucciones_agente_raiz(),
        tools=[
            cargar_csv_tool,
            analytics_agent_tool,
            visualization_agent_tool
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.01
        )
    )

root_agent = get_root_agent()
