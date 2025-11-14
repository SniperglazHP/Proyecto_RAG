
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE")

st.set_page_config(page_title="Chat RAG")
st.title("Retrieval")
st.caption("Haz preguntas basadas en los documentos procesados anteriormente.")

# Historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente RAG. Pregúntame sobre los documentos que has subido."}
    ]

# Muestra historial previo
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta..."):
    # Añade el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu pregunta..."):
            try:
                response = requests.post(f"{API_BASE}/retrieval/", data={"query": prompt})
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "No se obtuvo respuesta.")
                else:
                    answer = f"Error del servidor ({response.status_code})"
            except Exception as e:
                answer = f"Error de conexión: {e}"

            st.markdown(answer)

    # Guarda la respuesta en el historial
    st.session_state.messages.append({"role": "assistant", "content": answer})
