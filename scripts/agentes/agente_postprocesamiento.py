"""
Agente de postprocesamiento para mejorar respuestas generadas por el sistema RAG.
Usa OpenAI Agents SDK.
"""
#-->Importar librerias
import os
from dotenv import load_dotenv
from agents import Agent, Runner

#-->Cargar variables de entorno
load_dotenv()

#-->Configurar el agente de postprocesamiento
MODEL_NAME = os.getenv("LLM_MODEL", "gpt-5-mini")

#-->Definir el agente de postprocesamiento
agente_postprocesador = Agent( #Aqui Agent es la clase que define el agente de postprocesamiento
    name="AgentePostprocesadorRAG",
    model=MODEL_NAME,
    instructions=(
        "Eres un agente encargado de mejorar respuestas generadas por un sistema RAG. "
        "Tu tarea es mejorar la claridad, coherencia y redacción de la respuesta, "
        "sin agregar información nueva ni inventar datos. "
        "Debes basarte únicamente en el contexto proporcionado."
    ),
)

#-->Función para ejecutar el agente de postprocesamiento
async def ejecutar_agente_postprocesamiento( #Aqui se define la funcion principal que sera llamada desde el sistema RAG
    pregunta: str,
    contexto: str,
    respuesta_base: str
) -> str:
    """
    Ejecuta el agente de postprocesamiento y devuelve la respuesta mejorada.
    """

    prompt = ( #Aqui se construye el prompt para el agente
        f"PREGUNTA:\n{pregunta}\n\n"
        f"CONTEXTO:\n{contexto}\n\n"
        f"RESPUESTA BASE:\n{respuesta_base}\n\n"
        "INSTRUCCIONES: Mejora la respuesta sin inventar información."
    )

    resultado = await Runner.run( #Aqui se ejecuta el agente de postprocesamiento
        agente_postprocesador,
        prompt
    )

    texto_final = resultado.final_output #Aqui se obtiene la respuesta mejorada para devolverla a la funcion principal

    if not texto_final or not isinstance(texto_final, str): #Aqui se maneja el caso de error
        return respuesta_base 

    return f"Respuesta_Mejorada:\n{texto_final.strip()}" #Aqui se devuelve la respuesta mejorada despues de tomar en cuenta los posibles errores de la parte de retrieval
