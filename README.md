# Proyecto_RAG

Repositorio personal de residencias profesionales con multiples proyectos alrededor de RAG, agentes y plataformas de analitica de datos.

## Resumen

Este repositorio contiene varias iteraciones del trabajo realizado durante residencias:

- Pipeline RAG clasico (ingesta, chunking, embeddings, retrieval y respuesta con LLM).
- Evaluacion de respuestas con metricas y juez pointwise.
- Prototipos de agentes para analisis EDA y generacion automatica de dashboards.
- Plataformas multiagente con backend FastAPI y frontends para visualizacion.
- Variantes con Google ADK + Gemini y uso de servicios externos como Pinecone y Supabase.

## Estructura principal del repo

- `scripts/`: codigo fuente principal y subproyectos.
- `scripts/main.py`: API FastAPI del flujo RAG base (ingesta + retrieval).
- `scripts/streamlit_app.py` y `scripts/pages/`: interfaz Streamlit del sistema RAG.
- `scripts/uploads/`, `scripts/outputs/`, `scripts/embeddings/`: insumos y resultados del pipeline.
- `scripts/generacion_respuestas/`: generacion y evaluacion de respuestas (datasets, metricas y graficas).
- `scripts/agente_dashboards/`: pipeline de agentes para EDA de CSV y dashboard React generado.
- `scripts/agente_google_adk/`: proyecto de analisis de datos con Google ADK (agentes + tools).
- `scripts/agente_plataforma/`: backend modular con agentes, tools y servicios (ADK + Supabase).
- `scripts/agente_proyecto_plataforma/`: version fullstack (backend + frontend) del proyecto de plataforma.
- `scripts/plataforma/`: backend FastAPI de plataforma multiagente orientada a analitica.
- `scripts/plataforma_multiagente/`: version orientada a app Streamlit + orquestacion por agentes.
- `scripts/agentes/`: prototipos previos de agentes y pruebas de dashboards.
- `scripts_test/`: scripts de prueba/experimentos.
- `docs/`: documentacion del proyecto (MkDocs).
- `rag/`: paquete base del template original del proyecto.

## Tecnologias usadas

- Python 3.11
- FastAPI + Uvicorn
- Streamlit
- OpenAI API
- Google ADK y Google GenAI (Gemini)
- Pinecone (vector DB)
- Supabase (storage y metadatos)
- Pandas / NumPy / Matplotlib
- Frontend React + Vite (en subproyectos de dashboards)

## Configuracion rapida

1. Crear y activar entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno en `.env` segun el subproyecto:
- `OPENAI_API_KEY`
- `GEMINI_API_KEY` (o `GOOGLE_API_KEY` en algunos flujos)
- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_BUCKET`

4. Ejecutar el subproyecto que necesites (ejemplos):

```bash
uvicorn scripts.main:app --reload
```

```bash
streamlit run scripts/streamlit_app.py
```

## Nota

Este repositorio conserva versiones historicas y experimentales, por lo que pueden coexistir flujos similares con distinta arquitectura.

