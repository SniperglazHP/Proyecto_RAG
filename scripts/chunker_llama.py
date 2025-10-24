"""
Este módulo que recibe texto o documentos y los divide
en fragmentos chunks para facilitar su procesamiento posterior.
"""
#-->Importa librerías
from llama_index.core import Document #Clase de LlamaIndex que representa un documento de texto
from llama_index.core.node_parser import SimpleNodeParser #Clase de LlamaIndex para dividir documentos en nodos/chunks
from pathlib import Path #Maneja rutas de archivos de forma segura y de manera multiplataforma

#-->Función principal para dividir texto o documentos en chunks 
def chunk_text(docs_or_path): #Recibe una lista de documentos, texto plano o una ruta a un archivo .md
    # Si se pasa una ruta a archivo .md
    if isinstance(docs_or_path, (str, Path)) and Path(docs_or_path).suffix == ".md":
        with open(docs_or_path, "r", encoding="utf-8") as f:
            full_text = f.read()

    elif isinstance(docs_or_path, list):
        full_text = "\n".join([doc.text for doc in docs_or_path if hasattr(doc, "text")])

    elif isinstance(docs_or_path, str):
        full_text = docs_or_path

    else:
        raise TypeError("El parámetro debe ser lista de documentos, string o ruta .md válida.")

    # Crear documento y dividirlo en chunks
    document = Document(text=full_text)
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=100)
    nodes = parser.get_nodes_from_documents([document])
    return nodes
