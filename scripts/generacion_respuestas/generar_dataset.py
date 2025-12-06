"""
Genera 4 preguntas y respuestas por cada documento
"""
#-->Importar librerías
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader #Para contar las páginas

#-->Cargar .env
load_dotenv()

#-->Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#-->Rutas de carpetas de uploads y outputs
UPLOADS_PATH = Path(__file__).resolve().parent.parent.parent / "scripts" / "uploads"
OUTPUTS_PATH = Path(__file__).resolve().parent.parent.parent / "scripts" / "outputs"
SAVE_PATH = Path(__file__).resolve().parent / "dataset_preguntas_respuestas.json"

#-->Funcion que cuenta páginas reales del documento PDF
def contar_paginas_pdf(pdf_path):
    """Devuelve la cantidad REAL de páginas del PDF"""
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except:
        print(f"-->Error leyendo PDF: {pdf_path}")
        return 1

#-->Función para dividir el texto en N partes iguales
def dividir_texto_en_paginas_por_proporcion(texto, n_paginas):
    """
    Divide el contenido del .md en N partes iguales,
    usando la cantidad de páginas del PDF original.
    """
    lineas = texto.split("\n")
    total_lineas = len(lineas)
    tamaño_pagina = total_lineas // n_paginas
    paginas = []

    for i in range(n_paginas):
        inicio = i * tamaño_pagina
        fin = (i + 1) * tamaño_pagina if i < n_paginas - 1 else total_lineas
        paginas.append("\n".join(lineas[inicio:fin]).strip())
    return paginas

#-->Función para generar preguntas y respuestas usando GPT-5-mini
def generar_preguntas_respuestas(texto, n=4):
    """Usa GPT-5-mini para generar preguntas/respuestas."""
    prompt = f"""
Genera EXACTAMENTE {n} pares de preguntas y respuestas basadas SOLO en el texto dado.

Formato obligatorio JSON:
[
  {{
    "pregunta": "...",
    "respuesta": "..."
  }}
]

TEXTO:
\"\"\"
{texto}
\"\"\"
"""
    resp = client.responses.create(model="gpt-5-mini", input=prompt)
    try:
        return json.loads(resp.output_text)
    except:
        print("-->El modelo no devolvió JSON válido.")
        return []

#-->Función principal para generar el dataset
def main():
    dataset = []
    print("\n-->Generando dataset<--\n")
    for pdf in UPLOADS_PATH.glob("*.pdf"):

        nombre_pdf = pdf.name
        nombre_md = nombre_pdf.replace(".pdf", ".md")
        md_path = OUTPUTS_PATH / nombre_md

        if not md_path.exists():
            print(f"-->No existe el MD para {nombre_pdf}. Saltando.")
            continue
        print(f"\n-->Procesando documento: {nombre_pdf}")

        #1.Contar páginas reales del PDF
        paginas_pdf = contar_paginas_pdf(pdf)
        print(f"-->Páginas reales: {paginas_pdf}")

        #2.Cargar contenido del .md
        with open(md_path, "r", encoding="utf-8") as f:
            texto = f.read()

        #3.Dividir el texto en páginas proporcionales
        paginas_texto = dividir_texto_en_paginas_por_proporcion(texto, paginas_pdf)

        #4.Generar preguntas por página
        for num, pagina in enumerate(paginas_texto, start=1):
            print(f"-->Generando 4 preguntas para página {num}...")

            pares = generar_preguntas_respuestas(pagina, n=4)

            for par in pares:
                dataset.append({
                    "documento": nombre_pdf,
                    "pagina": num,
                    "pregunta": par["pregunta"],
                    "respuesta": par["respuesta"]
                })

    #5.Guardar dataset
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    print("\n-->Dataset generado con éxito.")
    print(f"-->Guardado en: {SAVE_PATH}")

#-->Ejecutar main
if __name__ == "__main__":
    main()
