"""
En este archivo se crean los endpoints principales para trabajar con el sistema RAG usando FastAPI
"""
#-->Importa librerías
from fastapi import FastAPI, UploadFile, File, Form  #Maneja la creación de la API y la carga de archivos
from fastapi.responses import JSONResponse  #Respuestas JSON personalizadas
import os  # Operaciones del sistema
from dotenv import load_dotenv  # Carga variables de entorno
from openai import OpenAI  # Cliente oficial de OpenAI
from scripts.parser_docling import parse_with_docling  # Conversión a Markdown con Docling
from scripts.chunker_llama import chunk_text  # Divide texto en chunks
from scripts.embeddings_llama import generate_embeddings  # Genera embeddings usando OpenAI
from scripts.pinecone_client import pc, INDEX_NAME  # Cliente Pinecone y nombre del índice
from scripts.agentes.agente_postprocesamiento import ejecutar_agente_postprocesamiento

#-->Carga variables de entorno en el .env
load_dotenv()

#-->Inicializa FastAPI esto es una instancia de la app
app = FastAPI(title="Proyecto RAG")

#-->Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Este es mi cliente de OpenAI
llm_model = os.getenv("LLM_MODEL", "gpt-5-mini")

#--------
#ingesta
#--------
@app.post("/ingesta/")
async def ingesta(file: UploadFile = File(...)):
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
# retrieval
#----------
@app.post("/retrieval/")
async def retrieval(query: str = Form(...)):
    try:
        embedding_response = client.embeddings.create(
            model="text-embedding-3-large",
            input=query
        )
        query_vector = embedding_response.data[0].embedding

        index = pc.Index(INDEX_NAME)
        results = index.query(
            vector=query_vector,
            top_k=10,
            include_metadata=True
        )

        context = "\n\n".join([
            match["metadata"].get("text")
            or match["metadata"].get("preview", "")
            for match in results.get("matches", [])
        ])

        if not context.strip():
            return {
                "query": query,
                "answer": "No se encontró información relevante.",
                "matches_found": 0,
                "context": "",
                "results": []
            }

        response = client.responses.create(
            model=llm_model,
            input=[
                {
                    "role": "system",
                    "content": "Responde solo con base en el contexto."
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPregunta: {query}"
                }
            ],
        )

        answer_base = response.output_text

        # ✅ AHORA SÍ: await correcto
        answer_mejorada = await ejecutar_agente_postprocesamiento(
            pregunta=query,
            contexto=context,
            respuesta_base=answer_base
        )

        retrieval_results = []
        for i, match in enumerate(results.get("matches", [])):
            retrieval_results.append({
                "doc_id": match.get("id"),
                "score": match.get("score"),
                "metadata": match.get("metadata", {}),
                "rank": i + 1
            })

        return {
            "query": query,
            "answer": answer_mejorada,
            "matches_found": len(results.get("matches", [])),
            "context": context,
            "results": retrieval_results
        }

    except Exception as e:
        print("❌ ERROR RETRIEVAL:", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )



