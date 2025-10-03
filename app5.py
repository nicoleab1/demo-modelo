import streamlit as st
import numpy as np

def pantalla_inicio():
    """Pantalla de inicio: nombre de la organización y tipo de entidad"""
    st.title("Bienvenido a la herramienta de planificación municipal")

    # Nombre de la organización
    st.session_state.org_name = st.text_input(
        "Nombre de la organización/entidad:",
        st.session_state.org_name
    )

    # Tipo de entidad (sin espacio en blanco inicial)
    opciones_entidad = ["Local", "Autonómica", "Provincial o conjunto de municipios"]
    if not st.session_state.tipo_entidad:
        st.session_state.tipo_entidad = opciones_entidad[0]  # valor por defecto
    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        opciones_entidad,
        index=opciones_entidad.index(st.session_state.tipo_entidad)
    )

    # Prioridades
    prioridades_posibles = [
        "Agua", "Energía", "Cambio climático", "Emisiones", "Economía circular",
        "Gobernanza", "Modelo de ciudad", "Vivienda", "Movilidad sostenible",
        "Biodiversidad", "Desigualdades", "Digitalización", "Datos"
    ]
    st.session_state.prioridades = st.multiselect(
        "Selecciona las prioridades de la entidad:",
        prioridades_posibles,
        default=st.session_state.prioridades
    )

    # Botón continuar
    if st.button("Continuar ➡️"):
        # Al pasar a la siguiente pantalla, si no existen estados guardados para las prioridades, se generan
        if not st.session_state.get("prioridades_estados"):
            estados_posibles = ["verde", "amarillo", "rojo"]
            st.session_state.prioridades_estados = {
                p: np.random.choice(estados_posibles) for p in st.session_state.prioridades
            }
        st.session_state.step = 2

def pantalla_prioridades_actuales():
    """Pantalla 2: visualización de la situación actual de las prioridades"""
    st.title(f"{st.session_state.org_name} - Situación actual")

    st.subheader("Tipo de entidad: " + st.session_state.tipo_entidad)

    st.markdown("---")
    st.subheader("📊 Situación actual de las prioridades seleccionadas")

    # Descripciones y colores
    descripciones = {"verde": "Sobresaliente", "amarillo": "Satisfactorio", "rojo": "Necesita mejorar"}
    colores = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}

    # Mostrar prioridades guardadas con sus estados
    prioridades = st.session_state.prioridades
    estados = st.session_state.prioridades_estados
    n_cols = 4
    n_prioridades = len(prioridades)

    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            estado = estados.get(prioridad, "amarillo")  # valor por defecto si falta
            with cols[j]:
                st.markdown(
                    f"""
                    <div style="text-align:center; margin-bottom:10px;">
                        <div style="width:70px; height:70px; border-radius:50%; background-color:{colores[estado]}; margin:auto;"></div>
                        <p style="margin:5px 0 0 0; font-weight:bold;">{prioridad}</p>
                        <p style="margin:0; font-size:0.9em;">{descripciones[estado]}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

    st.markdown("---")
    if st.button("Continuar ➡️"):
        st.session_state.step = 3  # siguiente pantalla (ejemplo: creación del plan)

# ------------------------
# Inicialización de session_state
# ------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "org_name" not in st.session_state:
    st.session_state.org_name = ""
if "tipo_entidad" not in st.session_state:
    st.session_state.tipo_entidad = ""
if "prioridades" not in st.session_state:
    st.session_state.prioridades = []
if "prioridades_estados" not in st.session_state:
    st.session_state.prioridades_estados = {}

# ------------------------
# Control de pantallas
# ------------------------
if st.session_state.step == 1:
    pantalla_inicio()
elif st.session_state.step == 2:
    pantalla_prioridades_actuales()
