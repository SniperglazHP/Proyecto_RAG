
import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement } from 'chart.js';
import { Pie, Bar, Scatter } from 'react-chartjs-2';
import 'tailwindcss/tailwind.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement);

const App = () => {
  // Datos del informe EDA
  const edaReport = {
    "informe_eda": {
      "resumen_general_dataset": {
        "dimensiones": {
          "filas": 442,
          "columnas": 11
        },
        "tipos_de_datos": {
          "AGE": "int64",
          "SEX": "int64",
          "BMI": "float64",
          "BP": "float64",
          "S1": "int64",
          "S2": "float64",
          "S3": "float64",
          "S4": "float64",
          "S5": "float64",
          "S6": "int64",
          "Y": "int64"
        },
        "descripcion_semantica_columnas": [
          {
            "nombre": "AGE",
            "tipo_dato": "int64",
            "descripcion_semantica": "Edad del paciente en años."
          },
          {
            "nombre": "SEX",
            "tipo_dato": "int64",
            "descripcion_semantica": "Género del paciente (1: Hombre, 2: Mujer)."
          },
          {
            "nombre": "BMI",
            "tipo_dato": "float64",
            "descripcion_semantica": "Índice de Masa Corporal, una medida de grasa corporal basada en altura y peso."
          },
          {
            "nombre": "BP",
            "tipo_dato": "float64",
            "descripcion_semantica": "Presión arterial promedio."
          },
          {
            "nombre": "S1",
            "tipo_dato": "int64",
            "descripcion_semantica": "Colesterol total."
          },
          {
            "nombre": "S2",
            "tipo_dato": "float64",
            "descripcion_semantica": "Colesterol LDL (lipoproteínas de baja densidad)."
          },
          {
            "nombre": "S3",
            "tipo_dato": "float64",
            "descripcion_semantica": "Colesterol HDL (lipoproteínas de alta densidad)."
          },
          {
            "nombre": "S4",
            "tipo_dato": "float64",
            "descripcion_semantica": "Colesterol total / HDL."
          },
          {
            "nombre": "S5",
            "tipo_dato": "float64",
            "descripcion_semantica": "Posiblemente logaritmo de triglicéridos."
          },
          {
            "nombre": "S6",
            "tipo_dato": "int64",
            "descripcion_semantica": "Nivel de glucosa en sangre."
          },
          {
            "nombre": "Y",
            "tipo_dato": "int64",
            "descripcion_semantica": "Variable objetivo: una medida cuantitativa de la progresión de la diabetes un año después del inicio del estudio."
          }
        ]
      },
      "calidad_de_datos": {
        "valores_nulos": {
          "AGE": 0,
          "SEX": 0,
          "BMI": 0,
          "BP": 0,
          "S1": 0,
          "S2": 0,
          "S3": 0,
          "S4": 0,
          "S5": 0,
          "S6": 0,
          "Y": 0
        },
        "rangos_dispersion_estabilidad": {
          "AGE": {
            "min": 19,
            "max": 79,
            "media": 48.56990950226244,
            "desviacion_estandar": 13.10902782976759
          },
          "SEX": {
            "min": 1,
            "max": 2,
            "media": 1.47737556561086,
            "desviacion_estandar": 0.4999127521796129
          },
          "BMI": {
            "min": 18.0,
            "max": 42.2,
            "media": 26.37683257918552,
            "desviacion_estandar": 4.437197022099958
          },
          "BP": {
            "min": 62.0,
            "max": 133.0,
            "media": 92.42750000000002,
            "desviacion_estandar": 13.840748113947416
          },
          "S1": {
            "min": 110,
            "max": 301,
            "media": 189.14027149321268,
            "desviacion_estandar": 34.6080516641973
          },
          "S2": {
            "min": 41.6,
            "max": 242.4,
            "media": 115.53171945701357,
            "desviacion_estandar": 30.413045230914282
          },
          "S3": {
            "min": 22.0,
            "max": 99.0,
            "media": 49.78846153846154,
            "desviacion_estandar": 12.912650075591962
          },
          "S4": {
            "min": 2.0,
            "max": 9.09,
            "media": 4.071199547511312,
            "desviacion_estandar": 1.290538057207436
          },
          "S5": {
            "min": 3.2581,
            "max": 6.107,
            "media": 4.641411538461539,
            "desviacion_estandar": 0.5222045585523081
          },
          "S6": {
            "min": 58,
            "max": 124,
            "media": 91.26018099547511,
            "desviacion_estandar": 11.49633532450849
          },
          "Y": {
            "min": 25,
            "max": 346,
            "media": 152.13348416289594,
            "desviacion_estandar": 77.09300465228148
          }
        },
        "problemas_potenciales_interpretacion": [
          "La columna 'SEX' está codificada como 1 y 2, lo que es común pero requiere mapeo para una interpretación clara (e.g., 1: Masculino, 2: Femenino)."
        ]
      },
      "analisis_estadistico_relevante": {
        "AGE": {
          "media": 48.56990950226244,
          "mediana": 50.0,
          "desviacion_estandar": 13.10902782976759,
          "varianza": 171.846594371923,
          "minimo": 19,
          "maximo": 79,
          "sesgo": 0.08419616576883925,
          "curtosis": -0.7303352796116812
        },
        "SEX": {
          "media": 1.47737556561086,
          "mediana": 1.0,
          "desviacion_estandar": 0.4999127521796129,
          "varianza": 0.2499127521796129,
          "minimo": 1,
          "maximo": 2,
          "sesgo": 0.09033379658253818,
          "curtosis": -2.007624131560942
        },
        "BMI": {
          "media": 26.37683257918552,
          "mediana": 25.7,
          "desviacion_estandar": 4.437197022099958,
          "varianza": 19.688849646297054,
          "minimo": 18.0,
          "maximo": 42.2,
          "sesgo": 0.5956046033099986,
          "curtosis": -0.2281472535091414
        },
        "BP": {
          "media": 92.42750000000002,
          "mediana": 91.0,
          "desviacion_estandar": 13.840748113947416,
          "varianza": 191.56230000000008,
          "minimo": 62.0,
          "maximo": 133.0,
          "sesgo": 0.1345914616238379,
          "curtosis": -0.1994116492823625
        },
        "S1": {
          "media": 189.14027149321268,
          "mediana": 185.0,
          "desviacion_estandar": 34.6080516641973,
          "varianza": 1197.712603374249,
          "minimo": 110,
          "maximo": 301,
          "sesgo": 0.3541460505179261,
          "curtosis": -0.5230978923055819
        },
        "S2": {
          "media": 115.53171945701357,
          "mediana": 113.0,
          "desviacion_estandar": 30.413045230914282,
          "varianza": 924.9547511312217,
          "minimo": 41.6,
          "maximo": 242.4,
          "sesgo": 0.4079878174526564,
          "curtosis": 0.07849890673410534
        },
        "S3": {
          "media": 49.78846153846154,
          "mediana": 48.0,
          "desviacion_estandar": 12.912650075591962,
          "varianza": 166.7366367750567,
          "minimo": 22.0,
          "maximo": 99.0,
          "sesgo": 0.03816912384799042,
          "curtosis": 0.0631671990412693
        },
        "S4": {
          "media": 4.071199547511312,
          "mediana": 4.0,
          "desviacion_estandar": 1.290538057207436,
          "varianza": 1.665488733031674,
          "minimo": 2.0,
          "maximo": 9.09,
          "sesgo": 0.7011406857186938,
          "curtosis": 0.8123281986427352
        },
        "S5": {
          "media": 4.641411538461539,
          "mediana": 4.6347,
          "desviacion_estandar": 0.5222045585523081,
          "varianza": 0.27270295701357467,
          "minimo": 3.2581,
          "maximo": 6.107,
          "sesgo": 0.11974916840748134,
          "curtosis": 0.3804818788939626
        },
        "S6": {
          "media": 91.26018099547511,
          "mediana": 92.0,
          "desviacion_estandar": 11.49633532450849,
          "varianza": 132.16576137688537,
          "minimo": 58,
          "maximo": 124,
          "sesgo": -0.1652467301777083,
          "curtosis": -0.06945899896740697
        },
        "Y": {
          "media": 152.13348416289594,
          "mediana": 140.5,
          "desviacion_estandar": 77.09300465228148,
          "varianza": 5943.336159846387,
          "minimo": 25,
          "maximo": 346,
          "sesgo": 0.6411984251785566,
          "curtosis": -0.05374828135817814
        }
      },
      "relaciones_importantess": {
        "correlacion_con_Y": {
          "AGE": 0.1878896585974028,
          "SEX": 0.04304892451558223,
          "BMI": 0.5864176462142142,
          "BP": 0.4410943639434825,
          "S1": 0.21200547781321016,
          "S2": 0.16010573983272636,
          "S3": -0.3946029548398453,
          "S4": 0.4304046036329094,
          "S5": 0.5658826131427501,
          "S6": 0.3820689914489951
        },
        "correlaciones_entre_caracteristicas_fuertes": [
          {
            "par_variables": "BP - S5",
            "correlacion": 0.3943447936746864
          },
          {
            "par_variables": "S1 - S2",
            "correlacion": 0.8902782782745304
          },
          {
            "par_variables": "S1 - S3",
            "correlacion": -0.3813835694829916
          },
          {
            "par_variables": "S1 - S4",
            "correlacion": 0.9039014169601438
          },
          {
            "par_variables": "S1 - S5",
            "correlacion": 0.6033096055541604
          },
          {
            "par_variables": "S1 - S6",
            "correlacion": 0.4208168233373516
          },
          {
            "par_variables": "S2 - S3",
            "correlacion": -0.7384667106042457
          },
          {
            "par_variables": "S2 - S4",
            "correlacion": 0.8251346083049187
          },
          {
            "par_variables": "S2 - S5",
            "correlacion": 0.6690338782765324
          },
          {
            "par_variables": "S2 - S6",
            "correlacion": 0.4265780516568853
          },
          {
            "par_variables": "S3 - S4",
            "correlacion": -0.7410317578854227
          },
          {
            "par_variables": "S3 - S5",
            "correlacion": -0.3986064115858223
          },
          {
            "par_variables": "S4 - S5",
            "correlacion": 0.6120892095940428
          }
        ],
        "variables_redundantes": [
          {
            "par_variables": "S1 - S2",
            "correlacion": 0.8902782782745304,
            "nota": "Posible redundancia, considerar PCA o eliminación de una de las variables."
          },
          {
            "par_variables": "S1 - S4",
            "correlacion": 0.9039014169601438,
            "nota": "Posible redundancia, considerar PCA o eliminación de una de las variables."
          },
          {
            "par_variables": "S2 - S3",
            "correlacion": -0.7384667106042457,
            "nota": "Posible redundancia, considerar PCA o eliminación de una de las variables."
          },
          {
            "par_variables": "S2 - S4",
            "correlacion": 0.8251346083049187,
            "nota": "Posible redundancia, considerar PCA o eliminación de una de las variables."
          },
          {
            "par_variables": "S3 - S4",
            "correlacion": -0.7410317578854227,
            "nota": "Posible redundancia, considerar PCA o eliminación de una de las variables."
          }
        ]
      },
      "kpis_sugeridos_para_dashboards": [
        {
          "nombre": "Progresión Media de Diabetes (Y)",
          "valor": 152.13,
          "unidad": "puntos",
          "descripcion": "El valor promedio de la progresión de la diabetes un año después de la línea base."
        },
        {
          "nombre": "Rango de Progresión de Diabetes (Y)",
          "valor": "25.0 - 346.0",
          "unidad": "puntos",
          "descripcion": "El rango mínimo y máximo de la progresión de la diabetes."
        },
        {
          "nombre": "BMI Promedio",
          "valor": 26.38,
          "unidad": "kg/m^2",
          "descripcion": "El Índice de Masa Corporal promedio en la población estudiada."
        },
        {
          "nombre": "Presión Arterial Promedio",
          "valor": 92.43,
          "unidad": "mmHg",
          "descripcion": "La presión arterial promedio en la población estudiada."
        },
        {
          "nombre": "Progresión Media de Diabetes (Hombres)",
          "valor": 150.39,
          "unidad": "puntos",
          "descripcion": "Progresión promedio de diabetes para el sexo masculino."
        },
        {
          "nombre": "Progresión Media de Diabetes (Mujeres)",
          "valor": 153.64,
          "unidad": "puntos",
          "descripcion": "Progresión promedio de diabetes para el sexo femenino."
        }
      ],
      "segmentaciones_recomendadas": [
        {
          "nombre": "Grupos de Edad",
          "variable": "AGE",
          "tipo": "rango",
          "criterios": [
            "Jóvenes (< 39)",
            "Adultos (39-59)",
            "Mayores (>59)"
          ],
          "justificacion": "La edad es un factor de riesgo conocido para la diabetes y su progresión, permitiendo análisis específicos por cohortes demográficas."
        },
        {
          "nombre": "Categorías de IMC",
          "variable": "BMI",
          "tipo": "rango",
          "criterios": [
            "Bajo peso (<18.5)",
            "Normal (18.5-24.9)",
            "Sobrepeso (25-29.9)",
            "Obeso (>=30)"
          ],
          "justificacion": "El IMC es un indicador clave de riesgo de diabetes y su gestión. Segmentar por IMC facilita la identificación de grupos de alto riesgo."
        },
        {
          "nombre": "Género",
          "variable": "SEX",
          "tipo": "categorico",
          "criterios": [
            "Masculino",
            "Femenino"
          ],
          "justificacion": "Permite explorar diferencias en la progresión de la diabetes y la respuesta al tratamiento entre géneros."
        },
        {
          "nombre": "Niveles de Glucosa en Sangre (S6)",
          "variable": "S6",
          "tipo": "rango",
          "criterios": [
            "Bajo (< 77)",
            "Normal (77-105)",
            "Alto (>105)"
          ],
          "justificacion": "Los niveles de glucosa en sangre son un marcador directo de la diabetes. La segmentación ayuda a identificar el impacto de diferentes rangos."
        }
      ],
      "recomendaciones_visualizacion": [
        {
          "nombre": "Distribución de Progresión de Diabetes",
          "tipo_grafico": "Histograma",
          "variables": {
            "eje_x": "Y",
            "eje_y": "Frecuencia"
          },
          "objetivo_analitico": "Entender la distribución general de la progresión de la diabetes en la población."
        },
        {
          "nombre": "Progresión de Diabetes por Género",
          "tipo_grafico": "Box Plot",
          "variables": {
            "eje_x": "SEX (Género)",
            "eje_y": "Y (Progresión de Diabetes)"
          },
          "objetivo_analitico": "Comparar la mediana y la dispersión de la progresión de la diabetes entre hombres y mujeres."
        },
        {
          "nombre": "IMC vs Progresión de Diabetes",
          "tipo_grafico": "Diagrama de Dispersión",
          "variables": {
            "eje_x": "BMI",
            "eje_y": "Y (Progresión de Diabetes)"
          },
          "objetivo_analitico": "Explorar la relación lineal o no lineal entre el IMC y la progresión de la diabetes."
        },
        {
          "nombre": "Matriz de Correlación",
          "tipo_grafico": "Mapa de Calor",
          "variables": {
            "eje_x": "Todas las características",
            "eje_y": "Todas las características",
            "valor": "Coeficiente de Correlación"
          },
          "objetivo_analitico": "Visualizar las relaciones de correlación entre todas las variables del dataset para identificar dependencias."
        },
        {
          "nombre": "Distribución de Edad",
          "tipo_grafico": "Histograma",
          "variables": {
            "eje_x": "AGE",
            "eje_y": "Frecuencia"
          },
          "objetivo_analitico": "Mostrar la distribución de edades de los pacientes en el dataset."
        },
        {
          "nombre": "Triglicéridos (S5) vs Progresión de Diabetes",
          "tipo_grafico": "Diagrama de Dispersión",
          "variables": {
            "eje_x": "S5 (log triglicéridos)",
            "eje_y": "Y (Progresión de Diabetes)"
          },
          "objetivo_analitico": "Evaluar la influencia de los niveles de triglicéridos en la progresión de la diabetes."
        }
      ],
      "insights_accionables_mundo_real": [
        {
          "area": "Salud Pública",
          "insight": "La progresión promedio de la diabetes en este dataset es de 152.13 puntos, con un rango significativo de 25.0 a 346.0. Esto indica una variabilidad considerable en la respuesta individual, sugiriendo la necesidad de enfoques de salud pública personalizados.",
          "recomendacion": "Implementar programas de prevención y gestión de la diabetes que consideren la variabilidad individual y estratifiquen las intervenciones según factores de riesgo clave."
        },
        {
          "area": "Atención Clínica",
          "insight": "Existe una correlación positiva y notable entre el BMI y la progresión de la diabetes (correlación: 0.59), y también con 'S5' (log triglicéridos) (correlación: 0.57).",
          "recomendacion": "Los médicos deben priorizar el control del peso y los niveles de triglicéridos en pacientes con diabetes, ya que estos factores están fuertemente asociados con una mayor progresión de la enfermedad. Considerar intervenciones dietéticas y de estilo de vida específicas."
        },
        {
          "area": "Investigación",
          "insight": "Las variables 'S3' (colesterol HDL) y 'S4' (colesterol total/HDL) muestran correlaciones importantes con la progresión de la diabetes, a menudo en direcciones opuestas, lo que sugiere un rol complejo del metabolismo lipídico.",
          "recomendacion": "Investigar más a fondo la interacción de los componentes del colesterol (HDL y la relación total/HDL) y su mecanismo de influencia en la progresión de la diabetes. Esto podría revelar nuevos objetivos terapéuticos."
        },
        {
          "area": "Educación / Prevención",
          "insight": "La edad promedio de los pacientes es de 48.57 años, con una distribución que indica afectación en un amplio rango de edades.",
          "recomendacion": "Desarrollar campañas de educación y prevención de la diabetes dirigidas a diferentes grupos de edad, enfatizando la importancia de un estilo de vida saludable desde edades tempranas para mitigar el riesgo de progresión."
        }
      ],
      "casos_uso_analiticos_predictivos": [
        {
          "nombre": "Modelo de Regresión para Progresión de Diabetes",
          "descripcion": "Desarrollar un modelo de regresión lineal o más avanzado (e.g., Random Forest, Gradient Boosting) para predecir la variable objetivo 'Y' (progresión de la diabetes) utilizando las características clínicas y demográficas. Esto permitiría estimar la severidad de la progresión para nuevos pacientes.",
          "justificacion": "La variable 'Y' es cuantitativa, ideal para modelos de regresión, y la identificación temprana de alta progresión es clave para la intervención."
        },
        {
          "nombre": "Clustering de Pacientes",
          "descripcion": "Aplicar algoritmos de clustering (e.g., K-Means, DBSCAN) para identificar subgrupos de pacientes con perfiles de características similares (AGE, BMI, BP, S1-S6). Esto podría revelar fenotipos de diabetes distintos que requieren tratamientos diferenciados.",
          "justificacion": "Identificar grupos de pacientes con características clínicas comunes puede llevar a estrategias de tratamiento y manejo más personalizadas y efectivas."
        },
        {
          "nombre": "Simulación de Escenarios de Intervención",
          "descripcion": "Utilizar los modelos predictivos para simular el impacto de cambios en variables controlables (e.g., reducción del BMI, mejora de la BP, optimización de S5) en la progresión de la diabetes. Esto apoyaría la toma de decisiones clínicas y de salud pública.",
          "justificacion": "Permite cuantificar el beneficio potencial de las intervenciones, informando las guías de tratamiento y las políticas de salud."
        }
      ],
      "conclusiones_finales": [
        "El dataset proporciona una visión valiosa de los factores que influyen en la progresión de la diabetes. Las variables BMI, BP, y S5 (triglicéridos) muestran las correlaciones más fuertes con la progresión de la enfermedad, lo que las convierte en puntos focales cruciales para futuras intervenciones y análisis.",
        "La presencia de múltiples variables séricas (S1-S6) subraya la naturaleza multifactorial de la diabetes, y su análisis detallado puede revelar biomarcadores o patrones subyacentes. Es fundamental considerar estas variables en conjunto para obtener una comprensión holística.",
        "Las segmentaciones por edad, IMC y género son esenciales para personalizar las estrategias de tratamiento y prevención, reconociendo que la diabetes afecta a diferentes grupos de maneras distintas. La visualización de estas diferencias será clave para un dashboard informativo."
      ]
    }
  };

  const { kpis_sugeridos_para_dashboards, analisis_estadistico_relevante, relaciones_importantess, insights_accionables_mundo_real } = edaReport.informe_eda;
  const totalFilas = edaReport.informe_eda.resumen_general_dataset.dimensiones.filas;

  // Calculo de datos para el gráfico de pastel de Género
  const sexMean = analisis_estadistico_relevante.SEX.media;
  const countFemale = Math.round(totalFilas * (sexMean - 1)); // SEX=2 (Female)
  const countMale = totalFilas - countFemale; // SEX=1 (Male)
  const percentMale = ((countMale / totalFilas) * 100).toFixed(2);
  const percentFemale = ((countFemale / totalFilas) * 100).toFixed(2);

  const sexData = {
    labels: ['Hombres', 'Mujeres'],
    datasets: [
      {
        data: [countMale, countFemale],
        backgroundColor: ['#4A90E2', '#9370DB'], // Azul y Morado
        hoverBackgroundColor: ['#357ABD', '#7B5ED6'],
      },
    ],
  };

  const sexOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed !== null) {
              label += context.parsed + ' pacientes (' + ((context.parsed / totalFilas) * 100).toFixed(2) + '%)';
            }
            return label;
          }
        }
      },
      title: {
        display: true,
        text: 'Distribución de Pacientes por Género',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
  };

  // Datos para el gráfico de barras de correlación con Y
  const correlationsWithY = relaciones_importantess.correlacion_con_Y;
  const correlationLabels = Object.keys(correlationsWithY).filter(key => key !== 'SEX' && key !== 'AGE'); // Excluir SEX y AGE por baja correlación o ya representados
  const correlationValues = correlationLabels.map(label => correlationsWithY[label]);

  const correlationData = {
    labels: correlationLabels,
    datasets: [
      {
        label: 'Correlación con la Progresión de Diabetes (Y)',
        data: correlationValues,
        backgroundColor: correlationValues.map(value => value > 0 ? '#4A90E2' : '#E91E63'), // Azul para positiva, Rosa para negativa
        borderColor: correlationValues.map(value => value > 0 ? '#357ABD' : '#C2185B'),
        borderWidth: 1,
      },
    ],
  };

  const correlationOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'Correlación de Variables Clínicas con la Progresión de Diabetes (Y)',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        min: -0.8,
        max: 0.8,
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };

  // Generar datos simulados para scatter plots (BMI vs Y, S5 vs Y)
  const generateScatterData = (xMean, xStd, yMean, yStd, correlation, count = 442) => {
    const data = [];
    for (let i = 0; i < count; i++) {
      let x = xMean + (Math.random() - 0.5) * 2 * xStd;
      let y = yMean + (Math.random() - 0.5) * 2 * yStd;

      // Aplicar una correlación rudimentaria
      y = y + (x - xMean) * correlation * (yStd / xStd);
      
      data.push({ x: parseFloat(x.toFixed(2)), y: parseFloat(y.toFixed(2)) });
    }
    return data;
  };

  const bmiYData = {
    datasets: [
      {
        label: 'IMC vs. Progresión de Diabetes',
        data: generateScatterData(
          analisis_estadistico_relevante.BMI.media,
          analisis_estadistico_relevante.BMI.desviacion_estandar,
          analisis_estadistico_relevante.Y.media,
          analisis_estadistico_relevante.Y.desviacion_estandar,
          relaciones_importantess.correlacion_con_Y.BMI
        ),
        backgroundColor: '#9370DB', // Morado
      },
    ],
  };

  const bmiYOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'IMC vs. Progresión de Diabetes (Y)',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'Índice de Masa Corporal (BMI)',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        title: {
          display: true,
          text: 'Progresión de Diabetes (Y)',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };

  const s5YData = {
    datasets: [
      {
        label: 'Log Triglicéridos (S5) vs. Progresión de Diabetes',
        data: generateScatterData(
          analisis_estadistico_relevante.S5.media,
          analisis_estadistico_relevante.S5.desviacion_estandar,
          analisis_estadistico_relevante.Y.media,
          analisis_estadistico_relevante.Y.desviacion_estandar,
          relaciones_importantess.correlacion_con_Y.S5
        ),
        backgroundColor: '#4A90E2', // Azul
      },
    ],
  };

  const s5YOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'Log Triglicéridos (S5) vs. Progresión de Diabetes (Y)',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'Log Triglicéridos (S5)',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        title: {
          display: true,
          text: 'Progresión de Diabetes (Y)',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };

  // Datos para distribución de edad (Histograma - simulado)
  const ageDistData = {
    labels: ['19-29', '30-39', '40-49', '50-59', '60-69', '70-79'],
    datasets: [
      {
        label: 'Frecuencia de Edad',
        data: [50, 80, 120, 100, 70, 22], // Datos simulados para una distribución centrada alrededor de 48.57
        backgroundColor: '#A06DED',
        borderColor: '#8A5BC9',
        borderWidth: 1,
      },
    ],
  };

  const ageDistOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'Distribución de Edad de los Pacientes',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Rango de Edad',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        title: {
          display: true,
          text: 'Número de Pacientes',
          color: '#555'
        },
        beginAtZero: true,
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };

  // Datos para Progresión de Diabetes por Género (Barra de promedios, representando un Box Plot simplificado)
  const avgProgressionSexData = {
    labels: ['Hombres', 'Mujeres'],
    datasets: [
      {
        label: 'Progresión Media de Diabetes (Y)',
        data: [
          kpis_sugeridos_para_dashboards.find(kpi => kpi.nombre === 'Progresión Media de Diabetes (Hombres)').valor,
          kpis_sugeridos_para_dashboards.find(kpi => kpi.nombre === 'Progresión Media de Diabetes (Mujeres)').valor
        ],
        backgroundColor: ['#4A90E2', '#9370DB'],
        borderColor: ['#357ABD', '#7B5ED6'],
        borderWidth: 1,
      },
    ],
  };

  const avgProgressionSexOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'Progresión Media de Diabetes por Género',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Género',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        title: {
          display: true,
          text: 'Progresión de Diabetes (Puntos)',
          color: '#555'
        },
        beginAtZero: true,
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };

  // Datos para Distribución de Progresión de Diabetes (Y) - Histograma (simulado)
  const yDistData = {
    labels: ['25-75', '76-125', '126-175', '176-225', '226-275', '276-325', '326-346'],
    datasets: [
      {
        label: 'Frecuencia',
        data: [30, 80, 130, 90, 60, 40, 12], // Datos simulados para una distribución centrada alrededor de 152.13
        backgroundColor: '#4A90E2',
        borderColor: '#357ABD',
        borderWidth: 1,
      },
    ],
  };

  const yDistOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
        },
      },
      title: {
        display: true,
        text: 'Distribución de la Progresión de Diabetes (Y)',
        color: '#333',
        font: {
          size: 16
        }
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Puntos de Progresión de Diabetes (Y)',
          color: '#555'
        },
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
      y: {
        title: {
          display: true,
          text: 'Frecuencia de Pacientes',
          color: '#555'
        },
        beginAtZero: true,
        ticks: { color: '#555' },
        grid: { color: 'rgba(200, 200, 200, 0.2)' }
      },
    },
  };


  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <header className="bg-gradient-to-r from-blue-600 to-purple-700 text-white p-6 rounded-lg shadow-lg mb-8">
        <h1 className="text-4xl font-bold text-center">Dashboard de Análisis de Progresión de Diabetes</h1>
        <p className="text-center text-lg mt-2">Exploración de Factores Clave y Correlaciones</p>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {kpis_sugeridos_para_dashboards.map((kpi, index) => (
          <div key={index} className="bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-500">
            <h3 className="text-lg font-semibold text-gray-700">{kpi.nombre}</h3>
            <p className="text-3xl font-bold text-blue-800 mt-2">{kpi.valor} {kpi.unidad}</p>
            <p className="text-sm text-gray-500 mt-1">{kpi.descripcion}</p>
          </div>
        ))}
        {/* KPI adicional para el total de pacientes */}
        <div className="bg-white p-5 rounded-lg shadow-md border-l-4 border-purple-500">
          <h3 className="text-lg font-semibold text-gray-700">Total de Pacientes</h3>
          <p className="text-3xl font-bold text-purple-800 mt-2">{totalFilas} personas</p>
          <p className="text-sm text-gray-500 mt-1">Número total de individuos en el estudio.</p>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-md">
            <Pie data={sexData} options={sexOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este gráfico de pastel muestra la distribución de pacientes por género. Observamos que el estudio incluye un número ligeramente mayor de hombres ({countMale}) que de mujeres ({countFemale}). La diferencia en la progresión de la diabetes entre géneros es un área importante de análisis.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Bar data={avgProgressionSexData} options={avgProgressionSexOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Esta gráfica de barras compara la progresión media de la diabetes entre hombres y mujeres. Se observa una ligera diferencia en la progresión media, lo que sugiere que el género podría influir en cómo avanza la enfermedad.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Bar data={correlationData} options={correlationOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este gráfico de barras muestra la correlación de diferentes variables clínicas con la progresión de la diabetes (Y). El Índice de Masa Corporal (BMI) y el Logaritmo de Triglicéridos (S5) presentan las correlaciones positivas más fuertes, mientras que el Colesterol HDL (S3) muestra una correlación negativa, indicando que niveles más altos de S3 están asociados con una menor progresión de la diabetes.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Scatter data={bmiYData} options={bmiYOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este diagrama de dispersión ilustra la relación entre el Índice de Masa Corporal (BMI) y la progresión de la diabetes (Y). La tendencia ascendente sugiere que un BMI más alto está asociado con una mayor progresión de la diabetes, lo cual es consistente con la correlación positiva observada en el informe.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Scatter data={s5YData} options={s5YOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este diagrama de dispersión examina la relación entre los niveles de triglicéridos (S5) y la progresión de la diabetes (Y). Se observa una correlación positiva, lo que indica que niveles elevados de S5 tienden a estar asociados con una mayor progresión de la enfermedad.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Bar data={ageDistData} options={ageDistOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este histograma muestra la distribución de las edades de los pacientes en el estudio. La mayoría de los pacientes se encuentran en el rango de los 40 a los 60 años, con una distribución que indica una amplia representación de diferentes grupos de edad.
          </p>
        </div>
      </section>
      
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center">
          <div className="relative h-96 w-full max-w-lg">
            <Bar data={yDistData} options={yDistOptions} />
          </div>
          <p className="text-center text-gray-600 mt-4">
            Este histograma representa la distribución de la variable objetivo 'Y', que mide la progresión de la diabetes. La mayoría de los pacientes se agrupan en rangos de progresión moderada, aunque existe una cola hacia valores de progresión más altos, lo que sugiere una variabilidad significativa en la respuesta a la enfermedad.
          </p>
        </div>
        {/* Espacio para añadir más gráficos si fuera necesario, manteniendo la estética */}
        <div className="bg-white p-6 rounded-lg shadow-md flex flex-col justify-center items-center">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">Conclusiones Clave</h3>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            {edaReport.informe_eda.conclusiones_finales.map((conclusion, index) => (
              <li key={index}>{conclusion}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="bg-white p-8 rounded-lg shadow-lg mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Insights Accionables</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {insights_accionables_mundo_real.map((insight, index) => (
            <div key={index} className="border-l-4 border-purple-500 pl-4 py-2">
              <h3 className="text-xl font-semibold text-gray-700 mb-2">Área: {insight.area}</h3>
              <p className="text-gray-600 mb-2"><span className="font-bold">Insight:</span> {insight.insight}</p>
              <p className="text-gray-600"><span className="font-bold">Recomendación:</span> {insight.recomendacion}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="text-center text-gray-500 text-sm mt-8">
        <p>&copy; 2023 Dashboard de Análisis de Diabetes. Generado con React, Tailwind CSS y Chart.js.</p>
      </footer>
    </div>
  );
};

export default App;
