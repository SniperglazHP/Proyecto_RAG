
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()
API_BASE = os.getenv("API_BASE")

st.set_page_config(page_title="Ingesta de Documentos")
st.title("Ingesta de Documentos")

st.markdown("""
Sube tus documentos (PDF, DOCX, TXT, imágenes) para que sean analizados
y almacenados en la base vectorial Pinecone.  
Esto permitirá que el sistema RAG los utilice en futuras consultas.
""")

uploaded_file = st.file_uploader("Selecciona un archivo", type=["pdf", "docx", "txt", "png", "jpg"])

if uploaded_file:
    st.write(f"Archivo seleccionado: **{uploaded_file.name}**")
    if st.button("Procesar Documento"):
        with st.spinner("Procesando documento..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(f"{API_BASE}/ingesta/", files=files)
                if response.status_code == 200:
                    st.success("Documento procesado correctamente.")
                    st.json(response.json())
                else:
                    st.error(f"Error del servidor: {response.status_code}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
