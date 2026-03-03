#Script del backend de la plataforma, que define distintos endpoints con FastAPI para manejar la carga de archivos, detección de intenciones en mensajes de texto, análisis de datos, generación de visualizaciones y construcción de dashboards, utilizando agentes especializados para cada tarea y herramientas para interactuar con Supabase como almacenamiento de datasets.

#-->Librerias
import json
import re
from typing import Optional
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from agents import (
    extract_text,
    get_analysis_agent,
    get_explanation_agent,
    get_generator_agent,
    get_intent_agent,
    safe_json_parse,
)
from analysis_engine import base_analysis, from_eda_contract, merge_analysis, to_eda_contract
from generator_engine import build_dashboard_cards, plan_visualization, render_chart
from tools import load_dataset_from_supabase, upload_to_supabase

#-->Carga de variables de entorno
load_dotenv()
app = FastAPI(title="Plataforma Multiagente Data Science")
VALID_INTENTS = {"upload", "analyze", "visualize", "dashboard", "explain", "greeting"}

#-->Funcion auxiliar para normalizar el texto de entrada, eliminando espacios extra, convirtiendo a minúsculas y facilitando la detección de intenciones mediante palabras clave
def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower().strip())

#-->Funcion para detectar la intención del usuario a partir de su mensaje
def _detect_intent(message: str) -> str:
    text = _normalize_text(message)

    if any(k in text for k in ["dashboard", "tablero", "panel"]):
        return "dashboard"
    if any(k in text for k in ["grafica", "gráfica", "plot", "chart", "barra", "barras", "scatter", "histograma", "pie"]):
        return "visualize"
    if any(k in text for k in ["analiza", "análisis", "resumen", "eda"]):
        return "analyze"
    if any(k in text for k in ["explica", "explain", "interpreta"]):
        return "explain"
    if text in {"hola", "buenas", "hello", "hi", "saludos"}:
        return "greeting"

    try:
        raw = extract_text(get_intent_agent().run(input=message)).lower().strip()
        if raw in VALID_INTENTS:
            return raw
    except Exception:
        pass

    return "analyze"

#-->Endpoint para la carga de archivos, que recibe un archivo CSV o Excel, lo sube a Supabase utilizando la función upload_to_supabase, y devuelve una respuesta JSON
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        return json.loads(upload_to_supabase(content, file.filename))
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})

#-->Endpoint para manejar las interacciones de chat, que recibe un mensaje del usuario y opcionalmente el nombre de un archivo cargado, detecta la intención del mensaje, y ejecuta la lógica correspondiente para análisis, visualización o generación de dashboards, utilizando los agentes especializados y devolviendo una respuesta estructurada en JSON.
@app.post("/chat/")
async def chat(message: str = Form(...), filename: Optional[str] = Form(default=None)):
    try:
        intent = _detect_intent(message)

        if intent == "greeting":
            return {"intent": intent, "response": "Hola! Muy buenas. Sube un CSV/XLSX y pídeme análisis, gráficas o dashboard."}

        if intent in {"analyze", "visualize", "dashboard"} and not filename:
            return {"intent": intent, "response": "Primero sube un archivo CSV/XLSX para continuar."}

        dataset = load_dataset_from_supabase(filename) if filename else None
        df = pd.DataFrame(dataset["data"]) if dataset else None

        if intent == "analyze":
            fallback = base_analysis(df)
            context = {
                "solicitud_usuario": message,
                "rows": dataset["rows"],
                "columns": dataset["columns"],
                "dtypes": dataset["dtypes"],
                "sample": dataset["data"][:30],
            }
            try:
                raw = extract_text(get_analysis_agent().run(input=json.dumps(context, ensure_ascii=False)))
                agent_analysis = from_eda_contract(safe_json_parse(raw))
            except Exception:
                agent_analysis = {}

            analysis = merge_analysis(agent_analysis, fallback)
            report = to_eda_contract(analysis)
            return {
                "intent": intent,
                "response": "Quedo listo, preparé un análisis enriquecido con significado de columnas, outliers y usos prácticos.",
                "analysis": report,
            }

        if intent == "visualize":
            analysis = base_analysis(df)
            report = to_eda_contract(analysis)
            try:
                raw = extract_text(get_generator_agent().run(input=json.dumps({
                    "solicitud_usuario": message,
                    "columnas": dataset["columns"],
                    "tipos": dataset["dtypes"],
                    "informe_eda": report["informe_eda"],
                }, ensure_ascii=False)))
                model_config = safe_json_parse(raw)
            except Exception:
                model_config = {}

            config = plan_visualization(message, dataset, df, model_config)
            image = render_chart(df, config)
            suffix = " para todas las columnas" if config.get("scope") == "all_columns" else ""
            return {
                "intent": intent,
                "response": f"Generé una gráfica tipo {config['chart_type']}{suffix}.",
                "chart_base64": image,
                "chart_mime": "image/png",
                "chart_config": config,
            }

        if intent == "dashboard":
            analysis = base_analysis(df)
            report = to_eda_contract(analysis)
            cards = build_dashboard_cards(df, analysis)
            kpis = analysis["data_quality"] | {
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
                "numeric_columns": len(analysis["numeric_columns"]),
                "categorical_columns": len(analysis["categorical_columns"]),
                "domain": analysis["dataset_context"]["domain_label"],
            }
            return {
                "intent": intent,
                "response": "Listo, generé un dashboard en dos vistas con explicación por cada gráfica.",
                "dashboard_cards": cards,
                "kpis": kpis,
                "insights": analysis["insights"],
                "real_world_uses": analysis["real_world_uses"],
                "analysis_contract": report,
            }

        if intent == "explain":
            return {"intent": intent, "response": extract_text(get_explanation_agent().run(input=message))}

        return {"intent": intent, "response": "No entendí tu solicitud."}

    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})
