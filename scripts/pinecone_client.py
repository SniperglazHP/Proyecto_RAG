"""
Este codigo se encarga de la configuración e interacción con Pinecone,
un servicio de base de datos vectorial en la nube, para almacenar y gestionar
"""
#-->Importa librerías
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno
from dotenv import load_dotenv #Carga las variables de entorno desde un archivo .env
from pinecone import Pinecone, ServerlessSpec #Librería oficial de Pinecone para interactuar con su servicio

#-->Carga las variables de entorno del archivo .env
load_dotenv() #Asegúrate de tener esto ANTES de usar os.getenv

#-->Inicializa Pinecone con tu API Key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY")) #Usa la clave API desde .env

#-->Obtiene el nombre del índice desde .env
INDEX_NAME = os.getenv("INDEX_NAME", "rag-index") #Nombre del índice en Pinecone

#-->Verifica si el índice ya existe
if INDEX_NAME not in [index["name"] for index in pc.list_indexes()]: #Lista los índices existentes y verifica si el deseado ya está creado
    print(f"-->Creando índice '{INDEX_NAME}' con dimensión 3072 (text-embedding-3-large)...") #Crea el índice si no existe
    pc.create_index(
        name=INDEX_NAME, #Nombre del índice
        dimension=3072, #Modelo text-embedding-3-large
        metric="cosine", #Métrica de similitud
        spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENV", "us-east-1")) #Especificaciones del servidor
    )
else:
    print(f"-->Índice '{INDEX_NAME}' ya existe en Pinecone.") #Si no el índice ya existente

#-->Conecta al índice existente o recién creado
index = pc.Index(INDEX_NAME) #Crea una instancia del índice para operaciones posteriores

#-->Función para subir embeddings al índice en Pinecone
def upload_embeddings_to_pinecone(embeddings): #Recibe una lista de embeddings generados
    vectors = [] #Lista para almacenar los vectores formateados
    for emb in embeddings: #Itera sobre cada embedding
        vectors.append({ #Prepara el formato requerido por Pinecone
            "id": str(emb["id"]), #Usa el ID como cadena
            "values": emb["vector"],  #Usa el vector completo generado
            "metadata": {"text_preview": emb["text_preview"]} #Incluye una vista previa del texto como metadato
        })

    index.upsert(vectors=vectors) #Sube los vectores al índice en Pinecone
    print(f"-->{len(vectors)} embeddings subidos correctamente al índice '{INDEX_NAME}' en Pinecone.") #Confirma la subida exitosa
