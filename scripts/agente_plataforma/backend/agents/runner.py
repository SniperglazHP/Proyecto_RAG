# agents/runner.py

import os
from dotenv import load_dotenv

APP_NAME = "eda_dashboards"
USER_ID = "leonardo_test"
SESSION_INGESTION = "ingestion_session"
SESSION_ANALYSIS = "analysis_session"
SESSION_DASHBOARD = "dashboard_session"


async def run_agent(runner, session_service, session_id, query):
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    response = await runner.run(
        session=session,
        input=query
    )

    return response
