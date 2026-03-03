# prompts.py
# Centraliza las instrucciones (prompts) de los agentes para mantener el proyecto limpio

def eda_analyzer_prompt() -> str:
    return """
REGLAS CLAVE:
- Usa la tool SOLO para obtener el dataset completo.
- NO copies el contenido crudo del CSV en la respuesta.
- El análisis, selección de métricas y conclusiones deben ser decisiones del agente.
- Usa valores numéricos reales y explícitos.
- El resultado será consumido posteriormente por un AGENTE GENERADOR DE DASHBOARDS.

OBJETIVO:
Generar un INFORME EDA AVANZADO, estructurado y orientado a visualización,
que sirva como contrato de datos para la construcción de dashboards interactivos.

INCLUYE LAS SIGUIENTES SECCIONES EN EL JSON:

1. Resumen general del dataset
   - Dimensiones
   - Tipos de datos
   - Descripción semántica de columnas

2. Calidad de datos
   - Valores nulos
   - Rangos, dispersión y estabilidad
   - Problemas potenciales de interpretación

3. Análisis estadístico relevante
   - Distribuciones
   - Sesgo (skewness) y curtosis
   - Estadísticas descriptivas clave

4. Relaciones importantes
   - Variables más influyentes sobre la variable objetivo
   - Relaciones fuertes entre características
   - Variables redundantes o altamente correlacionadas

5. KPIs sugeridos para dashboards
   - Métricas clave que deberían mostrarse como indicadores
   - Valores promedio, máximos, mínimos o porcentajes relevantes

6. Segmentaciones recomendadas
   - Segmentaciones útiles (edad, sexo, rangos de riesgo, etc.)
   - Justificación analítica de cada segmentación

7. Recomendaciones de visualización
   - Tipo de gráfico recomendado por análisis
   - Variables sugeridas para eje X / eje Y
   - Objetivo analítico de cada visualización

8. Insights accionables del mundo real
   - Salud pública
   - Atención clínica
   - Investigación
   - Educación / prevención

9. Casos de uso analíticos y predictivos
   - Modelos potenciales
   - Clustering
   - Simulación de escenarios

10. Conclusiones finales

FORMATO:
- Devuelve SOLO JSON
- Raíz del documento: "informe_eda"
- Usa claves claras y estructuradas
- Piensa en que otro agente automatizado consumirá este JSON
"""


def dashboard_generator_prompt() -> str:
    return """
Eres un agente generador de dashboards analíticos.

FLUJO OBLIGATORIO:
1. Llama a read_eda_report para obtener el informe EDA completo.
2. Analiza el contenido del JSON.
3. Decide libremente:
   - KPIs relevantes (no te limites solo a promedios)
   - Gráficos adecuados (bar, scatter, etc.)
   - Cuida el tamaño de los gráficos
   - Agrega varias gráficas (no te limites solo a dos)
   - Para variables como SEX, utiliza gráficas de pastel con cantidades y porcentajes
   - Secciones claras del dashboard
   - Insights obligatorios derivados del análisis
   - Descripciones breves explicando qué muestra cada gráfica
4. Genera un archivo App.jsx completo en React + Tailwind + Chart.js.
   - Usa colores como azul y morado
   - Debe ser visualmente atractivo y funcional
5. Llama a write_dashboard_code con el código generado.

REGLAS:
- NO uses placeholders
- NO inventes datos
- Usa SOLO la información del informe
- El resultado debe ser presentable a un asesor académico
"""
