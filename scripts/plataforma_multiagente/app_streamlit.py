import streamlit as st
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.agents import agente_analizador

# ===============================
# CONFIGURACIÓN GLOBAL
# ===============================
APP_NAME = "eda_dashboards"
USER_ID = "leonardo_test"
SESSION_ID = "eda_session_001"

session_service = InMemorySessionService()

runner = Runner(
    agent=agente_analizador,
    app_name=APP_NAME,
    session_service=session_service
)

# ===============================
# FUNCIÓN SYNC PARA STREAMLIT
# ===============================
def run_agent_sync(query: str):

    async def _run():
        # ✅ 1️⃣ CREAR O RECUPERAR SESIÓN (CLAVE)
        session = await session_service.get_or_create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        # ✅ 2️⃣ Agregar mensaje del usuario
        session.add_user_message(query)

        # ✅ 3️⃣ Ejecutar el agente
        await runner.run()

        # ✅ 4️⃣ Obtener última respuesta del agente
        return session.messages[-1].content

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    result = loop.run_until_complete(_run())
    loop.close()

    return result

# ===============================
# STREAMLIT UI
# ===============================
st.title("📊 Plataforma EDA Multiagente")

user_input = st.text_area("Escribe tu consulta:")

if st.button("Enviar") and user_input:
    with st.spinner("Pensando..."):
        response = run_agent_sync(user_input)

    st.markdown("### 🤖 Respuesta del agente")
    st.write(response)
