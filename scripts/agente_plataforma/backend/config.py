import os

# === APP CONFIG ===
APP_NAME = "eda_dashboards"
USER_ID = "leonardo_user"

# === SUPABASE ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = "dataset"

# === ADK ===
MODEL_NAME = "gemini-2.5-flash"
