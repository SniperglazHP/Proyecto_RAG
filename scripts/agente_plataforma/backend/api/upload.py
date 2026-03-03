from fastapi import APIRouter, UploadFile, File
from services.supabase_service import upload_dataset, save_metadata

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    path = upload_dataset(file)
    save_metadata(file.filename, path)

    return {
        "message": "Archivo subido correctamente",
        "filename": file.filename,
        "storage_path": path
    }
