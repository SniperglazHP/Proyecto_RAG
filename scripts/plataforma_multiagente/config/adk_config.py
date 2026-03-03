import os
from dotenv import load_dotenv

load_dotenv()

ADK_CONFIG = {
    "model": "gemini-2.5-flash",
    "api_key": os.getenv("GOOGLE_API_KEY"),
}
