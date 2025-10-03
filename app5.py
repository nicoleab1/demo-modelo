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
    st.title("Bienvenido")

    st.session_state.org_name = st.text_input("Nombre de la organización/entidad:", st.session_state.org_name)

    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        ["", "Local", "Autonómica", "Provincial o conjunto de municipios"],
        index=0 if not st.session_state.tipo_entidad else ["", "Local", "Autonómica", "Provincial o conjunto de municipios"].index(st.session_state.tipo_entidad)
    )

    prioridades = st.multiselect(
        "Selecciona las prioridades de la entidad:",
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

    st.subheader("Tipo de entidad: " + st.session_state.tipo_entidad)
    st.markdown("---")
    st.subheader("Datos del municipio")
    st.write("Población: 118,000 habitantes")
    st.write("Región: Comunidad de Madrid")

    st.subheader("📊 Situación actual de las prioridades seleccionadas")
    # Mockup: estado aleatorio de cada prioridad (más adelante usar datos reales)
    estados_posibles = ["verde", "amarillo", "rojo"]
    descripciones = {"verde": "Sobresaliente", "amarillo": "Satisfactorio", "rojo": "Necesita mejorar"}
    colores = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}

    # Columnas por fila
    n_cols = 4
    prioridades = st.session_state.prioridades
    n_prioridades = len(prioridades)
    
    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            estado = np.random.choice(estados_posibles)  # mockup, reemplazar con datos reales
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
    if st.button("Volver a inicio"):
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
    horizonte_plan = st.selectbox("Horizonte temporal:", ["2025", "2030", "2040", "2050"])

    if st.button("➡️ Ir a actuaciones"):
        if not nombre_plan:
            st.warning("Por favor escribe el nombre del plan antes de continuar.")
        else:
            st.session_state.plan["nombre"] = nombre_plan
            st.session_state.plan["descripcion"] = descripcion_plan
            st.session_state.plan["horizonte"] = horizonte_plan
            next_step()

    if st.button("Volver a prioridades"):
        prev_step()


# ==========================
# Pantalla 4: Actuaciones
# ==========================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    #Nombre de la actuación. editado de app5.2:
    nombre_act = st.text_input("Nombre de la actuación:")
    areas = st.multiselect("Áreas relacionadas:", st.session_state.prioridades)

    # Tags dinámicos según áreas
    tags_por_area = {
        "Agua": ["Riego de zonas verdes", "Agua recuperada y regenerada", "Cantidad total de agua"],
        "Energía": ["Consumo final de combustibles", "Producción local EE.RR", "Consumo final de energía eléctrica", 
                    "Eficiencia energética de las viviendas", "Medidas de ahorro y eficiencia energética", "Alumbrado urbano"],
        "Cambio climático": ["Inundaciones", "Seguridad"],
        "Economía circular": ["Eficiencia de la estructura y logística de la recogida separativa de residuos",
                              "IoT (smart cities)", "Control y vigilancia del tráfico", 
                              "Infraestructura para el soporte de la electrificación de las flotas",
                              "Movilidad compartida", "Economía colaborativa"],
        "Economía": ["Actividad comercial, de ocio, hostelería y turismo (servicios)",
                     "Adecuación del perfil de la población disponible a la demanda de empleo"],
        "Gobernanza": ["Calidad de los planes y políticas", "Acceso a información", "Ineficiencias internas",
                       "Capacitación y formación para el personal público", "Colaboración efectiva",
                       "Participación efectiva"],
        "Datos": ["Accesibilidad de la información pública", "Calidad de la información y datos puestos a disposición de la población",
                  "Capacidad tecnológica y disponibilidad de medios de la entidad"],
        "Modelo de ciudad": ["Regeneración y rehabilitación", "Calidad de las infraestructuras", "Calidad de la planificación urbana",
                             "Patrimonio cultural", "Suelo destinado a usos comerciales", "Suelo destinado a usos residenciales",
                             "Distribución equilibrada de los usos del suelo", "Selección de especies adaptadas a las condiciones climáticas",
                             "Servicios socio-culturales", "Planificación para la biodiversidad urbana", "Uso servicios culturales",
                             "Mantenimiento de los equipamientos e infraestructuras", "Estado del parque edificatorio público",
                             "Especies autóctonas", "Cubiertas verdes y jardines verticales", "Huertos urbanos",
                             "Zonas deportivas", "Espacios públicos de ocio", "Calidad del espacio público",
                             "Suelo destinado a zonas verdes y espacios abiertos"],
        "Vivienda": ["Población con acceso al alquiler", "Población con acceso a compra", "Parque de vivienda disponible"],
        "Movilidad sostenible": ["Viario por el que pueden circular peatones", "Viario para la circulación de bicicletas",
                                 "Infraestructuras de transporte público colectivo", "Aparcamiento",
                                 "Separación de las IF para el tráfico motorizado de otros modos de transporte",
                                 "Caminabilidad", "Accesibilidad física a carriles bici",
                                 "Desplazamientos en otros modos de micromovilidad",
                                 "Accesibilidad física a transporte público", "Interconexión entre zonas",
                                 "Facilidad de desplazamiento en transporte público", "Limitación del tráfico en núcleos urbanos",
                                 "Seguridad vial", "Nodos multimodales", "Parque de vivienda disponible para alquiler"],
        "Biodiversidad": ["Gestión adecuada y protección de las zonas naturales"],
        "Desigualdades": ["Desigualdades educativas", "Desigualdades espaciales", "Desigualdades en cuidados",
                          "Desigualdades culturales", "Población en situación económica vulnerable", "Carga del cuidado"],
        "Digitalización": ["Brecha digital", "Barreras a la accesibilidad universal"]
    }

    # Construir lista de tags según áreas seleccionadas
    tags = []
    for area in areas:
        tags.extend(tags_por_area.get(area, []))
        
    # Selección de tags activados
    tags_sel = st.multiselect("Selecciona los tags activados:", tags)

    # Sliders
    esfuerzo = st.slider("Esfuerzo (0=pequeño presupuesto, 100=gran presupuesto)", 0, 100, 50)
    importancia = st.slider("Importancia estratégica (0=baja, 100=alta)", 0, 100, 50)
    escala = st.slider("Escala geográfica (0=local, 100=toda la entidad)", 0, 100, 50)

    # Botones
    col1, col2 = st.columns(2)
    if col1.button("Añadir actuación"):
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
    if st.button("Volver a plan"):
        prev_step()

     # Mostrar actuaciones registradas
    if st.session_state.actuaciones:
        st.subheader("Actuaciones registradas")
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
