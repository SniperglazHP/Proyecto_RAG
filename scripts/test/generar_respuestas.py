"""
Este script carga un conjunto de preguntas desde un archivo JSON, genera respuestas automáticas
utilizando un el RAG previamente hecho y guarda los resultados en un archivo JSON.
"""
#-->Importar Librerías
import json #Manejo de archivos JSON
import os #Interacción con el sistema operativo
from pathlib import Path #Manejo de rutas de archivos
from openai import OpenAI #Cliente OpenAI
from dotenv import load_dotenv #Cargar variables de entorno
from pinecone import Pinecone #Cliente Pinecone
import sys #Manipulación de rutas del sistema
from pinecone_client import INDEX_NAME, pc #Importar configuración de Pinecone

#-->Agregar ruta del proyecto al sys.path para importar módulos correctamente
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

#-->Cargar variables de entorno
load_dotenv()

#-->Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#-->Ruta del archivo de preguntas
PREGUNTAS_PATH = Path(__file__).resolve().parent / "preguntas.json"

#-->Archivo donde guardaremos respuestas automáticas
OUTPUT_PATH = Path(__file__).resolve().parent / "resultados_respuestas.json"

#-->Función para generar respuesta
def generar_respuesta(query):

    #-->Esta parte genera el embedding de la consulta para buscar en Pinecone
    embedding_response = client.embeddings.create(
        model="text-embedding-3-large",
        input=query
    )
    query_vector = embedding_response.data[0].embedding #data es una lista, tomamos el primer embedding

    #-->Accedo a Pinecone y busco el contexto relevante
    index = pc.Index(INDEX_NAME) #Acceder al índice de Pinecone
    results = index.query(
        vector=query_vector,
        top_k=5, #Le decimos a pinecone que nos traiga los 5 matches más relevantes
        include_metadata=True
    )

    #-->Aquí construyo el contexto a partir de los resultados obtenidos
    contexto = "\n\n".join([
        match["metadata"].get("text") or match["metadata"].get("preview", "") 
        for match in results["matches"] 
    ])

    #-->Manejo caso sin contexto
    if not contexto.strip():
        contexto = "(No se encontró contexto relevante en Pinecone.)"

    #-->Genero la respuesta usando el contexto con OpenAI
    response = client.responses.create(
        model=os.getenv("LLM_MODEL", "gpt-5-mini"),
        input=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente que responde únicamente con la información "
                    "del contexto dado. Si no está en el contexto, responde: "
                    "'No hay información suficiente en el contexto'."
                )
            },
            {
                "role": "user",
                "content": f"Contexto:\n{contexto}\n\nPregunta: {query}"
            }
        ],
    )
    answer = response.output_text
    return answer, contexto

#-->Función principal que hace el proceso completo de la generación de respuestas
def main():
    with open(PREGUNTAS_PATH, "r", encoding="utf-8") as f: #Abrir archivo de preguntas
        data = json.load(f) #Cargar preguntas desde JSON
    resultados = []

    #-->Aqui iteramos sobre cada bloque de preguntas
    for bloque in data:
        seccion = bloque["seccion"]

        for subtema in bloque["subtemas"]:
            tema = subtema["tema"]

            todas = [subtema["pregunta_original"]] + subtema["variaciones"] #Combinar pregunta original y variaciones

            for pregunta in todas:
                print(f"\n----- Procesando: {pregunta} -----")

                respuesta, contexto = generar_respuesta(pregunta)

                resultados.append({
                    "seccion": seccion,
                    "tema": tema,
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                    "contexto_usado": contexto
                })

    #-->Guardamos resultados
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    #-->Mensaje de finalización
    print("\n\n=== PROCESO FINALIZADO ===")
    print(f"Respuestas guardadas en: {OUTPUT_PATH}")

#-->Ejecutar función principal
if __name__ == "__main__":
    main()
