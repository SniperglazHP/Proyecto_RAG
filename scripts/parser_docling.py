"""
Este módulo usa Docling para convertir cualquier documento (PDF, DOCX, TXT, CSV, XLS, imágenes)
a texto estructurado y lo guarda como archivo Markdown (.md).
"""
#-->Importa librerías
import os  #Maneja operaciones del sistema como rutas de archivos y variables de entorno
from pathlib import Path  #Maneja rutas de archivos de forma segura y multiplataforma
from docling.document_converter import DocumentConverter  #Clase principal de Docling para convertir documentos

#-->Define la carpeta donde se guardarán los archivos Markdown convertidos
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"  #Aquí se guardan los archivos .md generados
OUTPUT_DIR.mkdir(exist_ok=True)  #Crea la carpeta si no existe

#-->Función principal para convertir documentos a Markdown usando Docling
def parse_with_docling(file_path: str): #Función principal para convertir documentos a Markdown usando Docling
    try:
        #-->Crea una instancia del convertidor de documentos
        converter = DocumentConverter() #Instancia del convertidor de Docling

        #-->Convierte el documento
        result = converter.convert(file_path) #Convierte el archivo al formato interno de Docling

        #-->Exporta el contenido convertido a formato Markdown
        md_text = result.document.export_to_markdown() #Obtiene el texto en formato Markdown

        #-->Genera el nombre del archivo Markdown basado en el nombre original
        md_filename = Path(file_path).stem + ".md" #Nombre del archivo con extensión .md
        md_path = OUTPUT_DIR / md_filename #Ruta completa del archivo de salida

        #-->Guarda el archivo .md
        with open(md_path, "w", encoding="utf-8") as f: #Abre el archivo en modo escritura con codificación UTF-8
            f.write(md_text if md_text.strip() else "No se detectó texto en el documento.") #Escribe el contenido Markdown o un mensaje si está vacío
        print(f"-->Archivo procesado y guardado como: {md_path}") #Confirma la creación del archivo
        return md_path #Devuelve la ruta del archivo Markdown generado

    #-->Manejo de errores en la conversión
    except Exception as e:
        raise RuntimeError(f"Error procesando archivo con Docling: {str(e)}")
