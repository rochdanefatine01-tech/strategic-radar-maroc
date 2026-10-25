import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

WB_API = "https://api.worldbank.org/v2"

COUNTRIES = {
    "Maroc": "MAR",
    "France": "FRA",
    "Espagne": "ESP",
    "Allemagne": "DEU",
    "États-Unis": "USA",
    "Chine": "CHN",
    "Inde": "IND",
    "Turquie": "TUR",
    "Arabie saoudite": "SAU",
    "Émirats arabes unis": "ARE",
    "Égypte": "EGY",
    "Tunisie": "TUN",
    "Algérie": "DZA",
    "Royaume-Uni": "GBR",
    "Italie": "ITA",
    "Japon": "JPN",
    "Brésil": "BRA",
    "Canada": "CAN",
    "Afrique du Sud": "ZAF",
    "Sénégal": "SEN",
}

INDICATORS = {
    "PIB (USD courants)": {
        "code": "NY.GDP.MKTP.CD",
        "unit": "USD"
    },
    "Croissance du PIB (%)": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "unit": "%"
    },
    "Inflation (%)": {
        "code": "FP.CPI.TOTL.ZG",
        "unit": "%"
    },
    "Chômage (%)": {
        "code": "SL.UEM.TOTL.ZS",
        "unit": "%"
    },
    "Population": {
        "code": "SP.POP.TOTL",
        "unit": "habitants"
    },
    "Dette extérieure (USD)": {
        "code": "DT.DOD.DECT.CD",
        "unit": "USD"
    },
    "Investissement étranger direct (USD)": {
        "code": "BX.KLT.DINV.CD.WD",
        "unit": "USD"
    },
    "Exportations de biens et services (% PIB)": {
        "code": "NE.EXP.GNFS.ZS",
        "unit": "%"
    },
    "Importations de biens et services (% PIB)": {
        "code": "NE.IMP.GNFS.ZS",
        "unit": "%"
    },
    "PIB par habitant (USD)": {
        "code": "NY.GDP.PCAP.CD",
        "unit": "USD"
    },
}

CENTRAL_BANKS = {
    "Federal Reserve (États-Unis)": "https://www.federalreserve.gov/",
    "Banque centrale européenne": "https://www.ecb.europa.eu/",
    "Bank Al-Maghrib": "https://www.bkam.ma/",
    "Bank of England": "https://www.bankofengland.co.uk/",
    "Bank of Japan": "https://www.boj.or.jp/en/",
    "Banque du Canada": "https://www.bankofcanada.ca/",
    "Banque nationale suisse": "https://www.snb.ch/",
}

MARKET_SOURCES = {
    "Bourse de Casablanca": "https://www.casablanca-bourse.com/",
    "AMMC — Marché des capitaux marocain": "https://www.ammc.ma/",
    "Nasdaq": "https://www.nasdaq.com/",
    "S&P Dow Jones Indices": "https://www.spglobal.com/spdji/",
    "Euronext Paris": "https://www.euronext.com/",
    "Deutsche Börse": "https://www.deutsche-boerse.com/",
    "London Stock Exchange": "https://www.londonstockexchange.com/",
    "CME Group — matières premières": "https://www.cmegroup.com/",
}

OTHER_SOURCES = {
    "Banque mondiale — Données": "https://data.worldbank.org/",
    "Banque mondiale — API": "https://api.worldbank.org/v2/",
    "FRED — Federal Reserve Bank of St. Louis": "https://fred.stlouisfed.org/",
    "Haut-Commissariat au Plan (Maroc)": "https://www.hcp.ma/",
    "Base de données statistiques du HCP": "https://bds.hcp.ma/",
    "Office des Changes": "https://www.oc.gov.ma/",
    "Fonds monétaire international": "https://www.imf.org/",
    "OCDE": "https://www.oecd.org/",
}

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d1b;
    --panel: #111c31;
    --border: #263650;
    --text: #edf4ff;
    --muted: #98a9c5;
    --cyan: #65e6f5;
    --blue: #527cff;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 90% 0%, rgba(0, 176, 205, 0.12), transparent 28%),
        radial-gradient(circle at 0% 30%, rgba(61, 90, 180, 0.12), transparent 30%),
        var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(8, 13, 27, 0.92);
}

[data-testid="stSidebar"] {
    background: #0b1425;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: var(--text);
    letter-spacing: -0.5px;
}

.hero {
    padding: 32px;
    border: 1px solid #294662;
    border-radius: 24px;
    background: linear-gradient(120deg, #101d36, #102b40);
    margin-bottom: 24px;
}

.hero-kicker {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    color: var(--cyan);
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(30px, 5vw, 50px);
    font-weight: 800;
    line-height: 1.1;
    margin-top: 15px;
}

.hero-title span {
    color: var(--cyan);
}

.hero-description {
    color: #b6c5dd;
    font-size: 16px;
    line-height: 1.8;
    max-width: 850px;
    margin-top: 18px;
}

.metric-card {
    background: linear-gradient(145deg, #14233b, #10192c);
    border: 1px solid #293b59;
    border-radius: 18px;
    padding: 22px;
    min-height: 130px;
    margin-bottom: 12px;
}

.metric-label {
    font-size: 13px;
    color: var(--muted);
}

.metric-value {
    font-family: 'Manrope', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: var(--text);
    margin-top: 12px;
}

.metric-caption {
    color: var(--cyan);
    font-size: 12px;
    margin-top: 5px;
}

.section-label {
    color: var(--cyan);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.source-card {
    background: #101a2d;
    border: 1px solid #263650;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 10px;
}

div[data-testid="stMetric"] {
    background: #111c31;
    border: 1px solid #263650;
    padding: 15px;
    border-radius: 15px;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #385170;
    min-height: 42px;
}

.stDownloadButton > button {
    border-radius: 10px;
}

a {
    color: #65e6f5 !important;
}

hr {
    border-color: #263650;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA FUNCTIONS
# =========================================================

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_world_bank(country_code, indicator_code, start_year=2000, end_year=None):
    """
    Récupère une série historique depuis l'API officielle
    de la Banque mondiale. Le cache est valable 24 heures.
    """
    if end_year is None:
        end_year = datetime.now().year

    url = (
        f"{WB_API}/country/{country_code}/indicator/"
        f"{indicator_code}"
    )

    params = {
        "format": "json",
        "per_page": 2000,
        "date": f"{start_year}:{end_year}"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=25,
            headers={"User-Agent": "StrategicRadarMaroc/1.0"}
        )
        response.raise_for_status()
        payload = response.json()

        if not isinstance(payload, list) or len(payload) < 2:
            return pd.DataFrame()

        records = payload[1]

        if not records:
            return pd.DataFrame()

        rows = []

        for item in records:
            value = item.get("value")

            if value is None:
                continue

            rows.append({
                "Année": int(item["date"]),
                "Valeur": float(value),
                "Pays": item["country"]["value"],
                "Code pays": country_code,
                "Indicateur": item["indicator"]["value"],
                "Code indicateur": indicator_code
            })

        df = pd.DataFrame(rows)

        if df.empty:
            return df

        return df.sort_values("Année")

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return pd.DataFrame()


def get_latest_value(country_code, indicator_code):
    df = fetch_world_bank(country_code, indicator_code)

    if df.empty:
        return None, None

    last = df.dropna(subset=["Valeur"]).sort_values("Année").iloc[-1]

    return float(last["Valeur"]), int(last["Année"])


def format_value(value, unit):
    if value is None:
        return "Non disponible"

    if unit == "%":
        return f"{value:,.2f} %"

    if unit == "USD":
        if abs(value) >= 1_000_000_000_000:
            return f"{value / 1_000_000_000_000:,.2f} T USD"
        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:,.2f} Md USD"
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:,.2f} M USD"
        return f"{value:,.2f} USD"

    return f"{value:,.0f}"


def show_source_links(sources):
    for name, url in sources.items():
        st.markdown(f"- [{name}]({url})")


def metric_card(label, value, caption):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🌐 STRATEGIC RADAR")
    st.caption("MAROC · ECONOMIC INTELLIGENCE")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Vue globale",
            "Économie mondiale",
            "Comparateur de pays",
            "Banques centrales",
            "Marchés financiers",
            "Devises & matières premières",
            "Villes & régions",
            "Entreprises",
            "Moteur d’analyse",
            "Sources & méthodologie"
        ],
        index=0
    )

    st.markdown("---")
    st.caption("DONNÉES")
    st.markdown(
        "🟢 API officielle : Banque mondiale\n\n"
        "🔵 Sources institutionnelles\n\n"
        "🟠 Marchés : flux direct non garanti"
    )

    st.markdown("---")
    st.caption("Prototype académique · 2026")


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-kicker">
        Global Economic & Financial Intelligence
    </div>
    <div class="hero-title">
        Strategic Radar<br><span>Maroc</span>
    </div>
    <div class="hero-description">
        Une plateforme d'intelligence économique pour explorer
        les économies mondiales, comparer les indicateurs,
        suivre les institutions financières et transformer
        les données disponibles en analyses utiles à la décision.
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Transparence : les données historiques sont récupérées depuis "
    "les sources identifiées. Les dernières années disponibles varient "
    "selon les indicateurs. Les pages de marchés renvoient aux sources "
    "officielles et ne prétendent pas afficher des cours en direct "
    "sans fournisseur connecté."
)

# =========================================================
# PAGE 1: OVERVIEW
# =========================================================

if page == "Vue globale":
    st.markdown("## 🌍 Vue globale")
    st.markdown(
        '<div class="section-label">Economic intelligence dashboard</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Pays suivis", str(len(COUNTRIES)), "Comparaison internationale")

    with c2:
        metric_card("Indicateurs", str(len(INDICATORS)), "Catalogue Banque mondiale")

    with c3:
        metric_card("Banques centrales", str(len(CENTRAL_BANKS)), "Sources officielles")

    with c4:
        metric_card("Sources", str(len(OTHER_SOURCES) + len(MARKET_SOURCES)), "Références institutionnelles")

    st.markdown("### 📊 Explorer la plateforme")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌐 Macroéconomie")
        st.write(
            "PIB, inflation, chômage, population, dette extérieure, "
            "investissement et commerce international."
        )

        st.markdown("#### 🏦 Politique monétaire")
        st.write(
            "Consulte les sites officiels des banques centrales "
            "et leurs publications relatives aux taux d'intérêt."
        )

        st.markdown("#### 🏙️ Territoires")
        st.write(
            "Accède aux sources institutionnelles marocaines "
            "pour les statistiques régionales et locales."
        )

    with col2:
        st.markdown("#### 📈 Marchés financiers")
        st.write(
            "Accède aux sites des grandes places financières "
            "et de la Bourse de Casablanca."
        )

        st.markdown("#### 💱 Devises et matières premières")
        st.write(
            "Consulte les sources de référence pour les taux de change, "
            "l'or, le pétrole et les autres matières premières."
        )

        st.markdown("#### 🧠 Analyse économique")
        st.write(
            "Compare les séries historiques et repère les variations "
            "à examiner avec prudence."
        )

    st.markdown("---")
    st.markdown("### 🇲🇦 Focus Maroc")

    selected_indicator = st.selectbox(
        "Choisir un indicateur pour le Maroc",
        list(INDICATORS.keys()),
        key="overview_indicator"
    )

    info = INDICATORS[selected_indicator]

    df_ma = fetch_world_bank("MAR", info["code"])

    if not df_ma.empty:
        latest = df_ma.iloc[-1]
        st.metric(
            f"{selected_indicator} — dernière observation disponible",
            format_value(float(latest["Valeur"]), info["unit"]),
            help=f"Année de référence : {int(latest['Année'])}"
        )

        st.caption(
            f"Année observée : {int(latest['Année'])} · "
            "Source : Banque mondiale"
        )

        fig = px.line(
            df_ma,
            x="Année",
            y="Valeur",
            markers=True,
            title=f"Évolution historique — {selected_indicator}"
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(
            "Aucune observation disponible pour cet indicateur "
            "dans la période demandée."
        )

# =========================================================
# PAGE 2: GLOBAL ECONOMY
# =========================================================

elif page == "Économie mondiale":
    st.markdown("## 🌍 Économie mondiale")
    st.write(
        "Explore les indicateurs macroéconomiques publiés "
        "par la Banque mondiale."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        country_name = st.selectbox(
            "Pays",
            list(COUNTRIES.keys()),
            index=list(COUNTRIES.keys()).index("Maroc"),
            key="economy_country"
        )

    with col2:
        indicator_name = st.selectbox(
            "Indicateur",
            list(INDICATORS.keys()),
            key="economy_indicator"
        )

    with col3:
        start_year = st.selectbox(
            "Début de période",
            [1990, 2000, 2005, 2010, 2015, 2020],
            index=1
        )

    country_code = COUNTRIES[country_name]
    indicator = INDICATORS[indicator_name]

    df = fetch_world_bank(
        country_code,
        indicator["code"],
        start_year=start_year
    )

    if not df.empty:
        latest = df.iloc[-1]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(
                "Dernière observation",
                format_value(float(latest["Valeur"]), indicator["unit"])
            )
            st.caption(f"Année : {int(latest['Année'])}")

        with col2:
            fig = px.line(
                df,
                x="Année",
                y="Valeur",
                markers=True,
                title=f"{indicator_name} — {country_name}"
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Données historiques")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Télécharger CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"{country_code}_{indicator['code']}.csv",
            mime="text/csv"
        )
    else:
        st.warning(
            "Pas de données disponibles pour cette combinaison. "
            "Essaie un autre indicateur ou un autre pays."
        )

    st.markdown("### Sources")
    show_source_links({
        "Banque mondiale — données": "https://data.worldbank.org/",
        "API officielle": "https://api.worldbank.org/v2/"
    })

# =========================================================
# PAGE 3: COUNTRY COMPARISON
# =========================================================

elif page == "Comparateur de pays":
    st.markdown("## 📊 Comparateur international")
    st.write(
        "Compare les dernières observations disponibles "
        "pour plusieurs pays et un même indicateur."
    )

    indicator_name = st.selectbox(
        "Indicateur à comparer",
        list(INDICATORS.keys()),
        key="comparison_indicator"
    )

    selected_countries = st.multiselect(
        "Sélectionner les pays",
        list(COUNTRIES.keys()),
        default=["Maroc", "France", "Espagne", "États-Unis"],
        max_selections=10
    )

    info = INDICATORS[indicator_name]
    comparison_rows = []

    with st.spinner("Récupération des données officielles..."):
        for country in selected_countries:
            code = COUNTRIES[country]
            value, year = get_latest_value(code, info["code"])

            if value is not None:
                comparison_rows.append({
                    "Pays": country,
                    "Code": code,
                    "Année": year,
                    "Valeur": value,
                    "Unité": info["unit"]
                })

    if comparison_rows:
        df_compare = pd.DataFrame(comparison_rows)

        fig = px.bar(
            df_compare,
            x="Pays",
            y="Valeur",
            color="Pays",
            hover_data=["Année", "Code"],
            title=f"Comparaison : {indicator_name}"
        )
        fig.update_layout(
            template="plotly_dark",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            df_compare,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Exporter la comparaison",
            data=df_compare.to_csv(index=False).encode("utf-8-sig"),
            file_name="comparaison_pays.csv",
            mime="text/csv"
        )

        st.info(
            "Attention : les dernières années peuvent différer entre pays. "
            "Vérifie la colonne Année avant de comparer les valeurs."
        )
    else:
        st.warning(
            "Aucune donnée disponible. Sélectionne au moins un pays "
            "et réessaie."
        )

    show_source_links({
        "Banque mondiale": "https://data.worldbank.org/",
        "API Banque mondiale": "https://api.worldbank.org/v2/"
    })

# =========================================================
# PAGE 4: CENTRAL BANKS
# =========================================================

elif page == "Banques centrales":
    st.markdown("## 🏦 Banques centrales")
    st.write(
        "Les décisions de politique monétaire doivent être vérifiées "
        "dans les communiqués officiels de chaque institution."
    )

    st.warning(
        "Cette page fournit les accès officiels. Elle ne prétend pas "
        "récupérer automatiquement toutes les décisions ou les taux "
        "directeurs en temps réel."
    )

    for name, url in CENTRAL_BANKS.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Consulter le site officiel", url)

    st.markdown("### Comparaison des politiques monétaires")
    st.write(
        "Pour une comparaison rigoureuse, relève pour chaque banque : "
        "le taux directeur, la date de décision, le taux précédent, "
        "la variation en points de base et le communiqué associé."
    )

    st.dataframe(
        pd.DataFrame([
            {
                "Institution": name,
                "Taux directeur": "À vérifier dans la source officielle",
                "Dernière décision": "À vérifier dans le communiqué",
                "Source": url
            }
            for name, url in CENTRAL_BANKS.items()
        ]),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Les valeurs de taux ne sont pas inventées : elles ne sont "
        "pas affichées comme observations vérifiées tant qu'elles "
        "ne sont pas récupérées depuis une source appropriée."
    )

# =========================================================
# PAGE 5: FINANCIAL MARKETS
# =========================================================

elif page == "Marchés financiers":
    st.markdown("## 📈 Marchés financiers")
    st.write(
        "Accède aux sources officielles des principales places "
        "financières et consulte leurs publications."
    )

    st.warning(
        "Les cours boursiers en direct nécessitent un fournisseur de "
        "données adapté. Les liens ci-dessous ne sont pas des cotations "
        "en temps réel."
    )

    for name, url in MARKET_SOURCES.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Ouvrir la source", url)

    st.markdown("### Indices à suivre")

    indices = pd.DataFrame([
        {"Marché": "États-Unis", "Indice": "S&P 500", "Source": "S&P Dow Jones Indices"},
        {"Marché": "États-Unis", "Indice": "Nasdaq Composite", "Source": "Nasdaq"},
        {"Marché": "France", "Indice": "CAC 40", "Source": "Euronext"},
        {"Marché": "Allemagne", "Indice": "DAX", "Source": "Deutsche Börse"},
        {"Marché": "Maroc", "Indice": "MASI", "Source": "Bourse de Casablanca"},
    ])

    st.dataframe(indices, use_container_width=True, hide_index=True)

# =========================================================
# PAGE 6: FX & COMMODITIES
# =========================================================

elif page == "Devises & matières premières":
    st.markdown("## 💱 Devises & matières premières")

    st.write(
        "Cette rubrique centralise les sources utiles pour examiner "
        "les taux de change et les prix des matières premières."
    )

    st.warning(
        "Aucun prix actuel n'est fabriqué ou simulé. Les cours nécessitent "
        "une source datée ou un fournisseur de marché connecté."
    )

    sources = {
        "Office des Changes — Maroc": "https://www.oc.gov.ma/",
        "Bank Al-Maghrib": "https://www.bkam.ma/",
        "Banque centrale européenne — taux de change": "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html",
        "FRED — données économiques": "https://fred.stlouisfed.org/",
        "CME Group — matières premières": "https://www.cmegroup.com/",
        "U.S. Energy Information Administration": "https://www.eia.gov/",
        "World Gold Council": "https://www.gold.org/",
    }

    for name, url in sources.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Consulter la source", url)

    st.markdown("### Actifs à suivre")

    assets = pd.DataFrame([
        {"Catégorie": "Devise", "Actif": "EUR/USD", "Données": "Source de change requise"},
        {"Catégorie": "Devise", "Actif": "USD/MAD", "Données": "Source officielle marocaine requise"},
        {"Catégorie": "Matière première", "Actif": "Or", "Données": "Fournisseur de prix requis"},
        {"Catégorie": "Énergie", "Actif": "Pétrole Brent", "Données": "Fournisseur de prix requis"},
        {"Catégorie": "Énergie", "Actif": "Gaz naturel", "Données": "Fournisseur de prix requis"},
    ])

    st.dataframe(assets, use_container_width=True, hide_index=True)

# =========================================================
# PAGE 7: CITIES & REGIONS
# =========================================================

elif page == "Villes & régions":
    st.markdown("## 🏙️ Villes & régions du Maroc")

    st.write(
        "Les statistiques locales doivent être consultées auprès "
        "des organismes publics compétents. La disponibilité dépend "
        "de l'indicateur et du niveau géographique."
    )

    city_sources = {
        "Haut-Commissariat au Plan": "https://www.hcp.ma/",
        "Base de données statistiques du HCP": "https://bds.hcp.ma/",
        "Portail national des collectivités territoriales": "https://www.collectivites-territoriales.gov.ma/",
        "Data.gov.ma — portail de données ouvertes": "https://data.gov.ma/",
    }

    for name, url in city_sources.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Accéder aux données", url)

    st.markdown("### Indicateurs locaux à rechercher")

    st.dataframe(
        pd.DataFrame([
            {"Indicateur": "Population", "Niveau": "Région / ville selon disponibilité"},
            {"Indicateur": "Chômage", "Niveau": "Selon les publications disponibles"},
            {"Indicateur": "Activité économique", "Niveau": "Selon les publications disponibles"},
            {"Indicateur": "Prix et coût de la vie", "Niveau": "Selon les publications disponibles"},
            {"Indicateur": "Éducation et santé", "Niveau": "Selon les publications disponibles"},
        ]),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Les données municipales ne sont pas générées artificiellement. "
        "L'intégration automatique nécessite un fichier de données "
        "ou une API officielle compatible."
    )

# =========================================================
# PAGE 8: COMPANIES
# =========================================================

elif page == "Entreprises":
    st.markdown("## 🏢 Entreprises & intelligence financière")

    st.write(
        "Consulte les sources officielles pour les sociétés cotées, "
        "les publications réglementaires et les données financières."
    )

    company_sources = {
        "Bourse de Casablanca": "https://www.casablanca-bourse.com/",
        "Autorité marocaine du marché des capitaux (AMMC)": "https://www.ammc.ma/",
        "Office des Changes": "https://www.oc.gov.ma/",
        "OMPIC — propriété industrielle et commerciale": "https://www.ompic.ma/",
    }

    for name, url in company_sources.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Consulter la source officielle", url)

    st.markdown("### Grille d'analyse d'une entreprise")

    st.write(
        "Pour analyser une entreprise, collecte ses états financiers, "
        "son chiffre d'affaires, son résultat net, son endettement, "
        "sa rentabilité et les informations réglementaires disponibles."
    )

    uploaded_file = st.file_uploader(
        "Importer un fichier CSV d'entreprise pour l'analyser",
        type=["csv"],
        help="Le fichier doit contenir des données financières réelles."
    )

    if uploaded_file is not None:
        try:
            df_company = pd.read_csv(uploaded_file)

            st.success("Fichier chargé.")
            st.dataframe(df_company, use_container_width=True)

            numeric_cols = df_company.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_cols:
                selected_col = st.selectbox(
                    "Variable numérique à visualiser",
                    numeric_cols
                )

                fig = px.line(
                    df_company,
                    y=selected_col,
                    markers=True,
                    title=f"Évolution de {selected_col}"
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.download_button(
                "⬇️ Télécharger les données chargées",
                data=df_company.to_csv(index=False).encode("utf-8-sig"),
                file_name="entreprise_analyse.csv",
                mime="text/csv"
            )

        except Exception as exc:
            st.error(f"Impossible de lire le fichier : {exc}")

# =========================================================
# PAGE 9: ANALYTICS ENGINE
# =========================================================

elif page == "Moteur d’analyse":
    st.markdown("## 🧠 Moteur d'analyse économique")

    st.write(
        "Cet outil calcule les variations observées dans une série "
        "historique. Les résultats constituent des signaux descriptifs, "
        "pas des prévisions certaines."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        country_name = st.selectbox(
            "Pays",
            list(COUNTRIES.keys()),
            index=list(COUNTRIES.keys()).index("Maroc"),
            key="analysis_country"
        )

    with col2:
        indicator_name = st.selectbox(
            "Indicateur",
            list(INDICATORS.keys()),
            key="analysis_indicator"
        )

    with col3:
        period_start = st.selectbox(
            "Début de la période",
            [1990, 2000, 2005, 2010, 2015, 2020],
            index=1,
            key="analysis_start"
        )

    info = INDICATORS[indicator_name]

    df_analysis = fetch_world_bank(
        COUNTRIES[country_name],
        info["code"],
        start_year=period_start
    )

    if not df_analysis.empty:
        df_analysis = df_analysis.sort_values("Année").copy()
        df_analysis["Variation absolue"] = df_analysis["Valeur"].diff()
        df_analysis["Variation (%)"] = (
            df_analysis["Valeur"].pct_change() * 100
        )

        latest = df_analysis.iloc[-1]

        st.markdown("### Résultats descriptifs")

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Dernière valeur",
                format_value(float(latest["Valeur"]), info["unit"])
            )

        with b:
            variation = latest["Variation absolue"]
            st.metric(
                "Variation absolue",
                "N/D" if pd.isna(variation) else f"{variation:,.3f}"
            )

        with c:
            pct = latest["Variation (%)"]
            st.metric(
                "Variation relative",
                "N/D" if pd.isna(pct) else f"{pct:,.2f} %"
            )

        fig = px.line(
            df_analysis,
            x="Année",
            y="Valeur",
            markers=True,
            title=f"{indicator_name} — {country_name}"
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Signal descriptif sur la variation récente
        pct = latest["Variation (%)"]

        st.markdown("### Signal descriptif")

        if pd.isna(pct):
            st.info(
                "Pas assez de données successives pour calculer "
                "la variation récente."
            )
        elif pct >= 5:
            st.success(
                f"Variation positive de {pct:.2f} %. "
                "Il s'agit d'une hausse observée ; son interprétation "
                "économique dépend de la nature de l'indicateur."
            )
        elif pct <= -5:
            st.warning(
                f"Variation négative de {pct:.2f} %. "
                "Cette baisse mérite une analyse du contexte économique "
                "et des autres indicateurs."
            )
        else:
            st.info(
                f"Variation récente de {pct:.2f} %. "
                "La variation reste comprise entre -5 % et +5 %."
            )

        st.markdown("### Tableau d'analyse")

        st.dataframe(
            df_analysis,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Télécharger l'analyse",
            data=df_analysis.to_csv(index=False).encode("utf-8-sig"),
            file_name="analyse_economique.csv",
            mime="text/csv"
        )

        st.caption(
            "Une variation n'est pas automatiquement une opportunité "
            "ou un risque. Il faut tenir compte du contexte, de la "
            "qualité des données et d'autres variables économiques."
        )
    else:
        st.warning(
            "Données indisponibles pour cette série. "
            "Essaie un autre indicateur."
        )

# =========================================================
# PAGE 10: SOURCES & METHODOLOGY
# =========================================================

elif page == "Sources & méthodologie":
    st.markdown("## 📚 Sources & méthodologie")

    st.markdown("### Sources institutionnelles")
    show_source_links(OTHER_SOURCES)

    st.markdown("### Marchés financiers")
    show_source_links(MARKET_SOURCES)

    st.markdown("### Banques centrales")
    show_source_links(CENTRAL_BANKS)

    st.markdown("### Méthodologie")

    st.markdown("""
    **1. Données économiques**

    Les séries de la Banque mondiale sont récupérées depuis son API
    publique. Les valeurs nulles sont exclues des séries affichées.
    La dernière observation disponible n'est pas nécessairement celle
    de l'année en cours.

    **2. Comparaison internationale**

    Les comparaisons utilisent les observations disponibles par pays.
    Les années de référence peuvent différer : il faut vérifier l'année
    avant de conclure qu'un pays dépasse un autre.

    **3. Marchés et politique monétaire**

    Les liens donnent accès aux sources officielles. Les cotations
    boursières en direct, les taux directeurs actuels et les actualités
    ne sont pas considérés comme intégrés automatiquement sans connexion
    à une API ou récupération vérifiée.

    **4. Analyse**

    Les variations sont des calculs descriptifs effectués à partir
    des observations récupérées. Elles ne constituent ni une preuve
    de causalité ni une prévision certaine.

    **5. Transparence**

    Aucune donnée manquante n'est remplacée par une valeur inventée.
    Les résultats doivent être interprétés selon la source, la période,
    l'unité et la définition de chaque indicateur.
    """)

    st.markdown("### Dernière actualisation de l'application")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    st.caption(
        "Cette heure indique l'affichage de la page, pas l'heure "
        "de publication de chaque statistique."
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="display:flex;justify-content:space-between;
    gap:12px;flex-wrap:wrap;color:#98a9c5;font-size:12px;">
        <span>🌐 Strategic Radar Maroc</span>
        <span>Veille → Données → Analyse → Décision</span>
        <span>Prototype académique</span>
    </div>
    """,
    unsafe_allow_html=True
)