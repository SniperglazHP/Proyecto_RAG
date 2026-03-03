#Script que define los agentes adk para la plataforma, incluyendo agentes para la identificación de intenciones, análisis de datos, generación de visualizaciones y explicación de resultados, así como funciones auxiliares para extraer texto y parsear JSON de manera segura.

#-->Librerias
import json
from typing import Any
from google.adk.agents import LlmAgent
from prompts import (
    analysis_prompt,
    explanation_prompt,
    intent_prompt,
    visualization_prompt,
)
from tools import load_csv_tool

#-->Modelo a utilizar para los agentes
MODEL_NAME = "gemini-2.5-flash"

#-->Agente para la identificación de intenciones, que clasifica el mensaje del usuario en categorías predefinidas para dirigir el flujo de la conversación.
def get_intent_agent() -> LlmAgent:
    return LlmAgent(
        name="intent_agent",
        model=MODEL_NAME,
        instruction=intent_prompt(),
    )

#-->Agente para el análisis de datos, que toma el dataset cargado y genera un informe EDA avanzado con insights accionables y contexto del dominio.
def get_analysis_agent() -> LlmAgent:
    return LlmAgent(
        name="analysis_agent",
        model=MODEL_NAME,
        instruction=analysis_prompt(),
        tools=[load_csv_tool],
    )

#-->Agente para la generación de visualizaciones, que planifica y crea gráficos basados en el análisis de datos y las solicitudes del usuario, con un enfoque en la utilidad práctica de las visualizaciones.
def get_generator_agent() -> LlmAgent:
    return LlmAgent(
        name="generator_agent",
        model=MODEL_NAME,
        instruction=visualization_prompt(),
    )

#-->Agente para la explicación de resultados, que traduce los insights y visualizaciones generados en explicaciones claras y accesibles para usuarios no técnicos, facilitando la comprensión y la toma de decisiones informadas.
def get_explanation_agent() -> LlmAgent:
    return LlmAgent(
        name="explanation_agent",
        model=MODEL_NAME,
        instruction=explanation_prompt(),
    )

#-->Función auxiliar para extraer texto de la salida de los agentes, manejando diferentes formatos de respuesta y asegurando que se obtenga el contenido relevante de manera robusta.
def extract_text(agent_output: Any) -> str:
    if agent_output is None:
        return ""

    if isinstance(agent_output, str):
        return agent_output.strip()

    if isinstance(agent_output, dict):
        for key in ("output_text", "text", "content", "response"):
            value = agent_output.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return str(agent_output).strip()

#-->Función auxiliar para parsear JSON de manera segura, que intenta extraer un objeto JSON válido incluso si el modelo devuelve texto adicional o formato incorrecto, mejorando la robustez de la interacción con los agentes.
def safe_json_parse(raw: str) -> dict[str, Any]:
    text = (raw or "").strip()

    if not text:
        raise ValueError("El modelo no devolvió ningún texto para parsear.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise ValueError("No se encontró un objeto JSON válido en la salida del modelo.")
