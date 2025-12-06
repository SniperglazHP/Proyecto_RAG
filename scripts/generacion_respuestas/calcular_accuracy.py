"""
Este script calcula el accuracy del conjunto de respuestas generadas
"""
#-->Importar librerías
import json
from pathlib import Path

#-->Ruta del archivo json de métricas
BASE = Path(__file__).resolve().parent
INPUT = BASE / "metricas_resultados.json"

with open(INPUT, "r", encoding="utf-8") as f: #Abrir archivo JSON con métricas
    data = json.load(f) #Cargar datos del archivo JSON

#-->Umbral para considerar una respuesta como correcta
THRESHOLD = 0.75
tp = 0 #Verdaderos positivos
fn = 0 #Falsos negativos

#-->Calcular accuracy utilizando BertScore
for item in data:
    f1 = item["metricas"]["bertscore"]["f1"]
    if f1 >= THRESHOLD:
        tp += 1
    else:
        fn += 1

accuracy = tp / (tp + fn)

#-->Imprimir resultados
print("=== RESULTADOS DE ACCURACY ===")
print(f"Umbral usado: {THRESHOLD}")
print(f"Respuestas correctas (TP): {tp}")
print(f"Respuestas incorrectas (FN): {fn}")
print(f"Accuracy final: {accuracy:.4f}")
