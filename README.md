Predicción y Simulación del Mundial de Fútbol 2026 mediante Machine Learning

Descripción del proyecto:
Este proyecto tiene como objetivo desarrollar un sistema de Machine Learning capaz de predecir el resultado esperado de partidos internacionales de selecciones nacionales de fútbol y utilizar dichas predicciones para simular el Mundial de Fútbol 2026.

A partir de datos históricos de partidos internacionales, rankings FIFA y puntuaciones Elo, se entrenarán distintos modelos de aprendizaje automático para estimar la diferencia de goles esperada entre dos selecciones. 
Posteriormente, el mejor modelo será utilizado para simular miles de ediciones completas del Mundial 2026 mediante técnicas de Monte Carlo.

El resultado final permitirá estimar:
Probabilidad de superar la fase de grupos.
Probabilidad de alcanzar cada ronda eliminatoria.
Probabilidad de disputar la final.
Probabilidad de proclamarse campeón del mundo.


Objetivo principal
Desarrollar y comparar distintos modelos de Machine Learning para predecir la diferencia de goles en partidos internacionales de selecciones nacionales.

Objetivos específicos
Realizar la limpieza y preparación de múltiples fuentes de datos.
Construir un dataset unificado para el entrenamiento de modelos predictivos.
Diseñar variables que representen la fuerza y forma reciente de cada selección.
Comparar diferentes modelos de Machine Learning.
Simular el Mundial 2026 mediante técnicas de Monte Carlo.
Estimar probabilidades de clasificación y campeonato para cada selección.

Dataset utilizados:

Results Dataset: Contiene resultados históricos de partidos internacionales entre selecciones nacionales.

Variables principales:
Fecha del partido.
Selección local.
Selección visitante.
Goles local.
Goles visitante.
Competición.
Campo neutral.

FIFA Ranking Dataset: Contiene la evolución histórica del ranking FIFA de las selecciones nacionales.

Variables principales:
Fecha del ranking.
Selección.
Posición FIFA.
Puntuación FIFA.
Confederación.

Elo Ratings Dataset: Contiene las puntuaciones Elo de las selecciones nacionales.

Variables principales:
Fecha.
Selección.
Elo Rating.
Variación del Elo.
Variable objetivo

La variable objetivo utilizada durante el entrenamiento será la diferencia de goles:

goal_diff = home_score - away_score

Interpretación:
Valor positivo → victoria del equipo local.
Valor cero → empate.
Valor negativo → victoria del equipo visitante.

Esta formulación permite representar mediante una única variable los tres posibles resultados de un partido.


Se entrenarán y compararán los siguientes modelos:



Los modelos serán evaluados mediante:
MAE
Error absoluto medio.
RMSE
R²
Coeficiente de determinación.

El modelo con mejor rendimiento será seleccionado para la fase de simulación.

Simulación del Mundial 2026

Una vez seleccionado el mejor modelo:
Se generarán todos los encuentros de la fase de grupos.
Se calcularán los resultados esperados de cada partido.
Se construirán las clasificaciones de grupo.
Se determinarán los clasificados a las rondas eliminatorias.
Se simulará el torneo completo.

Este proceso será repetido miles de veces utilizando simulación Monte Carlo.

##  Estructura del Proyecto

## 📂 Estructura del Proyecto

```text
proyecto_ml/
│
├── data/
│   │
│   ├── raw/
│   │   ├── results.csv
│   │   ├── fifa_ranking_2026.csv
│   │   └── elo.csv
│   │
│   └── processed/
│       ├── results_normalized.csv
│       ├── results1_normalized.csv
│       ├── results_final.csv
│       ├── fifa_normalized.csv
│       ├── fifa_final.csv
│       ├── elo_normalized.csv
│       ├── elo_final.csv
│       ├── dataset_modelado.csv
│       ├── dataset_mundial_final.csv
│       ├── selecciones_mundial_2026.csv
│       ├── selecciones_actuales_mundial.csv
│       └── selecciones_actuales_mundial_prueba.csv
│
├── notebook/
│   ├── limpieza_results.ipynb
│   ├── limpieza_ranking.ipynb
│   ├── normalizacion_nombres.ipynb
│   ├── normalizacion_elo.ipynb
│   ├── elo.ipynb
│   ├── datasetfinal.ipynb
│   ├── analisis.ipynb
│   ├── muestras.ipynb
│   ├── preparacion_mundial_2026.ipynb
│   ├── mundial_simulacion.ipynb
│   ├── mundial_simulacion_ridge.ipynb
│   ├── mundial_simulacion_codigo.ipynb
│   └── simulacion_mundial.ipynb
│
├── modelos/
│   ├── modelo_regresion_lineal.pkl
│   ├── modelo_ridge.pkl
│   ├── scaler.pkl
│   ├── modelos_ml.ipynb
│   └── comparacion_modelos.csv
│
├── resultados/
│   ├── probabilidades_mundial.csv
│   ├── probabilidades_mundial_1.csv
│   ├── probabilidades_mundial_2.csv
│   ├── probabilidades_mundial_20.csv
│   ├── probabilidades_mundial_50.csv
│   ├── probabilidades_mundial_100.csv
│   ├── probabilidades_mundial_500.csv
│   ├── probabilidades_mundial_500_2.csv
│   ├── probabilidades_mundial_mil.csv
│   └── probabilidades_mundial_5mil.csv
│
├── imagenes/
│   ├── analisis/
│   ├── simulacion/
│   ├── copa_mundo.png
│   └── estadio_fondo.png
│
├── codigos/
│   ├── codigo_limpieza.py
│   ├── codigo_normalizacion_nombres.py
│   ├── codigo_normalizacion_elo.py
│   ├── codigo_datasetfinal.py
│   ├── codigo_analisis.py
│   ├── codigo_muestras.py
│   ├── codigo_modelos.py
│   ├── codigo_pre_mundial.py
│   ├── codigo_preparacion_mundial.py
│   └── codigo_simulacion.py
│
├── app.py
├── streamlit.py
├── simular.py
├── memoria.ipynb
├── README.md
├── presentacion_ML_final.pdf
├── presentacion_ML_streamlit.pdf
└── .gitignore
```