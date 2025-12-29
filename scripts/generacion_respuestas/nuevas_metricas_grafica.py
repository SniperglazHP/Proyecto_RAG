import json
import matplotlib.pyplot as plt
from pathlib import Path

METRICAS_PATH = Path(__file__).resolve().parent / "metricas_finales.json"

with open(METRICAS_PATH, "r", encoding="utf-8") as f:
    metricas = json.load(f)

preguntas = list(metricas.keys())

# Extraer métricas
P10 = [metricas[p]["P@10"] for p in preguntas]
R10 = [metricas[p]["R@10"] for p in preguntas]
nDCG10 = [metricas[p]["nDCG@10"] for p in preguntas]
AP10 = [metricas[p]["AP@10"] for p in preguntas]

# --------------------------
# Función para graficar
# --------------------------
def graficar_metrica(valores, titulo, etiqueta_x, archivo):
    plt.figure(figsize=(10, 6))
    plt.barh(preguntas, valores)
    plt.xlim(0, 1)
    plt.xlabel(etiqueta_x)
    plt.title(titulo)
    plt.grid(axis="x", linestyle="--", alpha=0.6)

    # Mostrar valores
    for i, v in enumerate(valores):
        plt.text(v + 0.01, i, f"{v:.2f}", va="center")

    plt.tight_layout()
    plt.savefig(archivo)
    plt.close()

# --------------------------
# Generar gráficas
# --------------------------
graficar_metrica(
    P10,
    "Precisión en el Top 10 (P@10)",
    "Proporción de documentos relevantes en el Top 10",
    "grafica_P10.png"
)

graficar_metrica(
    R10,
    "Recall en el Top 10 (R@10)",
    "Proporción de documentos relevantes recuperados",
    "grafica_R10.png"
)

graficar_metrica(
    nDCG10,
    "nDCG@10 por pregunta",
    "Calidad del ranking (relevancia y posición)",
    "grafica_nDCG10.png"
)

graficar_metrica(
    AP10,
    "Average Precision en el Top 10 (AP@10)",
    "Precisión promedio considerando el orden",
    "grafica_AP10.png"
)

print("Gráficas generadas correctamente.")
