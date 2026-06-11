import pandas as pd
import numpy as np
import joblib
from collections import defaultdict
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning
)

# Cargamos dataset

dataset_modelado = pd.read_csv(
    "../data/processed/dataset_modelado.csv"
)

selecciones = pd.read_csv(
    "../data/processed/selecciones_actuales_mundial.csv"
)

# Cargamos los modelos

modelo = joblib.load(
    "../models/modelo_regresion_lineal.pkl"
)
scaler = joblib.load(
    "../models/scaler.pkl"
)

equipos_dict = {}

for _, fila in selecciones.iterrows():

    equipos_dict[
        fila["team"]
    ] = fila


def obtener_equipo(nombre):

    return equipos_dict[nombre]

# Funcion crear partido

def crear_partido(equipo_local, equipo_visitante):

    local = obtener_equipo(equipo_local)
    visitante = obtener_equipo(equipo_visitante)

    return np.array([[
    1,
    10,
    local["rank"] - visitante["rank"],
    local["total_points"] - visitante["total_points"],
    local["elo"] - visitante["elo"],
    local["last5_points"] - visitante["last5_points"],
    local["last5_goals_for"] - visitante["last5_goals_for"],
    local["last5_goals_against"] - visitante["last5_goals_against"],
    local["last5_goal_balance"] - visitante["last5_goal_balance"]
]])
# Funcion simular partido, con rsme de simulacion

rmse = 1.6435
rmse_simulacion = 0.8

def simular_partido(equipo_local, equipo_visitante):

    partido = crear_partido(
        equipo_local,
        equipo_visitante
    )

    partido_scaled = scaler.transform(
        partido
    )

    prediccion = modelo.predict(
        partido_scaled
    )[0]

    error = np.random.normal(
        loc=0,
        scale=rmse_simulacion
    )

    diferencia_final = prediccion + error

    return diferencia_final

# Funcion generar marcadores

def generar_marcador(diferencia):

    diferencia_redondeada = int(round(diferencia))

    if diferencia_redondeada == 0:

        goles = np.random.randint(0, 4)

        return goles, goles

    goles_base = np.random.randint(0, 3)

    if diferencia_redondeada > 0:

        return (
            goles_base + diferencia_redondeada,
            goles_base
        )

    else:

        return (
            goles_base,
            goles_base + abs(diferencia_redondeada)
        )

# Funcion para actualizar la tabla 

def actualizar_tabla(
    tabla,
    local,
    visitante,
    goles_local,
    goles_visitante
):

    # Partidos jugados

    tabla.loc[local, "PJ"] += 1
    tabla.loc[visitante, "PJ"] += 1

    # Goles

    tabla.loc[local, "GF"] += goles_local
    tabla.loc[local, "GC"] += goles_visitante

    tabla.loc[visitante, "GF"] += goles_visitante
    tabla.loc[visitante, "GC"] += goles_local

    # Resultado

    if goles_local > goles_visitante:

        tabla.loc[local, "PG"] += 1
        tabla.loc[local, "PTS"] += 3

        tabla.loc[visitante, "PP"] += 1

    elif goles_local < goles_visitante:

        tabla.loc[visitante, "PG"] += 1
        tabla.loc[visitante, "PTS"] += 3

        tabla.loc[local, "PP"] += 1

    else:

        tabla.loc[local, "PE"] += 1
        tabla.loc[visitante, "PE"] += 1

        tabla.loc[local, "PTS"] += 1
        tabla.loc[visitante, "PTS"] += 1

    return tabla

# Funcion para simular los diferentes grupos del mundial

def simular_grupo(equipos):

    tabla = pd.DataFrame({
        "team": equipos,
        "PJ": 0,
        "PG": 0,# 
        "PE": 0,
        "PP": 0,
        "GF": 0,
        "GC": 0,
        "DG": 0,
        "PTS": 0
    })

    tabla = tabla.set_index(
        "team"
    )

    partidos = []

    resultados_partidos = []

    for i in range(len(equipos)):

        for j in range(i + 1, len(equipos)):

            partidos.append(
                (
                    equipos[i],
                    equipos[j]
                )
            )

    for local, visitante in partidos:

        diferencia = simular_partido(
            local,
            visitante
        )

        goles_local, goles_visitante = generar_marcador(
            diferencia
        )

        resultados_partidos.append(
            {
                "local": local,
                "visitante": visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante
            }
        )

        actualizar_tabla(
            tabla,
            local,
            visitante,
            goles_local,
            goles_visitante
        )

    tabla["DG"] = (
        tabla["GF"]
        - tabla["GC"]
    )

    tabla = tabla.sort_values(
        by=["PTS", "DG", "GF"],
        ascending=False
    )

    tabla = tabla.reset_index()

    tabla["posicion"] = range(
        1,
        len(tabla) + 1
    )

    tabla = tabla[
        [
            "posicion",
            "team",
            "PJ",
            "PG",
            "PE",
            "PP",
            "GF",
            "GC",
            "DG",
            "PTS"
        ]
    ]

    partidos_df = pd.DataFrame(
        resultados_partidos
    )

    return tabla, partidos_df

# Funcion para obtener los clasificados

def obtener_clasificados(clasificacion):

    primero = clasificacion.iloc[0]
    segundo = clasificacion.iloc[1]
    tercero = clasificacion.iloc[2]
    cuarto = clasificacion.iloc[3]

    return primero, segundo, tercero, cuarto

# Grupos del mundial

grupos = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],

    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],

    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],

    "D": ["United States", "Paraguay", "Australia", "Turkey"],

    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],

    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],

    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],

    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],

    "I": ["France", "Senegal", "Iraq", "Norway"],

    "J": ["Argentina", "Algeria", "Austria", "Jordan"],

    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],

    "L": ["England", "Croatia", "Ghana", "Panama"]
}

# Funcion para obtener los equipos clasificados de cada grupo

def simular_fase_grupos(grupos):

    clasificaciones = {}

    partidos_grupos = {}

    primeros = []

    segundos = []

    terceros = []

    cuartos = []

    for nombre_grupo, equipos in grupos.items():

        clasificacion, partidos = simular_grupo(
            equipos
        )

        clasificaciones[nombre_grupo] = clasificacion

        partidos_grupos[nombre_grupo] = partidos

        primero = clasificacion.iloc[0].copy()
        primero["grupo"] = nombre_grupo
        primeros.append(primero)

        segundo = clasificacion.iloc[1].copy()
        segundo["grupo"] = nombre_grupo
        segundos.append(segundo)

        tercero = clasificacion.iloc[2].copy()
        tercero["grupo"] = nombre_grupo
        terceros.append(tercero)

        cuarto = clasificacion.iloc[3].copy()
        cuarto["grupo"] = nombre_grupo
        cuartos.append(cuarto)

    primeros = pd.DataFrame(primeros)

    segundos = pd.DataFrame(segundos)

    terceros = pd.DataFrame(terceros)

    cuartos = pd.DataFrame(cuartos)

    return (
        clasificaciones,
        partidos_grupos,
        primeros,
        segundos,
        terceros,
        cuartos
    )

 # Funcion para simular las eliminatorias
 
def simular_eliminatoria(local, visitante):

    diferencia = simular_partido(
        local,
        visitante
    )

    goles_local, goles_visitante = generar_marcador(
        diferencia
    )

    if goles_local > goles_visitante:

        ganador = str(local)

    elif goles_visitante > goles_local:

        ganador = str(visitante)

    else:

        ganador = str (np.random.choice(
            [local, visitante])
        )

    return {
        "local": local,
        "visitante": visitante,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "ganador": ganador
    }

# Diferentes Cruces

cruces_octavos = {

    89: (74, 77),
    90: (73, 75),
    91: (76, 78),
    92: (79, 80),

    93: (83, 84),
    94: (81, 82),
    95: (86, 88),
    96: (85, 87)
}

cruces_cuartos = {

    97: (89, 90),

    98: (93, 94),

    99: (91, 92),

    100: (95, 96)
}

cruces_semifinales = {

    101: (97, 98),

    102: (99, 100)
}

# Funcion para simular el mundia completo

def simular_mundial():

    (
        clasificaciones,
        partidos_grupos,
        primeros,
        segundos,
        terceros,
        cuartos
    ) = simular_fase_grupos(
        grupos
    )

    ranking_terceros = (
        terceros
        .sort_values(
            by=["PTS", "DG", "GF"],
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    mejores_terceros = (
        ranking_terceros.head(8)
    )

    equipos_por_grupo = {}

    for _, fila in primeros.iterrows():

        equipos_por_grupo[
            (fila["grupo"], "1º")
        ] = fila["team"]

    for _, fila in segundos.iterrows():

        equipos_por_grupo[
            (fila["grupo"], "2º")
        ] = fila["team"]

    for _, fila in mejores_terceros.iterrows():

        equipos_por_grupo[
            (fila["grupo"], "3º")
        ] = fila["team"]

    terceros_ordenados = (
        mejores_terceros["team"]
        .tolist()
    )

    cruces_terceros = {

        74: (
            equipos_por_grupo[("E", "1º")],
            terceros_ordenados[0]
        ),

        77: (
            equipos_por_grupo[("I", "1º")],
            terceros_ordenados[1]
        ),

        79: (
            equipos_por_grupo[("A", "1º")],
            terceros_ordenados[2]
        ),

        80: (
            equipos_por_grupo[("L", "1º")],
            terceros_ordenados[3]
        ),

        81: (
            equipos_por_grupo[("D", "1º")],
            terceros_ordenados[4]
        ),

        82: (
            equipos_por_grupo[("G", "1º")],
            terceros_ordenados[5]
        ),

        85: (
            equipos_por_grupo[("B", "1º")],
            terceros_ordenados[6]
        ),

        87: (
            equipos_por_grupo[("K", "1º")],
            terceros_ordenados[7]
        )
    }

    cruces_fijos = {

        73: (
            equipos_por_grupo[("A", "2º")],
            equipos_por_grupo[("B", "2º")]
        ),

        75: (
            equipos_por_grupo[("F", "1º")],
            equipos_por_grupo[("C", "2º")]
        ),

        76: (
            equipos_por_grupo[("C", "1º")],
            equipos_por_grupo[("F", "2º")]
        ),

        78: (
            equipos_por_grupo[("E", "2º")],
            equipos_por_grupo[("I", "2º")]
        ),

        83: (
            equipos_por_grupo[("K", "2º")],
            equipos_por_grupo[("L", "2º")]
        ),

        84: (
            equipos_por_grupo[("H", "1º")],
            equipos_por_grupo[("J", "2º")]
        ),

        86: (
            equipos_por_grupo[("J", "1º")],
            equipos_por_grupo[("H", "2º")]
        ),

        88: (
            equipos_por_grupo[("D", "2º")],
            equipos_por_grupo[("G", "2º")]
        )
    }

    partidos_eliminatoria = {}

    for numero, (local, visitante) in cruces_fijos.items():

        partidos_eliminatoria[numero] = {
            "local": local,
            "visitante": visitante
        }

    for numero, (local, visitante) in cruces_terceros.items():

        partidos_eliminatoria[numero] = {
            "local": local,
            "visitante": visitante
        }

    resultados_eliminatoria = {}

    def ganador(numero_partido):

        return resultados_eliminatoria[
            numero_partido
        ]["ganador"]

    def jugar(numero_partido):

        local = partidos_eliminatoria[
            numero_partido
        ]["local"]

        visitante = partidos_eliminatoria[
            numero_partido
        ]["visitante"]

        resultado = simular_eliminatoria(
            local,
            visitante
        )

        resultados_eliminatoria[
            numero_partido
        ] = resultado

    # Dieciseisavos

    for partido in range(73, 89):

        jugar(partido)

    # Octavos

    cruces_octavos = {

        89: (74, 77),
        90: (73, 75),
        91: (76, 78),
        92: (79, 80),

        93: (83, 84),
        94: (81, 82),
        95: (86, 88),
        96: (85, 87)
    }

    for partido, (p1, p2) in cruces_octavos.items():

        resultado = simular_eliminatoria(
            ganador(p1),
            ganador(p2)
        )

        resultados_eliminatoria[
            partido
        ] = resultado

    # Cuartos

    cruces_cuartos = {

        97: (89, 90),

        98: (93, 94),

        99: (91, 92),

        100: (95, 96)
    }

    for partido, (p1, p2) in cruces_cuartos.items():

        resultado = simular_eliminatoria(
            ganador(p1),
            ganador(p2)
        )

        resultados_eliminatoria[
            partido
        ] = resultado

    # Semifinales

    resultado = simular_eliminatoria(
        ganador(97),
        ganador(98)
    )

    resultados_eliminatoria[101] = resultado

    resultado = simular_eliminatoria(
        ganador(99),
        ganador(100)
    )

    resultados_eliminatoria[102] = resultado

# Final

    final = simular_eliminatoria(
        ganador(101),
        ganador(102)
)

    resultados_eliminatoria[104] = final


# Equipos que alcanzan cada ronda

    equipos_16avos = set()

    for partido in range(73, 89):

        equipos_16avos.add(
        partidos_eliminatoria[partido]["local"]
    )

        equipos_16avos.add(
        partidos_eliminatoria[partido]["visitante"]
    )


    equipos_octavos = set()

    for partido in range(89, 97):

        equipos_octavos.add(
        resultados_eliminatoria[partido]["local"]
    )

        equipos_octavos.add(
        resultados_eliminatoria[partido]["visitante"]
    )


    equipos_cuartos = set()

    for partido in range(97, 101):

        equipos_cuartos.add(
        resultados_eliminatoria[partido]["local"]
    )

        equipos_cuartos.add(
        resultados_eliminatoria[partido]["visitante"]
    )


    equipos_semis = set()

    for partido in [101, 102]:

        equipos_semis.add(
        resultados_eliminatoria[partido]["local"]
    )

        equipos_semis.add(
        resultados_eliminatoria[partido]["visitante"]
    )


    equipos_final = {

        resultados_eliminatoria[104]["local"],
        resultados_eliminatoria[104]["visitante"]

}
    return {

    "campeon":
        resultados_eliminatoria[104]["ganador"],

    "equipos_16avos":
        equipos_16avos,

    "equipos_octavos":
        equipos_octavos,

    "equipos_cuartos":
        equipos_cuartos,

    "equipos_semis":
        equipos_semis,

    "equipos_final":
        equipos_final,

    "final":
        resultados_eliminatoria[104],

    "resultados":
        resultados_eliminatoria
}

# Para realizar la simulacion y obtener las probabilidades de cada selección

contador_16avos = defaultdict(int)

contador_octavos = defaultdict(int)

contador_cuartos = defaultdict(int)

contador_semis = defaultdict(int)

contador_final = defaultdict(int)

contador_campeon = defaultdict(int)


n_simulaciones = 50


for _ in range(n_simulaciones):

    resultado = simular_mundial()

    for equipo in resultado["equipos_16avos"]:

        contador_16avos[equipo] += 1

    for equipo in resultado["equipos_octavos"]:

        contador_octavos[equipo] += 1

    for equipo in resultado["equipos_cuartos"]:

        contador_cuartos[equipo] += 1

    for equipo in resultado["equipos_semis"]:

        contador_semis[equipo] += 1

    for equipo in resultado["equipos_final"]:

        contador_final[equipo] += 1

    contador_campeon[
        resultado["campeon"]
    ] += 1

equipos = sorted(
    selecciones["team"].unique()
)

probabilidades = []

for equipo in equipos:

    probabilidades.append({

        "team": equipo,

        "16avos":
            contador_16avos[equipo]
            / n_simulaciones * 100,

        "Octavos":
            contador_octavos[equipo]
            / n_simulaciones * 100,

        "Cuartos":
            contador_cuartos[equipo]
            / n_simulaciones * 100,

        "Semifinal":
            contador_semis[equipo]
            / n_simulaciones * 100,

        "Final":
            contador_final[equipo]
            / n_simulaciones * 100,

        "Campeon":
            contador_campeon[equipo]
            / n_simulaciones * 100
    })

probabilidades = pd.DataFrame(
    probabilidades
)

probabilidades = probabilidades.sort_values(
    "Campeon",
    ascending=False
)

probabilidades.to_csv(
    "../resultados/probabilidades_mundial_50.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV guardado correctamente.")