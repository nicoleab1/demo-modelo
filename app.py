import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("Demo Modelo de Causalidad - Ayuntamientos")

# --- Cargar CSVs ---
st.sidebar.header("Cargar datos (solo demo, ya pre-cargados)")
df_cat = pd.read_csv("df_categorias_nombres.csv")
df_id = pd.read_csv("df_relacion_nombres.csv")
df_todos = pd.read_csv("df_todos.csv")  # por ahora no lo usamos, pero lo cargamos

# --- Crear grafo ---
G = nx.DiGraph()
for _, row in df_cat.iterrows():
    G.add_node(row["ELEMENTO"], 
               ID_EL=row.get("ID_EL",""),
               TIPO=row.get("TIPO",""),
               BLOQUE=row.get("BLOQUE",""),
               SDG_TARGET=row.get("SDG_TARGET",""),
               OBJETIVO_KPI=row.get("OBJETIVO_KPI",""))

for _, row in df_id.iterrows():
    G.add_edge(row["EL1"], row["EL2"], signo=row.get("REL", 1))

st.sidebar.subheader("Actuación del plan")
actuacion = st.sidebar.text_input("Introduce una actuación:")

# --- Selección de tags (simulado) ---
if actuacion:
    posibles_tags = [n for n, d in G.nodes(data=True) if d["TIPO"] in ["Entrada","COND"]]
    seleccion = st.sidebar.multiselect("Selecciona los tags asociados:", posibles_tags[:20])  # limitar demo

    if seleccion:
        # --- Propagación simple ---
        impactados = set()
        for tag in seleccion:
            impactados |= nx.descendants(G, tag)

        # Filtrar solo KPIs
        kpis = [n for n in impactados if G.nodes[n]["TIPO"] == "KPI"]

        # Calcular puntuación normalizada simple
        total_kpis = len([n for n, d in G.nodes(data=True) if d["TIPO"] == "KPI"])
        puntuacion = len(kpis) / total_kpis * 100 if total_kpis > 0 else 0

        # --- Mostrar resultados ---
        st.subheader("Resultados del proyecto")
        col1, col2 = st.columns(2)
        col1.metric("Puntuación normalizada", f"{puntuacion:.1f}/100")
        col2.write("KPIs impactados:")
        col2.write(kpis)


        # --- Visualización subgrafo ---
        subG = G.subgraph(seleccion + kpis)
        fig, ax = plt.subplots(figsize=(10,6))
        nx.draw(subG, with_labels=True, node_color="skyblue", node_size=800, ax=ax)
        st.pyplot(fig)

else:
    st.write("Introduce una actuación en la barra lateral para ver resultados.")
