from google.adk.tools import FunctionTool


def build_chart_config(chart_type: str, x: str, y: str) -> dict:
    """
    Construye la configuración de una gráfica para el frontend.

    Parámetros:
    - chart_type: bar, line, pie, etc.
    - x: columna eje X
    - y: columna eje Y
    """
    return {
        "chart_type": chart_type,
        "x_axis": x,
        "y_axis": y,
        "framework": "chartjs",
        "status": "ready"
    }


build_chart_config_tool = FunctionTool(build_chart_config)
