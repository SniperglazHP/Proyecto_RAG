"""
Este script crea una interfaz web usando Streamlit para interactuar con el sistema RAG preciamente hecho.
"""
#-->Importa librerías
import streamlit as st #Framework para crear aplicaciones web interactivas y st es el alias comúnmente usado
import requests #Maneja solicitudes HTTP
from dotenv import load_dotenv #Carga variables de entorno
import os #Operaciones del sistema

#-->Carga variables de entorno
load_dotenv()

#-->Configura la URL base de la API
API_BASE = os.getenv("API_BASE")

#-->Configuración de la página
st.set_page_config(page_title="RAG", layout="wide")
st.title("RAG - Interfaz con Streamlit")
st.markdown("Interfaz para probar el endpoint de retrieval e ingesta del sistema RAG")

#-->Ingesta
st.sidebar.header("Ingesta de documentos")
uploaded_file = st.sidebar.file_uploader("Sube un PDF/DOCX/TXT/imagen", type=["pdf","docx","txt","png","jpg","jpeg"])
if uploaded_file: #Si se ha subido un archivo
    st.sidebar.write(f"Archivo: {uploaded_file.name}")
    if st.sidebar.button("Enviar a ingesta"):
        with st.spinner("Subiendo y procesando..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())} #Aqui preparamos el archivo para enviarlo
            try:
                resp = requests.post(f"{API_BASE}/ingesta/", files=files, timeout=999) #Enviamos el archivo al endpoint de ingesta
                resp.raise_for_status() #Lanza un error si la respuesta HTTP es mala
                st.sidebar.success("Documento procesado correctamente.") #Muestra mensaje de éxito
                st.sidebar.json(resp.json()) #Muestra la respuesta JSON de la API de ingesta
            except Exception as e: 
                st.sidebar.error(f"Error en ingesta: {e}")

#-->Retrieval
st.header("Consultas (Retrieval)") #Encabezado principal para la sección de consultas
query = st.text_input("Escribe tu pregunta", "") #Query de texto para la consulta
col1, col2 = st.columns([3,1]) #Dos columnas, una para la consulta y otra para el historial

with col1: #Columna principal para la consulta
    if st.button("Preguntar"): #Botón para enviar la consulta
        if not query.strip():
            st.warning("Escribe algo antes de enviar.") #Advertencia si no hay texto
        else:
            with st.spinner("Consultando el backend..."): #Muestra un spinner mientras se procesa la consulta
                try:
                    #-->Enviamos como formulario igual que tu FastAPI espera
                    data = {"query": query}
                    resp = requests.post(f"{API_BASE}/retrieval/", data=data, timeout=999) #Enviamos la consulta al endpoint de retrieval
                    resp.raise_for_status() #Lanza un error si la respuesta HTTP es mala
                    result = resp.json() #Obtenemos la respuesta JSON de la API de retrieval
                    st.subheader("Respuesta del modelo") #Encabezado para la respuesta
                    st.write(result.get("answer", "Sin respuesta")) #Muestra la respuesta del modelo
                    st.markdown("---") #Separador visual
                    st.write("Matches encontrados:", result.get("matches_found", 0)) #Muestra el número de matches encontrados
                except Exception as e:
                    st.error(f"Error en retrieval: {e}") #Muestra un error si falla la consulta

#-->Manejo del historial de preguntas
with col2:
    st.info("Historial de preguntas")
    if "history" not in st.session_state:
        st.session_state.history = []
    if st.button("Guardar en historial"):
        if query.strip():
            st.session_state.history.append(query)
    for q in reversed(st.session_state.history[-10:]):
        st.write("-", q)
