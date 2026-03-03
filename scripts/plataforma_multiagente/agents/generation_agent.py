from google.adk.agents import Agent

def get_generation_agent():
    return Agent(
        name="GenerationAgent",
        description="Explica los resultados del análisis en lenguaje natural",
        system_prompt="""
        Eres un científico de datos experto.
        Explica los resultados de forma clara, concisa y comprensible
        para usuarios no técnicos.
        """
    )

