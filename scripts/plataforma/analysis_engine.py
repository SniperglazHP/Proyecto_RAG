#Script para el motor de análisis de datos, que incluye funciones para detectar el dominio del dataset, generar un informe EDA enriquecido con insights y recomendaciones, y manejar la integración con los agentes de análisis y visualización.

#-->Librerías
import re
from typing import Any
import pandas as pd

#-->Glosarios de términos para diferentes dominios, que ayudan a los agentes a interpretar correctamente las columnas del dataset y generar análisis más relevantes y contextualizados.
DOMAIN_GLOSSARIES = {
    "diabetes": {
        "age": "edad de la persona", "sex": "sexo/género biológico codificado", "bmi": "índice de masa corporal",
        "bp": "presión arterial media", "s1": "colesterol total en suero", "s2": "lipoproteínas de baja densidad (LDL)",
        "s3": "lipoproteínas de alta densidad (HDL)", "s4": "proporción colesterol total/HDL",
        "s5": "triglicéridos séricos (log)", "s6": "nivel de glucosa en sangre",
    },
    "salud": {
        "bmi": "índice de masa corporal", "imc": "índice de masa corporal", "bp": "presión arterial",
        "glucose": "nivel de glucosa", "glucosa": "nivel de glucosa", "sex": "sexo/género de la persona",
        "gender": "sexo/género de la persona",
    },
    "ventas": {
        "sales": "monto de ventas", "revenue": "ingresos", "profit": "ganancia",
        "price": "precio", "discount": "descuento aplicado",
    },
}
GENERIC_HINTS = {
    "age": "edad de la persona", "edad": "edad de la persona", "sex": "sexo/género de la persona",
    "gender": "sexo/género de la persona", "bmi": "índice de masa corporal", "imc": "índice de masa corporal",
    "bp": "presión arterial", "glucose": "nivel de glucosa", "glucosa": "nivel de glucosa",
    "cholesterol": "nivel de colesterol", "income": "ingreso económico", "salary": "salario",
}

#-->Función para normalizar nombres de columnas, que elimina caracteres especiales y convierte a minúsculas para facilitar la comparación y el mapeo con los glosarios de dominios.
def _norm(col: str) -> str:
    return re.sub(r"[^a-z0-9áéíóúñ]", "", col.lower())

#-->Función para detectar el dominio del dataset, que analiza los nombres de las columnas y sugiere un dominio basado en la presencia de términos clave, ayudando a contextualizar el análisis y las recomendaciones generadas.
def _domain(columns: list[str]) -> str:
    cols = [_norm(c) for c in columns]
    if len({"age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"}.intersection(cols)) >= 5:
        return "diabetes"
    joined = " ".join(cols)
    scores = {k: sum(1 for t in DOMAIN_GLOSSARIES[k] if t in joined) for k in ("salud", "ventas")}
    best = max(scores, key=scores.get)
    return best if scores[best] >= 2 else "general"

#-->Función para generar un informe EDA enriquecido, que combina análisis estadístico, detección de calidad de datos, insights accionables y recomendaciones prácticas para el usuario, sirviendo como base para la generación de visualizaciones y dashboards.
def _context(df: pd.DataFrame) -> dict[str, Any]:
    d = _domain(df.columns.tolist())
    g = DOMAIN_GLOSSARIES.get(d, {})
    gloss = {}
    for c in df.columns:
        n = _norm(c)
        m = g.get(n)
        if not m:
            m = next((v for k, v in g.items() if k in n), None)
        if not m:
            m = next((v for k, v in GENERIC_HINTS.items() if k in n), None)
        if m:
            gloss[c] = m
    return {
        "domain": d,
        "domain_label": {"diabetes": "salud/diabetes", "salud": "salud", "ventas": "ventas/comercial"}.get(d, "general"),
        "column_glossary": gloss,
    }

#-->Función para realizar un análisis básico del dataset, que incluye estadísticas descriptivas, detección de valores faltantes, outliers y correlaciones, proporcionando una base sólida para el análisis avanzado que realizará el agente de análisis.
def _col_meaning(col: str, dtype: str, ctx: dict[str, Any]) -> str:
    if col in ctx["column_glossary"]:
        return ctx["column_glossary"][col]
    return "variable numérica para analizar tendencia y variación" if any(x in dtype for x in ("int", "float")) else "variable categórica para segmentar y clasificar"

#-->Funcion auxiliar para el análisis de datos, que incluyen la detección de outliers
def _outliers(df: pd.DataFrame, num: list[str]) -> dict[str, dict[str, float]]:
    total, out = max(len(df), 1), {}
    for c in num:
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        if s.empty:
            continue
        q1, q3 = float(s.quantile(0.25)), float(s.quantile(0.75))
        lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
        n = int(((s < lo) | (s > hi)).sum())
        out[c] = {"lower_bound": round(lo, 4), "upper_bound": round(hi, 4), "outlier_count": n, "outlier_pct": round(100 * n / total, 2)}
    return out

#-->Funcion auxiliar para el análisis de datos, que incluyen la detección de correlaciones entre variables numéricas
def _top_corr(df: pd.DataFrame, num: list[str]) -> list[dict[str, Any]]:
    if len(num) < 2:
        return []
    corr, pairs = df[num].corr(numeric_only=True), []
    for i, x in enumerate(corr.columns):
        for y in corr.columns[i + 1 :]:
            v = corr.loc[x, y]
            if pd.notna(v):
                pairs.append({"x": x, "y": y, "corr": float(v)})
    return sorted(pairs, key=lambda z: abs(z["corr"]), reverse=True)[:5]

#-->funcion para generar KPIs sugeridos basados en el análisis del dataset, que proporciona métricas clave y recomendaciones
def _kpis(df: pd.DataFrame, a: dict[str, Any]) -> list[dict[str, Any]]:
    q = a["data_quality"]
    out = [
        {"name": "total_filas", "value": int(df.shape[0]), "description": "Cantidad total de registros"},
        {"name": "total_columnas", "value": int(df.shape[1]), "description": "Cantidad total de columnas"},
        {"name": "porcentaje_faltantes", "value": float(q.get("missing_pct", 0)), "description": "Porcentaje de celdas faltantes"},
    ]
    if a["numeric_columns"]:
        c = a["numeric_columns"][0]
        m = a["basic_stats"].get(c, {}).get("mean")
        if m is not None:
            out.append({"name": f"promedio_{c}", "value": round(float(m), 4), "description": f"Promedio de {c}"})
    return out

#-->Función para generar segmentaciones recomendadas basadas en el análisis del dataset, que sugiere columnas útiles para segmentar el análisis y detectar patrones relevantes.
def _segmentations(a: dict[str, Any]) -> list[dict[str, str]]:
    seg = [{"column": c, "why": "Permite comparar subgrupos y detectar diferencias relevantes."} for c in a["categorical_columns"][:3]]
    seg += [{"column": c, "why": "Útil para crear rangos y análisis por niveles."} for c in a["numeric_columns"][:2]]
    return seg

#-->Función para generar recomendaciones de visualización basadas en el análisis del dataset
def _viz_recs(a: dict[str, Any]) -> list[dict[str, str]]:
    cat, num, r = a["categorical_columns"], a["numeric_columns"], []
    if cat and num:
        r.append({"chart_type": "bar", "x": cat[0], "y": num[0], "objective": "Comparar promedio numérico entre categorías."})
    if len(num) >= 2:
        r.append({"chart_type": "scatter", "x": num[0], "y": num[1], "objective": "Evaluar relación entre variables numéricas."})
    if num:
        r.append({"chart_type": "histogram", "x": num[0], "y": "", "objective": "Analizar distribución y sesgo."})
    return r

#-->Función para generar casos de uso predictivo basados en el análisis del dataset
def _predictive(a: dict[str, Any]) -> list[str]:
    base = [
        "Modelos de regresión para estimar variables continuas.",
        "Modelos de clasificación para segmentar riesgo o categorías.",
        "Clustering para descubrir perfiles latentes.",
    ]
    if a["dataset_context"]["domain"] == "ventas":
        base.append("Forecasting de demanda/ventas si existe variable temporal.")
    return base

#-->Función principal para realizar el análisis del dataset, que se integra con los agentes de análisis y visualización para generar un informe completo y útil para el usuario, sirviendo como el núcleo del motor de análisis de datos.
def base_analysis(df: pd.DataFrame) -> dict[str, Any]:
    num = df.select_dtypes(include="number").columns.tolist()
    cat = [c for c in df.columns if c not in num]
    ctx = _context(df)
    dtypes = {c: str(t) for c, t in df.dtypes.items()}
    miss = int(df.isna().sum().sum())
    miss_pct = round(100 * miss / max(int(df.shape[0] * df.shape[1]), 1), 2)

    basic = {}
    if num:
        desc = df[num].describe().to_dict()
        for c in num:
            s = desc.get(c, {})
            basic[c] = {k: (float(s.get(k, 0)) if pd.notna(s.get(k, 0)) else 0) for k in ("count", "mean", "std", "min", "max")}

    a = {
        "summary": f"EDA enriquecido con {df.shape[0]} filas y {df.shape[1]} columnas en dominio {ctx['domain_label']}.",
        "dataset_context": ctx,
        "numeric_columns": num,
        "categorical_columns": cat,
        "column_definitions": {c: {"dtype": dtypes[c], "meaning": _col_meaning(c, dtypes[c], ctx)} for c in df.columns},
        "data_quality": {"missing_values": miss, "missing_pct": miss_pct, "duplicate_rows": int(df.duplicated().sum())},
        "basic_stats": basic,
        "outliers": _outliers(df, num),
        "top_correlations": _top_corr(df, num),
        "insights": [
            f"Contexto detectado: {ctx['domain_label']}.",
            f"Columnas numéricas: {len(num)}. Categóricas: {len(cat)}.",
            f"Valores faltantes: {miss} ({miss_pct}%).",
        ],
        "real_world_uses": [
            "Generar línea base del comportamiento del dataset.",
            "Soportar toma de decisiones con evidencia cuantitativa.",
        ],
        "recommendations": [
            "Tratar outliers antes de modelar.",
            "Aplicar estrategia de imputación para faltantes críticos.",
        ],
    }
    a["kpis_suggested"] = _kpis(df, a)
    a["segmentations_recommended"] = _segmentations(a)
    a["visualization_recommendations"] = _viz_recs(a)
    a["predictive_use_cases"] = _predictive(a)
    a["final_conclusions"] = a["insights"][:3] + ["El informe sirve como contrato de datos para dashboards automáticos."]
    return a

#-->Función para fusionar el análisis generado por el agente con un análisis de respaldo, que combina la información proporcionada por el agente con un análisis básico para asegurar que se mantenga la integridad y utilidad del informe EDA incluso si el agente no proporciona toda la información esperada.
def merge_analysis(agent_analysis: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    merged = dict(fallback)
    if isinstance(agent_analysis, dict):
        for k, v in agent_analysis.items():
            if v not in (None, "", [], {}):
                merged[k] = v
    for k, v in fallback.items():
        merged.setdefault(k, v)
    return merged

#-->Funciones para convertir el análisis a un formato de contrato específico para el informe EDA que se espera que el agente de análisis genere, facilitando la integración y el intercambio de información entre los componentes del sistema.
def to_eda_contract(analysis: dict[str, Any]) -> dict[str, Any]:
    return {"informe_eda": analysis}

#-->Función para extraer el análisis del contrato generado por el agente, que permite obtener el contenido relevante del informe EDA para su uso en la generación de visualizaciones, dashboards y explicaciones, asegurando que se maneje correctamente la estructura del contrato.
def from_eda_contract(payload: dict[str, Any]) -> dict[str, Any]:
    return payload["informe_eda"] if isinstance(payload, dict) and isinstance(payload.get("informe_eda"), dict) else payload
