
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Strategic Radar Maroc")
st.subheader("Plateforme multisectorielle d'intelligence économique")

st.info(
    "Prototype académique : les chiffres de démonstration "
    "sont fictifs et ne représentent pas des données réelles."
)

SECTEURS = {
    "Agriculture": {
        "indicateur": "Coût des intrants",
        "unite": "%",
        "valeurs": [100, 102, 101, 106, 114],
        "risque": "Hausse du coût des intrants"
    },
    "Industrie": {
        "indicateur": "Coût de production",
        "unite": "%",
        "valeurs": [100, 101, 103, 105, 112],
        "risque": "Pression sur les coûts de production"
    },
    "Commerce international": {
        "indicateur": "Coût des importations",
        "unite": "%",
        "valeurs": [100, 104, 103, 108, 116],
        "risque": "Hausse potentielle des coûts d'importation"
    },
    "Énergie": {
        "indicateur": "Indice du coût énergétique",
        "unite": "%",
        "valeurs": [100, 103, 105, 104, 115],
        "risque": "Volatilité du coût énergétique"
    },
    "Finance & banque": {
        "indicateur": "Indice de risque financier",
        "unite": "points",
        "valeurs": [35, 38, 37, 44, 52],
        "risque": "Augmentation de l'indice de risque"
    },
    "Transport & logistique": {
        "indicateur": "Coût logistique",
        "unite": "%",
        "valeurs": [100, 102, 105, 111, 118],
        "risque": "Hausse des coûts logistiques"
    },
    "Tourisme": {
        "indicateur": "Indice de demande touristique",
        "unite": "points",
        "valeurs": [100, 104, 107, 105, 113],
        "risque": "Variation de la demande touristique"
    },
    "Technologie & numérique": {
        "indicateur": "Indice de coûts numériques",
        "unite": "%",
        "valeurs": [100, 99, 103, 105, 109],
        "risque": "Évolution des coûts numériques"
    },
    "Immobilier & construction": {
        "indicateur": "Indice du coût de construction",
        "unite": "%",
        "valeurs": [100, 102, 106, 109, 117],
        "risque": "Hausse du coût de construction"
    },
    "Commerce & distribution": {
        "indicateur": "Indice des coûts commerciaux",
        "unite": "%",
        "valeurs": [100, 101, 104, 107, 113],
        "risque": "Pression sur les marges commerciales"
    }
}

st.sidebar.header("⚙️ Paramètres")

secteur = st.sidebar.selectbox(
    "Choisir un secteur",
    list(SECTEURS.keys())
)

seuil = st.sidebar.slider(
    "Seuil d'alerte (%)",
    min_value=1,
    max_value=25,
    value=5
)

scenario = SECTEURS[secteur]
valeurs = scenario["valeurs"]

df = pd.DataFrame({
    "Période": ["P1", "P2", "P3", "P4", "P5"],
    scenario["indicateur"]: valeurs
})

variation = (valeurs[-1] - valeurs[-2]) / valeurs[-2] * 100
variation_totale = (valeurs[-1] - valeurs[0]) / valeurs[0] * 100

st.header(f"📊 Tableau de bord — {secteur}")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Dernière valeur",
    f"{valeurs[-1]} {scenario['unite']}"
)

c2.metric(
    "Variation récente",
    f"{variation:+.2f}%",
    f"{valeurs[-1] - valeurs[-2]:+.1f}"
)

c3.metric(
    "Variation depuis P1",
    f"{variation_totale:+.2f}%"
)

st.subheader(f"Évolution : {scenario['indicateur']}")

fig = px.line(
    df,
    x="Période",
    y=scenario["indicateur"],
    markers=True,
    title=f"Évolution de l'indicateur — {secteur}"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Période",
    yaxis_title=scenario["unite"]
)

st.plotly_chart(fig, use_container_width=True)

if variation >= seuil:
    st.error(
        f"🚨 ALERTE : hausse de {variation:.2f}%. "
        f"{scenario['risque']}. "
        "Vérifier les données et rechercher les causes."
    )
else:
    st.success(
        "✅ Aucun dépassement du seuil d'alerte "
        "pour la dernière variation."
    )

st.subheader("🧠 Diagnostic stratégique")

if variation > 0:
    st.write(
        f"L'indicateur augmente dans le secteur {secteur}. "
        "Cette évolution mérite une vérification des données, "
        "des causes possibles et de ses conséquences économiques."
    )
elif variation < 0:
    st.write(
        f"L'indicateur diminue dans le secteur {secteur}. "
        "Il convient de vérifier si cette évolution est durable."
    )
else:
    st.write("L'indicateur reste stable entre les deux dernières périodes.")

st.caption(
    "Le seuil est un paramètre de démonstration, "
    "pas une norme universelle. Une alerte signale une variation, "
    "pas nécessairement une crise."
)

st.divider()

st.header("🔬 Simulateur de décision")

impact = st.slider(
    "Variation hypothétique supplémentaire (%)",
    min_value=-20,
    max_value=30,
    value=10
)

valeur_simulee = valeurs[-1] * (1 + impact / 100)

st.metric(
    "Valeur simulée à la prochaine période",
    f"{valeur_simulee:.2f} {scenario['unite']}",
    f"{impact:+.1f}%"
)

if impact > 0:
    st.warning(
        "Scénario : l'indicateur augmente. "
        "Étudier les mesures de réduction des coûts "
        "ou de diversification selon le contexte."
    )
elif impact < 0:
    st.info(
        "Scénario : l'indicateur diminue. "
        "Vérifier les hypothèses avant toute décision."
    )
else:
    st.info("Scénario : l'indicateur reste à son niveau actuel.")

st.subheader("📋 Données utilisées")
st.dataframe(df, use_container_width=True)

st.caption(
    "Strategic Radar Maroc — prototype académique. "
    "Données fictives : aucune connexion aux marchés en temps réel."
)
