from scripts.agente.agentes import ejecutar_pipeline

if __name__ == "__main__":
    ejecutar_pipeline(
        ruta_csv="scripts/agente/data/Diabetes.csv",
        ruta_salida="scripts/agente/output/dashboard_ui.json"
    )
