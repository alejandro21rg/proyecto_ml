import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    "MENÚ",
    [
        "Inicio",
        "Equipos",
        "Comparar Selecciones",
        "Simular Partido",
        "Simular Mundial",
        "Probabilidades"
    ]
)

# --------------------------------------------------
# INICIO
# --------------------------------------------------

if pagina == "Inicio":

    st.markdown(
        """
        <div class='main-title'>
        SIMULADOR MUNDIAL 2026
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='subtitle'>
        Aprendizaje automático 
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<br>", unsafe_allow_html=True)

    st.header(
        "Grupos del Mundial 2026"
    )

    grupos_visual = {
        "Grupo A": ["México","República Checa","Irán","Curazao"],
        "Grupo B": ["Suiza","Canadá","Austria","RD Congo"],
        "Grupo C": ["Marruecos","Brasil","Corea del Sur","Nueva Caledonia"],
        "Grupo D": ["Turquía","Paraguay","Australia","Honduras"],
        "Grupo E": ["Ecuador","Costa de Marfil","Alemania","EAU"],
        "Grupo F": ["Japón","Países Bajos","Túnez","Irak"],
        "Grupo G": ["Nueva Zelanda","Egipto","Bélgica","Panamá"],
        "Grupo H": ["España","Uruguay","Argelia","Guatemala"],
        "Grupo I": ["Senegal","Francia","Noruega","Venezuela"],
        "Grupo J": ["Argentina","Croacia","Nigeria","Jamaica"],
        "Grupo K": ["Inglaterra","Colombia","Serbia","Sudáfrica"],
        "Grupo L": ["Portugal","Dinamarca","Estados Unidos","Costa Rica"]
    }

    columnas = st.columns(3)

    contador = 0

    for grupo, equipos in grupos_visual.items():

        with columnas[contador % 3]:

            st.markdown(
                f"""
                <div class="card">
                <h3>{grupo}</h3>
                {'<br>'.join(equipos)}
                </div>
                """,
                unsafe_allow_html=True
            )

        contador += 1

# --------------------------------------------------
# EQUIPOS
# --------------------------------------------------

elif pagina == "Equipos":

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
# COMPARAR
# --------------------------------------------------

elif pagina == "Comparar Selecciones":

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

    comparacion = pd.DataFrame({

        equipo1: [

            int(fila1["rank"]),
            round(fila1["elo"], 0),
            round(fila1["total_points"], 2)

        ],

        equipo2: [

            int(fila2["rank"]),
            round(fila2["elo"], 0),
            round(fila2["total_points"], 2)

        ]

    },

    index=[

        "Ranking FIFA",
        "ELO",
        "Puntos FIFA"

    ])

    st.subheader(
        "Comparación de selecciones"
    )

    st.dataframe(
        comparacion,
        use_container_width=True
    )

    st.subheader(
        "Comparación visual"
    )

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    metricas = [

        "Ranking FIFA",
        "ELO",
        "Puntos FIFA"

    ]

    valores1 = [

        fila1["rank"],
        fila1["elo"],
        fila1["total_points"]

    ]

    valores2 = [

        fila2["rank"],
        fila2["elo"],
        fila2["total_points"]

    ]

    x = range(
        len(metricas)
    )

    ax.bar(

        [i - 0.2 for i in x],

        valores1,

        width=0.4,

        label=equipo1

    )

    ax.bar(

        [i + 0.2 for i in x],

        valores2,

        width=0.4,

        label=equipo2

    )

    ax.set_xticks(
        list(x)
    )

    ax.set_xticklabels(
        metricas
    )

    ax.legend()

    st.pyplot(
        fig
    )

    st.subheader(
        "Resumen"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Ranking FIFA",
            int(fila1["rank"])
        )

        st.metric(
            "ELO",
            round(fila1["elo"], 0)
        )

    with col2:

        st.metric(
            "Ranking FIFA",
            int(fila2["rank"])
        )

        st.metric(
            "ELO",
            round(fila2["elo"], 0)
        )

    st.info(
        "Más adelante añadiremos enfrentamientos históricos, goles marcados, goles recibidos y competiciones."
    )

# --------------------------------------------------
# SIMULAR PARTIDO
# --------------------------------------------------

elif pagina == "Simular Partido":

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

    if st.button(
        "Simular partido"
    ):

        st.success(
            f"{local} vs {visitante}"
        )

        st.info(
            "Aquí conectaremos simular_partido()"
        )
# --------------------------------------------------
# MUNDIAL
# --------------------------------------------------

elif pagina == "Simular Mundial":

    st.info(
        "Aquí conectaremos simular_mundial()"
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

elif pagina == "Probabilidades":

    st.subheader(
        "Probabilidades Monte Carlo"
    )

    tabla = probabilidades.sort_values(
        "Campeon",
        ascending=False
    )

    st.dataframe(
        tabla
    )

    grafico = (
        tabla
        .head(10)
        .set_index("team")
    )

    st.bar_chart(
        grafico["Campeon"]
    )


    