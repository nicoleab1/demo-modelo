import streamlit as st
import pandas as pd

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

# Navegación
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1


# ==========================
# Pantalla 1: Inicio
# ==========================
def pantalla_inicio():
    st.title("Bienvenido 👋")

    st.session_state.org_name = st.text_input("Nombre de la organización:", st.session_state.org_name)

    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        ["", "Local", "Autonómica", "Provincial o conjunto de municipios"],
        index=0 if not st.session_state.tipo_entidad else ["", "Local", "Autonómica", "Provincial o conjunto de municipios"].index(st.session_state.tipo_entidad)
    )

    prioridades = st.multiselect(
        "Selecciona las prioridades de tu entidad:",
        ["Agua", "Energía", "Economía circular", "Movilidad sostenible",
         "Biodiversidad", "Gobernanza", "Reducción de desigualdades", "Datos", "Modelo de ciudad", "Vivienda", "Cambio climático", "Digitalización"],
        default=st.session_state.prioridades
    )
    st.session_state.prioridades = prioridades

    if st.button("➡️ Ir a situación actual"):
        next_step()


# ==========================
# Pantalla 2: Situación actual
# ==========================
def pantalla_entidad():
    st.title(f"{st.session_state.org_name} - Situación actual")

    st.subheader("📍 Datos del municipio")
    st.write("Población: 118,000 habitantes (mockup)")
    st.write("Región: Comunidad de Madrid (mockup)")

    st.subheader("📊 Situación de prioridades")
    col1, col2, col3 = st.columns(3)

    estados = {
        "verde": "Sobresaliente",
        "amarillo": "En desarrollo",
        "rojo": "Necesita mejorar"
    }

    import random
    for i, prioridad in enumerate(st.session_state.prioridades):
        color = random.choice(["verde", "amarillo", "rojo"])
        texto = estados[color]

        if i % 3 == 0:
            with col1:
                st.markdown(f"### ● {prioridad}\n**{texto}**")
        elif i % 3 == 1:
            with col2:
                st.markdown(f"### ● {prioridad}\n**{texto}**")
        else:
            with col3:
                st.markdown(f"### ● {prioridad}\n**{texto}**")

    if st.button("⬅️ Volver a inicio"):
        prev_step()
    if st.button("➡️ Ir a creación de plan"):
        next_step()


# ==========================
# Pantalla 3: Crear plan
# ==========================
def pantalla_crear_plan():
    st.title("Crea un nuevo plan")

    # Inputs del plan
    nombre_plan = st.text_input("Nombre del plan:", st.session_state.plan.get("nombre", ""))
    descripcion_plan = st.text_area("Descripción del plan:", st.session_state.plan.get("descripcion", ""))
    horizonte_plan = st.text_input("Horizonte temporal:", st.session_state.plan.get("horizonte", ""))

    if st.button("➡️ Ir a actuaciones"):
        if not nombre_plan:
            st.warning("Por favor escribe el nombre del plan antes de continuar.")
        else:
            st.session_state.plan["nombre"] = nombre_plan
            st.session_state.plan["descripcion"] = descripcion_plan
            st.session_state.plan["horizonte"] = horizonte_plan
            next_step()

    if st.button("⬅️ Volver a prioridades"):
        prev_step()


# ==========================
# Pantalla 4: Añadir actuaciones
# ==========================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    with st.form("form_actuacion", clear_on_submit=True):
        nombre_act = st.text_input("Nombre de la actuación:")
        areas = st.multiselect("Áreas relacionadas:", st.session_state.prioridades)

        # Tags dinámicos según áreas
        TAGS_POR_AREA = {
            "Agua": ["Riego de zonas verdes", "Agua recuperada y regenerada", "Cantidad total de agua"],
            "Energía": ["Consumo final de combustibles", "Producción local EE.RR", "Consumo final de energía eléctrica",
                        "Eficiencia energética de las viviendas", "Medidas de ahorro y eficiencia energética", "Alumbrado urbano"],
            "Cambio climático": ["Inundaciones", "Seguridad"],
            "Economía circular": ["Eficiencia de la estructura de residuos", "IoT (smart cities)", "Control y vigilancia del tráfico",
                                   "Infraestructura para electrificación de flotas", "Movilidad compartida", "Economía colaborativa"],
            "Economía": ["Actividad comercial, ocio, hostelería y turismo", "Adecuación del perfil de la población a la demanda de empleo"],
            "Gobernanza": ["Calidad de los planes y políticas", "Acceso a información", "Ineficiencias internas",
                           "Capacitación y formación", "Colaboración efectiva", "Participación efectiva"],
            "Datos": ["Accesibilidad de la información pública", "Calidad de la información y datos", "Capacidad tecnológica y disponibilidad de medios"],
            "Modelo de ciudad": ["Regeneración y rehabilitación", "Calidad de las infraestructuras", "Calidad de la planificación urbana"],
            "Vivienda": ["Acceso a alquiler", "Acceso a compra", "Parque de vivienda disponible"],
            "Movilidad sostenible": ["Viario peatonal", "Viario bicicletas", "Infraestructura transporte público", "Aparcamiento", "Caminabilidad"],
            "Biodiversidad": ["Gestión y protección de zonas naturales"],
            "Desigualdades": ["Desigualdades educativas", "Desigualdades espaciales", "Población vulnerable", "Carga de cuidado"],
            "Digitalización": ["Brecha digital", "Barreras a la accesibilidad universal"]
        }

        tags = []
        for a in areas:
            tags.extend(TAGS_POR_AREA.get(a, []))
        tags_sel = st.multiselect("Selecciona los tags activados:", tags)

        esfuerzo = st.slider("Esfuerzo (0=pequeño presupuesto, 100=gran presupuesto)", 0, 100, 50)
        importancia = st.slider("Importancia estratégica (0=baja, 100=alta)", 0, 100, 50)
        escala = st.slider("Escala geográfica (0=local, 100=toda la entidad)", 0, 100, 50)

        submitted = st.form_submit_button("💾 Guardar actuación")
        if submitted:
            st.session_state.actuaciones.append({
                "nombre": nombre_act,
                "areas": areas,
                "tags": tags_sel,
                "esfuerzo": esfuerzo,
                "importancia": importancia,
                "escala": escala
            })
            st.success(f"Actuación '{nombre_act}' añadida.")

    if st.button("➡️ Simular impacto"):
        next_step()
    if st.button("⬅️ Volver a plan"):
        prev_step()

    if st.session_state.actuaciones:
        st.subheader("Actuaciones guardadas")
        st.write(pd.DataFrame(st.session_state.actuaciones))


# ==========================
# Renderizar según paso
# ==========================
if st.session_state.step == 1:
    pantalla_inicio()
elif st.session_state.step == 2:
    pantalla_entidad()
elif st.session_state.step == 3:
    pantalla_crear_plan()
elif st.session_state.step == 4:
    pantalla_actuaciones()
