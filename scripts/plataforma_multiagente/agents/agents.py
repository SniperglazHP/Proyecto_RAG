from google.adk.agents import LlmAgent
from google.adk.tools import Tool

def load_csv_tool(path: str) -> str:
    return f"CSV cargado desde {path}"

agente_analizador = LlmAgent(
    name="eda_full_control_agent",
    model="gemini-2.5-flash",
    description="Agente EDA con control total sobre un dataset CSV completo.",
    tools=[Tool(load_csv_tool)],
    instruction="""
Eres un agente experto en análisis exploratorio de datos.
Explica, analiza y responde claramente sobre datasets CSV.
"""
)
