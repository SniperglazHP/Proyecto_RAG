"""
En este archivo se crean los endpoints principales para trabajar con el sistema RAG usando FastAPI
"""
#-->Importa librerías
from fastapi import FastAPI, UploadFile, File, Form  # Maneja la creación de la API y la carga de archivos
from fastapi.responses import JSONResponse  # Respuestas JSON personalizadas
import os  # Operaciones del sistema
from dotenv import load_dotenv  # Carga variables de entorno
from openai import OpenAI  # Cliente oficial de OpenAI
from scripts.parser_docling import parse_with_docling  # Conversión a Markdown con Docling
from scripts.chunker_llama import chunk_text  # Divide texto en chunks
from scripts.embeddings_llama import generate_embeddings  # Genera embeddings usando OpenAI
from scripts.pinecone_client import pc, INDEX_NAME  # Cliente Pinecone y nombre del índice

#-->Carga variables de entorno en el .env
load_dotenv()

#-->Inicializa FastAPI
app = FastAPI(title="Proyecto RAG")

#-->Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm_model = os.getenv("LLM_MODEL", "gpt-5-mini")

#--------
#ingesta
#--------
@app.post("/ingesta/")
async def process_document(file: UploadFile = File(...)):
    """
    Procesa un documento:
    - Lo convierte a texto markdown con Docling
    - Divide el texto en chunks
    - Genera embeddings con OpenAI
    - Sube los embeddings al índice de Pinecone
    """
    try:
        #-->Guarda el archivo subido
        file_path = os.path.join("scripts", "uploads", file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        #-->Convierte el documento a Markdown con Docling
        md_path = parse_with_docling(file_path)

        #-->Lee el contenido del Markdown
        with open(md_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        #-->Divide en chunks manejables
        chunks = chunk_text(text_content)

        #-->Genera embeddings y los sube a Pinecone (usa nombre del archivo como referencia)
        embeddings = generate_embeddings(chunks, filename=file.filename)
        print(f"-->Documento procesado y embeddings generados para: {file.filename}")

        return {
            "message": "Documento procesado correctamente.",
            "chunks_created": len(chunks),
            "embeddings_stored": len(embeddings),
            "file": file.filename
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error procesando documento: {str(e)}"})


#----------
#retrieval
#----------
@app.post("/retrieval/")
async def retrieval(query: str = Form(...)):
    """
    Realiza una búsqueda semántica sobre los embeddings almacenados en Pinecone
    y genera una respuesta contextual con el modelo GPT-5-mini.
    """
    try:
        #-->Genera el embedding de la consulta
        embedding_response = client.embeddings.create(
            model="text-embedding-3-large",
            input=query
        )
        query_vector = embedding_response.data[0].embedding

        #-->Consulta semántica en Pinecone
        index = pc.Index(INDEX_NAME)
        results = index.query(
            vector=query_vector,
            top_k=5,
            include_metadata=True
        )

        #-->Construye contexto a partir de los textos recuperados
        context = "\n\n".join([
            match["metadata"]["text_preview"]
            for match in results["matches"]
        ])

        if not context.strip():
            return {
                "query": query,
                "answer": "No se encontró información relevante en la base vectorial.",
                "matches_found": 0
            }

        #-->Genera la respuesta usando GPT-5-mini
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente que responde de forma breve y clara "
                        "usando solo la información del contexto. "
                        "Si el contexto no contiene la respuesta, responde: "
                        "'No tengo información sobre eso en mis datos.'"
                    )
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPregunta:\n{query}"
                }
            ],
            max_completion_tokens=400
        )

        #-->Extrae la respuesta del modelo (GPT-5-mini usa 'output' y 'content')
        answer = None
        if hasattr(response, "output"):
            try:
                answer = response.output[0].content[0].text
            except Exception:
                answer = None
        elif hasattr(response, "choices") and len(response.choices) > 0:
            message_obj = response.choices[0].message
            answer = getattr(message_obj, "content", None)

        return {
            "query": query,
            "answer": answer if answer else "No se obtuvo respuesta del modelo.",
            "matches_found": len(results["matches"]),
            "retrieved_documents": [
                {
                    "id": match["id"],
                    "similarity_score": match["score"],
                    "text_excerpt": match["metadata"]["text_preview"][:200],
                }
                for match in results["matches"]
            ],
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error durante el retrieval: {str(e)}"}
        )
