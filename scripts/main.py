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
#retrieval
#----------
@app.post("/retrieval/") #Se crea el endpoint de retrieval de tipo post para recibir datos del usuario
async def retrieval(query: str = Form(...)): #Creamos esta funcion asincrona que recibe un query de tipo string desde un formulario
    try:
        #-->Genera el embedding del query usando OpenAI
        embedding_response = client.embeddings.create( #Llama a la API de OpenAI para generar el embedding del query
            model="text-embedding-3-large", #Modelo de embeddings
            input=query #Texto del query proporcionado por el usuario
        )
        query_vector = embedding_response.data[0].embedding #Obtiene el vector de embedding del query

        #-->Consulta el índice de Pinecone para recuperar chunks similares
        index = pc.Index(INDEX_NAME) #Conecta al índice de Pinecone
        results = index.query( #Realiza la consulta en Pinecone usando el vector del query
            vector=query_vector, #Vector del query que dio OpenAI del usuario
            top_k=5, #Número de vectores similares de Pinecone a recuperar
            include_metadata=True #Muestra la metadata asociada a cada vector recuperado
        )

        #-->Construye el contexto de la metadata a partir de los chunks (no olvidar, es una tecnica llamada comprension de listas en python)
        context = "\n\n".join([
            match["metadata"].get("text") 
            or match["metadata"].get("preview", "")
            for match in results["matches"]
        ])


        #-->Verifica si se encontró contexto, si es asi manda de respuesta error
        if not context.strip(): #Verifica si el contexto está vacío
            return {
                "query": query,
                "answer": "No se encontró información relevante en la base vectorial.",
                "matches_found": 0
            }

        #-->Genera la respuesta usando Responses API (importante da contexto y menciona que es el reemplazo de Completions)
        response = client.responses.create( #Llama a la API de OpenAI para generar la respuesta basada en el contexto
            model=llm_model, #Modelo LLM definido en este caso gpt-5-mini
            input=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente que responde preguntas basadas en el contexto proporcionado. "
                        "Si la información no está en el contexto, indica que no la conoces."
                    )
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPregunta: {query}"
                }
            ],
        )

        #-->Obtiene la respuesta generada
        answer = response.output_text #Obtiene el texto de la respuesta generada por OpenAI

        #-->Devuelve la respuesta junto con el número de coincidencias encontradas
        return {
            "query": query,
            "answer": answer,
            "matches_found": len(results["matches"]),
            "context": context  
        }

    #-->Captura errores durante el proceso de retrieval
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error durante retrieval: {str(e)}"})
