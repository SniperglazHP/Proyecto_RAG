"""
Aqui es el FastAPI principal para ingesta de archivos, parsing, chunking y embeddings
"""
#-->Importa librerías
from fastapi import FastAPI, UploadFile, File #Importa FastAPI y clases para manejo de archivos subidos
from tests.parser_llama import parse_document #Importa la función de parsing de documentos
from tests.chunker_llama import chunk_text #Importa la función de chunking de texto
from tests.embeddings_llama import generate_embeddings #Importa la función de generación de embeddings
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno

#-->Crea la aplicación FastAPI con el nombre "app"
app = FastAPI()

#-->Define el endpoint /ingesta/ que recibe un archivo y procesa todo el flujo
@app.post("/ingesta/")
async def process_document(file: UploadFile = File(...)): #Recibe un archivo subido por el usuario
    """
    Este Endpoint de ingesta se va a encargar de lo siguiente:
    -->Recibe un archivo PDF, DOCX, TXT o imagen.
    -->Lo convierte a Markdown (.md) usando LlamaIndex.
    -->Lo divide en chunks.
    -->Genera embeddings del texto.
    """
    upload_dir = "uploads" #Define la carpeta donde se guardan los archivos subidos
    os.makedirs(upload_dir, exist_ok=True) #Crea la carpeta si no existe

    file_path = os.path.join(upload_dir, file.filename) #Define la ruta completa del archivo subido
    with open(file_path, "wb") as f: #Guarda el archivo subido en la carpeta uploads
        f.write(await file.read()) #Escribe el contenido del archivo subido

    #-->Paso 1: Parsing (incluye OCR si el archivo es imagen)
    docs = parse_document(file_path)

    #-->Paso 2: Chunking del texto
    chunks = chunk_text(docs)

    #-->Paso 3: Generación de embeddings
    embeddings = generate_embeddings(chunks, filename=file.filename)

    return { #Retorna un resumen del proceso
        "filename": file.filename, #Nombre del archivo subido
        "total_chunks": len(chunks), #Total de chunks generados
        "embedding_model": os.getenv("EMBEDDING_MODEL"), #Modelo de embeddings utilizado
        "embedding_preview": embeddings[:2],  # Muestra los primeros 2 embeddings
    }
