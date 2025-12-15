"""
Este script evalúa respuestas generadas por un modelo LLM utilizando otro LLM como juez.
"""
#-->Importar librerías
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import matplotlib.pyplot as plt

#-->Configuración inicial de OpenAI y rutas del .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#-->Rutas de archivos para las entradas y salidas
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "metricas_resultados.json"
OUTPUT_PATH = BASE_DIR / "judge_resultados.json"
PLOT_PATH = BASE_DIR / "judge_plot.png"

#-->Función para evaluar utilizando un LLM como juez
def evaluar_con_juez(pregunta, ground_truth, respuesta):
    prompt = f"""
Eres un juez experto. Evalúa si la RESPUESTA es correcta respecto al GROUND TRUTH.

Reglas:
- Si coincide en significado, números, hechos → correcto = true.
- Si falta información importante → correcto = false.
- Si los datos están mal (cantidades, fechas, porcentajes) → correcto = false.
- Categoriza el error como:
    - "omision"
    - "dato_incorrecto"
    - "respuesta_parcial"
    - "irrelevante"
    - "ninguno" (si es correcta)

Responde SOLO en JSON:

{{
    "correcto": <true/false>,
    "confianza": <number 0-1>,
    "error_tipo": "<tipo>",
    "razon": "<explicacion corta>"
}}

PREGUNTA: {pregunta}
GROUND TRUTH: {ground_truth}
RESPUESTA: {respuesta}
"""
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )
        raw = response.output_text

        #-->Convertir a diccionario JSON
        data = json.loads(raw)
        return data

    except Exception as e:
        return {
            "correcto": False,
            "confianza": 0,
            "error_tipo": "error_llm",
            "razon": f"No se pudo evaluar: {e}"
        }

#-->Función principal para ejecutar el proceso
def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        metricas = json.load(f)

    resultados_finales = []
    total_correctas = 0
    total_incorrectas = 0

    print("\n---EVALUANDO RESPUESTAS CON LLM AS A JUDGE---\n")

    for item in metricas:
        pregunta = item["pregunta_variante"]
        ground = item["ground_truth"]
        respuesta = item["respuesta_generada"]

        print(f"Evaluando: {pregunta}")

        #-->extraer F1 de bertscore del archivo
        f1 = item["metricas"]["bertscore"]["f1"]

        evaluacion = evaluar_con_juez(
            pregunta=pregunta,
            ground_truth=ground,
            respuesta=respuesta
        )

        if evaluacion["correcto"]:
            total_correctas += 1
        else:
            total_incorrectas += 1

        resultados_finales.append({
            "seccion": item["seccion"],
            "tema": item["tema"],
            "pregunta_variante": pregunta,
            "ground_truth": ground,
            "respuesta_generada": respuesta,
            "bertscore_f1": f1,
            "evaluacion_juez": evaluacion
        })

    #-->Guardar salida final
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados_finales, f, indent=4, ensure_ascii=False)
    print("\n---PROCESO TERMINADO---")
    print(f"-->Resultados guardados en: {OUTPUT_PATH}")

    #-->Gráfica de las resultados
    labels = ["Correctas", "Incorrectas"]
    valores = [total_correctas, total_incorrectas]
    total = total_correctas + total_incorrectas
    pct_correctas = total_correctas / total * 100
    pct_incorrectas = total_incorrectas / total * 100
    colores = ["#4CAF50", "#F44336"]
    plt.figure(figsize=(8, 6), dpi=150)

    #-->Barras
    bars = plt.bar(labels, valores, color=colores, alpha=0.85)

    #-->Título
    plt.title("Evaluación Final — LLM as Judge", fontsize=16, fontweight="bold")

    #-->Etiqueta del eje Y
    plt.ylabel("Número de Respuestas", fontsize=12)

    #-->Grid elegante
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    #-->Texto encima de cada barra con conteo y porcentaje
    for i, bar in enumerate(bars):
        height = bar.get_height()
        pct = pct_correctas if i == 0 else pct_incorrectas
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height} ({pct:.1f}%)",
            ha="center",
            fontsize=12,
            fontweight="bold"
        )

    #-->Línea horizontal de referencia
    plt.axhline(total / 2, color="gray", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    plt.show()
    print(f"Gráfica mejorada guardada en: {PLOT_PATH}")

#-->Ejecutar del script principal
if __name__ == "__main__":
    main()
