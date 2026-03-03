from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_BUCKET

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def upload_dataset(file):
    content = file.file.read()
    path = f"{file.filename}"

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        content,
        {"content-type": file.content_type}
    )

    return path


def save_metadata(filename, storage_path):
    supabase.table("datasets").insert({
        "filename": filename,
        "storage_path": storage_path
    }).execute()
