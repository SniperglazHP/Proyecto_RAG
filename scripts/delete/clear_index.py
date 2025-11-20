"""
Este script elimina todos los vectores del índice de Pinecone rag-index
"""
#-->Importa librerías
from pinecone import Pinecone #Librería oficial de Pinecone
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno
from dotenv import load_dotenv #Carga las variables de entorno desde un archivo .env

#-->Carga las variables de entorno del archivo .env
load_dotenv()

#-->Inicializa Pinecone con la API Key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#-->Elimina todos los vectores del índice rag-index
index_name = "rag-index"
index = pc.Index(index_name)
index.delete(delete_all=True)

#-->Confirma la eliminación
print("-->Todos los vectores han sido eliminados del índice.")
