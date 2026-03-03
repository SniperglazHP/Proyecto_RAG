#Script que se encarga de la interfaz de usuario utilizando Streamlit, permitiendo a los usuarios subir archivos, enviar mensajes al asistente multiagente, y visualizar las respuestas, análisis, gráficos y dashboards generados por el backend.

#-->Librerias
import base64
import requests
import streamlit as st

#-->URL del backend para las solicitudes de análisis, visualización y gestión de archivos.
BACKEND_URL = "http://127.0.0.1:8000"

#-->Titulo y configuración inicial de la página de Streamlit, estableciendo un diseño amplio y un título descriptivo para la plataforma multiagente de análisis de datos.
st.set_page_config(page_title="Plataforma Multiagente", layout="wide")
st.title("Plataforma Multiagente Data Science")
st.caption("Asistente multiagente para analizar datasets, crear gráficas y construir dashboards automáticamente.")

#-->Inicialización de variables de estado para manejar el historial de mensajes, el archivo cargado actualmente, y evitar recargas innecesarias al subir el mismo archivo varias veces.
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None

uploaded_file = st.file_uploader("Sube tu CSV o Excel", type=["csv", "xlsx", "xls"])

#-->Si se ha subido un archivo nuevo, se envía al backend utilizando una solicitud POST al endpoint de carga
if uploaded_file and uploaded_file.name != st.session_state.last_uploaded_name:
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")
    }

    try:
        response = requests.post(f"{BACKEND_URL}/upload/", files=files, timeout=120)
        result = response.json()

        if response.ok and result.get("status") == "uploaded":
            st.session_state.uploaded_filename = result.get("filename", uploaded_file.name)
            st.session_state.last_uploaded_name = uploaded_file.name
            st.success(f"Archivo subido: {st.session_state.uploaded_filename}")
        else:
            st.error(result.get("error", "No se pudo subir el archivo."))
    except Exception as exc:
        st.error(f"Error al conectar con backend: {exc}")

#-->Si ya hay un archivo cargado, se muestra su nombre para que el usuario tenga claro qué dataset está activo para análisis y visualización.
if st.session_state.uploaded_filename:
    st.info(f"Archivo activo: {st.session_state.uploaded_filename}")

#-->Parte donde se botones que permiten al usuario enviar solicitudes rápidas para análisis, visualización o generación de dashboards.
quick_prompt = None
col1, col2, col3 = st.columns(3)
if col1.button("Análisis rápido"):
    quick_prompt = "Analiza este dataset y dame los hallazgos principales."
if col2.button("Dashboard general"):
    quick_prompt = "Genera un dashboard general del dataset."
if col3.button("Gráfica rápida"):
    quick_prompt = "Genera una gráfica de barras útil con las columnas más relevantes."

#-->Renderizado del historial de mensajes, donde se muestra el contenido de cada mensaje según su tipo (texto, análisis, gráfica o dashboard), utilizando componentes de Streamlit para mostrar texto, JSON, imágenes y explicaciones de manera clara y organizada.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        kind = msg.get("kind", "text")
        if kind == "text":
            st.write(msg["content"])
        elif kind == "analysis":
            st.write(msg.get("content", "Aquí está el análisis del dataset."))
            st.json(msg["analysis"])
        elif kind == "chart":
            st.write(msg.get("content", "Aquí tienes la visualización."))
            image_bytes = base64.b64decode(msg["chart_base64"])
            st.image(image_bytes)
            if msg.get("chart_config"):
                st.caption(f"Config: {msg['chart_config']}")
        elif kind == "dashboard":
            st.write(msg.get("content", "Aquí tienes el dashboard."))
            cards = msg.get("dashboard_cards", [])
            total_cards = len(cards)
            for idx, card in enumerate(cards):
                st.subheader(card.get("title", "Vista de dashboard"))
                if card.get("description"):
                    st.caption(card["description"])
                image_bytes = base64.b64decode(card["image_base64"])
                st.image(image_bytes)
                if card.get("plot_descriptions") and idx < total_cards - 1:
                    st.markdown("**Explicación de gráficas**")
                    for item in card["plot_descriptions"]:
                        st.markdown(f"- **{item.get('plot', 'Gráfica')}**: {item.get('text', '')}")

#-->Se encarga de manejar la entrada del usuario en el chat
user_input = st.chat_input("Escribe tu mensaje...")
if quick_prompt and not user_input:
    user_input = quick_prompt

#-->Se enfoca en definir claramente el formato de entrada y salida esperado, así como las reglas que deben seguir para generar análisis, visualizaciones y explicaciones útiles y accionables para los usuarios.
if user_input:
    st.session_state.messages.append({"role": "user", "kind": "text", "content": user_input})

    payload = {
        "message": user_input,
        "filename": st.session_state.uploaded_filename,
    }

    try:
        response = requests.post(f"{BACKEND_URL}/chat/", data=payload, timeout=120)
        result = response.json()

        if not response.ok:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "kind": "text",
                    "content": result.get("error", "Error interno en backend"),
                }
            )
        else:
            if "response" in result:
                st.session_state.messages.append(
                    {"role": "assistant", "kind": "text", "content": result["response"]}
                )

            if "analysis" in result:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "kind": "analysis",
                        "content": result.get("response", "Listo, aquí está el análisis del dataset."),
                        "analysis": result["analysis"],
                    }
                )

            if "chart_base64" in result:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "kind": "chart",
                        "content": result.get("response", "Listo, aquí tienes la visualización."),
                        "chart_base64": result["chart_base64"],
                        "chart_config": result.get("chart_config"),
                    }
                )

            if "dashboard_cards" in result:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "kind": "dashboard",
                        "content": result.get("response", "Listo, aquí tienes el dashboard."),
                        "dashboard_cards": result["dashboard_cards"],
                    }
                )

    except Exception as exc:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "kind": "text",
                "content": f"Error al conectar con backend: {exc}",
            }
        )

    st.rerun()
