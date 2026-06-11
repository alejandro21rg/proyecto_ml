import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Limpieza results.csv

results = pd.read_csv("../data/raw/results.csv")

results = results.dropna(
    subset=["home_score", "away_score"]
)

#  Conversión de Variables Temporales

results["date"] = pd.to_datetime(results["date"])


# Creación target

results["goal_diff"] = (
    results["home_score"]
    - results["away_score"]
)

# Variables 

results_clean = results[
    [
        "date",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "tournament",
        "neutral",
        "goal_diff"
    ]
]

# Fechas con las que nos quedamos

results_clean = results_clean[
    (results_clean["date"] >= "2000-01-01") &
    (results_clean["date"] <= "2025-12-31")
]

# Guardar

results_clean.to_csv(
    "../data/processed/results_final.csv",
    index=False
)

# Limpieza fifa_ranking_2006.csv

fifa = pd.read_csv("../data/raw/fifa_ranking_2026.csv")

fifa = fifa.dropna(
    subset=["rank"]
)

fifa = fifa.drop(
    columns=["Unnamed: 0"]
)

#  Conversión de Variables Temporales

fifa["rank_date"] = pd.to_datetime(
    fifa["rank_date"]
)

# Variables 

fifa = fifa[
    [
        "rank_date",
        "country_full",
        "rank",
        "total_points"
    ]
]

# Fechas con las que nos quedamos

fifa = fifa[
    (fifa["rank_date"] >= "2000-01-01") &
    (fifa["rank_date"] <= "2025-12-31")
]

# Guardar

fifa.to_csv(
    "../data/processed/fifa_final.csv",
    index=False
)

# Limpieza eloratings.csv

elo = pd.read_csv("../data/raw/eloratings.csv")

elo = elo.dropna()

#  Conversión de Variables Temporales

elo["date"] = pd.to_datetime(
    elo["date"],
    format="mixed"
)

# Variables 

elo_clean = elo[
    [
        "date",
        "team",
        "rating"
    ]
]

# Fechas con las que nos quedamos

elo = elo[
    (elo["date"] >= "2000-01-01") &
    (elo["date"] <= "2025-12-31")
]

# Guardar

elo_clean.to_csv(
    "../data/raw/elo_final.csv",
    index=False
)




