import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# Inicialización de estado
# ==============================
if "step" not in st.session_state:
    st.session_state.step = 1
if "org_name" not in st.session_state:
    st.session_state.org_name = ""
if "entidad" not in st.session_state:
    st.session_state.entidad = ""
if "prioridades" not in st.session_state:
    st.session_state.prioridades = []
if "plan" not in st.session_state:
    st.session_state.plan = {}
if "actuaciones" not in st.session_state:
    st.session_state.actuaciones = []

# ==============================
# Funciones para navegación
# ==============================
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# ==============================
# Pantalla 1 - Inicio
# ==============================
def pantalla_inicio():
    st.title("Bienvenido al simulador de impacto")
    st.write("Por favor, completa la información inicial:")

    org_name = st.text_input("Nombre de la entidad:", st.session_state.org_name)
    entidad = st.selectbox("Tipo de entidad:", ["Local", "Autonómica", "Provincial o conjunto de municipios"], index=0)
    prioridades = st.multiselect(
        "Selecciona las prioridades de la entidad:",
        ["Agua", "Energía", "Cambio climático", "Emisiones", "Economía circular", "Gobernanza de datos", "Modelo de ciudad", "Vivienda", "Movilidad sostenible", "Biodiversidad", "Reducción de desigualdades"],
        default=st.session_state.prioridades
    )

    if st.button("Continuar ➡️") and org_name and entidad:
        st.session_state.org_name = org_name
        st.session_state.entidad = entidad
        st.session_state.prioridades = prioridades
        next_step()

# ==============================
# Pantalla 2 - Datos de la entidad
# ==============================
def pantalla_entidad():
    st.title(f"Entidad: {st.session_state.org_name}")
    st.subheader("Datos del municipio (mockup)")
    st.write("📍 Ubicación: Comunidad de Madrid")
    st.write("👥 Población: 118,000 habitantes (Alcobendas)")
    st.write("🌍 Región: Zona Norte de Madrid")

    st.subheader("Situación actual de prioridades")
    # Colores de ejemplo
    colores = {"Agua": "green", "Energía": "red", "Economía circular": "yellow",
               "Movilidad sostenible": "green", "Biodiversidad": "red",
               "Gobernanza de datos": "yellow", "Reducción de desigualdades": "green"}

    for pr in st.session_state.prioridades:
        color = colores.get(pr, "gray")
        st.markdown(f"**{pr}**: <span style='color:{color}'>●</span>", unsafe_allow_html=True)

    if st.button("Crea un plan para insertar actuaciones ➡️"):
        next_step()

# ==============================
# Pantalla 3 - Creación de plan
# ==============================
def pantalla_plan():
    st.title("Creación de plan estratégico")
    plan_name = st.text_input("Nombre del plan:")
    descripcion = st.text_area("Descripción del plan:")
    horizonte = st.selectbox("Horizonte temporal:", ["2025", "2030", "2040", "2050"])

    if st.button("Guardar plan y añadir actuaciones ➡️") and plan_name:
        st.session_state.plan = {
            "nombre": plan_name,
            "descripcion": descripcion,
            "horizonte": horizonte
        }
        next_step()

    if st.button("⬅️ Atrás"):
        prev_step()

# ==============================
# Pantalla 4 - Actuaciones
# ==============================
def pantalla_actuaciones():
    st.title("Añadir actuación")

    nombre_act = st.text_input("Nombre de la actuación:")
    areas = st.multiselect("Áreas relacionadas:", st.session_state.prioridades)

    tags = []
    if areas:
        # Mockup de tags
        for a in areas:
            tags.extend([f"{a}_tag1", f"{a}_tag2"])
    tags_sel = st.multiselect("Selecciona los tags activados:", tags)

    esfuerzo = st.slider("Esfuerzo (0=pequeño presupuesto, 100=gran presupuesto)", 0, 100, 50)
    importancia = st.slider("Importancia estratégica (0=baja, 100=alta)", 0, 100, 50)
    escala = st.slider("Escala geográfica (0=local, 100=toda la entidad)", 0, 100, 50)

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

    if col2.button("Simula el impacto ➡️"):
        next_step()

    if st.button("⬅️ Atrás"):
        prev_step()

    if st.session_state.actuaciones:
        st.subheader("Actuaciones registradas")
        st.write(pd.DataFrame(st.session_state.actuaciones))

# ==============================
# Pantalla 5 - Dashboard resumen
# ==============================
def pantalla_dashboard():
    st.title(f"{st.session_state.org_name}")

    st.subheader("🎯 Impacto del plan")
    # Valor total de impacto del plan (mockup)
    progreso = np.random.randint(50, 100)  # 0-100%
    
    # Gráfico de anillo
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [progreso, 100 - progreso],
        colors=["#4CAF50", "#E0E0E0"],
        startangle=90,
        counterclock=False,
        wedgeprops={"width":0.3, "edgecolor":"white"}
    )
    ax.text(0, 0, f"{progreso}%", ha="center", va="center", fontsize=24, fontweight="bold")
    ax.set_aspect("equal")
    
    st.pyplot(fig)

    st.subheader("📊 Prioridades: situación actual vs impacto esperado")
    st.write("Situación actual: colores verde/amarillo/rojo (mockup)")
    st.write("Impacto esperado: variación simulada (mockup)")

    st.subheader("🔍 Detalle por áreas")
    area = st.selectbox("Selecciona un área para ver detalles:", categorias)
    if area:
        st.write(f"Proyectos relacionados con {area}:")
        for act in st.session_state.actuaciones:
            if area in act["areas"]:
                st.write(f"- {act['nombre']} (KPIs simulados, ODS relacionados, etc.)")

    st.subheader("📌 KPIs más impactados (mockup)")
    kpis = ["KPI_Aire", "KPI_Movilidad", "KPI_Desigualdades"]
    intensidades = np.random.randn(len(kpis))
    df_kpi = pd.DataFrame({"KPI": kpis, "Impacto": intensidades})
    st.bar_chart(df_kpi.set_index("KPI"))

    kpi_sel = st.selectbox("Elige un KPI para ver proyectos relacionados:", kpis)
    if kpi_sel:
        st.write(f"Proyectos que más afectan a {kpi_sel}:")
        for act in st.session_state.actuaciones:
            st.write(f"- {act['nombre']}")

    if st.button("⬅️ Atrás"):
        prev_step()

# ==============================
# Flujo principal
# ==============================
if st.session_state.step == 1:
    pantalla_inicio()
elif st.session_state.step == 2:
    pantalla_entidad()
elif st.session_state.step == 3:
    pantalla_plan()
elif st.session_state.step == 4:
    pantalla_actuaciones()
elif st.session_state.step == 5:
    pantalla_dashboard()
