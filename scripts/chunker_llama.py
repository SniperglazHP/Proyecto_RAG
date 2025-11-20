"""
Chunker de texto usando LlamaIndex con un parser robusto
Utiliza SentenceWindowNodeParser para dividir el texto en chunks manejables
"""
#-->Importar librerias
from llama_index.core import Document #Clase principal de LlamaIndex para manejar documentos
from llama_index.core.node_parser import SentenceWindowNodeParser #Parser avanzado para dividir texto en chunks
from pathlib import Path #Maneja rutas de archivos de forma segura y multiplataforma
import re #Maneja operaciones con expresiones regulares

#-->Función principal para dividir texto en chunks usando LlamaIndex
def chunk_text(docs_or_path):

    #-->Cargar texto de forma universal con el markdown de path o lista de documentos
    if isinstance(docs_or_path, (str, Path)) and Path(docs_or_path).suffix == ".md": #Si es una ruta a un archivo markdown
        full_text = Path(docs_or_path).read_text(encoding="utf-8") #Lee el contenido del archivo
    elif isinstance(docs_or_path, list): #Si es una lista de documentos
        full_text = "\n".join([doc.text for doc in docs_or_path]) #Concatena el texto de todos los documentos
    elif isinstance(docs_or_path, str): #Si es una cadena de texto
        full_text = docs_or_path #Usa el texto directamente
    else:
        raise TypeError("Tipo no permitido.") #Lanza un error si el tipo no es soportado

    #-->Evita texto pegado sin saltos, respeta estructura en encabezados y reduce espacios
    full_text = full_text.replace("#", "\n\n# ") #Asegura saltos antes de encabezados
    full_text = re.sub(r'\s{2,}', ' ', full_text) #Reduce espacios dobles dentro del texto

    #-->Crea el documento de LlamaIndex
    document = Document(text=full_text) #Se usa Document de para manejar el texto completo y facilitar el chunking

    #-->Configura el parser de chunks
    parser = SentenceWindowNodeParser( #Usa SentenceWindowNodeParser para dividir el texto en chunks
        window_size=4,      #Tamaño típico recomendado del chunk
        window_overlap=1,   #Solapamiento ligero
    )

    #1gkdgfdsgfsdgkhgdskkj           #4fjdhfjkdsfjkgsdkfgjgfjk
    #2kfjhdkjfkjdsgfjkgdsfjkg        #5hgksjdgjkgsdjkfhjkdsjfh
    #3jfdgjkfdksjfgjksdgfjkdgjk      #6jkbdbvbkdsbfjbdbskjb
    #4fjdhfjkdsfjkgsdkfgjgfjk        #7jhdgfhgdfhgdfhgdfhgd

    #-->Genera los chunks y los devuelve como una lista de nodos
    nodes = parser.get_nodes_from_documents([document]) #Este metodo recibe una lista de documentos y devuelve una lista de nodos (chunks)
    return nodes #Devuelve la lista de chunks generados
