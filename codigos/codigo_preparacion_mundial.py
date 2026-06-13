# Importar librerías

import pandas as pd

# Cargar datos

fifa = pd.read_csv(
    "../data/processed/fifa_normalized.csv"
)

elo = pd.read_csv(
    "../data/processed/elo_normalized.csv"
)

# Convertir fechas

fifa["rank_date"] = pd.to_datetime(
    fifa["rank_date"]
)

elo["date"] = pd.to_datetime(
    elo["date"]
)

# Obtener último ranking FIFA

fifa_actual = (
    fifa.sort_values("rank_date")
    .groupby("country_full")
    .tail(1)
)

# Definir selecciones clasificadas

selecciones_mundial = [
    "Mexico", "South Africa", "South Korea", "Czech Republic",
    "Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland",
    "Brazil", "Morocco", "Haiti", "Scotland",
    "United States", "Paraguay", "Australia", "Turkey",
    "Germany", "Curacao", "Ivory Coast", "Ecuador",
    "Netherlands", "Japan", "Sweden", "Tunisia",
    "Belgium", "Egypt", "Iran", "New Zealand",
    "Spain", "Cape Verde", "Saudi Arabia", "Uruguay",
    "France", "Senegal", "Iraq", "Norway",
    "Argentina", "Algeria", "Austria", "Jordan",
    "Portugal", "DR Congo", "Uzbekistan", "Colombia",
    "England", "Croatia", "Ghana", "Panama"
]

selecciones_df = pd.DataFrame(
    {"team": selecciones_mundial}
)

# Adaptar nombres para FIFA

equivalencias_fifa = {
    "South Korea": "Korea Republic",
    "Iran": "IR Iran",
    "DR Congo": "Congo DR",
    "Czech Republic": "Czechia",
    "Cape Verde": "Cabo Verde",
    "Ivory Coast": "Côte d'Ivoire",
    "United States": "USA",
    "Turkey": "Türkiye",
    "Curacao": "Curaçao"
}

selecciones_df["country_fifa"] = (
    selecciones_df["team"]
    .replace(equivalencias_fifa)
)

# Incorporar ranking FIFA

fifa_mundial = (
    selecciones_df.merge(
        fifa_actual,
        left_on="country_fifa",
        right_on="country_full",
        how="left"
    )
)

fifa_mundial = fifa_mundial[
    [
        "team",
        "rank",
        "total_points"
    ]
]

# Obtener último ranking Elo

elo_actual = (
    elo.sort_values("date")
    .groupby("team")
    .tail(1)
)

# Adaptar nombres para Elo

equivalencias_elo = {
    "Curacao": "Curaçao",
    "Czech Republic": "Czechia",
    "DR Congo": "Democratic Republic of Congo"
}

selecciones_df["team_elo"] = (
    selecciones_df["team"]
    .replace(equivalencias_elo)
)

# Incorporar ranking Elo

elo_mundial = (
    selecciones_df.merge(
        elo_actual,
        left_on="team_elo",
        right_on="team",
        how="left"
    )
)

elo_mundial = elo_mundial[
    [
        "team_x",
        "rating"
    ]
]

elo_mundial.columns = [
    "team",
    "elo"
]

# Crear dataset final

simulacion_df = fifa_mundial.merge(
    elo_mundial,
    on="team",
    how="inner"
)

# Guardar resultados

simulacion_df.to_csv(
    "../data/processed/selecciones_mundial_2026.csv",
    index=False
)

print("Selecciones Mundial 2026 generadas correctamente.")