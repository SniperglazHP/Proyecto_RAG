"""
Este modulo se encarga de:
-->Leer y parsear documentos usando LlamaIndex.
-->Guardar el texto procesado en formato Markdown (.md).
-->Devuelve los documentos procesados para chunking posterior.
"""
#-->Importar librerías
import os #Controla operaciones del sistema, esto nos permite manejar rutas de archivos y variables de entorno
from pathlib import Path #Maneja rutas de archivos de forma segura y multiplataforma, crea objetos que representan rutas de archivos
from llama_index.readers.file import PDFReader, DocxReader, FlatReader #Importa lectores de archivos de LlamaIndex (para PDF, DOCX y texto plano)
from llama_index.core import Document #Document es una clase de LlamaIndex usada para representar texto en su estructura interna
from PIL import Image #PIL (Python Imaging Library) se usa para abrir imágenes
import pytesseract #pytesseract permite realizar OCR reconocimiento óptico de caracteres en imágenes

#-->Define la carpeta donde se guardarán los archivos Markdown generados
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" #OUTPUT_DIR es la ruta completa de la carpeta outputs
OUTPUT_DIR.mkdir(exist_ok=True) #mkdir crea la carpeta si no existe

#-->Es la ruta del ejecutable Tesseract OCR para su uso con pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#-->Función principal para parsear documentos, procesa diferentes tipos de archivos para extraer texto y guardarlo en Markdown
def parse_document(file_path: str): #file_path es la ruta del archivo a procesar y str indica que es una cadena de texto
    ext = os.path.splitext(file_path)[1].lower() #Obtiene la extensión del archivo (.pdf, .docx, .jpg, etc.)

    if ext == ".pdf": #Si el archivo es PDF, usa el lector PDFReader de LlamaIndex
        reader = PDFReader()
        docs = reader.load_data(file_path)

    elif ext == ".docx": #Si el archivo es Word (.docx), usa DocxReader de LlamaIndex
        reader = DocxReader()
        docs = reader.load_data(file_path)

    elif ext in [".jpg", ".jpeg", ".png"]: #Si el archivo es imagen (jpg, jpeg, png), aplica OCR manual
        try:
            image = Image.open(file_path) #Abre la imagen con PIL
            ocr_text = pytesseract.image_to_string(image, lang="spa+eng") #El pytesseract extrae el texto en español e inglés de la imagen
            docs = [Document(text=ocr_text)] #Crea un documento LlamaIndex con el texto OCR
        except Exception as e:
            docs = [Document(text=f"Error procesando imagen: {str(e)}")] #Crea un documento con el mensaje de error

    else: #Si no es ninguno de los tipos anteriores, se asume texto plano
        reader = FlatReader()
        docs = reader.load_data(file_path)

    md_text = "\n\n".join([doc.text for doc in docs if hasattr(doc, "text") and doc.text.strip()]) #md_text usa "\n\n".join para concatenar el texto de todos los documentos y separarlos con dos saltos de línea, hasattr verifica que el documento tenga el atributo text y strip elimina espacios en blanco

    md_filename = Path(file_path).stem + ".md" #Define el nombre y la ruta del archivo Markdown (.md)
    md_path = OUTPUT_DIR / md_filename #md_path es la ruta completa del archivo Markdown, OUTPUT_DIR es la carpeta de salida y md_filename es el nombre del archivo

    with open(md_path, "w", encoding="utf-8") as f: #Guarda el texto extraído en un archivo Markdown, w indica que se abre para escritura y encoding="utf-8" asegura que se guarden caracteres especiales correctamente
        f.write(md_text if md_text else "No se detectó texto en el documento.") #Si no se extrajo texto, guarda un mensaje indicando que no se detectó texto

    return docs #Retorna la lista de documentos procesados (para el siguiente paso: chunking)
