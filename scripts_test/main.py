"""
main.py
-------
API con FastAPI que:
1. Recibe un archivo (PDF, DOCX, XLS, CSV, TXT o imagen).
2. Usa Docling para procesarlo.
3. Guarda el resultado como archivo .md en /outputs.
"""

from fastapi import FastAPI, UploadFile, File
from scripts_test.parser_docling import parse_with_docling
import os

app = FastAPI(title="Docling Markdown Converter API")

@app.post("/convert/")
async def convert_file(file: UploadFile = File(...)):
    """
    Endpoint para convertir cualquier archivo soportado a Markdown usando Docling.
    """
    # Carpeta temporal para subir el archivo
    upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Ruta completa donde se guardará el archivo subido
    file_path = os.path.join(upload_dir, file.filename)

    # Guarda el archivo en el servidor
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Procesar con Docling
    md_path = parse_with_docling(file_path)

    return {
        "filename": file.filename,
        "markdown_path": md_path,
        "message": "Archivo convertido exitosamente con Docling."
    }
