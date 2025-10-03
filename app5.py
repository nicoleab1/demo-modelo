import streamlit as st
import pandas as pd
import numpy as np

# ==========================
# Inicialización de estados
# ==========================
if "step" not in st.session_state:
    st.session_state.step = 1
if "org_name" not in st.session_state:
    st.session_state.org_name = ""
if "tipo_entidad" not in st.session_state:
    st.session_state.tipo_entidad = ""
if "prioridades" not in st.session_state:
    st.session_state.prioridades = []
if "plan" not in st.session_state:
    st.session_state.plan = {}
if "actuaciones" not in st.session_state:
    st.session_state.actuaciones = []

# Funciones de navegación
def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# ==========================
# Pantalla 1: Inicio
# ==========================
def pantalla_inicio():
    st.title("Bienvenido")

    st.session_state.org_name = st.text_input(
        "Nombre de la organización/entidad:",
        st.session_state.org_name
    )

    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        ["Local", "Autonómica", "Provincial o conjunto de municipios"],
        index=0 if not st.session_state.tipo_entidad else
        ["Local", "Autonómica", "Provincial o conjunto de municipios"].index(st.session_state.tipo_entidad)
    )

    st.session_state.prioridades = st.multiselect(
        "Selecciona las prioridades de la entidad:",
        ["Agua", "Energía", "Economía circular", "Movilidad sostenible",
         "Biodiversidad", "Gobernanza", "Desigualdades", "Datos",
         "Modelo de ciudad", "Vivienda", "Cambio climático", "Digitalización"],
        default=st.session_state.prioridades
    )

    if st.button("➡️ Ir a situación actual"):
        next_step()

# ==========================
# Pantalla 2: Situación actual
# ==========================
def pantalla_entidad():
    st.title(f"{st.session_state.org_name} - Situación actual")

    st.subheader(f"Tipo de entidad: {st.session_state.tipo_entidad}")
    st.markdown("---")

    st.subheader("📊 Situación actual de las prioridades seleccionadas")
    estados_posibles = ["verde", "amarillo", "rojo"]
    descripciones = {
        "verde": "Sobresaliente",
        "amarillo": "Satisfactorio",
        "rojo": "Necesita mejorar"
    }
    colores = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}

    prioridades = st.session_state.prioridades
    for prioridad in prioridades:
        estado = np.random.choice(estados_posibles)
        st.markdown(
            f"""
            <div style="margin:5px 0; padding:8px; border-radius:8px; background-color:{colores[estado]}33;">
                <b>{prioridad}</b>: {descripciones[estado]}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Volver a inicio"):
        prev_step()
    if col2.button("➡️ Ir a creación de plan"):
        next_step()

# ==========================
# Pantalla 3: Crear plan
# ==========================
def pantalla_crear_plan():
    st.title("Crea un nuevo plan")

    nombre_plan = st.text_input(
        "Nombre del plan:",
        st.session_state.plan.get("nombre", "")
    )
    descripcion_plan = st.text_area(
        "Descripción del plan:",
        st.session_state.plan.get("descripcion", "")
    )
    horizonte_plan = st.selectbox(
        "Horizonte temporal:",
        ["2025", "2030", "2040", "2050"],
        index=0
    )

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Volver a situación actual"):
        prev_step()
    if col2.button("➡️ Ir a actuaciones"):
        if not nombre_plan:
            st.warning("Por favor escribe el nombre del plan antes de continuar.")
        else:
            st.session_state.plan = {
                "nombre": nombre_plan,
                "descripcion": descripcion_plan,
                "horizonte": horizonte_plan
            }
            next_step()

# ==========================
# Pantalla 4: Actuaciones
# ==========================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    nombre_act = st.text_input("Nombre de la actuación:")
    areas = st.multiselect("Áreas relacionadas:", st.session_state.prioridades)
    tags_sel = st.multiselect("Selecciona tags (ejemplo):", ["Tag1", "Tag2", "Tag3"])

    esfuerzo = st.slider("Esfuerzo", 0, 100, 50)
    importancia = st.slider("Importancia", 0, 100, 50)
    escala = st.slider("Escala", 0, 100, 50)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Volver a plan"):
        prev_step()
    if col2.button("Guardar actuación"):
        if not nombre_act:
            st.warning("Introduce un nombre para la actuación.")
        else:
            st.session_state.actuaciones.append({
                "nombre": nombre_act,
                "areas": areas,
                "tags": tags_sel,
                "esfuerzo": esfuerzo,
                "importancia": importancia,
                "escala": escala
            })
            st.success(f"Actuación '{nombre_act}' guardada.")

    if st.session_state.actuaciones:
        st.subheader("Actuaciones registradas")
        st.write(pd.
