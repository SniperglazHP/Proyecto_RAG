#Script principal del motor de generación de visualizaciones, que se encarga de interpretar las solicitudes del usuario, planificar las visualizaciones adecuadas basadas en el análisis del dataset y generar gráficos útiles y relevantes para la toma de decisiones, integrándose con los agentes de análisis y explicación para proporcionar una experiencia completa y coherente al usuario.

#-->Librerias
import base64
import io
from typing import Any, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec

#-->Constantes y configuraciones para la generación de visualizaciones
SUPPORTED_CHARTS = {"bar", "line", "scatter", "histogram", "box", "pie"}
_BG, _AX_BG = "#F5F7FB", "#FFFFFF"
_C = {"blue": "#2563EB", "purple": "#7C3AED", "green": "#059669", "orange": "#EA580C", "red": "#DC2626", "teal": "#0D9488"}

#-->Función auxiliar para normalizar texto
def _norm(t: str) -> str:
    return " ".join((t or "").lower().split())

#-->Funcion para detectar el tipo de gráfico solicitado por el usuario a partir de su mensaje
def detect_chart_type(message: str) -> Optional[str]:
    m = _norm(message)
    for k, v in {
        "bar": ["barra", "barras", "bar"],
        "line": ["linea", "línea", "line"],
        "scatter": ["scatter", "dispers"],
        "histogram": ["histograma", "histogram"],
        "box": ["box", "caja", "boxplot"],
        "pie": ["pie", "pastel", "torta"],
    }.items():
        if any(x in m for x in v):
            return k
    return None

#-->Funcion para determinar si el usuario quiere incluir todas las columnas en la visualización
def wants_all_columns(message: str) -> bool:
    m = _norm(message)
    return any(k in m for k in ["todas las columnas", "todas las variables", "all columns", "todo el dataset"])

#-->Funcion para identificar qué columnas del dataset son mencionadas en el mensaje del usuario, lo que ayuda a priorizar esas columnas en la generación de visualizaciones y análisis.
def mentioned_columns(message: str, columns: list[str]) -> list[str]:
    m = _norm(message)
    return [c for c in columns if c.lower() in m]

#-->Funcion interna para identificar columnas numéricas en el dataset
def _numeric(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include="number").columns.tolist()

#-->Funcion interna para identificar columnas continuas en el dataset
def _continuous(df: pd.DataFrame) -> list[str]:
    out = []
    for c in _numeric(df):
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        if s.nunique() >= 12:
            out.append(c)
    return out

#-->Funcion _pick_cols para seleccionar las columnas más adecuadas para cada tipo de gráfico
def _pick_cols(chart_type: str, df: pd.DataFrame, preferred: list[str]) -> tuple[str, str]:
    num, cont = _numeric(df), _continuous(df)
    cat = [c for c in df.columns if c not in num]
    pnum, pcat = [c for c in preferred if c in num], [c for c in preferred if c in cat]

    if chart_type == "bar":
        return (pcat[0] if pcat else (cat[0] if cat else df.columns[0]), pnum[0] if pnum else (num[0] if num else ""))
    if chart_type == "line":
        base = pnum if len(pnum) >= 2 else (cont if len(cont) >= 2 else num)
        return (base[0], base[1]) if len(base) >= 2 else (df.columns[0], num[0] if num else "")
    if chart_type == "scatter":
        base = [c for c in pnum if c in cont] if len([c for c in pnum if c in cont]) >= 2 else cont
        return (base[0], base[1]) if len(base) >= 2 else ((num[0], num[1]) if len(num) >= 2 else (df.columns[0], ""))
    if chart_type in {"histogram", "box"}:
        return ((pnum[0] if pnum else (cont[0] if cont else (num[0] if num else df.columns[0]))), "")
    if chart_type == "pie":
        return (pcat[0] if pcat else (cat[0] if cat else df.columns[0]), pnum[0] if pnum else (num[0] if num else ""))
    return (df.columns[0], "")

#-->Funcion plan_visualization para planificar la visualización adecuada según la solicitud del usuario, el contexto del dataset y el informe EDA generado por el agente de análisis, integrando la información proporcionada por el agente de visualización para generar gráficos relevantes y útiles para la toma de decisiones.
def plan_visualization(message: str, dataset: dict[str, Any], df: pd.DataFrame, model_config: dict[str, Any]) -> dict[str, Any]:
    cfg = dict(model_config or {})
    req = detect_chart_type(message)
    if req:
        cfg["chart_type"] = req
    t = str(cfg.get("chart_type", "bar")).lower().strip()
    if t not in SUPPORTED_CHARTS:
        t = "bar"

    x, y = _pick_cols(t, df, mentioned_columns(message, dataset["columns"]))
    cfg.update({"chart_type": t, "x": x, "y": "" if t in {"histogram", "box"} else y})
    cfg["scope"] = "all_columns" if t == "bar" and (wants_all_columns(message) or x == y) else "focused"
    return cfg

#-->Funcion _style para aplicar un estilo consistente a las visualizaciones generadas
def _style(ax: plt.Axes) -> None:
    ax.set_facecolor(_AX_BG)
    ax.grid(alpha=0.2, linestyle="--")

#-->Funcion _safe_bar para generar un gráfico de barras de manera segura, manejando casos donde los datos pueden estar vacíos o no ser relevantes, y proporcionando mensajes informativos en esos casos.
def _safe_bar(ax: plt.Axes, series: pd.Series, title: str, color: str, ylabel: str = "") -> None:
    _style(ax)
    if series.empty or float(series.fillna(0).sum()) == 0:
        ax.text(0.5, 0.5, "Sin datos relevantes", ha="center", va="center", color="#6B7280")
        ax.set_title(title)
        return
    series.plot(kind="bar", ax=ax, color=color)
    ax.set_title(title)
    if ylabel:
        ax.set_ylabel(ylabel)

#-->Funcion _safe_hist para generar un histograma de manera segura, manejando casos donde los datos pueden no ser numéricos o estar vacíos, y proporcionando mensajes informativos en esos casos.
def _safe_hist(ax: plt.Axes, series: pd.Series, title: str, color: str) -> None:
    _style(ax)
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        ax.text(0.5, 0.5, "Sin datos numéricos suficientes", ha="center", va="center", color="#6B7280")
        ax.set_title(title)
        return
    s.plot(kind="hist", bins=25, ax=ax, color=color, alpha=0.9)
    ax.set_title(title)

#-->Funcion _safe_scatter para generar un gráfico de dispersión de manera segura, manejando casos donde las columnas especificadas pueden no existir o no ser numéricas
def _safe_scatter(ax: plt.Axes, df: pd.DataFrame, x: str, y: str, title: str, color: str) -> None:
    _style(ax)
    if x not in df.columns or y not in df.columns:
        ax.text(0.5, 0.5, "No se pudo construir relación", ha="center", va="center", color="#6B7280")
        ax.set_title(title)
        return
    df.plot.scatter(x=x, y=y, ax=ax, color=color, alpha=0.7)
    ax.set_title(title)

#-->Funcion render_chart para generar la visualización solicitada por el usuario en formato de imagen codificada en base64, que se puede mostrar fácilmente en interfaces web como Streamlit.
def render_chart(df: pd.DataFrame, config: dict[str, Any]) -> str:
    t, x, y, scope = (str(config.get("chart_type", "bar")).lower().strip(), str(config.get("x", "")).strip(), str(config.get("y", "")).strip(), str(config.get("scope", "focused")))
    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor=_BG)
    _style(ax)

    if t == "bar" and scope == "all_columns":
        n = max(len(df), 1)
        pd.DataFrame({"% no nulos": df.notna().mean() * 100, "% valores únicos": (df.nunique(dropna=False) / n * 100).clip(upper=100)}).sort_values("% valores únicos", ascending=False).plot(kind="bar", ax=ax, color=[_C["blue"], _C["purple"]], width=0.85)
        ax.set_title("Perfil general por columna")
        ax.set_ylabel("Porcentaje")
        ax.set_ylim(0, 105)
    elif t == "bar":
        if x not in df.columns:
            raise ValueError(f"La columna '{x}' no existe para bar chart.")
        if y and y in df.columns:
            df.groupby(x, dropna=False)[y].mean().sort_values(ascending=False).head(20).plot(kind="bar", ax=ax, color=_C["blue"])
            ax.set_ylabel(f"Promedio de {y}")
        else:
            df[x].value_counts(dropna=False).head(20).plot(kind="bar", ax=ax, color=_C["blue"])
            ax.set_ylabel("Frecuencia")
        ax.set_xlabel(x)
        ax.set_title(f"Bar chart: {x} vs {y or 'frecuencia'}")
    elif t == "line":
        if not (y and y in df.columns):
            raise ValueError("Line chart requiere columna y válida.")
        (df.plot(x=x, y=y, ax=ax, color=_C["orange"]) if x in df.columns else df[y].head(150).reset_index(drop=True).plot(ax=ax, color=_C["orange"]))
        ax.set_title(f"Line chart: {x or 'índice'} vs {y}")
    elif t == "scatter":
        if x not in df.columns or y not in df.columns:
            raise ValueError("Scatter requiere columnas x e y válidas.")
        df.plot.scatter(x=x, y=y, ax=ax, color=_C["green"], alpha=0.7)
        ax.set_title(f"Scatter: {x} vs {y}")
    elif t == "histogram":
        if x not in df.columns:
            raise ValueError(f"La columna '{x}' no existe para histogram.")
        pd.to_numeric(df[x], errors="coerce").dropna().plot(kind="hist", bins=30, ax=ax, color=_C["purple"])
        ax.set_title(f"Histograma: {x}")
    elif t == "box":
        if x not in df.columns:
            raise ValueError(f"La columna '{x}' no existe para box plot.")
        s = pd.to_numeric(df[x], errors="coerce").dropna()
        if s.empty:
            raise ValueError(f"La columna '{x}' no tiene valores numéricos para box plot.")
        ax.boxplot(s)
        ax.set_xticklabels([x])
        ax.set_title(f"Box plot: {x}")
    elif t == "pie":
        if x not in df.columns:
            raise ValueError(f"La columna '{x}' no existe para pie chart.")
        ((df.groupby(x, dropna=False)[y].mean().sort_values(ascending=False).head(10) if (y and y in df.columns) else df[x].value_counts(dropna=False).head(10)).plot(kind="pie", ax=ax, autopct="%1.1f%%"))
        ax.set_ylabel("")
        ax.set_title(f"Pie chart: {x}")

    fig.tight_layout()
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(b.getvalue()).decode("utf-8")

#-->Funcion _to_b64 para convertir una figura de Matplotlib a una cadena codificada en base64, lo que permite su fácil transmisión y visualización en interfaces web.
def _to_b64(fig: plt.Figure) -> str:
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(b.getvalue()).decode("utf-8")

#-->Funcion _first_col para seleccionar la primera columna que coincida con una lista de palabras clave
def _first_col(columns: list[str], keywords: list[str]) -> Optional[str]:
    return next((c for c in columns if any(k in c.lower() for k in keywords)), None)

#-->Funcion _best_scatter_pair para identificar el mejor par de columnas para un gráfico de dispersión basado en las correlaciones detectadas en el análisis del dataset
def _best_scatter_pair(df: pd.DataFrame, analysis: dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
    cont, top = _continuous(df), analysis.get("top_correlations", [])
    for p in top:
        if p["x"] in cont and p["y"] in cont:
            return p["x"], p["y"]
    return (cont[0], cont[1]) if len(cont) >= 2 else (None, None)

#-->Funcion _new_card para crear una tarjeta de dashboard con un título, descripción, figura y descripciones de las gráficas
def _new_card(title: str, desc: str, fig: plt.Figure, pdsc: list[dict[str, str]]) -> dict[str, Any]:
    return {"title": title, "description": desc, "plot_descriptions": pdsc, "image_base64": _to_b64(fig)}

#-->Funcion principal que se encarga de construir las tarjetas del dashboard basándose en el análisis del dataset, generando visualizaciones relevantes y explicaciones para cada una de ellas, y organizándolas de manera coherente para facilitar la interpretación por parte del usuario.
def build_dashboard_cards(df: pd.DataFrame, analysis: dict[str, Any]) -> list[dict[str, Any]]:
    num, cat = analysis.get("numeric_columns", []), analysis.get("categorical_columns", [])
    defs, ctx = analysis.get("column_definitions", {}), analysis.get("dataset_context", {})
    insights, uses, recs, kpis = analysis.get("insights", []), analysis.get("real_world_uses", []), analysis.get("recommendations", []), analysis.get("kpis_suggested", [])
    cards = []

    # 1) Resumen + calidad
    f1 = plt.figure(figsize=(15, 9), facecolor=_BG); g1 = GridSpec(2, 2, figure=f1)
    a1, a2, a3, a4 = [f1.add_subplot(g1[i, j]) for i in range(2) for j in range(2)]
    for a in (a2, a3, a4): _style(a)
    p1 = []
    a1.axis("off")
    a1.text(0.02, 0.88, "Resumen Ejecutivo", fontsize=14, fontweight="bold", color="#1E3A8A")
    a1.text(0.02, 0.70, f"Dominio detectado: {ctx.get('domain_label','general')}", fontsize=11, color="#374151")
    a1.text(0.02, 0.52, analysis.get("summary", ""), fontsize=10, color="#111827", wrap=True)
    p1.append({"plot": "Resumen ejecutivo", "text": "Presenta contexto y objetivo analítico del dataset."})
    _safe_bar(a2, pd.Series({k["name"]: float(k.get("value", 0)) for k in (kpis[:5] or [{"name": "filas", "value": len(df)}, {"name": "columnas", "value": df.shape[1]}])}), "KPIs sugeridos", _C["purple"], "Valor")
    p1.append({"plot": "KPIs", "text": "Concentra indicadores clave para seguimiento ejecutivo."})
    s = _first_col(df.columns.tolist(), ["sex", "gender", "genero", "género"])
    if s:
        df[s].astype(str).value_counts(dropna=False).head(8).plot(kind="pie", ax=a3, autopct="%1.1f%%")
        a3.set_ylabel(""); a3.set_title(f"Distribución por {s}")
        p1.append({"plot": f"Distribución por {s}", "text": f"Representa proporciones de '{s}' ({defs.get(s, {}).get('meaning','segmentación')})."})
    else:
        c = cat[0] if cat else df.columns[0]
        _safe_bar(a3, df[c].astype(str).value_counts(dropna=False).head(10), f"Top categorías: {c}", _C["blue"], "Frecuencia")
        p1.append({"plot": f"Top categorías ({c})", "text": "Muestra los segmentos más frecuentes."})
    miss = (df.isna().mean() * 100).sort_values(ascending=False).head(10)
    _safe_bar(a4, miss if miss.sum() > 0 else (df.nunique(dropna=False) / max(len(df), 1) * 100).sort_values(ascending=False).head(10), "Calidad: faltantes o cardinalidad", _C["red"], "%")
    p1.append({"plot": "Calidad", "text": "Evalúa faltantes o, si no existen, diversidad por columna."})
    f1.suptitle("Dashboard 1: Resumen Ejecutivo y Calidad", fontsize=15, fontweight="bold", color="#1F2937")
    f1.tight_layout(rect=[0, 0, 1, 0.97])
    cards.append(_new_card("Dashboard 1: Resumen Ejecutivo y Calidad", "Vista general orientada a decisiones.", f1, p1))

    # 2) Distribuciones y tendencias
    f2, axs2 = plt.subplots(2, 2, figsize=(14, 9), facecolor=_BG); b1, b2, b3, b4 = axs2.flatten(); [ _style(a) for a in (b1,b2,b3,b4) ]
    p2 = []
    if num: _safe_hist(b1, df[num[0]], f"Distribución: {num[0]}", _C["green"]); p2.append({"plot": f"Distribución {num[0]}", "text": "Muestra concentración y dispersión."})
    else: _safe_bar(b1, df[df.columns[0]].astype(str).value_counts(dropna=False).head(12), f"Frecuencia: {df.columns[0]}", _C["green"], "Frecuencia")
    x, y = _best_scatter_pair(df, analysis)
    if x and y: _safe_scatter(b2, df, x, y, f"Tendencia: {x} vs {y}", _C["purple"]); p2.append({"plot": "Relación numérica", "text": f"Relación entre {x} y {y}."})
    elif num: pd.to_numeric(df[num[0]], errors="coerce").dropna().head(150).reset_index(drop=True).plot(ax=b2, color=_C["purple"]); b2.set_title(f"Tendencia por índice: {num[0]}")
    else: _safe_bar(b2, df.nunique(dropna=False).sort_values(ascending=False).head(10), "Cardinalidad por columna", _C["purple"], "Valores únicos")
    out = analysis.get("outliers", {})
    _safe_bar(b3, (pd.Series({k: v["outlier_count"] for k, v in out.items()}).sort_values(ascending=False).head(10) if out else (df.nunique(dropna=False) / max(len(df), 1) * 100).sort_values(ascending=False).head(10)), "Outliers o cardinalidad", _C["teal"], "Conteo/%")
    p2.append({"plot": "Señales de variación", "text": "Indica atípicos o diversidad por variable."})
    focal = _first_col(df.columns.tolist(), ["imc", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6", "glucose", "glucosa"]) or (num[-1] if num else None)
    if focal: _safe_hist(b4, df[focal], f"Variable focal: {focal}", _C["orange"]); p2.append({"plot": "Variable focal", "text": f"Detalle de {focal} ({defs.get(focal, {}).get('meaning','clave')})."})
    else: _safe_bar(b4, df[df.columns[0]].astype(str).value_counts(dropna=False).head(10), f"Frecuencia: {df.columns[0]}", _C["orange"], "Frecuencia")
    f2.suptitle("Dashboard 2: Distribuciones y Tendencias", fontsize=15, fontweight="bold", color="#1F2937")
    f2.tight_layout(rect=[0, 0, 1, 0.97])
    cards.append(_new_card("Dashboard 2: Distribuciones y Tendencias", "Comportamiento estadístico de variables clave.", f2, p2))

    # 3) Relaciones y segmentación
    f3, axs3 = plt.subplots(2, 2, figsize=(14, 9), facecolor=_BG); c1, c2, c3, c4 = axs3.flatten(); [ _style(a) for a in (c1,c2,c3,c4) ]
    p3 = []
    if len(num) >= 2:
        corr = df[num].corr(numeric_only=True)
        im = c1.imshow(corr.values, cmap="Blues", aspect="auto")
        c1.set_xticks(range(len(corr.columns))); c1.set_xticklabels(corr.columns, rotation=45, ha="right")
        c1.set_yticks(range(len(corr.index))); c1.set_yticklabels(corr.index); c1.set_title("Matriz de correlación")
        f3.colorbar(im, ax=c1, fraction=0.046, pad=0.04)
        p3.append({"plot": "Correlación", "text": "Mide fuerza/dirección de relaciones lineales."})
    else:
        _safe_bar(c1, df.nunique(dropna=False).sort_values(ascending=False).head(10), "Diversidad por columna", _C["blue"], "Valores únicos")
    x, y = _best_scatter_pair(df, analysis)
    if x and y: _safe_scatter(c2, df, x, y, f"Relación más fuerte: {x} vs {y}", _C["purple"]); p3.append({"plot": "Relación dominante", "text": f"Mayor señal entre {x} y {y}."})
    else: _safe_bar(c2, (df.notna().mean() * 100).sort_values(ascending=False).head(10), "Cobertura por columna", _C["purple"], "% no nulos")
    if cat and num:
        c, n = cat[0], num[0]
        _safe_bar(c3, df.groupby(c, dropna=False)[n].mean().sort_values(ascending=False).head(12), f"Promedio de {n} por {c}", _C["green"], f"Promedio {n}")
        p3.append({"plot": "Segmentación", "text": f"Comparación de {n} entre grupos de {c}."})
    elif cat:
        c = cat[0]; _safe_bar(c3, df[c].value_counts(dropna=False).head(12), f"Frecuencia de {c}", _C["green"], "Frecuencia")
    else:
        _safe_bar(c3, (df.isna().mean() * 100).sort_values(ascending=False).head(10), "Riesgo de calidad", _C["green"], "% faltantes")
    if num:
        s = pd.to_numeric(df[num[0]], errors="coerce").dropna()
        c4.boxplot(s); c4.set_xticklabels([num[0]]); c4.set_title(f"Dispersión y outliers: {num[0]}")
    else:
        c4.axis("off"); c4.text(0.02, 0.75, "No hay columnas numéricas para boxplot", color="#6B7280")
    f3.suptitle("Dashboard 3: Relaciones y Segmentación", fontsize=15, fontweight="bold", color="#1F2937")
    f3.tight_layout(rect=[0, 0, 1, 0.97])
    cards.append(_new_card("Dashboard 3: Relaciones y Segmentación", "Dependencias y comparativas por grupos.", f3, p3))

    # 4) Narrativa
    f4 = plt.figure(figsize=(14, 8), facecolor=_BG); g4 = GridSpec(2, 2, figure=f4)
    d1, d2, d3, d4 = [f4.add_subplot(g4[i, j]) for i in range(2) for j in range(2)]
    for d in (d1, d2, d3, d4): d.axis("off")

    concl = analysis.get("final_conclusions", []) or insights
    pred = analysis.get("predictive_use_cases", [])

    d1.text(0.01, 0.90, "Conclusiones", fontsize=14, fontweight="bold", color="#1E3A8A")
    y0 = 0.76
    for it in concl[:4]:
        d1.text(0.02, y0, f"- {it}", fontsize=10, color="#111827", wrap=True); y0 -= 0.16

    d2.text(0.01, 0.90, "Recomendaciones", fontsize=14, fontweight="bold", color="#1E3A8A")
    y1 = 0.76
    for it in recs[:5]:
        d2.text(0.02, y1, f"- {it}", fontsize=10, color="#4338CA", wrap=True); y1 -= 0.14

    d3.text(0.01, 0.90, "Insights", fontsize=14, fontweight="bold", color="#1E3A8A")
    y2 = 0.76
    for it in (insights[:4] + pred[:2]):
        d3.text(0.02, y2, f"- {it}", fontsize=10, color="#111827", wrap=True); y2 -= 0.14

    d4.text(0.01, 0.90, "Usos en la vida real", fontsize=14, fontweight="bold", color="#1E3A8A")
    y3 = 0.76
    for it in uses[:5]:
        d4.text(0.02, y3, f"- {it}", fontsize=10, color="#111827", wrap=True); y3 -= 0.14
    d4.text(0.02, 0.06, "Material listo para defensa académica y toma de decisiones basada en evidencia.", fontsize=9.5, color="#6B7280", wrap=True)

    f4.suptitle("Dashboard 4: Narrativa Ejecutiva", fontsize=15, fontweight="bold", color="#1F2937")
    f4.tight_layout(rect=[0, 0, 1, 0.96])
    cards.append(_new_card("Dashboard 4: Narrativa Ejecutiva", "Bloques narrativos para exposición: conclusiones, recomendaciones, insights y usos reales.", f4, []))

    return cards
