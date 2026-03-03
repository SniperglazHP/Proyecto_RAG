#Script que define herramientas basadas en agentes para análisis y visualización de datos    

#-->Librerias
from google.adk.tools.agent_tool import AgentTool
from .analytics_agent import analytics_agent
from .visualization_agent import get_visualization_agent

#-->Cracion de agenttools
analytics_agent_tool = AgentTool(
    agent=analytics_agent
)
visualization_agent_tool = AgentTool(
    agent=get_visualization_agent()
)