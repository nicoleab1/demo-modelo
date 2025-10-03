import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ======================
# Función principal (tuya)
# ======================
def calcular_costes_y_impactos(G, df_todos, caso="CASO_ALC", alpha_loops=0.3, alpha_paths=0.3, epsilon=1e-6):
    entry_nodes = [n for n, d in G.nodes(data=True) if d.get(caso) == "MED"]
    kpi_nodes = [n for n, d in G.nodes(data=True) if d.get("TIPO") == "KPI"]

    df_todos = df_todos.copy()
    df_todos["FuerzaLoop"] = np.exp(-alpha_loops * df_todos["Longitud"])

    registros = []
    for _, row in df_todos.iterrows():
        signo = "+"
        if "Balancing" in row["Tipo"]:
            signo = "-"
        elif "Reinforcing" in row["Tipo"]:
            signo = "+"
        for nodo in row["Nodos"].split(" → "):
            registros.append({"Nodo": nodo, "Signo": signo, "FuerzaLoop": row["FuerzaLoop"]})
    df_expanded = pd.DataFrame(registros)

    reinforcing = df_expanded[df_expanded["Signo"] == "+"].groupby("Nodo")["FuerzaLoop"].sum()
    balancing = df_expanded[df_expanded["Signo"] == "-"].groupby("Nodo")["FuerzaLoop"].sum()
    S_el = reinforcing.reindex(G.nodes(), fill_value=0) - balancing.reindex(G.nodes(), fill_value=0)

    min_S, max_S = S_el.min(), S_el.max()
    if max_S != min_S:
        w_el = epsilon + ((S_el - min_S) * (1 - epsilon)) / (max_S - min_S)
    else:
        w_el = S_el.copy()
    nx.set_node_attributes(G, w_el.to_dict(), "peso_normalizado")

    caminos_costes = []
    for entry in entry_nodes:
        for kpi in kpi_nodes:
            for path in nx.all_simple_paths(G, source=entry, target=kpi, cutoff=8):
                L = len(path)
                pesos = [w_el[node] for node in path]
                coste = sum([w * np.exp(-alpha_paths * (L - 1)) for w in pesos])
                signo_path = np.prod([G[u][v].get("signo", 1) for u, v in zip(path[:-1], path[1:])])
                caminos_costes.append({
                    "entry": entry,
                    "kpi": kpi,
                    "path": " → ".join([G.nodes[n]["ID_EL"] for n in path]),
                    "longitud": L,
                    "coste": coste,
                    "signo": signo_path
                })
    df_caminos = pd.DataFrame(caminos_costes)

    if not df_caminos.empty:
        min_C, max_C = df_caminos["coste"].min(), df_caminos["coste"].max()
        df_caminos["coste_normalizado"] = epsilon + ((df_caminos["coste"] - min_C) * (1 - epsilon)) / (max_C - min_C)
    else:
        df_caminos["coste_normalizado"] = []

    intensidades = {}
    for kpi in kpi_nodes:
        P_p = df_caminos[(df_caminos["kpi"] == kpi) & (df_caminos["signo"] == 1)]["coste_normalizado"].sum()
        N_p = df_caminos[(df_caminos["kpi"] == kpi) & (df_caminos["signo"] == -1)]["coste_normalizado"].sum()
        objetivo = G.nodes[kpi].get("OBJETIVO_KPI", 1)
        try:
            objetivo = float(objetivo)
        except:
            objetivo = 1
        intensidades[kpi] = objetivo * (P_p - N_p)

    registros_sdg = []
    for kpi, intensidad in intensidades.items():
        sdgs = str(G.nodes[kpi].get("SDG_TARGET", "")).split(";")
        for sdg in sdgs:
            sdg = sdg.strip()
            if sdg != "" and sdg.upper() != "NO":
                registros_sdg.append({"SDG_TARGET": sdg, "Intensidad": intensidad})
    df_sdg = pd.DataFrame(registros_sdg)
    df_sdg_agg = df_sdg.groupby("SDG_TARGET")["Intensidad"].agg(["sum", "mean"]).reset_index()
    df_sdg_agg.rename(columns={"sum": "Intensidad_Suma", "mean": "Intensidad_Media"}, inplace=True)

    return S_el, w_el, df_caminos, intensidades, df_sdg_agg

# ======================
# 2. Cargar datos
# ======================
df_cat = pd.read_csv("df_categorias_nombres.csv")
df_rel = pd.read_csv("df_relacion_nombres.csv")
df_todos = pd.read_csv("df_todos.csv")

# Grafo
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
# 3. Interfaz Streamlit
# ======================
st.title("Demo 4 - Resultados reales con el modelo de causalidad")

proyecto = st.text_input("Introduce el nombre de la actuación")

if proyecto:
    st.write(f"**Proyecto ingresado:** {proyecto}")

    # Ejecutar cálculos reales para CASO_ALC
    S_el, w_el, df_caminos, intensidades, df_sdg = calcular_costes_y_impactos(G, df_todos, caso="CASO_ALC")

    # Mostrar tabla de intensidades KPI
    df_intensidades = pd.DataFrame(list(intensidades.items()), columns=["KPI", "Intensidad"])
    st.write("### Intensidades por KPI")
    st.dataframe(df_intensidades.sort_values("Intensidad", ascending=False).head(20))

    # Mostrar tabla de SDG
    st.write("### Intensidades agregadas por SDG")
    st.table(df_sdg)

    # Mostrar un gráfico de ejemplo de caminos hacia un KPI
    if not df_caminos.empty:
        st.write("### Caminos hacia un KPI (ejemplo)")
        ejemplo_kpi = df_caminos["kpi"].iloc[0]
        st.write(f"Mostrando caminos hacia: **{ejemplo_kpi}**")
        sub_paths = df_caminos[df_caminos["kpi"] == ejemplo_kpi].head(3)
        for _, row in sub_paths.iterrows():
            st.write(f"Path: {row['path']} | Coste: {row['coste_normalizado']:.3f}")

