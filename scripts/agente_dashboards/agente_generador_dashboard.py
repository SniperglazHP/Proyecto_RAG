#Script que tiene la funcion de generar un dashboard React a partir de un informe EDA

#-->Importar librerias
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import os
from prompts import dashboard_generator_prompt

#-->Configuracion de rutas para guardar el script App.jsx
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "generated_dashboard")
SRC_DIR = os.path.join(DASHBOARD_DIR, "src")

#-->Primera funcion tool que lee el informe EDA que genero el agente analizador
def read_eda_report(path="resultado/informe_eda.json") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

#-->Segunda funcion tool que escribe el código React generado por el agente
def write_dashboard_code(app_code: str) -> str:
    os.makedirs(SRC_DIR, exist_ok=True)
    output_file = os.path.join(SRC_DIR, "App.jsx")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(app_code)
    return f"App.jsx generado correctamente en {output_file}"

#-->Funciones tool que el agente generador utilizara
read_eda_tool = FunctionTool(read_eda_report)
write_dashboard_tool = FunctionTool(write_dashboard_code)

#-->Agente generador
dashboard_agent = LlmAgent(
    name="dashboard_generator_agent",
    model="gemini-2.5-flash",
    description="Genera dashboards React interpretando un informe EDA.",
    tools=[read_eda_tool, write_dashboard_tool],
    instruction=dashboard_generator_prompt()
)
