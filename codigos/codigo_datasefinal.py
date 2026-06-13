import pandas as pd
import numpy as np

# Cargar datos

results = pd.read_csv(
    "../data/processed/results1_normalized.csv"
)

fifa = pd.read_csv(
    "../data/processed/fifa_normalized.csv"
)

elo = pd.read_csv(
    "../data/processed/elo_normalized.csv"
)

# Fechas

results["date"] = pd.to_datetime(results["date"])
fifa["rank_date"] = pd.to_datetime(fifa["rank_date"])
elo["date"] = pd.to_datetime(elo["date"])

results = results.sort_values("date")
fifa = fifa.sort_values("rank_date")
elo = elo.sort_values("date")

# Peso del torneo

def assign_tournament_weight(tournament):

    if tournament == "FIFA World Cup":
        return 10

    elif tournament in [
        "UEFA Euro",
        "Copa América",
        "African Cup of Nations",
        "AFC Asian Cup",
        "CONCACAF Gold Cup",
        "Confederations Cup"
    ]:
        return 8

    elif "qualification" in tournament.lower():
        return 6

    elif "nations league" in tournament.lower():
        return 4

    elif tournament == "Friendly":
        return 1

    else:
        return 3


results["tournament_weight"] = (
    results["tournament"]
    .apply(assign_tournament_weight)
)

# Columnas Necesarias

results = results[
    [
        "date",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "tournament",
        "tournament_weight",
        "neutral",
        "goal_diff"
    ]
]

fifa = fifa[
    [
        "rank_date",
        "country_full",
        "rank",
        "total_points"
    ]
]

elo = elo[
    [
        "date",
        "team",
        "rating"
    ]
]

# Unificacion nombres FIFA


fifa_mapping = {
    "Korea Republic": "South Korea",
    "IR Iran": "Iran",
    "USA": "United States",
    "Türkiye": "Turkey",
    "Cabo Verde": "Cape Verde",
    "Côte d'Ivoire": "Ivory Coast",
    "Congo DR": "DR Congo"
}

fifa["country_full"] = (
    fifa["country_full"]
    .replace(fifa_mapping)
)

# FIFA home/away

fifa_home = fifa.rename(
    columns={
        "country_full": "home_team",
        "rank": "fifa_rank_home",
        "total_points": "fifa_points_home"
    }
)

fifa_away = fifa.rename(
    columns={
        "country_full": "away_team",
        "rank": "fifa_rank_away",
        "total_points": "fifa_points_away"
    }
)

# Dataset base

mundial_final = results.copy()

# Merge FIFA

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    fifa_home.sort_values("rank_date"),
    left_on="date",
    right_on="rank_date",
    by="home_team",
    direction="backward"
)

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    fifa_away.sort_values("rank_date"),
    left_on="date",
    right_on="rank_date",
    by="away_team",
    direction="backward"
)

mundial_final = mundial_final.drop(
    columns=[
        "rank_date_x",
        "rank_date_y"
    ]
)

# Merge ELO

elo_home = elo.rename(
    columns={
        "team": "home_team",
        "rating": "elo_home"
    }
)

elo_away = elo.rename(
    columns={
        "team": "away_team",
        "rating": "elo_away"
    }
)

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    elo_home.sort_values("date"),
    on="date",
    by="home_team",
    direction="backward"
)

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    elo_away.sort_values("date"),
    on="date",
    by="away_team",
    direction="backward"
)

# Diferencias FIFA Y ELO

mundial_final["fifa_rank_diff"] = (
    mundial_final["fifa_rank_away"]
    - mundial_final["fifa_rank_home"]
)

mundial_final["fifa_points_diff"] = (
    mundial_final["fifa_points_home"]
    - mundial_final["fifa_points_away"]
)

mundial_final["elo_diff"] = (
    mundial_final["elo_home"]
    - mundial_final["elo_away"]
)

# Formas recientes

home_df = mundial_final[
    [
        "date",
        "home_team",
        "away_team",
        "home_score",
        "away_score"
    ]
].copy()

home_df.columns = [
    "date",
    "team",
    "opponent",
    "goals_for",
    "goals_against"
]

away_df = mundial_final[
    [
        "date",
        "away_team",
        "home_team",
        "away_score",
        "home_score"
    ]
].copy()

away_df.columns = [
    "date",
    "team",
    "opponent",
    "goals_for",
    "goals_against"
]

matches_long = pd.concat(
    [home_df, away_df],
    ignore_index=True
)

# Resultados

matches_long["result"] = np.where(
    matches_long["goals_for"] >
    matches_long["goals_against"],
    3,
    np.where(
        matches_long["goals_for"] ==
        matches_long["goals_against"],
        1,
        0
    )
)

matches_long["goal_balance"] = (
    matches_long["goals_for"]
    - matches_long["goals_against"]
)

# Estadísticas ultimos 5 partidos

matches_long["last5_points"] = (
    matches_long.groupby("team")["result"]
    .transform(
        lambda x:
        x.shift().rolling(5, min_periods=1).sum()
    )
)

matches_long["last5_goals_for"] = (
    matches_long.groupby("team")["goals_for"]
    .transform(
        lambda x:
        x.shift().rolling(5, min_periods=1).sum()
    )
)

matches_long["last5_goals_against"] = (
    matches_long.groupby("team")["goals_against"]
    .transform(
        lambda x:
        x.shift().rolling(5, min_periods=1).sum()
    )
)

matches_long["last5_goal_balance"] = (
    matches_long.groupby("team")["goal_balance"]
    .transform(
        lambda x:
        x.shift().rolling(5, min_periods=1).sum()
    )
)


# Home form / away form

form_home = matches_long[
    [
        "date",
        "team",
        "last5_points",
        "last5_goals_for",
        "last5_goals_against",
        "last5_goal_balance"
    ]
].copy()

form_away = form_home.copy()

form_home = form_home.rename(
    columns={
        "team": "home_team",
        "last5_points": "home_last5_points",
        "last5_goals_for": "home_last5_goals_for",
        "last5_goals_against": "home_last5_goals_against",
        "last5_goal_balance": "home_last5_goal_balance"
    }
)

form_away = form_away.rename(
    columns={
        "team": "away_team",
        "last5_points": "away_last5_points",
        "last5_goals_for": "away_last5_goals_for",
        "last5_goals_against": "away_last5_goals_against",
        "last5_goal_balance": "away_last5_goal_balance"
    }
)

form_home = form_home.sort_values("date")
form_away = form_away.sort_values("date")

# Merge forma

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    form_home,
    on="date",
    by="home_team",
    direction="backward"
)

mundial_final = pd.merge_asof(
    mundial_final.sort_values("date"),
    form_away,
    on="date",
    by="away_team",
    direction="backward"
)

# Diferencia forma

mundial_final["form_points_diff"] = (
    mundial_final["home_last5_points"]
    - mundial_final["away_last5_points"]
)

mundial_final["form_goals_for_diff"] = (
    mundial_final["home_last5_goals_for"]
    - mundial_final["away_last5_goals_for"]
)

mundial_final["form_goals_against_diff"] = (
    mundial_final["home_last5_goals_against"]
    - mundial_final["away_last5_goals_against"]
)

mundial_final["form_goal_balance_diff"] = (
    mundial_final["home_last5_goal_balance"]
    - mundial_final["away_last5_goal_balance"]
)

# Limpieza final

dataset_final = mundial_final.copy()

dataset_final = dataset_final.dropna(
    subset=[
        "fifa_rank_diff",
        "fifa_points_diff",
        "elo_diff"
    ]
)

dataset_final = dataset_final.dropna()

# Guardar

dataset_final.to_csv(
    "dataset_mundial_final.csv",
    index=False
)

print("Dataset generado correctamente")
print(dataset_final.shape)