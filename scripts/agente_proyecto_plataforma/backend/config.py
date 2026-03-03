import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "plataforma_multiagente"
USER_ID = "frontend_user"

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
