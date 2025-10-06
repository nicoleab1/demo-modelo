
import streamlit as st
import numpy as np
import pandas as pd

# ======================
# PANTALLA 1: INICIO
# ======================
def pantalla_inicio():
    """Pantalla de inicio: nombre de la organización y tipo de entidad"""
    st.title("Bienvenido a la herramienta de planificación municipal 1")

    # Nombre de la organización
    st.session_state.org_name = st.text_input("Nombre de la organización/entidad:")

    # Tipo de entidad (sin valor en blanco)
    opciones_tipo = ["Local", "Autonómica", "Provincial o conjunto de municipios"]
    if not st.session_state.tipo_entidad:
        st.session_state.tipo_entidad = opciones_tipo[0]
    st.session_state.tipo_entidad = st.selectbox(
        "Tipo de entidad:",
        opciones_tipo,
        index=opciones_tipo.index(st.session_state.tipo_entidad)
    )

    # Prioridades (selección con un solo clic)
    prioridades_posibles = [
        "Agua", "Energía", "Cambio climático", "Emisiones", "Economía circular",
        "Gobernanza", "Modelo de ciudad", "Vivienda", "Movilidad sostenible",
        "Biodiversidad", "Desigualdades", "Digitalización", "Datos"
    ]

    # Usamos checkboxes para selección de un clic
    seleccionadas = []
    st.write("Selecciona las prioridades de la entidad:")
    cols = st.columns(4)
    for i, prioridad in enumerate(prioridades_posibles):
        if cols[i % 4].checkbox(prioridad, prioridad in st.session_state.prioridades):
            seleccionadas.append(prioridad)
    st.session_state.prioridades = seleccionadas

    # Botón continuar
    if st.button("Continuar ➡️"):
        st.session_state.step = 2


# ======================
# PANTALLA 2: SITUACIÓN ACTUAL
# ======================
def pantalla_prioridades_actuales():
    """Pantalla 2: visualización de la situación actual de las prioridades"""
    st.title(f"{st.session_state.org_name} - Situación actual")

    st.subheader("Tipo de entidad: " + st.session_state.tipo_entidad)

    st.markdown("---")
    st.subheader("📊 Situación actual de las prioridades seleccionadas")

    # Mockup de estado aleatorio
    estados_posibles = ["verde", "amarillo", "rojo"]
    descripciones = {"verde": "Sobresaliente", "amarillo": "Satisfactorio", "rojo": "Necesita mejorar"}
    colores = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}

    # Guardamos los estados aleatorios una sola vez
    if "estados_prioridades" not in st.session_state:
        st.session_state.estados_prioridades = {
            prioridad: np.random.choice(estados_posibles) for prioridad in st.session_state.prioridades
        }

    # Mostrar prioridades en cuadrícula
    n_cols = 4
    prioridades = st.session_state.prioridades
    n_prioridades = len(prioridades)
    
    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            estado = st.session_state.estados_prioridades.get(prioridad, "verde")
            with cols[j]:
                st.markdown(
                    f"""
                    <div style="text-align:center; margin-bottom:10px;">
                        <div style="width:70px; height:70px; border-radius:50%; background-color:{colores[estado]}; margin:auto;"></div>
                        <p style="margin:5px 0 0 0; font-weight:bold;">{prioridad}</p>
                        <p style="margin:0; font-size:0.9em;">{descripciones[estado]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Volver"):
        st.session_state.step = 1
    if col2.button("➡️ Crear plan"):
        st.session_state.step = 3


# ======================
# PANTALLA 3: CREAR PLAN
# ======================
def pantalla_crear_plan():
    """Pantalla 3: creación del plan"""
    st.title("Crea un nuevo plan")

    # Campos del plan
    nombre_plan = st.text_input("Nombre del plan:", st.session_state.plan.get("nombre", ""))
    descripcion_plan = st.text_area("Descripción del plan:", st.session_state.plan.get("descripcion", ""))
    horizonte_plan = st.selectbox(
        "Horizonte temporal:",
        ["2025", "2030", "2040", "2050"],
        index=0
    )

    # Botones
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Volver a prioridades"):
        st.session_state.step = 2

    if col2.button("Guardar y continuar ➡️"):
        if not nombre_plan:
            st.warning("Por favor escribe el nombre del plan antes de continuar.")
        else:
            st.session_state.plan["nombre"] = nombre_plan
            st.session_state.plan["descripcion"] = descripcion_plan
            st.session_state.plan["horizonte"] = horizonte_plan
            st.success("✅ Plan guardado correctamente.")
            st.session_state.step = 4


# ======================
# PANTALLA 4: ACTUACIONES
# ======================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    # Asegurarnos de que exista la lista de actuaciones
    if "actuaciones" not in st.session_state:
        st.session_state.actuaciones = []
    if "areas_sel" not in st.session_state:
        st.session_state.areas_sel = []
    if "tags_sel" not in st.session_state:
        st.session_state.tags_sel = []

    # Nombre de la actuación
    nombre_act = st.text_input("Nombre de la actuación:")

    # Selección de áreas
    areas = st.multiselect(
        "Áreas relacionadas:",
        st.session_state.prioridades,
        default=st.session_state.areas_sel
    )

    # Guardar la selección actual en session_state
    st.session_state.areas_sel = areas

    # Diccionario que mapea prioridades a tags
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
    tags = sorted(set(tags))

    # Selección de tags activados
    tags_sel = st.multiselect(
        "Selecciona los tags activados:",
        tags,
        default=st.session_state.tags_sel
    )
    st.session_state.tags_sel = tags_sel

    # Sliders
    esfuerzo = st.slider("Esfuerzo (0=pequeño presupuesto, 100=gran presupuesto)", 0, 100, 50)
    importancia = st.slider("Importancia estratégica (0=baja, 100=alta)", 0, 100, 50)
    escala = st.slider("Escala geográfica (0=local, 100=toda la entidad)", 0, 100, 50)

    # Botones
    col1, col2 = st.columns(2)
    if col1.button("Guardar actuación"):
        st.session_state.actuaciones.append({
            "nombre": nombre_act,
            "areas": areas,
            "tags": tags_sel,
            "esfuerzo": esfuerzo,
            "importancia": importancia,
            "escala": escala
        })
        st.success(f"Actuación '{nombre_act}' añadida.")
        # limpiar selección
        st.session_state.areas_sel = []
        st.session_state.tags_sel = []
        st.rerun()

    if col2.button("Simula el impacto ➡️"):
        st.session_state.step = st.session_state.get("step", 4) + 1

    if st.button("⬅️ Atrás"):
        st.session_state.step = max(1, st.session_state.get("step", 4) - 1)

    # Mostrar actuaciones registradas
    if st.session_state.actuaciones:
        st.subheader("Actuaciones registradas")
        st.write(pd.DataFrame(st.session_state.actuaciones))

def pantalla_dashboard():
    st.title(f"{st.session_state.org_name} - Resultados del plan")
    
    # ---------- Puntuación global ----------
    st.subheader("📈 Puntuación global del plan")
    plan_score = np.random.randint(1, 101)
    st.markdown(f"""
    <div style="display:flex; justify-content:center; align-items:center; margin-bottom:20px;">
        <svg width="150" height="150">
            <circle cx="75" cy="75" r="70" fill="#eee" />
            <circle cx="75" cy="75" r="70" fill="none" stroke="#4CAF50" stroke-width="20"
                    stroke-dasharray="{plan_score*4.4} 440" transform="rotate(-90 75 75)" />
            <text x="50%" y="50%" text-anchor="middle" dy="7" font-size="20" font-weight="bold">{plan_score}</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ---------- Situación actual por prioridades ----------
    st.subheader("📊 Situación actual por prioridades")
    colores_estado = {"verde": "#4CAF50", "amarillo": "#FFC107", "rojo": "#F44336"}
    descripciones = {"verde": "Sobresaliente", "amarillo": "Satisfactorio", "rojo": "Necesita mejorar"}
    
    prioridades = st.session_state.prioridades
    n_cols = 4
    n_prioridades = len(prioridades)
    
    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            estado = st.session_state.estados_prioridades.get(prioridad, "verde")
            with cols[j]:
                st.markdown(f"""
                <div style="text-align:center; margin-bottom:10px;">
                    <div style="width:70px; height:70px; border-radius:50%; background-color:{colores_estado[estado]}; margin:auto;"></div>
                    <p style="margin:5px 0 0 0; font-weight:bold;">{prioridad}</p>
                    <p style="margin:0; font-size:0.9em;">{descripciones[estado]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.subheader("🌟 Impactos esperados por prioridad")
    for i in range(0, n_prioridades, n_cols):
        cols = st.columns(n_cols)
        for j, prioridad in enumerate(prioridades[i:i+n_cols]):
            impacto = np.random.randint(0, 101)
            with cols[j]:
                st.markdown(f"""
                <div style="text-align:center; margin-bottom:10px;">
                    <svg width="70" height="70">
                        <circle cx="35" cy="35" r="32" fill="#eee" />
                        <circle cx="35" cy="35" r="32" fill="none" stroke="#4CAF50" stroke-width="6"
                                stroke-dasharray="{impacto*2.01} 201" transform="rotate(-90 35 35)" />
                        <text x="50%" y="50%" text-anchor="middle" dy="5" font-size="12">{impacto}</text>
                    </svg>
                    <p style="margin:2px 0 0 0; font-weight:bold;">{prioridad}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ---------- Cadenas de influencia ----------
    st.subheader("🔗 Ejemplos de cadenas de influencia (6 pasos)")
    import random
    cadenas_simuladas = []

    # Tomar las actuaciones y sus tags
    for act in st.session_state.actuaciones:
        for tag in act['tags']:
            cadena = [
                f"{act['nombre']}",
                f"Influencia sobre área: {tag}",
                f"Efecto intermedio 1",
                f"Efecto intermedio 2",
                f"Efecto intermedio 3",
                f"KPI final: {tag}"
            ]
            cadenas_simuladas.append(cadena)

    # Mostrar hasta 3 cadenas
    if cadenas_simuladas:
        for cadena in random.sample(cadenas_simuladas, min(3, len(cadenas_simuladas))):
            # Dibujar cada paso como círculo con línea de conexión
            html = '<div style="display:flex; align-items:center; justify-content:start; margin-bottom:10px;">'
            for i, paso in enumerate(cadena):
                html += f"""
                    <div style="
                        width:60px; height:60px; border-radius:50%; background-color:#4CAF50;
                        display:flex; align-items:center; justify-content:center;
                        color:white; font-size:10px; text-align:center; padding:5px; margin-right:5px;">
                        {paso}
                    </div>
                """
                if i < len(cadena) - 1:
                    html += '<div style="margin-right:5px;">→</div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay actuaciones registradas para generar cadenas de ejemplo.")
    
    # ---------- KPIs más impactados ----------
    st.markdown("---")
    st.subheader("📌 KPIs más impactados")
    if st.button("Ver KPIs más impactados"):
        if cadenas_simuladas:
            kpis = [c[-1] for c in cadenas_simuladas]
            st.write(list(set(kpis)))  # mostrar KPIs finales únicos
        else:
            st.info("No hay KPIs para mostrar.")


# ======================
# INICIALIZACIÓN DEL ESTADO
# ======================
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
if "estados_prioridades" not in st.session_state:
    st.session_state.estados_prioridades = {}
if "actuaciones" not in st.session_state:
    st.session_state.actuaciones = []


# ======================
# CONTROL DE PANTALLAS
# ======================
if st.session_state.step == 1:
    pantalla_inicio()
elif st.session_state.step == 2:
    pantalla_prioridades_actuales()
elif st.session_state.step == 3:
    pantalla_crear_plan()
elif st.session_state.step == 4:
    pantalla_actuaciones()
elif st.session_state.step == 5:
    pantalla_dashboard()  # <-- aquí llamamos al dashboard
