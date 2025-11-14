# scripts/streamlit_app.py
import streamlit as st
from pathlib import Path

# Configuración general
st.set_page_config(
    page_title="RAG System",
    layout="wide"
)

st.title("Sistema RAG")
st.markdown("""
### Bienvenido al sistema RAG
Selecciona una página desde la barra lateral para interactuar con el sistema:

-**Ingesta:** Sube y procesa documentos para la base vectorial.
            
-**Retrieval:** Conversa con el modelo basado en tus documentos.

---
""")

# Imagen ilustrativa o logo
logo_path = Path(__file__).parent / "logo.png"
if logo_path.exists():
    st.image(str(logo_path), width=250)
else:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=200)

st.info("Usa el menú lateral para navegar entre las secciones.")
