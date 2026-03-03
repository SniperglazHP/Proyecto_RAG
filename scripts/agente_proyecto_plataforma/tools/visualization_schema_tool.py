def build_chart_schema(chart_type: str, x: str, y: str, data: list) -> dict:
    """
    Devuelve un esquema genérico que React puede renderizar
    """

    return {
        "type": chart_type,
        "x_axis": x,
        "y_axis": y,
        "data": data
    }
