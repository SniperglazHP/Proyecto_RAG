"""
Script para evaluar respuestas de resultados_respuestas.json usando tres métricas:
->Levenshtein Distance
->Sentence Similarity
->BERTScore
"""
#-->Importar librerías
import json #Manejo los archivos JSON
import os #Interacción con el sistema operativo
from pathlib import Path #Manejo de rutas de archivos
from dotenv import load_dotenv #Cargar variables de entorno
from openai import OpenAI #Cliente OpenAI
from rapidfuzz.distance import Levenshtein #libreria encargada de calcular la distancia de Levenshtein
from scipy.spatial.distance import cosine #libreria para calcular la distancia coseno
from bert_score import score as bert_score #libreria para calcular BERTScore

#-->Cargar .env
load_dotenv()

#-->Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#-->Rutas de archivos json
INPUT_PATH = Path(__file__).resolve().parent / "resultados_respuestas.json"
OUTPUT_PATH = Path(__file__).resolve().parent / "metricas_resultados.json"


#----------------------------------
#-->Metrica 1: Levenshtein Distance
#----------------------------------
def levenshtein_score(a, b): #Calcula la similitud basada en la distancia de Levenshtein
    try:
        dist = Levenshtein.distance(a, b) #Calcular la distancia de Levenshtein
        max_len = max(len(a), len(b)) #Longitud máxima entre las dos cadenas
        return 1 - dist / max_len if max_len > 0 else 0 #Normalizar a un valor entre 0 y 1
    except:
        return 0

#---------------------------------
#-->Metrica 2: Sentence Similarity
#---------------------------------
def sentence_similarity(a, b):
    try:
        emb1 = client.embeddings.create(
            model="text-embedding-3-large",
            input=a
        ).data[0].embedding

        emb2 = client.embeddings.create(
            model="text-embedding-3-large",
            input=b
        ).data[0].embedding

        sim = 1 - cosine(emb1, emb2)
        return float(sim)
    except:
        return 0

#-----------------------
#-->Metrica 3: BERTScore
#-----------------------
def bertscore_metric(a, b):
    try:
        P, R, F1 = bert_score([a], [b], lang="es", verbose=False)
        return {
            "precision": float(P[0]),
            "recall": float(R[0]),
            "f1": float(F1[0])
        }
    except:
        return {
            "precision": 0,
            "recall": 0,
            "f1": 0
        }

#-->Proceso principal para evaluar las respuestas y guardar las métricas
def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    metricas = []

    for item in data:
        respuesta = item["respuesta"]
        ground = item["ground_truth"]

        print(f"\nEvaluando: {item['pregunta_variante']}")

        # Calcular métricas
        lev = levenshtein_score(respuesta, ground)
        sent = sentence_similarity(respuesta, ground)
        bert = bertscore_metric(respuesta, ground)

        metricas.append({
            "seccion": item["seccion"],
            "tema": item["tema"],
            "pregunta_original": item["pregunta_original"],
            "pregunta_variante": item["pregunta_variante"],
            "ground_truth": ground,
            "respuesta_generada": respuesta,

            "metricas": {
                "levenshtein": lev,
                "sentence_similarity": sent,
                "bertscore": bert
            }
        })

    #-->Guardar JSON final
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=4, ensure_ascii=False)

    print("\n=== PROCESO COMPLETADO ===")
    print(f"-->Métricas guardadas en: {OUTPUT_PATH}")

#-->Ejecutar el proceso principal
if __name__ == "__main__":
    main()
