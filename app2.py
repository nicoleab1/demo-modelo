import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ======================
# 1. Cargar datos
# ======================
df_cat = pd.read_csv("df_categorias_nombres.csv")
df_rel = pd.read_csv("df_relacion_nombres.csv")

# Crear grafo
G = nx.DiGraph()
for _, row in df_cat.iterrows():
    G.add_node(
        row["ELEMENTO"],
        ID_EL=row["ID_EL"],
        TIPO=row["TIPO"],
        BLOQUE=row["BLOQUE"],
        LOOP=row["LOOP"],
        CASO_ALC=row["CASO_ALC"],
        CASO_MNN=row["CASO_MNN"],
        SDG_TARGET=row["SDG_TARGET"],
        OBJETIVO_KPI=row["OBJETIVO_KPI"],
    )

for _, row in df_rel.iterrows():
    G.add_edge(row["EL1"], row["EL2"], signo=row["REL"])

# ======================
# 2. Interfaz
# ======================
st.title("Demo 2 - Evaluación de actuaciones con tabla de KPIs")

proyecto = st.text_input("Introduce el nombre de la actuación")

if proyecto:
    st.write(f"**Proyecto ingresado:** {proyecto}")

    # 🔹 Mockup de sugerencia de tags
    tags_sugeridos = ["Movilidad", "Calidad del aire", "Energía"]
    tags_elegidos = st.multiselect("Selecciona los tags relevantes:", tags_sugeridos)

    if tags_elegidos:
        st.subheader("Resultados del proyecto")

        # 🔹 Puntuación (mockup)
        puntuacion = 88.7
        st.metric("Puntuación normalizada", f"{puntuacion}/100")

        # 🔹 Mockup de KPIs impactados
        # (En el futuro, esto vendrá de tu grafo con cálculos reales)
        kpis = [
            {"KPI": "Reducción emisiones CO2", "Impacto": "+", "SDG": "13.2"},
            {"KPI": "Mejora calidad aire", "Impacto": "+", "SDG": "11.6"},
            {"KPI": "Tráfico urbano", "Impacto": "-", "SDG": "11.2"},
        ]

        df_kpis = pd.DataFrame(kpis)
        st.write("### KPIs impactados")
        st.table(df_kpis)

        # 🔹 Visualización simple de la red (subgrafo de ejemplo)
        st.write("### Red de impactos (mockup)")
        sub_nodes = list(df_kpis["KPI"]) + tags_elegidos
        subG = G.subgraph([n for n in G.nodes if n in sub_nodes])

        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.spring_layout(subG, seed=42)
        nx.draw(subG, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=8, ax=ax)
        st.pyplot(fig)

