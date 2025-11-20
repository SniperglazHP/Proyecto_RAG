"""
Este codigo se encarga de la configuración e interacción con Pinecone,
"""
#-->Importa librerías
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno
import uuid #Genera identificadores únicos para evitar reemplazos en Pinecone
from dotenv import load_dotenv #Carga las variables de entorno desde un archivo .env
from pinecone import Pinecone, ServerlessSpec #Librería oficial de Pinecone

#-->Carga las variables de entorno del archivo .env
load_dotenv()

#-->Inicializa Pinecone con la API Key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#-->Obtiene el nombre del índice desde .env
INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")

#-->Verifica si el índice ya existe
if INDEX_NAME not in [index["name"] for index in pc.list_indexes()]: #Aqui se hace la verificación
    print(f"-->Creando índice '{INDEX_NAME}' con dimensión 3072 (text-embedding-3-large)...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=3072, #Dimensión para text-embedding-3-large
        metric="cosine", #cosine sirve para medir similitud angular de vectores
        spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENV", "us-east-1")) #Especificaciones del servidor
    )
else:
    print(f"-->Índice '{INDEX_NAME}' ya existe en Pinecone.")

#-->Conecta al índice existente o recién creado
index = pc.Index(INDEX_NAME)

#-->Función para subir embeddings al índice en Pinecone
def upload_embeddings_to_pinecone(embeddings): #Esta función sube los embeddings generados al índice de Pinecone
    vectors = [] #Lista para almacenar los vectores a subir
    for emb in embeddings: #emb es una lista de vectores con sus IDs y datos asociados

        #-->Genera un ID único para cada embedding para evitar reemplazos
        unique_id = f"{emb['id']}_{uuid.uuid4().hex[:8]}"
        
        #-->Prepara el formato requerido para los vectores en Pinecone
        vectors.append({ 
            "id": unique_id,
            "values": emb["vector"],
            "metadata": {
                "text": emb.get("text", ""),       
                "preview": emb.get("preview", "")
            }

        })

    #-->Sube los vectores al índice
    index.upsert(vectors=vectors)

    #-->Confirma la subida de embeddings
    print(f"-->{len(vectors)} embeddings subidos correctamente al índice '{INDEX_NAME}' en Pinecone con IDs únicos.")
