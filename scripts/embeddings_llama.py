"""
Se encarga de generar embeddings a partir de los chunks creados en chunker_llama.py usando el 
modelo definido en el .env, también guarda los embeddings generados en la carpeta /embeddings en formato JSON.
"""
#-->Importa librerías
from scripts.pinecone_client import upload_embeddings_to_pinecone #Importa la función para subir embeddings a Pinecone
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno
import json #Maneja la serialización y deserialización de datos en formato JSON
from pathlib import Path #Maneja rutas de archivos de forma segura y multiplataforma
from dotenv import load_dotenv #Carga las variables de entorno desde un archivo .env
from llama_index.embeddings.openai import OpenAIEmbedding #Clase de LlamaIndex para crear embeddings

#-->Carga las variables de entorno del archivo .env
load_dotenv()

#-->Obtiene el modelo de embeddings desde .env o usa un valor por defecto
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large") 

#-->Obtiene la clave API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#-->Define la carpeta donde se guardarán los embeddings
EMBEDDINGS_DIR = Path(__file__).resolve().parent / "embeddings" #Aqui se guardan los embeddings generados, EMBEDDINGS_DIR es la ruta completa de la carpeta embeddings y __file__ es el archivo actual
EMBEDDINGS_DIR.mkdir(exist_ok=True) #Crea la carpeta si no existe

#-->Función principal para generar embeddings a partir de los chunks
def generate_embeddings(chunks, filename="document"):

    #-->Verifica que la clave API de OpenAI esté disponible
    if not OPENAI_API_KEY: #Verifica que exista la API Key
        raise ValueError("Falta la variable OPENAI_API_KEY en el archivo .env") #Si no existe, lanza un error

    #-->Crea el modelo de embeddings con la API Key de OpenAI
    embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY) #Crea el modelo de embeddings con la API Key de OpenAI
    embeddings = [] #Lista donde se guardarán los resultados, podria decirse como un array

    #-->Genera embeddings para cada chunk
    for i, chunk in enumerate(chunks): #Se encarga de iterar sobre cada chunk recibido, enumerate proporciona un índice (i) y el chunk actual
        try: 
            vector = embed_model.get_text_embedding(chunk.text)  #Llama a la API de OpenAI para obtener el vector numérico del texto
            embeddings.append({
            "id": i,
            "text": chunk.text,                 
            "text_preview": chunk.text[:200],   
            "vector": vector
            })

        except Exception as e: #Captura errores en la generación de embeddings
            print(f"Error generando embedding en chunk {i}: {e}") #Muestra el error en consola

    #-->Guarda los embeddings generados en un archivo JSON
    output_path = EMBEDDINGS_DIR / f"{Path(filename).stem}_embeddings.json" #Define la ruta del archivo donde se guardarán los embeddings, usa el nombre del archivo original sin extensión

    #-->Guarda los embeddings generados en un archivo JSON
    with open(output_path, "w", encoding="utf-8") as f: #Abre el archivo en modo escritura con codificación UTF-8
        json.dump(embeddings, f, indent=4) #Guarda los embeddings en formato JSON con una indentación de 4 espacios
    print(f"Embeddings guardados en: {output_path}") #Muestra en consola la ruta del archivo guardado
    upload_embeddings_to_pinecone(embeddings) #Sube los embeddings generados a Pinecone
    return embeddings #Devuelve los embeddings generados para su uso posterior en main.py
