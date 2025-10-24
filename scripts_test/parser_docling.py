"""
Se utilizara Docling para:
- Leer PDF, DOCX, CSV, XLSX, TXT e imágenes.
- Extraer el contenido estructurado.
- Exportarlo a Markdown (.md) en la carpeta /outputs.
"""
#-->Importa librerías
import os #Maneja operaciones del sistema como rutas de archivos
from pathlib import Path #Maneja rutas de archivos de forma segura y de manera multiplataforma
from docling.document_converter import DocumentConverter #Clase principal de Docling para conversión de documentos

#-->Carpeta donde se guardarán los archivos Markdown generados
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" #Aqui se guardan los archivos md generados, OUTPUT_DIR es la ruta completa de la carpeta outputs y __file__ es el archivo actual
OUTPUT_DIR.mkdir(exist_ok=True) #Crea la carpeta si no existe

#-->Función principal para parsear archivos con Docling y guardarlos como Markdown
def parse_with_docling(file_path: str) -> str: #Recibe la ruta de un archivo
    try:
        converter = DocumentConverter() #Crea una instancia del convertidor de documentos
        result = converter.convert(file_path) #Convierte el archivo al formato interno de Docling
        markdown_text = result.document.export_to_markdown() #Exporta el contenido a formato Markdown

        md_filename = Path(file_path).stem + ".md" #Nombre del archivo Markdown basado en el nombre original
        md_path = OUTPUT_DIR / md_filename #Ruta completa del archivo Markdown de salida

        with open(md_path, "w", encoding="utf-8") as f: #Abre el archivo en modo escritura con codificación UTF-8
            f.write(markdown_text) #Escribe el contenido Markdown en el archivo

        return str(md_path) #Devuelve la ruta del archivo Markdown generado

    except Exception as e: #Captura errores durante el proceso
        raise RuntimeError(f"Error procesando archivo con Docling: {str(e)}") #Lanza un error con el mensaje correspondiente
