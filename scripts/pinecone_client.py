import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()  #Asegúrate de tener esto ANTES de usar os.getenv

# Inicializa Pinecone con tu API Key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Obtiene el nombre del índice desde .env
INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")

# Verifica si el índice ya existe
if INDEX_NAME not in [index["name"] for index in pc.list_indexes()]:
    print(f"-->Creando índice '{INDEX_NAME}' con dimensión 3072 (text-embedding-3-large)...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,  #Modelo text-embedding-3-large
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENV", "us-east-1"))
    )
else:
    print(f"-->Índice '{INDEX_NAME}' ya existe en Pinecone.")

# Conecta al índice existente o recién creado
index = pc.Index(INDEX_NAME)

def upload_embeddings_to_pinecone(embeddings):
    """
    Sube los embeddings generados a Pinecone.
    Espera una lista con formato:
    [{"id": 0, "text_preview": "...", "vector": [...]}]
    """
    vectors = []
    for emb in embeddings:
        vectors.append({
            "id": str(emb["id"]),
            "values": emb["vector"],  #Usa el vector completo
            "metadata": {"text_preview": emb["text_preview"]}
        })

    #-->Envía los vectores al índice en la nube
    index.upsert(vectors=vectors)
    print(f"-->{len(vectors)} embeddings subidos correctamente al índice '{INDEX_NAME}' en Pinecone.")
