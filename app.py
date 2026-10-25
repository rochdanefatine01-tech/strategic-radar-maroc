import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Visual identity ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#eaf0ff; --muted:#9aa9c5; --panel:#111d35; --line:rgba(160,184,225,.16); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 80% 0%, rgba(34,211,238,.12), transparent 28%),
    radial-gradient(circle at 0% 18%, rgba(99,102,241,.18), transparent 30%),
    #081225;
  color:var(--ink);
}
[data-testid="stHeader"] { background:rgba(8,18,37,.8); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101d36,#0b1428); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#eaf0ff; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1440px; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:#f4f7ff; }
.hero {
  padding:30px 30px 26px; border:1px solid rgba(125,211,252,.22); border-radius:24px;
  background:linear-gradient(115deg,rgba(22,39,71,.97),rgba(12,27,51,.9) 58%,rgba(19,54,78,.8));
  box-shadow:0 20px 60px rgba(0,0,0,.2); margin-bottom:22px; position:relative; overflow:hidden;
}
.hero:after { content:""; position:absolute; width:240px;height:240px;right:-55px;top:-95px;border:1px solid rgba(103,232,249,.22);border-radius:50%; box-shadow:0 0 0 28px rgba(103,232,249,.025),0 0 0 58px rgba(103,232,249,.025); }
.eyebrow { color:#67e8f9; text-transform:uppercase; letter-spacing:.17em; font-size:.74rem; font-weight:700; }
.hero-title { font-family:'Manrope',sans-serif; font-weight:800; font-size:clamp(2rem,4vw,3.45rem); line-height:1.04; color:#f7fbff; margin:.55rem 0 .75rem; }
.hero-sub { max-width:760px; color:#b7c6df; font-size:1.02rem; line-height:1.7; }
.pill { display:inline-block; border:1px solid rgba(103,232,249,.3); background:rgba(34,211,238,.08); color:#a5f3fc; padding:6px 11px; border-radius:999px; font-size:.76rem; margin:12px 6px 0 0; }
.section-kicker { color:#67e8f9; text-transform:uppercase; letter-spacing:.13em; font-size:.72rem; font-weight:700; margin:1rem 0 .35rem; }
.metric-card { background:linear-gradient(145deg,rgba(20,35,63,.98),rgba(13,25,46,.98)); border:1px solid var(--line); border-radius:18px; padding:18px 19px; min-height:130px; }
.metric-label { color:#9fb0cd; font-size:.82rem; margin-bottom:9px; }
.metric-value { color:#f4f7ff; font-family:'Manrope',sans-serif; font-size:1.85rem; font-weight:800; letter-spacing:-.04em; }
.metric-note { color:#a5f3fc; font-size:.78rem; margin-top:5px; }
.panel { background:rgba(15,28,51,.78); border:1px solid var(--line); border-radius:20px; padding:20px 22px; }
.small-muted { color:#9aa9c5; font-size:.84rem; }
div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label { color:#cbd8ee; }
.stButton>button, .stDownloadButton>button { border-radius:11px; border:1px solid rgba(103,232,249,.3); background:linear-gradient(90deg,#0e7490,#2563eb); color:white; font-weight:700; }
.stButton>button:hover, .stDownloadButton>button:hover { border-color:#67e8f9; color:white; }
div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
div[data-testid="stAlert"] { border-radius:14px; }
div[data-testid="stAlert"] p { color:#edf6ff !important; }
div[data-testid="stAlert"] svg { color:#67e8f9 !important; }
div[data-testid="stAlert"][kind="info"] { background:rgba(25,78,125,.34); border:1px solid rgba(103,232,249,.24); }
div[data-testid="stAlert"][kind="warning"] { background:rgba(124,45,68,.28); border:1px solid rgba(251,113,133,.35); }
div[data-testid="stAlert"][kind="success"] { background:rgba(6,95,70,.25); border:1px solid rgba(52,211,153,.3); }
hr { border-color:var(--line); }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Demonstration data (clearly labelled) ----------
DATA = {
    "Agriculture": {"indicator":"Indice du coût des intrants", "values":[100,102,101,106,114], "unit":"indice (base 100)", "meaning":"Une hausse peut signaler une pression sur les coûts de production."},
    "Industrie": {"indicator":"Indice d'activité industrielle", "values":[100,101,103,105,112], "unit":"indice (base 100)", "meaning":"Une progression peut refléter une activité plus soutenue, à confirmer par des données officielles."},
    "Commerce international": {"indicator":"Indice des échanges", "values":[100,104,103,108,116], "unit":"indice (base 100)", "meaning":"Le mouvement mérite d'être comparé aux importations, exportations et soldes commerciaux."},
    "Énergie": {"indicator":"Indice de pression énergétique", "values":[100,103,105,104,115], "unit":"indice (base 100)", "meaning":"Une variation rapide peut modifier les coûts des entreprises et des ménages."},
    "Finance & banque": {"indicator":"Indice de volatilité simulé", "values":[35,38,37,44,52], "unit":"indice simulé", "meaning":"Une hausse de volatilité invite à examiner le contexte et l'exposition au risque."},
    "Transport & logistique": {"indicator":"Indice de coûts logistiques", "values":[100,102,105,111,118], "unit":"indice (base 100)", "meaning":"La hausse peut signaler une pression sur l'approvisionnement ou les délais."},
    "Tourisme": {"indicator":"Indice de demande touristique", "values":[100,104,107,105,113], "unit":"indice (base 100)", "meaning":"Une hausse de demande peut être positive; il faut aussi surveiller la capacité et la saisonnalité."},
    "Technologie & digital": {"indicator":"Indice d'adoption digitale", "values":[100,99,103,105,109], "unit":"indice (base 100)", "meaning":"La tendance peut aider à repérer des opportunités de transformation numérique."},
    "Immobilier & construction": {"indicator":"Indice d'activité immobilière", "values":[100,102,106,109,117], "unit":"indice (base 100)", "meaning":"À mettre en perspective avec les taux, les prix et le volume des transactions."},
    "Commerce & distribution": {"indicator":"Indice de coûts de distribution", "values":[100,101,104,107,113], "unit":"indice (base 100)", "meaning":"Une progression peut peser sur les marges et les prix finaux."},
}
SOLUTIONS = {
    "Agriculture": [
        ("Diversifier les fournisseurs", "Comparer plusieurs fournisseurs et sécuriser les intrants critiques.", "Suivre le coût moyen d'achat et la part d'approvisionnement par fournisseur."),
        ("Optimiser les stocks", "Identifier les intrants prioritaires et définir un stock de sécurité adapté.", "Suivre les jours de couverture et les pertes de stock."),
        ("Revoir le calendrier d'achat", "Comparer les périodes d'achat et négocier des contrats-cadres lorsque c'est pertinent.", "Suivre le prix d'achat et l'écart au budget.")
    ],
    "Industrie": [
        ("Améliorer l'efficacité opérationnelle", "Analyser les postes de coûts et les pertes de production les plus importants.", "Suivre le coût unitaire et le taux de rebut."),
        ("Sécuriser les approvisionnements", "Évaluer les fournisseurs critiques et prévoir des solutions de remplacement.", "Suivre les retards et les ruptures."),
        ("Réviser le mix de production", "Prioriser les produits selon la demande, la marge et les contraintes de capacité.", "Suivre la marge par produit.")
    ],
    "Commerce international": [
        ("Diversifier les marchés", "Évaluer les débouchés alternatifs et les risques de concentration.", "Suivre la part des ventes par marché."),
        ("Surveiller les coûts d'importation", "Comparer prix, transport, change et délais de livraison.", "Suivre le coût rendu et le délai moyen."),
        ("Renforcer la veille réglementaire", "Vérifier les changements de normes, droits et formalités auprès de sources officielles.", "Suivre les alertes réglementaires confirmées.")
    ],
    "Énergie": [
        ("Réduire la consommation", "Repérer les usages les plus énergivores et tester des mesures d'efficacité.", "Suivre les kWh par unité produite."),
        ("Diversifier les contrats", "Comparer les options d'approvisionnement et les risques contractuels.", "Suivre le coût moyen et l'exposition contractuelle."),
        ("Étudier l'autoproduction", "Évaluer la faisabilité technique et économique d'une solution renouvelable.", "Suivre le coût complet et le temps de retour estimé.")
    ],
    "Finance & banque": [
        ("Renforcer le suivi du risque", "Vérifier les expositions et les scénarios défavorables avant toute décision.", "Suivre les indicateurs de risque retenus."),
        ("Tester des scénarios", "Comparer plusieurs hypothèses sans les traiter comme des prévisions.", "Suivre l'écart entre scénario et réalisation."),
        ("Diversifier les expositions", "Examiner les concentrations et les limites internes applicables.", "Suivre les concentrations par catégorie.")
    ],
    "Transport & logistique": [
        ("Optimiser les itinéraires", "Comparer les itinéraires, les taux de remplissage et les délais.", "Suivre le coût par livraison."),
        ("Sécuriser les partenaires", "Identifier les partenaires critiques et préparer des solutions de secours.", "Suivre le taux de livraison à temps."),
        ("Améliorer la planification", "Coordonner commandes, stocks et transport pour réduire les urgences.", "Suivre les livraisons urgentes et les retards.")
    ],
    "Tourisme": [
        ("Adapter les capacités à la demande", "Ajuster les ressources aux périodes et segments de clientèle.", "Suivre le taux d'occupation et la satisfaction."),
        ("Diversifier les clientèles", "Étudier de nouveaux segments et marchés émetteurs.", "Suivre la répartition de la clientèle."),
        ("Renforcer la veille concurrentielle", "Comparer offres, saisonnalité et attentes des visiteurs.", "Suivre les prix comparables et les avis.")
    ],
    "Technologie & digital": [
        ("Accélérer la montée en compétences", "Identifier les compétences prioritaires et planifier des formations ciblées.", "Suivre les compétences acquises et l'usage des outils."),
        ("Tester des solutions numériques", "Lancer un pilote limité avant un déploiement plus large.", "Suivre le gain de temps et le taux d'adoption."),
        ("Renforcer la cybersécurité", "Vérifier les accès, sauvegardes et procédures de réponse aux incidents.", "Suivre les incidents et les actions correctives.")
    ],
    "Immobilier & construction": [
        ("Actualiser les hypothèses de coûts", "Comparer les coûts des matériaux, du financement et de la main-d'œuvre.", "Suivre l'écart au budget."),
        ("Phaser les investissements", "Comparer les scénarios de calendrier et préserver la flexibilité.", "Suivre les engagements et les besoins de trésorerie."),
        ("Diversifier les fournisseurs", "Comparer la disponibilité, les délais et la qualité des matériaux.", "Suivre les retards d'approvisionnement.")
    ],
    "Commerce & distribution": [
        ("Protéger les marges", "Analyser les coûts par catégorie et comparer plusieurs options de prix.", "Suivre la marge brute par catégorie."),
        ("Optimiser les stocks", "Repérer les produits à rotation lente et les risques de rupture.", "Suivre la rotation et le taux de rupture."),
        ("Renégocier les conditions", "Comparer les conditions d'achat, de transport et de paiement.", "Suivre le coût rendu et les délais.")
    ]
}

# ---------- Sidebar ----------
st.sidebar.markdown("## 🛰️ Strategic Radar")
st.sidebar.markdown("<div class='small-muted'>Centre de veille et d'aide à la décision</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
sector = st.sidebar.selectbox("Secteur à analyser", list(DATA.keys()))
threshold = st.sidebar.slider("Seuil d'alerte sur la variation récente (%)", 1, 20, 5)
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Vue stratégique", "Analyse sectorielle", "Simulateur de décision", "Méthodologie & données"])
st.sidebar.markdown("---")
st.sidebar.caption("Prototype académique • Données de démonstration")

# ---------- Common calculations ----------
record = DATA[sector]
values = record["values"]
recent = (values[-1] - values[-2]) / values[-2] * 100
overall = (values[-1] - values[0]) / values[0] * 100
all_recent = {s: (d["values"][-1]-d["values"][-2])/d["values"][-2]*100 for s,d in DATA.items()}
risk_count = sum(v >= threshold for v in all_recent.values())
chart_df = pd.DataFrame({"Période":[f"P{i}" for i in range(1,6)], "Valeur":values})

# ---------- Hero ----------
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">Intelligence économique • Maroc</div>
  <div class="hero-title">Strategic Radar <span style="color:#67e8f9">Maroc</span></div>
  <div class="hero-sub">Détecter les signaux. Comprendre les enjeux. Comparer les options. Une interface de démonstration pour transformer une veille multisectorielle en pistes d'analyse et d'action.</div>
  <span class="pill">10 secteurs suivis</span><span class="pill">Alertes paramétrables</span><span class="pill">Scénarios comparatifs</span><span class="pill">Données fictives clairement signalées</span>
</div>
""", unsafe_allow_html=True)

st.info("Prototype académique : les chiffres présentés sont fictifs et servent à illustrer le fonctionnement. Ils ne décrivent pas la situation économique réelle du Maroc.", icon="ℹ️")

if page == "Vue stratégique":
    st.markdown("<div class='section-kicker'>Vue d'ensemble</div>", unsafe_allow_html=True)
    st.header("Le radar économique")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Secteurs analysés</div><div class='metric-value'>{len(DATA)}</div><div class='metric-note'>Couverture multisectorielle</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Signaux au-dessus du seuil</div><div class='metric-value'>{risk_count}</div><div class='metric-note'>Seuil actuel : {threshold}%</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Secteur sélectionné</div><div class='metric-value' style='font-size:1.35rem'>{sector}</div><div class='metric-note'>Analyse détaillée disponible</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Variation récente</div><div class='metric-value'>{recent:+.2f}%</div><div class='metric-note'>Sur le dernier intervalle simulé</div></div>", unsafe_allow_html=True)

    left,right = st.columns([1.35,1])
    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Carte des signaux sectoriels")
        sector_df = pd.DataFrame({"Secteur":list(all_recent.keys()), "Variation récente (%)":list(all_recent.values())}).sort_values("Variation récente (%)")
        fig = px.bar(sector_df, x="Variation récente (%)", y="Secteur", orientation="h", color="Variation récente (%)",
                     color_continuous_scale=["#38bdf8","#818cf8","#fb7185"], text_auto=".1f")
        fig.add_vline(x=threshold, line_dash="dash", line_color="#fda4af", annotation_text="Seuil d'alerte")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#dbeafe", margin=dict(l=8,r=8,t=20,b=8), height=430,
                          coloraxis_showscale=False, xaxis_title="Variation récente (%)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Signaux à examiner")
        alerts = sector_df[sector_df["Variation récente (%)"] >= threshold].sort_values("Variation récente (%)", ascending=False)
        if alerts.empty:
            st.success("Aucun signal ne dépasse le seuil sélectionné dans cette démonstration.")
        else:
            for _, row in alerts.iterrows():
                st.markdown(f"""
                <div style="padding:12px 0;border-bottom:1px solid rgba(160,184,225,.13)">
                  <div style="font-weight:700;color:#f1f5f9">{row['Secteur']}</div>
                  <div style="color:#fda4af;font-size:1.2rem;font-weight:800">{row['Variation récente (%)']:+.2f}%</div>
                  <div class="small-muted">Signal statistique à vérifier — pas une preuve de crise.</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-kicker'>Point de départ</div>", unsafe_allow_html=True)
    st.markdown(f"**{sector} :** {record['meaning']} Les valeurs actuelles sont simulées; la prochaine étape d'une vraie veille serait de vérifier la tendance auprès de sources officielles et de plusieurs sources indépendantes.")
    st.caption("Pour approfondir ce secteur, choisissez « Analyse sectorielle » dans le menu de navigation à gauche.")

elif page == "Analyse sectorielle":
    st.markdown("<div class='section-kicker'>Diagnostic sectoriel</div>", unsafe_allow_html=True)
    st.header(f"Analyse — {sector}")
    st.caption(f"Indicateur : {record['indicator']} • Unité : {record['unit']}")
    m1,m2,m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Dernière valeur</div><div class='metric-value'>{values[-1]:g}</div><div class='metric-note'>{record['unit']}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Variation récente</div><div class='metric-value'>{recent:+.2f}%</div><div class='metric-note'>Entre P4 et P5</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Variation depuis P1</div><div class='metric-value'>{overall:+.2f}%</div><div class='metric-note'>Évolution cumulée simulée</div></div>", unsafe_allow_html=True)

    left,right = st.columns([1.25,1])
    with left:
        fig = px.line(chart_df, x="Période", y="Valeur", markers=True, text="Valeur")
        fig.update_traces(line=dict(color="#67e8f9",width=4), marker=dict(size=9,color="#a5f3fc"), textposition="top center")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#dbeafe", margin=dict(l=8,r=8,t=25,b=8), height=350,
                          xaxis_title="", yaxis_title=record["unit"])
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Lecture du signal")
        if recent >= threshold:
            st.warning(f"Le mouvement récent ({recent:+.2f}%) dépasse le seuil de {threshold}%. Vérifier la donnée, puis rechercher des explications externes.")
        elif recent <= -threshold:
            st.warning(f"Le mouvement récent ({recent:+.2f}%) dépasse le seuil de baisse. Vérifier la donnée et son contexte.")
        else:
            st.success(f"Le mouvement récent ({recent:+.2f}%) reste sous le seuil choisi.")
        st.write(record["meaning"])
        st.markdown("**Questions à vérifier**")
        st.markdown("- La donnée est-elle fiable et comparable dans le temps?\n- Observe-t-on le même signal dans une source indépendante?\n- Quels facteurs externes pourraient expliquer l'évolution?\n- Qui est exposé et quelle décision dépend de cette information?")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Solutions et recommandations")
    options = SOLUTIONS[sector]
    choice = st.selectbox("Choisir une piste à examiner", [x[0] for x in options])
    selected = next(x for x in options if x[0] == choice)
    st.markdown(f"<div class='panel'><div class='eyebrow'>Piste de réponse</div><h3>{selected[0]}</h3><p>{selected[1]}</p><div style='color:#67e8f9;font-weight:700'>Indicateur de suivi</div><p>{selected[2]}</p><p class='small-muted'>Piste indicative à valider avec le contexte, les ressources et les contraintes réelles de l'organisation.</p></div>", unsafe_allow_html=True)

    st.subheader("Données utilisées")
    table = pd.DataFrame({"Période":chart_df["Période"], record["indicator"]:values})
    table["Variation (%)"] = table[record["indicator"]].pct_change().mul(100).round(2)
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Télécharger les données de démonstration (CSV)", table.to_csv(index=False).encode("utf-8-sig"), file_name=f"radar_{sector.lower().replace(' ','_').replace('&','et')}.csv", mime="text/csv")

elif page == "Simulateur de décision":
    st.markdown("<div class='section-kicker'>Scénarios hypothétiques</div>", unsafe_allow_html=True)
    st.header("Simulateur de décision")
    st.write("Comparez une situation de référence, un scénario sans action et un scénario avec action. Les paramètres sont illustratifs : ce ne sont ni des prévisions ni des gains garantis.")
    col1,col2 = st.columns(2)
    with col1:
        before = st.slider("Variation hypothétique sans action (%)", 0, 30, 10)
    with col2:
        effect = st.slider("Effet hypothétique de l'action (%)", 0, 25, 5)
    current = float(values[-1])
    no_action = current * (1 + before/100)
    with_action = no_action * (1 - effect/100)
    a,b,c = st.columns(3)
    with a:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Valeur actuelle</div><div class='metric-value'>{current:.2f}</div><div class='metric-note'>Point de départ</div></div>", unsafe_allow_html=True)
    with b:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Scénario sans action</div><div class='metric-value'>{no_action:.2f}</div><div class='metric-note'>Variation simulée : +{before}%</div></div>", unsafe_allow_html=True)
    with c:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Scénario avec action</div><div class='metric-value'>{with_action:.2f}</div><div class='metric-note'>Effet supposé : −{effect}%</div></div>", unsafe_allow_html=True)
    sim_df = pd.DataFrame({"Scénario":["Valeur actuelle","Sans action","Avec action"],"Valeur":[current,no_action,with_action]})
    fig = px.bar(sim_df, x="Scénario", y="Valeur", color="Scénario", text_auto=".2f",
                 color_discrete_sequence=["#38bdf8","#fb7185","#34d399"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#dbeafe", showlegend=False, margin=dict(l=8,r=8,t=20,b=8), height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.info("À retenir : le simulateur illustre une méthode de comparaison. Pour l'utiliser en situation réelle, il faut estimer les effets à partir de données, d'hypothèses explicites et d'une validation métier.", icon="🧭")

else:
    st.markdown("<div class='section-kicker'>Transparence & fiabilité</div>", unsafe_allow_html=True)
    st.header("Méthodologie & données")
    st.markdown("""
    <div class='panel'>
      <h3>Comment lire cette plateforme?</h3>
      <p><b>1. Collecter :</b> réunir des informations pertinentes et datées provenant de sources vérifiables.</p>
      <p><b>2. Contrôler :</b> vérifier la définition de l'indicateur, l'unité, la période et la cohérence des données.</p>
      <p><b>3. Détecter :</b> comparer les valeurs et signaler les variations qui dépassent un seuil paramétrable.</p>
      <p><b>4. Interpréter :</b> rechercher des explications à partir de sources indépendantes et du contexte sectoriel.</p>
      <p><b>5. Décider :</b> comparer les options, leurs coûts, leurs risques et les indicateurs de suivi.</p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Sources à connecter pour une version réelle")
    sources = pd.DataFrame([
        ["Haut-Commissariat au Plan (HCP)", "Statistiques nationales, prix, emploi et conjoncture", "https://www.hcp.ma/"],
        ["Base de données statistiques HCP", "Données par thème : économie, énergie, transport, emploi", "https://bds.hcp.ma/"],
        ["Bank Al-Maghrib", "Indicateurs monétaires, financiers et rapports économiques", "https://www.bkam.ma/"],
        ["Office des Changes", "Statistiques du commerce extérieur et des échanges", "https://www.oc.gov.ma/"],
        ["Base de données du commerce extérieur", "Consultation et export des statistiques mensuelles d'import/export", "https://services.oc.gov.ma/DataBase/CommerceExterieur/login"],
        ["Ministère de l'Agriculture", "Informations et publications sectorielles", "https://www.agriculture.gov.ma/"],
        ["Office National des Aéroports (ONDA)", "Indicateurs de trafic aérien et données liées au tourisme", "https://www.onda.ma/"],
    ], columns=["Source institutionnelle","Informations possibles à rechercher","Site officiel"])
    st.dataframe(sources, use_container_width=True, hide_index=True)
    source_cols = st.columns(3)
    with source_cols[0]:
        st.link_button("Ouvrir le HCP", "https://www.hcp.ma/", use_container_width=True)
    with source_cols[1]:
        st.link_button("Ouvrir Bank Al-Maghrib", "https://www.bkam.ma/", use_container_width=True)
    with source_cols[2]:
        st.link_button("Ouvrir l'Office des Changes", "https://www.oc.gov.ma/", use_container_width=True)
    st.markdown("**Important :** ces liens sont des points de départ vers des sites institutionnels, pas la preuve que chaque indicateur affiché dans cette version a été récupéré depuis ces sites.")
    st.subheader("Données de démonstration")
    st.write("Les valeurs P1 à P5 sont fictives. Aucune connexion automatique aux marchés, API ou bases de données officielles n'est configurée dans cette version.")
    all_rows = []
    for s,d in DATA.items():
        for i,v in enumerate(d["values"],1):
            all_rows.append({"Secteur":s,"Indicateur":d["indicator"],"Période":f"P{i}","Valeur":v,"Statut":"Fictif — démonstration"})
    full = pd.DataFrame(all_rows)
    st.download_button("⬇️ Télécharger le jeu de démonstration complet", full.to_csv(index=False).encode("utf-8-sig"), file_name="strategic_radar_maroc_demo.csv", mime="text/csv")

st.markdown("---")
st.markdown("<div style='display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:#8292af;font-size:.78rem'><span>🛰️ Strategic Radar Maroc · Prototype académique</span><span>Veille → Analyse → Scénarios → Décision</span><span>Données de démonstration uniquement</span></div>", unsafe_allow_html=True)
