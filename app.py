import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import numpy as np
from simular import simular_mundial
from collections import Counter, defaultdict
# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Mundial 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CARGA DATOS
# --------------------------------------------------

selecciones = pd.read_csv(
    "data/processed/selecciones_mundial_2026.csv"
)

probabilidades = pd.read_csv(
    "resultados/probabilidades_mundial_5mil.csv"
)

selecciones_modelo = pd.read_csv(
    "data/processed/selecciones_actuales_mundial.csv"
)

dataset_modelado = pd.read_csv(
    "data/processed/dataset_modelado.csv"
)

modelo = joblib.load(
"models/modelo_regresion_lineal.pkl")

scaler = joblib.load(
    "models/scaler.pkl"
)

def obtener_equipo(nombre):

    return selecciones_modelo[
        selecciones_modelo["team"] == nombre
    ].iloc[0]

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


import streamlit as st

st.set_page_config(
    page_title="Simulador Mundial 2026",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>
    section[data-testid="stSidebar"]{

    background:
    linear-gradient(
        180deg,
        #07162f,
        #0b2457
    );
}
/* ==========================
   FONDO GENERAL
========================== */

.block-container{
    padding-top: 1rem;
}

/* ==========================
   TITULO PRINCIPAL
========================== */

.main-title{

    text-align:center;

    color:#ffffff;

    font-size:55px;

    font-weight:800;

    margin-top:10px;

    margin-bottom:30px;

    text-shadow:
    0 0 15px rgba(245,197,66,.4);
}

/* ==========================
   TARJETAS DE GRUPOS
========================== */

.card{

    background:
    rgba(12,35,85,.88);

    backdrop-filter: blur(8px);

    border-radius:20px;

    padding:20px;

    border:
    1px solid rgba(255,255,255,.08);

    box-shadow:
    0 8px 25px rgba(0,0,0,.25);

    margin-bottom:20px;

    color:white;

    line-height:1.8;
}

/* ==========================
   TITULO DE CADA GRUPO
========================== */

.grupo-titulo{

    background:
    linear-gradient(
        90deg,
        #f5c542,
        #ffdd77
    );

    color:#0a1f4d;

    font-weight:800;

    padding:10px 15px;

    border-radius:10px;

    margin-bottom:15px;

    text-align:center;

    font-size:22px;

    box-shadow:
    0 3px 10px rgba(245,197,66,.35);
}

/* ==========================
   METRICAS
========================== */

[data-testid="stMetric"]{

    background:
    rgba(12,35,85,.88);

    padding:15px;

    border-radius:15px;

    border:
    1px solid rgba(255,255,255,.08);

    box-shadow:
    0 5px 15px rgba(0,0,0,.2);
}

</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# MENÚ
# --------------------------------------------------

pagina = st.sidebar.radio(
    "MENÚ",
    [
        "INICIO",
        "EQUIPOS",
        "COMPARAR SELECCIONES",
        "SIMULAR PARTIDO",
        "MUNDIAL COMPLETO",
        "SIMULAR MUNDIAL"
    ]
)

# --------------------------------------------------
# INICIO
# --------------------------------------------------
if pagina == "INICIO":
    import base64

    with open("imagenes/estadio_fondo.png", "rb") as f:
        estadio = base64.b64encode(f.read()).decode()

    st.markdown(f"""
<style>

.stApp {{

    background:
    linear-gradient(
        rgba(0,15,50,0.82),
        rgba(0,15,50,0.90)
    ),
    url("data:image/png;base64,{estadio}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)

    hero1, hero2 = st.columns([3,2])

    with hero1:

        st.markdown("""
    <div class='main-title' style='text-align:left; margin-top:50px;'>

    SIMULADOR<br>
    MUNDIAL 2026

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='
        color:white;
        font-size:22px;
        margin-top:20px;
        margin-bottom:30px;
    '>

    Simula partidos, compara selecciones y descubre
    qué selección tiene más probabilidades de levantar
    la Copa del Mundo.

    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("Selecciones", 48)

    with c2:
        st.metric("Grupos", 12)

    with c3:
        st.metric("Partidos", 104)

    with hero2:
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image(
        "imagenes/copa_mundo.png",
        width=400
    )

    st.markdown("<br>", unsafe_allow_html=True)

    grupos_visual = {
        "Grupo A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
        "Grupo B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
        "Grupo C": ["Brazil", "Morocco", "Haiti", "Scotland"],
        "Grupo D": ["United States", "Paraguay", "Australia", "Turkey"],
        "Grupo E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
        "Grupo F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
        "Grupo G": ["Belgium", "Egypt", "Iran", "New Zealand"],
        "Grupo H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
        "Grupo I": ["France", "Senegal", "Iraq", "Norway"],
        "Grupo J": ["Argentina", "Algeria", "Austria", "Jordan"],
        "Grupo K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
        "Grupo L": ["England", "Croatia", "Ghana", "Panama"]
    }

    columnas = st.columns(3)

    contador = 0

    for grupo, equipos in grupos_visual.items():

        with columnas[contador % 3]:

            st.markdown(
                f"""
                <div class="card">
                     <div class="grupo-titulo">
                     {grupo}
                </div>     
                {'<br>'.join(equipos)}
                </div>
                """,
                unsafe_allow_html=True
            )

        contador += 1

# --------------------------------------------------
# EQUIPOS
# --------------------------------------------------

elif pagina == "EQUIPOS":

    equipo = st.selectbox(
        "Selecciona equipo",
        sorted(selecciones["team"].tolist())
    )

    fila = selecciones[
        selecciones["team"] == equipo
    ].iloc[0]

    

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        "Ranking FIFA",
        int(fila["rank"])
    )

    with col2:
        st.metric(
        "ELO",
        int(fila["elo"])
    )

    with col3:
        st.metric(
        "Puntos FIFA",
        round(fila["total_points"], 0)
    )

    st.subheader("Variables del modelo")

    st.dataframe(
    fila.to_frame()
    )

# --------------------------------------------------
# COMPARAR SELECCIONES
# --------------------------------------------------

elif pagina == "COMPARAR SELECCIONES":

    col1, col2 = st.columns(2)

    with col1:

        equipo1 = st.selectbox(
            "Equipo 1",
            sorted(selecciones["team"].tolist()),
            key="equipo1"
        )

    with col2:

        equipo2 = st.selectbox(
            "Equipo 2",
            sorted(selecciones["team"].tolist()),
            key="equipo2"
        )

    fila1 = selecciones[
        selecciones["team"] == equipo1
    ].iloc[0]

    fila2 = selecciones[
        selecciones["team"] == equipo2
    ].iloc[0]

    # ------------------------------------------
    # ESTADO ACTUAL
    # ------------------------------------------

    st.subheader(
        "Estado actual"
    )

    comparacion = pd.DataFrame({

        equipo1: [

            int(fila1["rank"]),
            round(fila1["elo"], 0),
            round(fila1["total_points"], 0)

        ],

        equipo2: [

            int(fila2["rank"]),
            round(fila2["elo"], 0),
            round(fila2["total_points"], 0)

        ]

    },

    index=[

        "Ranking FIFA",
        "ELO",
        "Puntos FIFA"

    ])

    st.dataframe(
        comparacion,
        use_container_width=True
    )

    # ------------------------------------------
    # HISTORIAL ENTRE SELECCIONES
    # ------------------------------------------

    historial = dataset_modelado[

        (
            (dataset_modelado["home_team"] == equipo1)
            &
            (dataset_modelado["away_team"] == equipo2)
        )

        |

        (
            (dataset_modelado["home_team"] == equipo2)
            &
            (dataset_modelado["away_team"] == equipo1)
        )

    ].copy()

    st.subheader(
        "Historial entre selecciones"
    )

    if len(historial) > 0:

        victorias_equipo1 = 0
        victorias_equipo2 = 0
        empates = 0

        for _, fila in historial.iterrows():

            if fila["home_score"] > fila["away_score"]:

                ganador = fila["home_team"]

            elif fila["away_score"] > fila["home_score"]:

                ganador = fila["away_team"]

            else:

                ganador = "Empate"

            if ganador == equipo1:

                victorias_equipo1 += 1

            elif ganador == equipo2:

                victorias_equipo2 += 1

            else:

                empates += 1

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Partidos",
                len(historial)
            )

        with col2:

            st.metric(
                equipo1,
                victorias_equipo1
            )

        with col3:

            st.metric(
                "Empates",
                empates
            )

        with col4:

            st.metric(
                equipo2,
                victorias_equipo2
            )

        # ------------------------------------------
        # COMPETICIONES
        # ------------------------------------------

        st.subheader(
            "Competiciones disputadas"
        )

        competiciones = (

            historial["tournament"]
            .value_counts()
            .reset_index()

        )

        competiciones.columns = [
            "Competición",
            "Partidos"
        ]

        st.dataframe(
            competiciones,
            use_container_width=True
        )

        # ------------------------------------------
        # ÚLTIMOS ENFRENTAMIENTOS
        # ------------------------------------------

        st.subheader(
            "Últimos enfrentamientos"
        )

        historial = historial.sort_values(
            "date",
            ascending=False
        )

        mostrar = historial[

            [
                "date",
                "home_team",
                "away_team",
                "home_score",
                "away_score",
                "tournament"
            ]

        ].head(10)

        st.dataframe(
            mostrar,
            use_container_width=True
        )

    else:

        st.info(
            "No hay enfrentamientos registrados entre estas selecciones."
        )

    # ------------------------------------------
    # ANÁLISIS RÁPIDO
    # ------------------------------------------

    st.subheader(
        "Análisis rápido"
    )

    mejor_elo = (
        equipo1
        if fila1["elo"] > fila2["elo"]
        else equipo2
    )

    mejor_rank = (
        equipo1
        if fila1["rank"] < fila2["rank"]
        else equipo2
    )

    st.write(
        f"Mejor ELO: **{mejor_elo}**"
    )

    st.write(
        f"Mejor Ranking FIFA: **{mejor_rank}**"
    )

    if fila1["elo"] > fila2["elo"] and fila1["rank"] < fila2["rank"]:

        st.success(
            f"{equipo1} llega mejor posicionado según los indicadores actuales."
        )

    elif fila2["elo"] > fila1["elo"] and fila2["rank"] < fila1["rank"]:

        st.success(
            f"{equipo2} llega mejor posicionado según los indicadores actuales."
        )

    else:

        st.info(
            "Los indicadores están muy equilibrados entre ambas selecciones."
        )

# --------------------------------------------------
# MUNDIAL COMPLETO
# --------------------------------------------------

elif pagina == "MUNDIAL COMPLETO":

    st.header(
        "Mundial Completo"
    )

    if st.button(
        "Simular Mundial Completo"
    ):

        resultado = simular_mundial()

        resultados = resultado["resultados"]

        final = resultados[104]

        st.success(
            f"Campeón: {resultado['campeon']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Finalista",
                final["local"]
            )

        with col2:

            st.metric(
                "Resultado",
                f"{final['goles_local']}-{final['goles_visitante']}"
            )

        with col3:

            st.metric(
                "Finalista",
                final["visitante"]
            )

        st.markdown("---")

        col16, col8, col4, col2, col1f = st.columns(5)

        # ----------------------------------
        # DIECISEISAVOS
        # ----------------------------------

        with col16:

            st.subheader("16avos")

            for partido in range(73, 89):

                p = resultados[partido]

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1e293b;
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:10px;
                        border-left:5px solid #22c55e;
                    ">
                    <b>{p['ganador']}</b><br>
                    {p['local']} {p['goles_local']} - {p['goles_visitante']} {p['visitante']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------
        # OCTAVOS
        # ----------------------------------

        with col8:

            st.subheader("Octavos")

            for partido in range(89, 97):

                p = resultados[partido]

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1e293b;
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:20px;
                        border-left:5px solid #22c55e;
                    ">
                    <b>{p['ganador']}</b><br>
                    {p['local']} {p['goles_local']} - {p['goles_visitante']} {p['visitante']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------
        # CUARTOS
        # ----------------------------------

        with col4:

            st.subheader("Cuartos")

            for partido in range(97, 101):

                p = resultados[partido]

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1e293b;
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:40px;
                        border-left:5px solid #22c55e;
                    ">
                    <b>{p['ganador']}</b><br>
                    {p['local']} {p['goles_local']} - {p['goles_visitante']} {p['visitante']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------
        # SEMIFINALES
        # ----------------------------------

        with col2:

            st.subheader("Semis")

            for partido in [101, 102]:

                p = resultados[partido]

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1e293b;
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:80px;
                        border-left:5px solid #22c55e;
                    ">
                    <b>{p['ganador']}</b><br>
                    {p['local']} {p['goles_local']} - {p['goles_visitante']} {p['visitante']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------
        # FINAL
        # ----------------------------------

        with col1f:

            st.subheader("Final")

            st.markdown(
                f"""
                <div style="
                    background-color:#14532d;
                    padding:15px;
                    border-radius:12px;
                    margin-top:120px;
                    border:2px solid gold;
                ">
                <b>{final['ganador']}</b><br><br>
                {final['local']} {final['goles_local']} - {final['goles_visitante']} {final['visitante']}
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------------------------------
# SIMULAR PARTIDO
# --------------------------------------------------

elif pagina == "SIMULAR PARTIDO":

    def probabilidades_partido(
        equipo_local,
        equipo_visitante,
        n_simulaciones=10
    ):

        local_gana = 0
        empate = 0
        visitante_gana = 0

        for _ in range(n_simulaciones):

            resultado = simular_partido(
                equipo_local,
                equipo_visitante
            )

            if resultado > 0.5:
                local_gana += 1

            elif resultado < -0.5:
                visitante_gana += 1

            else:
                empate += 1

        return {
            "local": local_gana / n_simulaciones * 100,
            "empate": empate / n_simulaciones * 100,
            "visitante": visitante_gana / n_simulaciones * 100
        }

    local = st.selectbox(
        "Local",
        sorted(selecciones["team"].tolist()),
        key="local"
    )

    visitante = st.selectbox(
        "Visitante",
        sorted(selecciones["team"].tolist()),
        key="visitante"
    )

    if st.button("Simular partido"):

        probs = probabilidades_partido(
            local,
            visitante,
            500
        )

        st.success(
            f"{local} vs {visitante}"
        )

        ganador = max(
            probs,
            key=probs.get
        )

        if ganador == "local":

            st.subheader(
                f"Favorito: {local}"
            )

        elif ganador == "visitante":

            st.subheader(
                f"Favorito: {visitante}"
            )

        else:

            st.subheader(
                "Partido muy igualado"
            )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                f"Victoria {local}",
                f"{probs['local']:.1f}%"
            )

        with col2:

            st.metric(
                "Empate",
                f"{probs['empate']:.1f}%"
            )

        with col3:

            st.metric(
                f"Victoria {visitante}",
                f"{probs['visitante']:.1f}%"
            )

# --------------------------------------------------
# SIMULAR MUNDIAL
# --------------------------------------------------

elif pagina == "SIMULAR MUNDIAL":

    st.header(
        "Simulación Mundial 2026"
    )

    num_sim = st.slider(
        "Número de simulaciones",
        min_value=1,
        max_value=100,
        value=10
    )

    if st.button(
        "Simular Mundial"
    ):

        contador_16avos = defaultdict(int)
        contador_octavos = defaultdict(int)
        contador_cuartos = defaultdict(int)
        contador_semis = defaultdict(int)
        contador_final = defaultdict(int)
        contador_campeon = defaultdict(int)

        progreso = st.progress(0)

        for i in range(num_sim):

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

            progreso.progress(
                (i + 1) / num_sim
            )

        equipos = sorted(
            selecciones["team"].unique()
        )

        tabla = []

        for equipo in equipos:

            tabla.append({

                "Equipo":
                    equipo,

                "16avos":
                    round(
                        contador_16avos[equipo]
                        / num_sim * 100,
                        1
                    ),

                "Octavos":
                    round(
                        contador_octavos[equipo]
                        / num_sim * 100,
                        1
                    ),

                "Cuartos":
                    round(
                        contador_cuartos[equipo]
                        / num_sim * 100,
                        1
                    ),

                "Semifinal":
                    round(
                        contador_semis[equipo]
                        / num_sim * 100,
                        1
                    ),

                "Final":
                    round(
                        contador_final[equipo]
                        / num_sim * 100,
                        1
                    ),

                "Campeón":
                    round(
                        contador_campeon[equipo]
                        / num_sim * 100,
                        1
                    )

            })

        tabla = pd.DataFrame(
            tabla
        )

        tabla = tabla.sort_values(
            "Campeón",
            ascending=False
        )

        st.subheader(
            "Probabilidad de alcanzar cada ronda"
        )

        st.dataframe(
            tabla,
            use_container_width=True
        )

        

        st.subheader(
            "Favoritos"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "1º Favorito",
                tabla.iloc[0]["Equipo"]
            )

        with col2:

            st.metric(
                "2º Favorito",
                tabla.iloc[1]["Equipo"]
            )

        with col3:

            st.metric(
                "3º Favorito",
                tabla.iloc[2]["Equipo"]
            )

        st.success(
            f"Se han simulado {num_sim} Mundiales"
        )




    