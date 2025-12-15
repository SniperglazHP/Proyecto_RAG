"""
Genera resultados_respuestas.json tomando preguntas de preguntas.json
"""
#-->Importar librerias
import json
import requests
from pathlib import Path

#-->Rutas de los archivos
BASE = Path(__file__).resolve().parent
PREGUNTAS_PATH = BASE / "preguntas.json"
OUTPUT_PATH = BASE / "resultados_respuestas.json"

#-->URL del endpoint del retrieval
API_URL = "http://127.0.0.1:8000/retrieval/"

#-->Funciones auxiliares para extraer doc_id
def extraer_doc_id(match):

    if "doc_id" in match and match["doc_id"]:
        return match["doc_id"]

    if "id" in match and match["id"]:
        return match["id"]

    meta = match.get("metadata", {})
    posibles = ["id", "doc_id", "chunk_id", "text_id", "source_id", "page_id"]

    for k in posibles:
        if k in meta and meta[k]:
            return meta[k]

    return f"unknown_{match.get('score', 0)}"


#--------------------------
# Llamada al endpoint
#--------------------------
def consultar_endpoint(query):
    try:
        response = requests.post(API_URL, data={"query": query})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "answer": f"ERROR: {e}",
            "context": "",
            "matches_found": 0,
            "results": []
        }


#--------------------------
# Script principal
#--------------------------
def main():

    with open(PREGUNTAS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = []

    print("\n=== GENERANDO resultados_respuestas.json ===\n")

    for bloque in data:
        seccion = bloque["seccion"]

        for subtema in bloque["subtemas"]:
            tema = subtema["tema"]
            pregunta_original = subtema["pregunta_original"]
            ground_truth = subtema.get("respuesta_original", "")

            for variante in subtema["variaciones"]:
                print(f"-- Consultando: {variante}")

                resultado_api = consultar_endpoint(variante)

                respuesta = resultado_api.get("answer", "")
                contexto = resultado_api.get("context", "")
                matches = resultado_api.get("matches_found", 0)

                # AQUÍ SE TOMA LO IMPORTANTE: "results"
                backend_results = resultado_api.get("results", [])

                retrieval_results = []

                for r in backend_results:
                    retrieval_results.append({
                        "doc_id": r.get("doc_id") or extraer_doc_id(r),
                        "score": r.get("score"),
                        "rank": r.get("rank")
                    })

                # Guardar resultados finales
                resultados.append({
                    "seccion": seccion,
                    "tema": tema,
                    "pregunta_original": pregunta_original,
                    "pregunta_variante": variante,
                    "ground_truth": ground_truth,
                    "respuesta": respuesta,
                    "contexto_usado": contexto,
                    "matches_found": matches,

                    # IMPORTANTE --> Esto sí lo usa IR-métricas
                    "results": retrieval_results
                })

    # Guardar archivo final
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("\n=== TERMINADO ===")
    print(f"Archivo generado: {OUTPUT_PATH}")


#--------------------------
# Ejecutar main
#--------------------------
if __name__ == "__main__":
    main()
