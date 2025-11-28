"""
Solo evalúa las variantes de las preguntas, utilizando el retrival de main.py.
Guarda: pregunta_original, pregunta_variante, ground_truth, respuesta, contexto, matches.
"""
#-->Importar Librerías
import json #Para manejar archivos JSON
import requests #Para hacer solicitudes HTTP
from pathlib import Path #Para manejar rutas de archivos

#-->Rutas de archivos
BASE = Path(__file__).resolve().parent 
PREGUNTAS_PATH = BASE / "preguntas.json"
OUTPUT_PATH = BASE / "resultados_respuestas.json"

#-->URL del endpoint del backend
API_URL = "http://127.0.0.1:8000/retrieval/"

#-->Función para consultar el endpoint del backend del retrieval
def consultar_endpoint(query):
    try:
        response = requests.post(API_URL, data={"query": query}) #Envía la pregunta al endpoint
        response.raise_for_status() #Verifica si la solicitud fue exitosa
        return response.json() #Devuelve la respuesta en formato JSON   
    except Exception as e: #Captura errores y devuelve un mensaje de error
        return {
            "answer": f"ERROR al llamar al endpoint: {e}",
            "context": "",
            "matches_found": 0
        }

#-->Función principal de la ejecución del script de la generación de respuestas
def main():

    with open(PREGUNTAS_PATH, "r", encoding="utf-8") as f: #Abre el archivo de preguntas JSON
        data = json.load(f) #Carga el contenido del archivo JSON
    resultados = [] #Lista para almacenar los resultados
 
    #-->Procesar bloques de preguntas
    for bloque in data:
        seccion = bloque["seccion"]

        #-->Procesar subtemas dentro de cada bloque
        for subtema in bloque["subtemas"]:
            tema = subtema["tema"]
            pregunta_original = subtema["pregunta_original"]
            ground_truth = subtema.get("respuesta_original", "")

            #-->Solo variaciones para evaluar
            for variante in subtema["variaciones"]:

                print(f"\n-- Consultando variante: {variante}")
                resultado_api = consultar_endpoint(variante)
                respuesta = resultado_api.get("answer", "")
                contexto = resultado_api.get("context", "")
                matches = resultado_api.get("matches_found", 0)

                #-->Guardar resultados en la lista para cada variante
                resultados.append({ # Guardar: pregunta_original, pregunta_variante, ground_truth, respuesta, contexto, matches para cada variante
                    "seccion": seccion,
                    "tema": tema,
                    "pregunta_original": pregunta_original,
                    "pregunta_variante": variante,
                    "ground_truth": ground_truth,
                    "respuesta": respuesta,
                    "contexto_usado": contexto,
                    "matches_found": matches
                })

    #-->Guarda los resultados en un archivo JSON en la ruta OUTPUT_PATH
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    #-->Imprime mensaje de finalización
    print("\n=== TERMINADO ===")
    print(f"Archivo generado: {OUTPUT_PATH}")

#-->Ejecución del script principal
if __name__ == "__main__":
    main()
