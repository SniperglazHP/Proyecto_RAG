"""
Este módulo se encarga de recibir texto o documentos (Markdown) de LlamaIndex y los divide
en fragmentos (chunks) utilizando LlamaIndex.
"""
#-->Importa librerías
from llama_index.core import Document #Document representa el texto en formato interno compatible con LlamaIndex
from llama_index.core.node_parser import SimpleNodeParser #SimpleNodeParser permite dividir un documento en secciones (chunks)

#-->Función principal para chunking
def chunk_text(docs): #El docs dentro del parentesis puede ser una lista de Documentos o una cadena de texto y viene del parser_llama.py 
    if isinstance(docs, list): #Si llega una lista de documentos, concatena su texto
        full_text = "\n".join([doc.text for doc in docs if hasattr(doc, "text")]) #full_text une el texto de todos los documentos con saltos de línea
    elif isinstance(docs, str): #Si llega una cadena, la usa directamente
        full_text = docs #Aqui full_text es igual a docs para el caso de que docs sea un string
    else:
        raise TypeError("El parámetro 'docs' debe ser lista de documentos o string") #Si llega un tipo no válido, lanza un error
    
    document = Document(text=full_text) #Crea un documento con el texto completo usando la clase Document de LlamaIndex

    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=100) #Crea un parser que divide el texto en chunks de 1024 caracteres con 100 de superposición y las superposiciones sirven para mantener contexto entre chunks

    nodes = parser.get_nodes_from_documents([document]) #Obtiene los nodos (chunks) a partir del documento

    return nodes #Retorna la lista de chunks generados y los manda a embeddings_llama.py para generar embeddings
