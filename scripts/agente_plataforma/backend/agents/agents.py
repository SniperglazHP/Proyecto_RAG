# agents/agents.py

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from agents.prompts import (
    orquestador_prompt,
    ingestador_prompt,
    analizador_prompt,
    generador_prompt
)

from tools.data_tools import load_dataset_tool

from tools.supabase_tools import save_dataset_metadata_tool
from tools.visualization_tools import build_chart_config_tool

# ===============================
# AGENTE INGESTADOR
# ===============================
ingestador_agent = LlmAgent(
    name="data_ingestion_agent",
    model="gemini-2.5-flash",
    description="Agente encargado de validar y describir datasets.",
    tools=[load_dataset_tool],
    instruction=ingestador_prompt()
)


# ===============================
# AGENTE ANALIZADOR
# ===============================
analizador_agent = LlmAgent(
    name="eda_analysis_agent",
    model="gemini-2.5-flash",
    description="Agente EDA con control total sobre datasets estructurados.",
    tools=[load_dataset_tool],
    instruction=analizador_prompt()
)


# ===============================
# AGENTE GENERADOR
# ===============================
generador_agent = LlmAgent(
    name="dashboard_generator_agent",
    model="gemini-2.5-flash",
    description="Agente generador de dashboards y visualizaciones.",
    tools=[build_chart_config_tool],
    instruction=generador_prompt()
)


# ===============================
# AGENTE ORQUESTADOR
# ===============================
orquestador_agent = LlmAgent(
    name="orchestrator_agent",
    model="gemini-2.5-flash",
    description="Agente coordinador del sistema multiagente.",
    tools=[
        AgentTool(agent=ingestador_agent),
        AgentTool(agent=analizador_agent),
        AgentTool(agent=generador_agent)
    ],
    instruction=orquestador_prompt()
)
