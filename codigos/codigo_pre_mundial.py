# Importar librerías

import pandas as pd
import numpy as np

# Cargar datos

selecciones = pd.read_csv(
    "../data/processed/selecciones_mundial_2026.csv"
)

dataset_final = pd.read_csv(
    "../data/processed/dataset_mundial_final.csv"
)

# Extraer estadísticas recientes como local

form_home = dataset_final[
    [
        "date",
        "home_team",
        "home_last5_points",
        "home_last5_goals_for",
        "home_last5_goals_against",
        "home_last5_goal_balance"
    ]
].copy()

form_home.columns = [
    "date",
    "team",
    "last5_points",
    "last5_goals_for",
    "last5_goals_against",
    "last5_goal_balance"
]

# Extraer estadísticas recientes como visitante

form_away = dataset_final[
    [
        "date",
        "away_team",
        "away_last5_points",
        "away_last5_goals_for",
        "away_last5_goals_against",
        "away_last5_goal_balance"
    ]
].copy()

form_away.columns = [
    "date",
    "team",
    "last5_points",
    "last5_goals_for",
    "last5_goals_against",
    "last5_goal_balance"
]

# Unificar estadísticas

form_total = pd.concat(
    [form_home, form_away],
    ignore_index=True
)

# Ordenar por fecha

form_total["date"] = pd.to_datetime(
    form_total["date"]
)

form_total = form_total.sort_values(
    "date"
)

# Obtener la última forma disponible de cada selección

form_actual = (
    form_total
    .groupby("team")
    .tail(1)
)

# Normalizar nombres

form_actual["team"] = form_actual["team"].replace({
    "Curaçao": "Curacao",
    "Czechia": "Czech Republic",
    "Congo": "DR Congo"
})

# Incorporar forma reciente a las selecciones del Mundial

selecciones_actuales = selecciones.merge(
    form_actual,
    on="team",
    how="left"
)

# Imputar valores faltantes

selecciones_actuales["last5_points"] = (
    selecciones_actuales["last5_points"]
    .fillna(
        selecciones_actuales["last5_points"].mean()
    )
)

selecciones_actuales["last5_goals_for"] = (
    selecciones_actuales["last5_goals_for"]
    .fillna(
        selecciones_actuales["last5_goals_for"].mean()
    )
)

selecciones_actuales["last5_goals_against"] = (
    selecciones_actuales["last5_goals_against"]
    .fillna(
        selecciones_actuales["last5_goals_against"].mean()
    )
)

selecciones_actuales["last5_goal_balance"] = (
    selecciones_actuales["last5_goal_balance"]
    .fillna(
        selecciones_actuales["last5_goal_balance"].mean()
    )
)

# Guardar dataset final

selecciones_actuales.to_csv(
    "../data/processed/selecciones_actuales_mundial.csv",
    index=False
)

print("Selecciones actuales generadas correctamente.")