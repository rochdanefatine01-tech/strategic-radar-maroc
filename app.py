import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Strategic Radar Maroc")
st.subheader("Radar intelligent de veille économique")

st.info(
    "Prototype de démonstration : "
    "les données ci-dessous sont fictives."
)

st.sidebar.header("Paramètres")
seuil = st.sidebar.slider(
    "Seuil d'alerte (%)", 1, 20, 5
)

df = pd.DataFrame({
    "Période": [
        "P1", "P2", "P3", "P4", "P5"
    ],
    "Prix du blé": [
        200, 205, 203, 215, 230
    ]
})

prix_initial = df["Prix du blé"].iloc[-2]
prix_final = df["Prix du blé"].iloc[-1]
variation = (
    (prix_final - prix_initial) / prix_initial
) * 100

c1, c2, c3 = st.columns(3)

c1.metric("Dernier prix fictif", prix_final)
c2.metric("Variation récente", f"{variation:.2f}%")
c3.metric("Seuil d'alerte", f"{seuil}%")

st.subheader("Évolution du prix du blé")
fig = px.line(
    df,
    x="Période",
    y="Prix du blé",
    markers=True,
    title="Évolution des prix par période"
)
st.plotly_chart(fig, use_container_width=True)

if variation > seuil:
    st.error(
        f"🚨 ALERTE STRATÉGIQUE : hausse de "
        f"{variation:.2f}%. Vérifier les coûts d'importation."
    )
else:
    st.success("Aucune alerte selon le seuil choisi.")

st.subheader("Données utilisées")
st.dataframe(df, use_container_width=True)

st.caption(
    "Projet académique — données fictives, "
    "sans connexion à des marchés en temps réel."
)
