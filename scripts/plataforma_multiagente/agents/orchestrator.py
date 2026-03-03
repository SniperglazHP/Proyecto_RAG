from google.adk.agents import Agent
from google.adk.tools import AgentTool

from agents.ingest_agent import get_ingest_agent
from agents.analysis_agent import get_analysis_agent
from agents.visualization_agent import get_visualization_agent
from agents.generation_agent import get_generation_agent

def get_orchestrator():
    return Agent(
        name="OrchestratorAgent",
        description="Coordina agentes de ciencia de datos",
        instructions="""
        Analiza la intención del usuario y decide qué agentes deben intervenir.
        Nunca hagas análisis directo.
        Siempre devuelve una respuesta final al usuario.
        """,
        tools=[
            AgentTool(agent=get_ingest_agent()),
            AgentTool(agent=get_analysis_agent()),
            AgentTool(agent=get_visualization_agent()),
            AgentTool(agent=get_generation_agent())
        ]
    )
