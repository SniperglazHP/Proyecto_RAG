from google.adk.agents import Agent
from tools.visualization_tools import bar_plot

def get_visualization_agent():
    return Agent(
        name="VisualizationAgent",
        description="Genera visualizaciones para ciencia de datos",
        tools=[bar_plot]
    )
