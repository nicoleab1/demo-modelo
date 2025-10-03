import streamlit as st
import pandas as pd
import numpy as np

# ==========================
# Inicialización session_state
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

# ==========================
# Funciones de navegación
# ==========================
def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# ==========================
# Pantalla 1: Inicio
# ==========================
def pantalla_inicio():
    st.title("Bienvenido a la herramienta de planificación municipal")

    st.session_state.org_name = st.text_input("Nombre de la organización/entidad:")

    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        ["Local", "Autonómica", "Provincial o conjunto de municipios"]
    )

    prioridades_posibles = [
        "Agua", "Energía", "Cambio climático", "Emisiones", "Economía circular",
        "Gobernanza", "Modelo de ciudad", "Vivienda", "Movilidad sostenible",
        "Biodiversidad", "Desigualdades", "Digitalización", "Datos"
    ]
    st.session_state.prioridades = st.multiselect(
        "Selecciona las prioridades de la entidad:",
        prioridades_posibles
    )

    if st.button("Continuar ➡️"):
        next_step()

# ==========================
# Pantalla 2: Prioridades actuales
# ==========================
def pantalla_prioridades_actuales():
    st.title(f"{st.session_state.org_name} - Situación actual")

    st.subheader("Tipo de entidad: " + st.session_state.tipo_entidad)

    st.markdown("---")
    st.subheader("📊 Situación actual de las prioridades seleccionadas")

    estados_posibles = ["verde", "amarillo", "rojo"]
    descripciones = {"verde": "Sobresaliente", "amarillo": "Satisfactorio", "rojo": "Necesita mejorar"}
    colores = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}

    n_cols = 4
    prioridades = st.session_state.prioridades
    n_prioridades = len(prioridades)

    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            estado = np.random.choice(estados_posibles)
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
        next_step()

# ==========================
# Pantalla 3: Crear plan
# ==========================
def pantalla_crear_plan():
    st.title("Crea un nuevo plan")
    st.session_state.plan["nombre"] = st.text_input("Nombre del plan:", st.session_state.plan.get("nombre", ""))
    st.session_state.plan["descripcion"] = st.text_area("Descripción del plan:", st.session_state.plan.get("descripcion", ""))
    st.session_state.plan["horizonte"] = st.text_input("Horizonte temporal:", st.session_state.plan.get("horizonte", ""))

    if st.button("Continuar ➡️"):
        next_step()

# ==========================
# Pantalla 4: Añadir actuaciones
# ==========================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    # Campos de actuación
    if "actuacion_tmp" not in st.session_state:
        st.session_state.actuacion_tmp = {
            "nombre": "",
            "areas": [],
            "tags": [],
            "esfuerzo": 50,
            "importancia": 50,
            "escala": 50
        }

    tmp = st.session_state.actuacion_tmp

    tmp["nombre"] = st.text_input("Nombre de la actuación:", tmp["nombre"])

    # Selección de áreas
    tmp["areas"] = st.multiselect("Áreas relacionadas:", st.session_state.prioridades, default=tmp["areas"])

    # Tags por área
    tags_por_area = {
        "Agua": ["Riego de zonas verdes", "Agua recuperada y regenerada", "Cantidad total de agua"],
        "Energía": ["Consumo final de combustibles", "Producción local EE.RR", "Consumo final de energía eléctrica", 
                    "Eficiencia energética de las viviendas", "Medidas de ahorro y eficiencia energética", "Alumbrado urbano"],
        "Cambio climático": ["Inundaciones", "Seguridad"],
        "Economía circular": ["Eficiencia de la estructura y logística de la recogida separativa de residuos",
                              "IoT (smart cities)", "Control y vigilancia del tráfico", 
                              "Infraestructura para electrificación de flotas",
                              "Movilidad compartida", "Economía colaborativa"],
        "Economía": ["Actividad comercial, de ocio, hostelería y turismo (servicios)",
                     "Adecuación del perfil de la población disponible a la demanda de empleo"],
        "Gobernanza": ["Calidad de los planes y políticas", "Acceso a información", "Ineficiencias internas",
                       "Capacitación y formación para el personal público", "Colaboración efectiva",
                       "Participación efectiva"],
        "Datos": ["Accesibilidad de la información pública", "Calidad de la información y datos disponibles",
                  "Capacidad tecnológica y medios de la entidad"],
        "Modelo de ciudad": ["Regeneración y rehabilitación", "Calidad de las infraestructuras", "Calidad de la planificación urbana"],
        "Vivienda": ["Población con acceso al alquiler", "Población con acceso a compra", "Parque de vivienda disponible"],
        "Movilidad sostenible": ["Viario para peatones", "Viario para bicicletas", "Transporte público colectivo"],
        "Biodiversidad": ["Gestión adecuada y protección de zonas naturales"],
        "Desigualdades": ["Desigualdades educativas", "Desigualdades espaciales", "Desigualdades en cuidados"],
        "Digitalización": ["Brecha digital", "Barreras a la accesibilidad universal"]
    }

    # Construir lista de tags según áreas seleccionadas
    tags = []
    for area in tmp["areas"]:
        tags.extend(tags_por_area.get(area, []))

    tmp["tags"] = st.multiselect("Selecciona los tags activados:", tags, default=tmp["tags"])

    # Sliders
    tmp["esfuerzo"] = st.slider("Esfuerzo (0=pequeño presupuesto, 100=gran presupuesto)", 0, 100, tmp["esfuerzo"])
    tmp["importancia"] = st.slider("Importancia estratégica (0=baja, 100=alta)", 0, 100, tmp["importancia"])
    tmp["escala"] = st.slider("Escala geográfica (0=local, 100=toda la entidad)", 0, 100, tmp["escala"])

    # Botón guardar
    if st.button("💾 Guardar actuación"):
        st.session_state.actuaciones.append(tmp.copy())
        st.success(f"Actuación '{tmp['nombre']}' guardada.")
        # limpiar tmp
        st.session_state.actuacion_tmp = {
            "nombre": "",
            "areas": [],
            "tags": [],
            "esfuerzo": 50,
            "importancia": 50,
            "escala": 50
        }

    # Mostrar opciones adicionales si ya hay actuaciones guardadas
    if st.session_state.actuaciones:
        st.subheader("Actuaciones registradas")
        st.write(pd.DataFrame(st.session_state.actuaciones))

        col1, col2 = st.columns(2)
        if col1.button("➕ Añadir nueva actuación"):
            # tmp ya fue limpiado al guardar, nada más se necesita
            pass
        if col2.button("Simular impacto ➡️"):
            next_step()

# ==========================
# Control de pantallas
# ==========================
if st.session_state.step == 1:
    pantalla_inicio()
elif st.session_state.step == 2:
    pantalla_prioridades_actuales()
elif st.session_state.step == 3:
    pantalla_crear_plan()
elif st.session_state.step == 4:
    pantalla_actuaciones()
