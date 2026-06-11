import pandas as pd
import matplotlib.pyplot as plt
import os


# CSV

csvs = {
    "50": pd.read_csv("../resultados/probabilidades_mundial_50.csv"),
    "100": pd.read_csv("../resultados/probabilidades_mundial_100.csv"),
    "20": pd.read_csv("../resultados/probabilidades_mundial_20.csv")
}

# Carpeta imágenes

carpeta = "../imagenes/simulacion"

os.makedirs(carpeta, exist_ok=True)

# Guardar

def guardar_grafica(nombre_archivo):

    ruta_imagen = os.path.join(
        carpeta,
        nombre_archivo
    )

    plt.savefig(
        ruta_imagen,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Imagen guardada en: {ruta_imagen}")

# Gráficas

for nombre, df in csvs.items():

    top8 = df.sort_values(
        "Campeon",
        ascending=False
    ).head(8)

    plt.figure(figsize=(8,8))

    plt.pie(
        top8["Campeon"],
        labels=top8["team"],
        autopct="%1.1f%%"
    )

    plt.title(
        f"Distribución de campeón ({nombre} simulaciones)"
    )

    guardar_grafica(
        f"tarta_campeon_{nombre}.png"
    )

for nombre, df in csvs.items():

    top10 = (
        df.sort_values("Campeon", ascending=False)
        .head(10)
        .sort_values("Campeon")
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top10["team"],
        top10["Campeon"]
    )

    plt.xlabel("Probabilidad de campeón (%)")

    plt.title(
        f"Top 10 favoritos al Mundial ({nombre} simulaciones)"
    )

    for i, valor in enumerate(top10["Campeon"]):
        plt.text(
            valor + 0.5,
            i,
            f"{valor:.1f}%"
        )

    plt.grid(axis="x", linestyle="--", alpha=0.5)

    guardar_grafica(
        f"barras_campeon_{nombre}.png"
    )

for nombre, df in csvs.items():

    top10 = (
        df.sort_values("Campeon", ascending=False)
        .head(10)
    )

    top10.set_index("team")[[
        "16avos",
        "Octavos",
        "Cuartos",
        "Semifinal",
        "Final",
        "Campeon"
    ]].plot(
        kind="bar",
        stacked=True,
        figsize=(12,6)
    )

    plt.title(
        f"Probabilidades acumuladas por ronda ({nombre} simulaciones)"
    )

    plt.ylabel("Probabilidad (%)")
    plt.xticks(rotation=45)

    guardar_grafica(
        f"probabilidades_rondas_{nombre}.png"
    )

for nombre, df in csvs.items():

    top5 = (
        df.sort_values("Campeon", ascending=False)
        .head(5)
    )

    rondas = [
        "16avos",
        "Octavos",
        "Cuartos",
        "Semifinal",
        "Final",
        "Campeon"
    ]

    plt.figure(figsize=(10,6))

    for _, fila in top5.iterrows():

        plt.plot(
            rondas,
            fila[rondas],
            marker="o",
            linewidth=2,
            label=fila["team"]
        )

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.title(
        f"Evolución de probabilidades - Top 5 ({nombre} simulaciones)"
    )

    plt.ylabel("Probabilidad (%)")

    guardar_grafica(
        f"evolucion_top5_{nombre}.png"
    )



