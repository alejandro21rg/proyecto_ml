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