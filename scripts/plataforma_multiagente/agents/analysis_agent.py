from google.adk.agents import Agent
from tools.data_tools import basic_eda

def get_analysis_agent():
    return Agent(
        name="AnalysisAgent",
        description="Realiza análisis exploratorio de datos (EDA)",
        tools=[basic_eda]
    )
