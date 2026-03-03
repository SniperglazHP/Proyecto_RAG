import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

BUCKET_NAME = "dataset"

def upload_file_to_supabase(file_bytes, filename):
    path = f"{datetime.utcnow().timestamp()}_{filename}"
    supabase.storage.from_(BUCKET_NAME).upload(path, file_bytes)
    return path

def save_dataset_metadata(filename, storage_path):
    data = {
        "filename": filename,
        "storage_path": storage_path
    }
    supabase.table("datasets").insert(data).execute()
    return data
