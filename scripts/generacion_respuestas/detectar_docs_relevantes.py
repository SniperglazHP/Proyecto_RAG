"""
Detecta documentos relevantes automáticamente usando:
- embedding del ground_truth
- score en Pinecone
- coincidencia de palabras clave
- coincidencia con el contexto generado

Genera: relevant_docs.json
"""

import json
import re
from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI
import pinecone

# ============================
# CARGA DE CONFIGURACIÓN
# ============================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = os.getenv("INDEX_NAME")
index = pc.Index(INDEX_NAME)

BASE = Path(__file__).resolve().parent
INPUT_PATH = BASE / "resultados_respuestas.json"
OUTPUT_PATH = BASE / "relevant_docs.json"


# ============================
# FUNCIONES DE UTILIDAD
# ============================

def clean_text(t):
    """Limpia texto para análisis."""
    return re.sub(r"[^a-zA-ZáéíóúñÁÉÍÓÚ0-9 ]", " ", t.lower())


def extract_keywords(text):
    """
    Extrae palabras clave simples del ground_truth.
    QUITA: artículos, preposiciones y palabras muy comunes.
    """
    stopwords = {
        "el", "la", "los", "las", "de", "del", "y", "en", "un",
        "una", "por", "con", "al", "lo", "que", "se", "fue",
        "es", "son", "más", "mas", "como", "total"
    }

    palabras = clean_text(text).split()
    return [p for p in palabras if len(p) > 3 and p not in stopwords]


def relevant_by_keywords(context, keywords):
    """Detecta si un chunk es relevante por palabras clave."""
    ctx_clean = clean_text(context)
    return sum(1 for kw in keywords if kw in ctx_clean)


# ============================
# PROCESO PRINCIPAL
# ============================

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados_finales = {}

    print("\n=== DETECTANDO DOCUMENTOS RELEVANTES ===\n")

    for entry in data:

        pregunta = entry["pregunta_variante"]
        ground = entry["ground_truth"]
        context = entry["contexto_usado"]
        retrieval = entry.get("results", [])

        qid = f"{entry['seccion']} - {entry['tema']}"

        # 1) Extraer palabras clave del ground truth
        keywords = extract_keywords(ground)

        # 2) Extraer también del contexto usado por el modelo
        ctx_keywords = extract_keywords(context)
        keywords_total = list(set(keywords + ctx_keywords))

        # 3) Consultar Pinecone con embedding del ground truth
        emb = client.embeddings.create(
            model="text-embedding-3-large",
            input=ground
        )
        qvec = emb.data[0].embedding

        pine_result = index.query(
            vector=qvec,
            top_k=20,
            include_metadata=True
        )

        relevantes = set()

        # =============================
        # A) Filtrado por score ≥ 0.70
        # =============================
        for match in pine_result["matches"]:
            if match["score"] >= 0.70:
                relevantes.add(match["id"])

        # =============================
        # B) Filtrado por palabras clave
        # =============================
        for match in pine_result["matches"]:
            texto = match["metadata"].get("text", "")
            if relevant_by_keywords(texto, keywords_total) >= 2:
                relevantes.add(match["id"])

        # =============================
        # C) Filtrado por estar en el contexto usado por el LLM
        # =============================
        for r in retrieval:
            relevantes.add(r["doc_id"])

        # Convertir a lista ordenada
        relevantes = list(relevantes)

        resultados_finales[qid] = {
            "pregunta": pregunta,
            "ground_truth": ground,
            "keywords_detectados": keywords_total,
            "relevant_docs": relevantes
        }

        print(f"[OK] {qid}: {len(relevantes)} relevantes detectados")

    # Guardar salida
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados_finales, f, indent=4, ensure_ascii=False)

    print("\n=== PROCESO COMPLETADO ===")
    print(f"Archivo generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
