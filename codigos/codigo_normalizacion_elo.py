# Importar librerías

import pandas as pd

# Cargar datos

results = pd.read_csv(
    "../data/processed/results_normalized.csv"
)

elo = pd.read_csv(
    "../data/processed/elo_final.csv"
)

# Limpiar nombres de equipos en Elo

elo["team"] = (
    elo["team"]
    .str.replace("\xa0", " ", regex=False)
    .str.strip()
)

# Crear diccionario de equivalencias

name_mapping_elo = {
    "American Samoa": "Samoa",
    "Brunei Darussalam": "Brunei",
    "Cabo Verde": "Cape Verde",
    "China PR": "China",
    "Chinese Taipei": "Taiwan",
    "Congo DR": "Democratic Republic of Congo",
    "Côte d'Ivoire": "Ivory Coast",
    "Hong Kong, China": "Hong Kong",
    "IR Iran": "Iran",
    "Korea DPR": "North Korea",
    "Korea Republic": "South Korea",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Macau": "Macao",
    "Republic of Ireland": "Ireland",
    "São Tomé and Príncipe": "Sao Tome and Principe",
    "Timor-Leste": "East Timor",
    "Türkiye": "Turkey",
    "USA": "United States"
}

# Normalizar nombres en Results

results["home_team"] = (
    results["home_team"]
    .replace(name_mapping_elo)
)

results["away_team"] = (
    results["away_team"]
    .replace(name_mapping_elo)
)

# Guardar resultados

elo.to_csv(
    "../data/processed/elo_normalized.csv",
    index=False
)

results.to_csv(
    "../data/processed/results1_normalized.csv",
    index=False
)

print("Normalización Elo completada.")