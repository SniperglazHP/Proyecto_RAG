"""
Cálculo de las métricas
"""
#Importar librerías
import json
from pathlib import Path
import ir_measures
from ir_measures import Qrel, ScoredDoc
from ir_measures import AP, P, R, nDCG

#Rutas de archivos para entrada y salida
BASE = Path(__file__).resolve().parent
RESULTADOS_PATH = BASE / "resultados_respuestas.json"
RELEVANTES_PATH = BASE / "relevant_docs.json"
OUTPUT_PATH = BASE / "metricas_finales.json"


def main():

    print("\n---GENERANDO MÉTRICAS IR (AP@10, P@10, R@10, nDCG@10)---\n")

    with open(RESULTADOS_PATH, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    with open(RELEVANTES_PATH, "r", encoding="utf-8") as f:
        relevantes = json.load(f)

    qrels = []
    run = []

    for entry in resultados:

        qid = f"{entry['seccion']} - {entry['tema']}"

        # --- Qrels: documentos relevantes verdaderos ---
        if qid in relevantes:
            for docid in relevantes[qid]["relevant_docs"]:
                qrels.append(Qrel(qid, docid, 1))

        # --- Run: documentos recuperados por Pinecone ---
        for rr in entry.get("results", []):
            run.append(
                ScoredDoc(
                    query_id=qid,
                    doc_id=rr["doc_id"],
                    score=float(rr["score"])
                )
            )

    medidas = [AP@10, P@10, R@10, nDCG@10]

    # ----------------------------
    #   CALCULAR POR QUERY
    # ----------------------------
    metricas_finales = {}

    for m in ir_measures.iter_calc(medidas, qrels, run):

        qid = m.query_id
        nombre = str(m.measure)   # ejemplo: "AP@10", "nDCG@10"
        valor = m.value

        if qid not in metricas_finales:
            metricas_finales[qid] = {}

        metricas_finales[qid][nombre] = valor

    # ----------------------------
    # Guardar resultado final
    # ----------------------------
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metricas_finales, f, indent=4, ensure_ascii=False)

    print("\n=== MÉTRICAS GENERADAS ===")
    print(f"Archivo creado: {OUTPUT_PATH}\n")


if __name__ == "__main__":
    main()
