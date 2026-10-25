import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timezone

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

WB_API = "https://api.worldbank.org/v2"

COUNTRIES = {
    "Maroc": "MAR",
    "États-Unis": "USA",
    "France": "FRA",
    "Espagne": "ESP",
    "Allemagne": "DEU",
    "Royaume-Uni": "GBR",
    "Chine": "CHN",
    "Japon": "JPN",
    "Inde": "IND",
    "Brésil": "BRA",
    "Canada": "CAN",
    "Italie": "ITA",
    "Turquie": "TUR",
    "Égypte": "EGY",
    "Arabie saoudite": "SAU",
    "Afrique du Sud": "ZAF",
    "Australie": "AUS",
    "Corée du Sud": "KOR",
    "Mexique": "MEX",
    "Suisse": "CHE",
}

INDICATORS = {
    "PIB (USD courants)": "NY.GDP.MKTP.CD",
    "Croissance du PIB (%)": "NY.GDP.MKTP.KD.ZG",
    "Inflation (%)": "FP.CPI.TOTL.ZG",
    "Population": "SP.POP.TOTL",
    "Chômage (%)": "SL.UEM.TOTL.ZS",
    "PIB par habitant (USD)": "NY.GDP.PCAP.CD",
    "Investissement étranger (% PIB)": "BX.KLT.DINV.WD.GD.ZS",
    "Exportations (% PIB)": "NE.EXP.GNFS.ZS",
    "Importations (% PIB)": "NE.IMP.GNFS.ZS",
    "Dette extérieure (% RNB)": "DT.DOD.DECT.GN.ZS",
}

CENTRAL_BANKS = {
    "Federal Reserve (États-Unis)": "https://www.federalreserve.gov/",
    "Banque centrale européenne": "https://www.ecb.europa.eu/",
    "Bank Al-Maghrib": "https://www.bkam.ma/",
    "Bank of England": "https://www.bankofengland.co.uk/",
    "Bank of Japan": "https://www.boj.or.jp/en/",
    "Swiss National Bank": "https://www.snb.ch/en/",
    "Bank of Canada": "https://www.bankofcanada.ca/",
    "Reserve Bank of Australia": "https://www.rba.gov.au/",
    "People's Bank of China": "http://www.pbc.gov.cn/en/",
    "Reserve Bank of India": "https://www.rbi.org.in/",
}

MARKET_SOURCES = {
    "Bourse de Casablanca": "https://www.casablanca-bourse.com/",
    "AMMC Maroc": "https://www.ammc.ma/",
    "NYSE": "https://www.nyse.com/",
    "Nasdaq": "https://www.nasdaq.com/",
    "London Stock Exchange": "https://www.londonstockexchange.com/",
    "Euronext": "https://www.euronext.com/",
    "Deutsche Börse": "https://www.deutsche-boerse.com/",
    "Tokyo Stock Exchange": "https://www.jpx.co.jp/english/",
    "Shanghai Stock Exchange": "https://english.sse.com.cn/",
}

ASSET_SOURCES = {
    "FRED — taux, inflation et économie américaine":
        "https://fred.stlouisfed.org/",
    "Federal Reserve — statistiques et publications":
        "https://www.federalreserve.gov/data.htm",
    "New York Fed — marchés":
        "https://markets.newyorkfed.org/",
    "Banque mondiale — données":
        "https://data.worldbank.org/",
    "FMI — données mondiales":
        "https://data.imf.org/",
    "Office des Changes Maroc":
        "https://www.oc.gov.ma/",
    "Bank Al-Maghrib — statistiques":
        "https://www.bkam.ma/",
    "U.S. Energy Information Administration — énergie":
        "https://www.eia.gov/",
    "LBMA — marché de l'or":
        "https://www.lbma.org.uk/",
}

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink:#eaf0ff;
    --muted:#9aa9c5;
    --panel:#111d35;
    --line:rgba(160,184,225,.16);
}

html, body, [class*="css"] {
    font-family:'DM Sans',sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 80% 0%, rgba(34,211,238,.12), transparent 28%),
      radial-gradient(circle at 0% 18%, rgba(99,102,241,.18), transparent 30%),
      #081225;
    color:var(--ink);
}

[data-testid="stHeader"] {
    background:rgba(8,18,37,.8);
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#101d36,#0b1428);
    border-right:1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color:#eaf0ff;
}

.block-container {
    padding-top:1.4rem;
    padding-bottom:3rem;
    max-width:1440px;
}

h1,h2,h3 {
    font-family:'Manrope',sans-serif !important;
    letter-spacing:-.035em;
    color:#f4f7ff;
}

.hero {
    padding:30px;
    border:1px solid rgba(125,211,252,.22);
    border-radius:24px;
    background:linear-gradient(
      115deg,
      rgba(22,39,71,.97),
      rgba(12,27,51,.9) 58%,
      rgba(19,54,78,.8)
    );
    box-shadow:0 20px 60px rgba(0,0,0,.2);
    margin-bottom:22px;
}

.eyebrow {
    color:#67e8f9;
    text-transform:uppercase;
    letter-spacing:.17em;
    font-size:.74rem;
    font-weight:700;
}

.hero-title {
    font-family:'Manrope',sans-serif;
    font-weight:800;
    font-size:clamp(2rem,4vw,3.3rem);
    line-height:1.1;
    color:#f7fbff;
    margin:.55rem 0 .75rem;
}

.hero-sub {
    max-width:850px;
    color:#b7c6df;
    font-size:1rem;
    line-height:1.7;
}

.metric-card {
    background:linear-gradient(145deg,rgba(20,35,63,.98),rgba(13,25,46,.98));
    border:1px solid var(--line);
    border-radius:18px;
    padding:18px;
    min-height:120px;
    margin-bottom:10px;
}

.metric-label {
    color:#9fb0cd;
    font-size:.82rem;
    margin-bottom:9px;
}

.metric-value {
    color:#f4f7ff;
    font-family:'Manrope',sans-serif;
    font-size:1.7rem;
    font-weight:800;
    overflow-wrap:anywhere;
}

.metric-note {
    color:#a5f3fc;
    font-size:.78rem;
    margin-top:5px;
}

.panel {
    background:rgba(15,28,51,.78);
    border:1px solid var(--line);
    border-radius:20px;
    padding:20px;
}

.small-muted {
    color:#9aa9c5;
    font-size:.84rem;
}

.stButton>button, .stDownloadButton>button {
    border-radius:11px;
    border:1px solid rgba(103,232,249,.3);
    background:linear-gradient(90deg,#0e7490,#2563eb);
    color:white;
    font-weight:700;
}

hr {
    border-color:var(--line);
}

footer {
    visibility:hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA FUNCTIONS
# =========================================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_world_bank_data(country_code, indicator_code):
    """Données économiques publiées par la Banque mondiale."""
    url = (
        f"{WB_API}/country/{country_code}"
        f"/indicator/{indicator_code}"
    )

    try:
        response = requests.get(
            url,
            params={"format": "json", "per_page": 100},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()

        if not isinstance(payload, list) or len(payload) < 2:
            return pd.DataFrame()

        observations = payload[1]
        if not observations:
            return pd.DataFrame()

        rows = []

        for item in observations:
            value = item.get("value")

            if value is not None:
                rows.append({
                    "Pays": item["country"]["value"],
                    "Code pays": country_code,
                    "Année": int(item["date"]),
                    "Valeur": float(value),
                    "Indicateur": item["indicator"]["value"],
                    "Code indicateur": indicator_code,
                    "Source": "Banque mondiale",
                })

        if not rows:
            return pd.DataFrame()

        return pd.DataFrame(rows).sort_values("Année")

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
    ):
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def get_fred_series(api_key, series_id):
    """Série FRED. Nécessite une clé API FRED valide."""
    url = "https://api.stlouisfed.org/fred/series/observations"

    try:
        response = requests.get(
            url,
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 120,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()

        rows = []
        for item in payload.get("observations", []):
            value = item.get("value")

            if value not in (None, ".", ""):
                rows.append({
                    "Date": item["date"],
                    "Valeur": float(value),
                })

        if not rows:
            return pd.DataFrame()

        return pd.DataFrame(rows).sort_values("Date")

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
    ):
        return pd.DataFrame()


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_source_links(source_dict):
    for name, url in source_dict.items():
        st.markdown(f"- [{name}]({url})")


def format_value(value, indicator_name):
    if pd.isna(value):
        return "N/D"

    if indicator_name == "Population":
        return f"{value:,.0f}".replace(",", " ")

    if "PIB (" in indicator_name:
        return f"{value:,.0f} USD".replace(",", " ")

    if "habitant" in indicator_name:
        return f"{value:,.0f} USD".replace(",", " ")

    return f"{value:,.2f}"


# =========================================================
# NAVIGATION
# =========================================================

st.sidebar.markdown("## 🛰️ Strategic Radar")
st.sidebar.caption("Intelligence économique & financière")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Vue globale",
        "Pays & macroéconomie",
        "Banques centrales",
        "Bourses mondiales",
        "Forex & matières premières",
        "Entreprises",
        "Villes & régions",
        "Analyse sectorielle",
        "Données américaines — FRED",
        "Méthodologie & sources",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Prototype académique • Sources et limites indiquées")

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
  <div class="eyebrow">Global economic & financial intelligence</div>
  <div class="hero-title">
    Strategic Radar <span style="color:#67e8f9">Maroc</span>
  </div>
  <div class="hero-sub">
    Une plateforme de veille pour explorer les économies,
    suivre les politiques monétaires, comparer les indicateurs
    et consulter les sources des marchés financiers mondiaux.
  </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Les données affichées dépendent des sources disponibles. "
    "Les statistiques économiques peuvent être publiées avec retard "
    "et révisées par les organismes producteurs."
)

# =========================================================
# PAGE: GLOBAL
# =========================================================

if page == "Vue globale":
    st.header("🌍 Vue globale")

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Pays disponibles", len(COUNTRIES), "Comparaison économique")

    with c2:
        metric_card("Indicateurs", len(INDICATORS), "Catalogue Banque mondiale")

    with c3:
        metric_card("Banques centrales", len(CENTRAL_BANKS), "Liens vers les sites officiels")

    st.subheader("Explorer la plateforme")

    st.markdown("""
    - **Pays & macroéconomie :** PIB, inflation, chômage, population et commerce.
    - **Banques centrales :** politiques monétaires et publications officielles.
    - **Bourses mondiales :** accès aux places financières et à leurs publications.
    - **Forex & matières premières :** sources pour les devises, l'or et l'énergie.
    - **Entreprises :** sources officielles et informations réglementaires.
    - **Données américaines — FRED :** séries économiques américaines si une clé API est fournie.
    """)

    st.info(
        "Les pages des marchés financiers donnent accès aux sources officielles. "
        "Les cours ne sont pas présentés comme des cotations en direct "
        "tant qu'un fournisseur de données de marché n'est pas connecté."
    )

# =========================================================
# PAGE: COUNTRIES
# =========================================================

elif page == "Pays & macroéconomie":
    st.header("🌍 Pays & macroéconomie")

    selected_indicator = st.selectbox(
        "Indicateur économique",
        list(INDICATORS.keys()),
    )

    selected_countries = st.multiselect(
        "Choisir les pays à comparer",
        list(COUNTRIES.keys()),
        default=["Maroc", "France", "États-Unis"],
    )

    if st.button("🔎 Charger les données officielles"):
        if not selected_countries:
            st.warning("Choisissez au moins un pays.")
        else:
            frames = []

            with st.spinner("Récupération des données de la Banque mondiale..."):
                for country in selected_countries:
                    df = get_world_bank_data(
                        COUNTRIES[country],
                        INDICATORS[selected_indicator],
                    )

                    if not df.empty:
                        df["Pays sélectionné"] = country
                        frames.append(df)

            if not frames:
                st.warning(
                    "Aucune observation disponible ou service temporairement "
                    "inaccessible. Réessayez plus tard."
                )
            else:
                data = pd.concat(frames, ignore_index=True)

                latest = (
                    data.sort_values("Année")
                    .groupby("Pays sélectionné", as_index=False)
                    .tail(1)
                    .sort_values("Pays sélectionné")
                )

                st.subheader("Dernière observation disponible")
                display = latest[
                    ["Pays sélectionné", "Année", "Valeur", "Indicateur", "Source"]
                ].copy()

                display["Valeur"] = display["Valeur"].map(
                    lambda x: f"{x:,.3f}".replace(",", " ")
                )

                st.dataframe(
                    display,
                    use_container_width=True,
                    hide_index=True,
                )

                fig = px.line(
                    data,
                    x="Année",
                    y="Valeur",
                    color="Pays sélectionné",
                    markers=True,
                    title=selected_indicator,
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#dbeafe",
                )

                st.plotly_chart(fig, use_container_width=True)

                st.download_button(
                    "⬇️ Télécharger les données CSV",
                    data.to_csv(index=False).encode("utf-8-sig"),
                    file_name="world_bank_data.csv",
                    mime="text/csv",
                )

                st.caption(
                    "Source : Banque mondiale. L'année la plus récente "
                    "disponible peut varier selon le pays et l'indicateur."
                )

    st.markdown(
        "[Ouvrir les données de la Banque mondiale](https://data.worldbank.org/)"
    )

# =========================================================
# PAGE: CENTRAL BANKS
# =========================================================

elif page == "Banques centrales":
    st.header("🏦 Banques centrales")

    st.write(
        "Consultez les sites officiels pour les taux directeurs, "
        "les décisions de politique monétaire, les communiqués "
        "et les rapports économiques."
    )

    st.warning(
        "Cette page répertorie les sources officielles. "
        "Les taux directeurs ne sont pas automatiquement récupérés "
        "dans cette version."
    )

    for name, url in CENTRAL_BANKS.items():
        st.markdown(f"**{name}** — [Site officiel]({url})")

    st.subheader("Questions utiles pour l'analyse")
    st.markdown("""
    - Le taux directeur a-t-il été augmenté, réduit ou maintenu ?
    - Quelle est la dernière donnée d'inflation publiée ?
    - Quel est le message principal du dernier communiqué ?
    - Quels risques sont mentionnés par la banque centrale ?
    - Les politiques monétaires des principales économies divergent-elles ?
    """)

# =========================================================
# PAGE: STOCK EXCHANGES
# =========================================================

elif page == "Bourses mondiales":
    st.header("📈 Bourses mondiales")

    st.write(
        "Accédez aux places financières et aux publications des marchés. "
        "Les cotations en direct nécessitent un fournisseur de données "
        "et peuvent être soumises à des licences."
    )

    for name, url in MARKET_SOURCES.items():
        st.markdown(f"**{name}** — [Site officiel]({url})")

    st.subheader("Indicateurs à analyser")
    st.markdown("""
    - Variation quotidienne, hebdomadaire et annuelle.
    - Volatilité historique.
    - Volume des échanges.
    - Rendement et comparaison entre indices.
    - Sensibilité aux taux d'intérêt et aux annonces économiques.
    """)

    st.info(
        "Aucun cours boursier n'est inventé ou simulé dans cette page. "
        "Les données de marché devront être connectées séparément."
    )

# =========================================================
# PAGE: FOREX & COMMODITIES
# =========================================================

elif page == "Forex & matières premières":
    st.header("💱 Forex & matières premières")

    st.subheader("Marchés à surveiller")

    assets = pd.DataFrame([
        ["EUR/USD", "Taux de change", "Données de marché à connecter"],
        ["USD/MAD", "Taux de change", "Consulter les sources marocaines officielles"],
        ["GBP/USD", "Taux de change", "Données de marché à connecter"],
        ["Or", "Métal précieux", "Source de référence : LBMA"],
        ["Argent", "Métal précieux", "Source de marché à connecter"],
        ["Pétrole", "Énergie", "Source de référence : EIA"],
        ["Gaz naturel", "Énergie", "Source de référence : EIA"],
        ["Bitcoin", "Cryptoactif", "Fournisseur de données crypto à connecter"],
        ["Ethereum", "Cryptoactif", "Fournisseur de données crypto à connecter"],
    ], columns=["Actif", "Catégorie", "Statut des données"])

    st.dataframe(assets, use_container_width=True, hide_index=True)

    st.subheader("Sources")
    show_source_links(ASSET_SOURCES)

    st.warning(
        "Les prix, variations et signaux de trading ne sont pas affichés "
        "sans flux de données fiable. Une analyse réelle devra indiquer "
        "la source, la devise, l'heure et le fuseau horaire."
    )

# =========================================================
# PAGE: COMPANIES
# =========================================================

elif page == "Entreprises":
    st.header("🏢 Entreprises & informations financières")

    st.write(
        "Consultez les publications des entreprises, les rapports financiers "
        "et les informations réglementaires à partir de sources officielles."
    )

    company_sources = {
        "SEC EDGAR — déclarations des entreprises américaines":
            "https://www.sec.gov/edgar",
        "Bourse de Casablanca":
            "https://www.casablanca-bourse.com/",
        "AMMC Maroc":
            "https://www.ammc.ma/",
        "Euronext":
            "https://www.euronext.com/",
        "Companies House — Royaume-Uni":
            "https://www.gov.uk/government/organisations/companies-house",
    }

    show_source_links(company_sources)

    st.subheader("Indicateurs financiers à étudier")
    st.markdown("""
    - Chiffre d'affaires et croissance.
    - Résultat opérationnel et résultat net.
    - Endettement et trésorerie.
    - Marge opérationnelle.
    - Flux de trésorerie.
    - Valorisation boursière, si disponible.
    """)

    st.info(
        "Les comptes, cours et ratios ne sont pas importés automatiquement "
        "dans cette page. Il faudra connecter une source adaptée à chaque "
        "marché et vérifier les droits d'utilisation."
    )

# =========================================================
# PAGE: CITIES AND REGIONS
# =========================================================

elif page == "Villes & régions":
    st.header("🏙️ Villes & régions")

    st.write(
        "Cette section prépare l'analyse territoriale du Maroc et "
        "d'autres régions lorsque les données comparables sont disponibles."
    )

    local_sources = {
        "Haut-Commissariat au Plan (HCP)":
            "https://www.hcp.ma/",
        "Base de données statistiques HCP":
            "https://bds.hcp.ma/",
        "Bank Al-Maghrib":
            "https://www.bkam.ma/",
        "Office des Changes":
            "https://www.oc.gov.ma/",
    }

    show_source_links(local_sources)

    st.subheader("Analyses envisageables")
    st.markdown("""
    - Population et évolution démographique.
    - Emploi et chômage.
    - Activité économique.
    - Prix et conditions de vie.
    - Commerce extérieur.
    - Comparaison entre régions selon les données disponibles.
    """)

    st.warning(
        "Aucune statistique municipale n'est générée artificiellement. "
        "Il faut vérifier que la source publie effectivement la donnée "
        "pour la ville, la région et l'année recherchées."
    )

# =========================================================
# PAGE: SECTORAL DEMONSTRATION
# =========================================================

elif page == "Analyse sectorielle":
    st.header("📊 Analyse sectorielle — démonstration")

    demo_data = {
        "Agriculture": [100, 102, 101, 106, 114],
        "Industrie": [100, 101, 103, 105, 112],
        "Énergie": [100, 103, 105, 104, 115],
        "Tourisme": [100, 104, 107, 105, 113],
        "Transport & logistique": [100, 102, 105, 111, 118],
    }

    sector = st.selectbox("Secteur", list(demo_data.keys()))
    values = demo_data[sector]

    df = pd.DataFrame({
        "Période": ["P1", "P2", "P3", "P4", "P5"],
        "Valeur fictive": values,
    })

    recent = (values[-1] - values[-2]) / values[-2] * 100
    overall = (values[-1] - values[0]) / values[0] * 100

    c1, c2 = st.columns(2)

    with c1:
        metric_card("Variation récente", f"{recent:+.2f}%", "P4 → P5")

    with c2:
        metric_card("Variation cumulée", f"{overall:+.2f}%", "P1 → P5")

    fig = px.line(
        df,
        x="Période",
        y="Valeur fictive",
        markers=True,
        title=f"{sector} — données fictives",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dbeafe",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "Les valeurs de cette section sont fictives. Elles servent "
        "uniquement à illustrer une méthode d'analyse et ne décrivent "
        "pas la situation réelle du secteur."
    )

    st.download_button(
        "⬇️ Télécharger les données de démonstration",
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name="demo_sectorielle.csv",
        mime="text/csv",
    )

# =========================================================
# PAGE: FRED
# =========================================================

elif page == "Données américaines — FRED":
    st.header("🇺🇸 Données économiques américaines — FRED")

    st.write(
        "FRED est une base de données économiques gérée par la Federal "
        "Reserve Bank of St. Louis. Une clé API est nécessaire pour "
        "récupérer les séries depuis cette application."
    )

    st.markdown(
        "[Créer ou consulter une clé API FRED](https://fred.stlouisfed.org/docs/api/api_key.html)"
    )

    api_key = st.text_input(
        "Clé API FRED",
        type="password",
        help="La clé saisie ici n'est pas enregistrée par ce code.",
    )

    series_options = {
        "Taux des fonds fédéraux": "DFF",
        "Inflation IPC américaine": "CPIAUCSL",
        "Chômage américain": "UNRATE",
        "Rendement du Treasury à 10 ans": "DGS10",
        "PIB réel américain": "GDPC1",
    }

    selected_series_name = st.selectbox(
        "Série économique",
        list(series_options.keys()),
    )

    if st.button("Charger la série FRED"):
        if not api_key.strip():
            st.warning("Saisissez d'abord votre clé API FRED.")
        else:
            with st.spinner("Chargement des observations FRED..."):
                fred_df = get_fred_series(
                    api_key.strip(),
                    series_options[selected_series_name],
                )

            if fred_df.empty:
                st.error(
                    "Aucune donnée récupérée. Vérifiez la clé API, "
                    "l'identifiant de série ou la connexion."
                )
            else:
                st.caption(
                    "Source : Federal Reserve Bank of St. Louis — FRED. "
                    "La fréquence et l'unité dépendent de la série."
                )

                fig = px.line(
                    fred_df,
                    x="Date",
                    y="Valeur",
                    title=selected_series_name,
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#dbeafe",
                )

                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(
                    fred_df.head(30),
                    use_container_width=True,
                    hide_index=True,
                )

                st.download_button(
                    "⬇️ Télécharger les données FRED",
                    fred_df.to_csv(index=False).encode("utf-8-sig"),
                    file_name="fred_data.csv",
                    mime="text/csv",
                )

# =========================================================
# PAGE: METHODOLOGY
# =========================================================

elif page == "Méthodologie & sources":
    st.header("📚 Méthodologie & sources")

    st.subheader("Règles de qualité")

    st.markdown("""
    1. **Source :** identifier l'organisme qui publie la donnée.
    2. **Date :** distinguer la date de publication de la période mesurée.
    3. **Unité :** vérifier la devise, le pourcentage et la fréquence.
    4. **Comparabilité :** éviter de comparer des définitions différentes.
    5. **Révision :** tenir compte des corrections possibles par la source.
    6. **Interprétation :** distinguer corrélation, hypothèse et causalité.
    7. **Transparence :** marquer toute valeur simulée comme fictive.
    """)

    st.subheader("Sources économiques")

    official_sources = {
        "Banque mondiale": "https://data.worldbank.org/",
        "API Banque mondiale": "https://api.worldbank.org/v2/",
        "FMI — données": "https://data.imf.org/",
        "FRED": "https://fred.stlouisfed.org/",
        "HCP Maroc": "https://www.hcp.ma/",
        "Bank Al-Maghrib": "https://www.bkam.ma/",
        "Office des Changes": "https://www.oc.gov.ma/",
        "Bourse de Casablanca": "https://www.casablanca-bourse.com/",
        "AMMC": "https://www.ammc.ma/",
        "SEC EDGAR": "https://www.sec.gov/edgar",
    }

    show_source_links(official_sources)

    st.subheader("État des connexions")
    status = pd.DataFrame([
        ["Banque mondiale", "Connexion API implémentée", "Données économiques disponibles selon l'indicateur"],
        ["FRED", "Connexion API conditionnelle", "Clé API nécessaire"],
        ["Banques centrales", "Liens officiels", "Collecte automatique non implémentée"],
        ["Bourses mondiales", "Liens officiels", "Cotations en direct non implémentées"],
        ["Forex & matières premières", "Liens de sources", "Flux de prix non implémenté"],
        ["Entreprises", "Sources officielles", "Importation automatique non implémentée"],
        ["Villes & régions", "Sources officielles", "Collecte territoriale non implémentée"],
        ["Analyse sectorielle", "Démonstration", "Valeurs fictives"],
    ], columns=["Module", "Statut", "Limites"])

    st.dataframe(status, use_container_width=True, hide_index=True)

    st.info(
        "Cette plateforme est un prototype d'analyse et de veille. "
        "Elle ne garantit ni des données en temps réel, ni des prévisions "
        "financières, ni des recommandations d'investissement."
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
      display:flex;
      justify-content:space-between;
      gap:12px;
      flex-wrap:wrap;
      color:#8292af;
      font-size:.78rem;">
      <span>🛰️ Strategic Radar Maroc</span>
      <span>Veille → Données → Analyse → Décision</span>
      <span>Prototype académique</span>
    </div>
    """,
    unsafe_allow_html=True,
)
