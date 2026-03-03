import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_SERVICE_KEY:", "OK" if os.getenv("SUPABASE_SERVICE_KEY") else "MISSING")


def upload_file_to_storage(file_path: str, filename: str) -> str:
    """
    Sube un archivo al bucket 'datasets' y devuelve el path en storage
    """
    with open(file_path, "rb") as f:
        supabase.storage.from_("datasets").upload(
            path=filename,
            file=f,
            file_options={"content-type": "application/octet-stream"}
        )

    return filename
