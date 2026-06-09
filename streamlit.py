import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Mundial 2026",
    page_icon="⚽",
    layout="wide"
)

# --------------------------------------------------
# CARGA DATOS
# --------------------------------------------------

selecciones = pd.read_csv(
    "data/processed/selecciones_mundial_2026.csv"
)

probabilidades = pd.read_csv(
    "data/processed/probabilidades_mundial.csv"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    color: white;
}

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    color: #22c55e;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
}

.card {
    background-color: rgba(
        255,
        255,
        255,
        0.08
    );

    padding: 20px;

    border-radius: 15px;

    border: 1px solid rgba(
        255,
        255,
        255,
        0.1
    );
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MENÚ
# --------------------------------------------------

pagina = st.sidebar.radio(
    "⚽ Menú",
    [
        "🏠 Inicio",
        "📊 Equipos",
        "⚔️ Comparar Selecciones",
        "🎯 Simular Partido",
        "🌎 Simular Mundial",
        "📈 Probabilidades"
    ]
)

# --------------------------------------------------
# INICIO
# --------------------------------------------------

if pagina == "🏠 Inicio":

    st.markdown(
        "<div class='main-title'>SIMULADOR MUNDIAL 2026</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Machine Learning + Monte Carlo</div>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Selecciones",
            48
        )

    with col2:
        st.metric(
            "Grupos",
            12
        )

    with col3:
        st.metric(
            "Modelo",
            "Regresión Lineal"
        )

    st.write("")
    st.write("")

    st.subheader(
        "Top favoritos según Monte Carlo"
    )

    st.dataframe(
        probabilidades
        .sort_values(
            "Campeon",
            ascending=False
        )
        .head(10)
    )

# --------------------------------------------------
# EQUIPOS
# --------------------------------------------------

elif pagina == "📊 Equipos":

    equipo = st.selectbox(
        "Selecciona equipo",
        sorted(
            selecciones["team"]
        )
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
            round(
                fila["elo"],
                0
            )
        )

    with col3:
        st.metric(
            "Puntos últimos 5",
            fila["last5_points"]
        )

    st.write("")

    st.dataframe(
        fila.to_frame()
    )

# --------------------------------------------------
# COMPARAR
# --------------------------------------------------

elif pagina == "⚔️ Comparar Selecciones":

    col1, col2 = st.columns(2)

    with col1:

        equipo1 = st.selectbox(
            "Equipo 1",
            sorted(
                selecciones["team"]
            )
        )

    with col2:

        equipo2 = st.selectbox(
            "Equipo 2",
            sorted(
                selecciones["team"]
            ),
            index=1
        )

    fila1 = selecciones[
        selecciones["team"] == equipo1
    ].iloc[0]

    fila2 = selecciones[
        selecciones["team"] == equipo2
    ].iloc[0]

    comparacion = pd.DataFrame({

        "Variable":[
            "Ranking",
            "ELO",
            "Last5 Points",
            "GF últimos 5",
            "GC últimos 5"
        ],

        equipo1:[
            fila1["rank"],
            fila1["elo"],
            fila1["last5_points"],
            fila1["last5_goals_for"],
            fila1["last5_goals_against"]
        ],

        equipo2:[
            fila2["rank"],
            fila2["elo"],
            fila2["last5_points"],
            fila2["last5_goals_for"],
            fila2["last5_goals_against"]
        ]

    })

    st.dataframe(
        comparacion
    )

# --------------------------------------------------
# SIMULAR PARTIDO
# --------------------------------------------------

elif pagina == "🎯 Simular Partido":

    st.info(
        "Conectaremos aquí tu función simular_partido()"
    )

    equipo1 = st.selectbox(
        "Local",
        sorted(
            selecciones["team"]
        )
    )

    equipo2 = st.selectbox(
        "Visitante",
        sorted(
            selecciones["team"]
        ),
        index=1
    )

    if st.button(
        "Simular"
    ):

        st.success(
            f"{equipo1} vs {equipo2}"
        )

# --------------------------------------------------
# MUNDIAL
# --------------------------------------------------

elif pagina == "🌎 Simular Mundial":

    st.info(
        "Conectaremos aquí simular_mundial()"
    )

    if st.button(
        "Simular Mundial"
    ):

        st.success(
            "Mundial simulado"
        )

# --------------------------------------------------
# PROBABILIDADES
# --------------------------------------------------

elif pagina == "📈 Probabilidades":

    st.subheader(
        "Monte Carlo"
    )

    st.dataframe(
        probabilidades
        .sort_values(
            "Campeon",
            ascending=False
        )
    )