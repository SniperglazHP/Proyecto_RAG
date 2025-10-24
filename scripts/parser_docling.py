"""
Este modulo usa Docling para convertir cualquier documento (PDF, DOCX, TXT, CSV, XLS, imágenes)
a texto estructurado y lo guarda como archivo Markdown (.md).
"""
#-->Importa librerías
import os #Maneja operaciones del sistema como rutas de archivos y variables de entorno
from pathlib import Path #Maneja rutas de archivos de forma segura y multiplataforma
from docling.document_converter import DocumentConverter #Clase principal de Docling para convertir documentos

#-->Define la carpeta donde se guardarán los archivos Markdown convertidos
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" #Aqui se guardan los archivos .md generados, OUTPUT_DIR es la ruta completa de la carpeta outputs y __file__ es el archivo actual
OUTPUT_DIR.mkdir(exist_ok=True) #Crea la carpeta si no existe

def parse_with_docling(file_path: str): #Función principal para convertir documentos a Markdown usando Docling
    try:
        converter = DocumentConverter() #Crea una instancia del convertidor de documentos de Docling
        result = converter.convert(file_path) #Convierte el archivo proporcionado
        md_text = result.document.export_to_markdown() #Exporta el contenido convertido a formato Markdown

        md_filename = Path(file_path).stem + ".md" #Genera el nombre del archivo Markdown basado en el nombre original
        md_path = OUTPUT_DIR / md_filename #Define la ruta completa del archivo Markdown de salida

        with open(md_path, "w", encoding="utf-8") as f: #Abre el archivo en modo escritura con codificación UTF-8
            f.write(md_text if md_text.strip() else "No se detectó texto en el documento.") #Escribe el contenido Markdown en el archivo, o un mensaje si está vacío

        print(f"-->Archivo procesado y guardado como: {md_path}") #Muestra en consola la ruta del archivo guardado
        return md_path #Retorna la ruta del archivo Markdown generado

    except Exception as e: #Captura errores durante el proceso de conversión
        raise RuntimeError(f"Error procesando archivo con Docling: {str(e)}") #Lanza un error con el mensaje correspondiente
