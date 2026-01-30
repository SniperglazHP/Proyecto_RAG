"""
Script para correr el agente dashboard ADK con un archivo CSV de ejemplo.
"""

from .agente_dashboard_react import ejecutar_agente_dashboard

ejecutar_agente_dashboard(
    ruta_csv="scripts/agentes/data/Diabetes.csv",
    ruta_salida="scripts/agentes/frontend/public/dashboard.json"
)








#scripts/agentes/Carencias-Parsing.csv