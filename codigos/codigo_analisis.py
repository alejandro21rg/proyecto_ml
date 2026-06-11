import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Cargar datos

dataset = pd.read_csv("../data/processed/dataset_mundial_final.csv")

# Carpeta de imágenes

carpeta = "../imagenes/analisis"

os.makedirs(carpeta, exist_ok=True)


# Función guardar

def guardar_grafica(nombre):

    ruta = os.path.join(
        carpeta,
        nombre
    )

    plt.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Imagen guardada: {ruta}")

# Gráficas

# Histograma de goal_diff

plt.figure(figsize=(10,5))

sns.histplot(
    dataset["goal_diff"],
    bins=30
)

plt.title("Distribución de la diferencia de goles")
plt.xlabel("Diferencia de goles")
plt.ylabel("Frecuencia")

guardar_grafica(
    "histograma_goal_diff.png"
)

# Boxplot goal_diff

plt.figure(figsize=(10,2))

sns.boxplot(
    x=dataset["goal_diff"]
)

plt.title(
    "Boxplot de diferencia de goles"
)

guardar_grafica(
    "boxplot_goal_diff.png"
)

# Heatmap correlaciones

numeric_cols = dataset.select_dtypes(
    include=np.number
).columns

corr = dataset[numeric_cols].corr()

plt.figure(figsize=(18,12))

sns.heatmap(
    corr,
    cmap="coolwarm",
    center=0
)

plt.title(
    "Matriz de correlación"
)

guardar_grafica(
    "heatmap_correlacion.png"
)

# Distribución Elo

plt.figure(figsize=(10,5))

sns.histplot(
    dataset["elo_home"],
    bins=30,
    kde=True
)

plt.title(
    "Distribución Elo local"
)

guardar_grafica(
    "histograma_elo.png"
)

# Elo vs Goal Diff

plt.figure(figsize=(10,6))

sns.scatterplot(
    data=dataset,
    x="elo_diff",
    y="goal_diff",
    alpha=0.3
)

plt.title(
    "Elo Difference vs Goal Difference"
)

guardar_grafica(
    "scatter_elo_goal_diff.png"
)

# Correlación con goal_diff

corr_goal = (
    corr["goal_diff"]
    .sort_values()
)

plt.figure(figsize=(10,8))

corr_goal.plot(
    kind="barh"
)

plt.title(
    "Correlación con goal_diff"
)

guardar_grafica(
    "correlacion_goal_diff.png"
)
