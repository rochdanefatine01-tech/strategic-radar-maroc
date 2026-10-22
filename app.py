import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Strategic Radar Maroc", page_icon="📡", layout="wide")

# Données fictives pour démonstration académique uniquement.
SECTEURS = {
    "Agriculture": {"indicateur":"Indice du coût des intrants","valeurs":[100,102,101,106,114],"unite":"indice (base 100)","sens":"cout","solutions":[("Diversifier les fournisseurs","Comparer plusieurs fournisseurs pour réduire la dépendance."),("Optimiser les achats","Regrouper les commandes si cela est pertinent et négocier les conditions."),("Améliorer l'efficacité des intrants","Analyser les consommations et limiter les pertes.") ]},
    "Industrie": {"indicateur":"Indice du coût de production","valeurs":[100,101,103,105,112],"unite":"indice (base 100)","sens":"cout","solutions":[("Auditer les coûts","Identifier les postes responsables de la hausse."),("Réduire les pertes de production","Examiner les rebuts, arrêts et consommations excessives."),("Planifier la maintenance","Limiter les arrêts imprévus et les coûts associés.") ]},
    "Commerce international": {"indicateur":"Indice du coût des importations","valeurs":[100,104,103,108,116],"unite":"indice (base 100)","sens":"cout","solutions":[("Diversifier les fournisseurs","Comparer les marchés selon coût, délais et risques."),("Surveiller le taux de change","Évaluer l'exposition aux devises et définir des seuils d'alerte."),("Simuler les coûts d'approvisionnement","Tester l'effet de variations de prix, fret et change.") ]},
    "Énergie": {"indicateur":"Indice du coût énergétique","valeurs":[100,103,105,104,115],"unite":"indice (base 100)","sens":"cout","solutions":[("Réaliser un audit énergétique","Identifier les équipements les plus consommateurs."),("Améliorer l'efficacité énergétique","Prioriser les actions à gain mesurable."),("Simuler plusieurs budgets","Comparer des scénarios de prix bas, central et élevé.") ]},
    "Finance & banque": {"indicateur":"Indice de risque financier","valeurs":[35,38,37,44,52],"unite":"points","sens":"risque","solutions":[("Renforcer le suivi des risques","Suivre les indicateurs de liquidité, crédit et concentration."),("Tester des scénarios de stress","Évaluer la sensibilité à plusieurs chocs hypothétiques."),("Diversifier les expositions","Examiner les concentrations par client, secteur ou devise.") ]},
    "Transport & logistique": {"indicateur":"Indice du coût logistique","valeurs":[100,102,105,111,118],"unite":"indice (base 100)","sens":"cout","solutions":[("Optimiser les itinéraires","Comparer trajets, délais et coûts."),("Comparer les prestataires","Évaluer le coût total et la fiabilité."),("Prévoir des alternatives","Identifier des itinéraires ou prestataires de secours.") ]},
    "Tourisme": {"indicateur":"Indice de demande touristique","valeurs":[100,104,107,105,113],"unite":"indice (base 100)","sens":"demande","solutions":[("Adapter les offres à la saisonnalité","Ajuster les offres aux tendances observées."),("Diversifier les marchés émetteurs","Réduire la dépendance à un seul segment."),("Suivre les réservations","Comparer réservations, annulations et demandes.") ]},
    "Technologie & numérique": {"indicateur":"Indice des coûts numériques","valeurs":[100,99,103,105,109],"unite":"indice (base 100)","sens":"cout","solutions":[("Auditer les abonnements","Repérer les outils redondants ou sous-utilisés."),("Comparer les fournisseurs","Comparer coûts, sécurité et conditions de sortie."),("Suivre les dépenses cloud","Mettre en place des indicateurs de consommation.") ]},
    "Immobilier & construction": {"indicateur":"Indice du coût de construction","valeurs":[100,102,106,109,117],"unite":"indice (base 100)","sens":"cout","solutions":[("Actualiser les estimations","Réviser les hypothèses de prix et d'incertitude."),("Comparer les fournisseurs","Comparer coût total, qualité et délais."),("Prévoir une marge de contingence","Tester plusieurs scénarios budgétaires.") ]},
    "Commerce & distribution": {"indicateur":"Indice des coûts commerciaux","valeurs":[100,101,104,107,113],"unite":"indice (base 100)","sens":"cout","solutions":[("Analyser les marges","Identifier les produits les plus exposés."),("Optimiser les stocks","Réduire ruptures et surstocks à partir des données."),("Négocier les conditions fournisseurs","Comparer prix, délais, volumes et paiement.") ]}
}

st.title("📡 Strategic Radar Maroc")
st.subheader("Plateforme multisectorielle d'intelligence économique")
st.info("Prototype académique : les chiffres affichés sont fictifs. Ils illustrent le fonctionnement et ne décrivent pas la situation réelle d'un secteur.")

with st.sidebar:
    st.header("⚙️ Paramètres de veille")
    secteur = st.selectbox("Choisir un secteur", list(SECTEURS))
    seuil = st.slider("Seuil d'alerte sur la variation récente (%)", 1, 25, 5)
s = SECTEURS[secteur]
v = s["valeurs"]
variation = (v[-1] - v[-2]) / v[-2] * 100
total = (v[-1] - v[0]) / v[0] * 100
df = pd.DataFrame({"Période":["P1","P2","P3","P4","P5"], s["indicateur"]:v})
df["Variation (%)"] = df[s["indicateur"]].pct_change() * 100

st.header(f"📊 Tableau de bord — {secteur}")
a,b,c = st.columns(3)
a.metric("Dernière valeur", f"{v[-1]} {s['unite']}")
b.metric("Variation récente", f"{variation:+.2f}%")
c.metric("Variation depuis P1", f"{total:+.2f}%")

fig = px.line(df, x="Période", y=s["indicateur"], markers=True, title=f"Évolution — {secteur}")
fig.update_layout(template="plotly_white", yaxis_title=s["unite"])
st.plotly_chart(fig, use_container_width=True)

if s["sens"] == "demande":
    if variation <= -seuil:
        st.warning(f"⚠️ ALERTE : baisse de la demande de {abs(variation):.2f}%. Vérifier la saisonnalité et les segments concernés.")
    elif variation >= seuil:
        st.success(f"📈 Hausse de la demande de {variation:.2f}% : signal potentiellement favorable à confirmer.")
    else:
        st.info("La variation de la demande reste sous le seuil choisi.")
else:
    if variation >= seuil:
        st.error(f"🚨 ALERTE : hausse de {variation:.2f}% de l'indicateur. Vérifier les données et rechercher les causes.")
    else:
        st.success("✅ La variation récente ne dépasse pas le seuil d'alerte choisi.")

st.header("🧠 Diagnostic stratégique")
if s["sens"] == "demande":
    st.write("L'indicateur représente la demande : une hausse peut être favorable, mais doit être vérifiée avec des données de fréquentation, de réservations ou de chiffre d'affaires.")
elif variation >= seuil:
    st.write(f"L'indicateur augmente au-delà du seuil choisi. Cela peut signaler une pression sur le secteur « {secteur} », mais ne prouve pas à lui seul une crise.")
elif variation > 0:
    st.write(f"L'indicateur augmente de {variation:.2f}%. Surveiller la tendance et vérifier les facteurs explicatifs.")
else:
    st.write("L'indicateur baisse ou reste stable. Vérifier si l'évolution est durable et significative.")
st.caption("Une alerte détecte une variation, pas automatiquement sa cause. Les seuils doivent être adaptés au contexte réel.")

st.divider()
st.header("💡 Solutions & recommandations stratégiques")
solutions = s["solutions"]
choix = st.selectbox("Choisir une solution à examiner", [x[0] for x in solutions])
st.subheader(choix)
st.write(next(x[1] for x in solutions if x[0] == choix))
st.markdown("**Plan d'action indicatif**")
st.write("1. Vérifier la donnée et confirmer le signal.  2. Mesurer l'exposition de l'organisation.  3. Comparer plusieurs options réalistes.  4. Définir un indicateur de suivi et réévaluer la décision.")
st.caption("Les recommandations sont des pistes de réflexion, pas des décisions automatiques.")

st.divider()
st.header("🔬 Simulateur de décision")
st.write("Les paramètres suivants sont hypothétiques et ne constituent pas une prévision.")
impact = st.slider("Variation hypothétique avant action (%)", -20, 30, 10)
effet = st.slider("Effet hypothétique de la solution (%)", 0, 30, 5)
sans_action = v[-1] * (1 + impact / 100)
if s["sens"] == "demande":
    avec_action = sans_action * (1 + effet / 100)
    st.caption("Pour la demande, l'effet de la solution est simulé comme une hausse éventuelle de l'indicateur.")
else:
    avec_action = sans_action * (1 - effet / 100)
    st.caption("Pour les coûts et risques, l'effet de la solution est simulé comme une réduction hypothétique de l'indicateur.")
x,y,z = st.columns(3)
x.metric("Valeur actuelle", f"{v[-1]:.2f}")
y.metric("Scénario sans action", f"{sans_action:.2f}", f"{impact:+.1f}%")
z.metric("Scénario avec action", f"{avec_action:.2f}", f"{effet:+.1f}%")
sim = pd.DataFrame({"Scénario":["Valeur actuelle","Sans action","Avec action"],"Valeur":[v[-1],sans_action,avec_action]})
st.plotly_chart(px.bar(sim, x="Scénario", y="Valeur", title="Comparaison des scénarios").update_layout(template="plotly_white", showlegend=False), use_container_width=True)

st.subheader("📋 Données utilisées")
st.dataframe(df, use_container_width=True, hide_index=True)
st.download_button("⬇️ Télécharger les données de démonstration (CSV)", df.to_csv(index=False).encode("utf-8"), file_name="strategic_radar_demo.csv", mime="text/csv")
st.caption("Strategic Radar Maroc — données fictives, sans connexion aux marchés en temps réel. Les résultats simulés ne garantissent aucun gain.")