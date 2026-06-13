import pandas as pd


# Cargar Datos

results = pd.read_csv(
    "../data/processed/results_final.csv"
)

fifa = pd.read_csv(
    "../data/processed/fifa_final.csv"
)

# Fechas

results["date"] = pd.to_datetime(
    results["date"]
)

fifa["rank_date"] = pd.to_datetime(
    fifa["rank_date"]
)

# Normalizacion de nombres


name_mapping = {
    "United States": "USA",
    "South Korea": "Korea Republic",
    "North Korea": "Korea DPR",
    "Iran": "IR Iran",
    "Turkey": "Türkiye",
    "Ivory Coast": "Côte d'Ivoire",
    "DR Congo": "Congo DR",
    "Cape Verde": "Cabo Verde",
    "Czech Republic": "Czechia",
    "Hong Kong": "Hong Kong, China",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Taiwan": "Chinese Taipei",
    "Brunei": "Brunei Darussalam"
}

results["home_team"] = (
    results["home_team"]
    .replace(name_mapping)
)

results["away_team"] = (
    results["away_team"]
    .replace(name_mapping)
)

# Filtrar equipos de FIFA


teams_fifa = set(
    fifa["country_full"]
)

results_fifa = results[
    (
        results["home_team"].isin(teams_fifa)
    )
    &
    (
        results["away_team"].isin(teams_fifa)
    )
]

# Guardar

results_fifa.to_csv(
    "../data/processed/results_normalized.csv",
    index=False
)

fifa.to_csv(
    "../data/processed/fifa_normalized.csv",
    index=False
)

print("Normalización de nombres completada.")
print(f"Partidos conservados: {len(results_fifa):,}")