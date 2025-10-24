"""
Se usa FastAPI que orquesta el flujo de parsing (Docling),
chunking (LlamaIndex) y embeddings (OpenAI).
"""
#-->Importa librerías
from fastapi import FastAPI, UploadFile, File #Framework web para crear APIs rápidas y manejo de archivos subidos
from scripts.parser_docling import parse_with_docling #Función para convertir documentos a Markdown usando Docling
from scripts.chunker_llama import chunk_text #Función para dividir texto en chunks usando LlamaIndex
from scripts.embeddings_llama import generate_embeddings #Función para generar embeddings usando OpenAI
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno

#-->Crea la aplicación FastAPI
app = FastAPI()

#-->Define el endpoint principal para procesar documentos
@app.post("/process/") #Define un endpoint POST en /process/
async def process_document(file: UploadFile = File(...)): #Recibe un archivo subido
    """
    Flujo principal:
    1. Recibe un archivo (PDF, DOCX, CSV, XLS, TXT, imagen, etc.).
    2. Lo convierte a Markdown con Docling.
    3. Divide el texto en chunks.
    4. Genera embeddings.
    """
    upload_dir = "uploads" #Carpeta donde se guardan los archivos subidos
    os.makedirs(upload_dir, exist_ok=True) #Crea la carpeta si no existe

    file_path = os.path.join(upload_dir, file.filename) #Ruta completa del archivo subido
    with open(file_path, "wb") as f: #Abre el archivo en modo escritura binaria
        f.write(await file.read()) #Escribe el contenido del archivo subido

    #-->Paso 1: Parsing con Docling
    md_path = parse_with_docling(file_path) #Convierte el archivo a Markdown y obtiene la ruta del archivo .md generado

    #-->Paso 2: Chunking con LlamaIndex 
    chunks = chunk_text(md_path) #Divide el texto del archivo .md en chunks

    #-->Paso 3: Generación de embeddings
    embeddings = generate_embeddings(chunks, filename=file.filename) #Genera embeddings a partir de los chunks

    return { #Respuesta JSON con detalles del procesamiento
        "filename": file.filename,
        "markdown_file": str(md_path),
        "total_chunks": len(chunks),
        "embedding_model": os.getenv("EMBEDDING_MODEL"),
        "embedding_preview": embeddings[:2],
    }
