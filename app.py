import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timezone

# =========================================================
# STRATEGIC RADAR MAROC
# Données macroéconomiques : API publique Banque mondiale
# Marchés : liens officiels, sans cours fictifs
# =========================================================

st.set_page_config(
    page_title="Strategic Radar Maroc",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#08111f"
PANEL = "#111e30"
BORDER = "#25364d"
CYAN = "#54d6e8"
MUTED = "#9eb0c7"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {{ color-scheme: dark; }}
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background: {NAVY}; color: #edf4ff; }}
[data-testid="stHeader"] {{ background: rgba(8,17,31,.96); }}
[data-testid="stSidebar"] {{ background: #0b1626; border-right: 1px solid {BORDER}; }}
[data-testid="stSidebar"] * {{ color: #e8f0fc; }}

.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1500px;
}}

h1, h2, h3 {{
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -.03em;
}}

h1 {{ font-size: clamp(2rem,4vw,3.1rem) !important; }}
h2 {{ font-size: clamp(1.35rem,2.3vw,1.8rem) !important; }}
p, li {{ line-height: 1.65; }}

.eyebrow {{
    color: {CYAN};
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .19em;
    text-transform: uppercase;
}}

.hero {{
    background: linear-gradient(120deg,#132640 0%,#102033 55%,#12313c 100%);
    border: 1px solid #29445f;
    border-radius: 22px;
    padding: 28px 30px;
    margin: 6px 0 22px 0;
}}

.hero p {{
    color: #b9c8da;
    max-width: 850px;
    margin-bottom: 0;
    font-size: 1rem;
}}

.pill {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #183448;
    color: {CYAN};
    font-size: .72rem;
    font-weight: 700;
    margin-right: 6px;
}}

.metric-card {{
    background: linear-gradient(145deg,#142239,#101a2a);
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px 18px 15px;
    min-height: 130px;
}}

.metric-label {{ color: {MUTED}; font-size: .82rem; }}

.metric-value {{
    font-family: 'Manrope', sans-serif;
    font-size: clamp(1.25rem,2vw,1.9rem);
    font-weight: 800;
    margin: 7px 0;
    color: #f2f7ff;
    overflow-wrap: anywhere;
}}

.metric-note {{ color: {CYAN}; font-size: .75rem; }}

.section-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 15px;
}}

.small-muted {{ color: {MUTED}; font-size: .85rem; }}
a {{ color: {CYAN} !important; }}

.stButton > button,
.stDownloadButton > button {{
    border-radius: 10px;
    border: 1px solid #2c4963;
}}

[data-testid="stPlotlyChart"] {{
    border: 1px solid {BORDER};
    border-radius: 14px;
    overflow: hidden;
}}

hr {{ border-color: {BORDER}; }}

@media (max-width: 700px) {{
    .block-container {{
        padding-left: .8rem;
        padding-right: .8rem;
    }}
    .hero {{
        padding: 20px;
        border-radius: 16px;
    }}
    .metric-card {{
        padding: 13px;
        min-height: 115px;
    }}
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DONNÉES ET INDICATEURS
# =========================================================

WB_API = "https://api.worldbank.org/v2"

WB_COUNTRIES = {
    "Maroc": "MAR",
    "France": "FRA",
    "Espagne": "ESP",
    "Allemagne": "DEU",
    "États-Unis": "USA",
    "Chine": "CHN",
    "Inde": "IND",
    "Brésil": "BRA",
    "Italie": "ITA",
    "Royaume-Uni": "GBR",
    "Japon": "JPN",
    "Canada": "CAN",
    "Tunisie": "TUN",
    "Égypte": "EGY",
    "Turquie": "TUR",
    "Afrique du Sud": "ZAF",
    "Arabie saoudite": "SAU",
    "Sénégal": "SEN",
    "Côte d'Ivoire": "CIV",
    "Portugal": "PRT",
}

INDICATORS = {
    "PIB (USD courants)": ("NY.GDP.MKTP.CD", "USD"),
    "Croissance du PIB (%)": ("NY.GDP.MKTP.KD.ZG", "%"),
    "Inflation, prix à la consommation (%)": ("FP.CPI.TOTL.ZG", "%"),
    "Chômage (%)": ("SL.UEM.TOTL.ZS", "%"),
    "Population": ("SP.POP.TOTL", "personnes"),
    "Dette publique (% du PIB)": ("GC.DOD.TOTL.GD.ZS", "%"),
    "Investissement étranger direct (% du PIB)": (
        "BX.KLT.DINV.WD.GD.ZS", "%"
    ),
    "Commerce (% du PIB)": ("NE.TRD.GNFS.ZS", "%"),
}


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_indicator(country_code: str, indicator_code: str):
    """Récupère une série historique depuis l'API de la Banque mondiale."""
    url = (
        f"{WB_API}/country/{country_code}"
        f"/indicator/{indicator_code}"
    )

    response = requests.get(
        url,
        params={"format": "json", "per_page": 70},
        timeout=18,
    )
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        return pd.DataFrame(columns=["Année", "Valeur"])

    if not payload[1]:
        return pd.DataFrame(columns=["Année", "Valeur"])

    rows = [
        {
            "Année": int(item["date"]),
            "Valeur": item["value"],
        }
        for item in payload[1]
        if item.get("value") is not None
    ]

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values("Année").reset_index(drop=True)

    return df


def latest_value(df):
    if df.empty:
        return None, None

    row = df.iloc[-1]
    return int(row["Année"]), float(row["Valeur"])


def fmt_value(value, unit):
    if value is None:
        return "N/D"

    if unit == "USD":
        if abs(value) >= 1e12:
            return f"{value / 1e12:,.2f} T$".replace(",", " ")

        if abs(value) >= 1e9:
            return f"{value / 1e9:,.2f} Md$".replace(",", " ")

        return f"{value:,.0f} $".replace(",", " ")

    if unit == "personnes":
        return f"{value:,.0f}".replace(",", " ")

    return f"{value:.2f} %"


def style_chart(fig, height=400):
    fig.update_layout(
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font_color="#eaf2ff",
        height=height,
        margin=dict(l=15, r=15, t=55, b=15),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        gridcolor="#293b51",
        zerolinecolor="#293b51",
    )
    return fig


def source_link(label, url, desc):
    st.markdown(
        f"**[{label}]({url})**  \n"
        f"<span class='small-muted'>{desc}</span>",
        unsafe_allow_html=True,
    )


def official_source_card(name, url, description):
    st.markdown(
        f"""
        <div class="section-card">
            <h3>{name}</h3>
            <p class="small-muted">{description}</p>
            <a href="{url}" target="_blank">
                Ouvrir la source officielle ↗
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        "<div class='eyebrow'>Global intelligence</div>",
        unsafe_allow_html=True,
    )
    st.markdown("## 🌐 Strategic Radar")
    st.caption("MAROC · ÉCONOMIE · FINANCE")

    page = st.radio(
        "NAVIGATION",
        [
            "Vue d'ensemble",
            "Macroéconomie",
            "Focus Maroc",
            "Banques centrales",
            "Marchés financiers",
            "Devises & matières premières",
            "Analyse économique",
            "Sources & méthodologie",
        ],
    )

    st.divider()
    st.caption("Données macroéconomiques : Banque mondiale")
    st.caption(
        "Les cours de marché ne sont pas affichés sans fournisseur connecté."
    )


st.markdown(
    "<div class='eyebrow'>Strategic Radar Maroc / Intelligence économique</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="pill">DONNÉES SOURCÉES</div>
        <div class="pill">TABLEAU DE BORD</div>
        <h1>
            Comprendre l’économie.<br>
            <span style="color:#54d6e8">
                Éclairer les décisions.
            </span>
        </h1>
        <p>
            Une plateforme d’analyse économique et financière pour suivre
            les indicateurs disponibles, comparer les pays et consulter
            les sources institutionnelles — avec une séparation claire
            entre données observées et interprétation.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 1. VUE D'ENSEMBLE
# =========================================================

if page == "Vue d'ensemble":
    st.subheader("Vue d’ensemble")

    st.markdown(
        "Un point d’entrée vers les principaux modules. "
        "Les indicateurs utilisent la dernière observation disponible "
        "de la Banque mondiale."
    )

    selected = st.selectbox(
        "Pays de référence",
        list(WB_COUNTRIES.keys()),
        index=0,
        key="overview_country",
    )

    code = WB_COUNTRIES[selected]

    chosen = [
        "PIB (USD courants)",
        "Croissance du PIB (%)",
        "Inflation, prix à la consommation (%)",
        "Chômage (%)",
    ]

    cols = st.columns(4)

    for col, name in zip(cols, chosen):
        indicator_code, unit = INDICATORS[name]

        with col:
            try:
                df = fetch_indicator(code, indicator_code)
                year, value = latest_value(df)

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{name}</div>
                        <div class="metric-value">
                            {fmt_value(value, unit)}
                        </div>
                        <div class="metric-note">
                            {"Année " + str(year) if year else "Donnée indisponible"}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{name}</div>
                        <div class="metric-value">N/D</div>
                        <div class="metric-note">
                            Source momentanément indisponible
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.write("")

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("### Évolution macroéconomique")

        metric = st.selectbox(
            "Indicateur à visualiser",
            list(INDICATORS.keys()),
            key="overview_indicator",
        )

        indicator_code, unit = INDICATORS[metric]

        try:
            df = fetch_indicator(code, indicator_code)

            if df.empty:
                st.info("Aucune observation disponible pour cette sélection.")

            else:
                fig = px.line(
                    df,
                    x="Année",
                    y="Valeur",
                    markers=True,
                    title=metric,
                )

                fig.update_traces(
                    line=dict(color=CYAN, width=3),
                    marker=dict(size=6),
                )

                fig.update_layout(
                    paper_bgcolor=PANEL,
                    plot_bgcolor=PANEL,
                    font_color="#eaf2ff",
                    margin=dict(l=12, r=12, t=55, b=12),
                    height=360,
                    xaxis_title="",
                    yaxis_title=unit,
                )

                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(gridcolor="#293b51")

                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    f"Source : Banque mondiale · "
                    f"Dernière observation : {int(df.iloc[-1]['Année'])}."
                )

        except Exception:
            st.warning(
                "La source n'a pas répondu. Réessaie dans quelques instants."
            )

    with right:
        st.markdown("### Accès rapide")

        quick = [
            ("🌍", "Macroéconomie", "PIB, inflation, chômage et croissance"),
            ("🇲🇦", "Focus Maroc", "Indicateurs du Maroc et séries historiques"),
            ("🏦", "Banques centrales", "Décisions et communiqués officiels"),
            ("📈", "Marchés financiers", "Accès aux places et indices de marché"),
            ("🧠", "Analyse économique", "Comparaisons et lecture des variations"),
        ]

        for icon, title, desc in quick:
            st.markdown(
                f"""
                <div class="section-card">
                    <b>{icon} &nbsp; {title}</b>
                    <div class="small-muted">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "Les dernières années disponibles dépendent de l’indicateur. "
        "Les données peuvent être révisées par l’organisme source."
    )


# =========================================================
# 2. MACROÉCONOMIE
# =========================================================

elif page == "Macroéconomie":
    st.subheader("Macroéconomie")

    c1, c2 = st.columns(2)

    with c1:
        country = st.selectbox(
            "Pays",
            list(WB_COUNTRIES.keys()),
            key="macro_country",
        )

    with c2:
        metric = st.selectbox(
            "Indicateur",
            list(INDICATORS.keys()),
            key="macro_metric",
        )

    indicator_code, unit = INDICATORS[metric]

    try:
        df = fetch_indicator(
            WB_COUNTRIES[country],
            indicator_code,
        )

        if df.empty:
            st.warning("Aucune donnée disponible pour ce pays et cet indicateur.")

        else:
            year, value = latest_value(df)

            a, b, c = st.columns(3)
            a.metric("Dernière valeur", fmt_value(value, unit))
            b.metric("Année observée", year)
            c.metric("Observations disponibles", len(df))

            fig = px.line(
                df,
                x="Année",
                y="Valeur",
                markers=True,
                title=f"{metric} — {country}",
            )

            fig.update_traces(line=dict(color=CYAN, width=3))
            style_chart(fig, height=420)
            fig.update_yaxes(title=unit)

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Série historique")
            st.dataframe(
                df.sort_values("Année", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Télécharger la série CSV",
                df.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"{country}_{indicator_code}.csv",
                mime="text/csv",
            )

            st.caption(
                f"Source : Banque mondiale · Indicateur {indicator_code} "
                f"· Dernière observation : {year}."
            )

    except Exception:
        st.error(
            "Impossible de récupérer les données pour le moment. "
            "Vérifie la connexion et réessaie."
        )


# =========================================================
# 3. FOCUS MAROC
# =========================================================

elif page == "Focus Maroc":
    st.subheader("🇲🇦 Focus Maroc")

    st.markdown(
        "Indicateurs macroéconomiques du Maroc récupérés depuis "
        "l’API publique de la Banque mondiale."
    )

    metric = st.selectbox(
        "Indicateur",
        list(INDICATORS.keys()),
        key="morocco_metric",
    )

    indicator_code, unit = INDICATORS[metric]

    try:
        df = fetch_indicator("MAR", indicator_code)

        if df.empty:
            st.warning("Aucune observation disponible.")

        else:
            year, value = latest_value(df)

            x, y, z = st.columns(3)
            x.metric("Dernière valeur disponible", fmt_value(value, unit))
            y.metric("Année observée", year)
            z.metric("Code indicateur", indicator_code)

            fig = px.area(
                df,
                x="Année",
                y="Valeur",
                title=metric,
            )

            fig.update_traces(
                line=dict(color=CYAN, width=2),
                fillcolor="rgba(84,214,232,.12)",
            )

            style_chart(fig, height=390)
            fig.update_yaxes(title=unit)

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                df.sort_values("Année", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Exporter les données",
                df.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"Maroc_{indicator_code}.csv",
                mime="text/csv",
            )

    except Exception:
        st.error("La Banque mondiale est momentanément inaccessible.")

    st.markdown("### Sources marocaines complémentaires")

    source_link(
        "Haut-Commissariat au Plan (HCP)",
        "https://www.hcp.ma/",
        "Statistiques nationales, enquêtes et publications.",
    )

    source_link(
        "Base de données statistiques du HCP",
        "https://bds.hcp.ma/",
        "Séries statistiques disponibles.",
    )

    source_link(
        "Office des Changes",
        "https://www.oc.gov.ma/",
        "Commerce extérieur et balance des paiements.",
    )

    source_link(
        "Bank Al-Maghrib",
        "https://www.bkam.ma/",
        "Politique monétaire et rapports économiques.",
    )


# =========================================================
# 4. BANQUES CENTRALES
# =========================================================

elif page == "Banques centrales":
    st.subheader("Banques centrales")

    st.markdown(
        "Consulte les décisions et communiqués à la source. "
        "Les taux ne sont pas recopiés ici sans extraction vérifiée et datée."
    )

    banks = [
        (
            "🇲🇦 Bank Al-Maghrib",
            "https://www.bkam.ma/",
            "Communiqués de politique monétaire, rapports et décisions.",
        ),
        (
            "🇺🇸 Federal Reserve (Fed)",
            "https://www.federalreserve.gov/monetarypolicy.htm",
            "Décisions et documents de politique monétaire.",
        ),
        (
            "🇪🇺 Banque centrale européenne (BCE)",
            "https://www.ecb.europa.eu/press/govcdec/mopo/html/index.en.html",
            "Décisions officielles de politique monétaire.",
        ),
        (
            "🇬🇧 Bank of England",
            "https://www.bankofengland.co.uk/monetary-policy",
            "Décisions et rapports monétaires.",
        ),
    ]

    for name, url, desc in banks:
        official_source_card(name, url, desc)

    st.warning(
        "Pour comparer les taux, vérifie la date de décision et le type de taux : "
        "taux directeur, taux de dépôt ou taux de refinancement."
    )


# =========================================================
# 5. MARCHÉS FINANCIERS
# =========================================================

elif page == "Marchés financiers":
    st.subheader("Marchés financiers")

    st.markdown(
        "Accès aux sources des places financières. Les valeurs de marché "
        "ne sont pas affichées dans ce prototype sans fournisseur de données connecté."
    )

    markets = [
        (
            "🇲🇦 Bourse de Casablanca",
            "https://www.casablanca-bourse.com/",
            "Marché marocain, indices, cours et publications.",
        ),
        (
            "🇺🇸 Nasdaq",
            "https://www.nasdaq.com/market-activity",
            "Indices et informations de marché.",
        ),
        (
            "🇺🇸 S&P 500",
            "https://www.spglobal.com/spdji/en/indices/equity/sp-500/",
            "Page officielle de l’indice S&P 500.",
        ),
        (
            "🇫🇷 Euronext Paris / CAC 40",
            "https://live.euronext.com/",
            "Informations de marché et indices.",
        ),
        (
            "🇩🇪 Deutsche Börse",
            "https://www.deutsche-boerse.com/",
            "Informations sur les marchés allemands.",
        ),
        (
            "📑 AMMC",
            "https://www.ammc.ma/",
            "Réglementation et informations du marché des capitaux marocain.",
        ),
    ]

    for name, url, desc in markets:
        official_source_card(name, url, desc)


# =========================================================
# 6. DEVISES ET MATIÈRES PREMIÈRES
# =========================================================

elif page == "Devises & matières premières":
    st.subheader("Devises & matières premières")

    st.markdown(
        "Les cours changent fréquemment. Pour éviter d’afficher des valeurs "
        "périmées ou inventées, cette rubrique renvoie aux sources de référence."
    )

    links = [
        (
            "💱 Taux de change — Office des Changes",
            "https://www.oc.gov.ma/",
            "Références marocaines sur les changes.",
        ),
        (
            "💶 BCE — taux de change de référence",
            "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html",
            "Taux de change de référence de l’euro.",
        ),
        (
            "🥇 Or — LBMA",
            "https://www.lbma.org.uk/prices-and-data",
            "Prix et données de référence du marché de l’or.",
        ),
        (
            "🛢️ Énergie — U.S. EIA",
            "https://www.eia.gov/",
            "Données énergétiques et séries statistiques.",
        ),
        (
            "🧾 Banque mondiale — matières premières",
            "https://www.worldbank.org/en/research/commodity-markets",
            "Rapports et données de prix des matières premières.",
        ),
    ]

    for name, url, desc in links:
        official_source_card(name, url, desc)


# =========================================================
# 7. ANALYSE ÉCONOMIQUE
# =========================================================

elif page == "Analyse économique":
    st.subheader("Analyse économique")

    st.markdown(
        "Compare deux pays sur un indicateur commun. "
        "Le tableau de bord calcule les écarts observés ; "
        "l’interprétation doit tenir compte du contexte économique."
    )

    a, b = st.columns(2)

    with a:
        country_a = st.selectbox(
            "Pays A",
            list(WB_COUNTRIES.keys()),
            index=0,
            key="compare_country_a",
        )

    with b:
        country_b = st.selectbox(
            "Pays B",
            list(WB_COUNTRIES.keys()),
            index=1,
            key="compare_country_b",
        )

    metric = st.selectbox(
        "Indicateur à comparer",
        list(INDICATORS.keys()),
        key="compare_metric",
    )

    indicator_code, unit = INDICATORS[metric]

    try:
        da = fetch_indicator(
            WB_COUNTRIES[country_a],
            indicator_code,
        ).rename(columns={"Valeur": country_a})

        db = fetch_indicator(
            WB_COUNTRIES[country_b],
            indicator_code,
        ).rename(columns={"Valeur": country_b})

        merged = pd.merge(
            da,
            db,
            on="Année",
            how="inner",
        ).sort_values("Année")

        if merged.empty:
            st.info("Pas d’années communes disponibles pour les deux pays.")

        else:
            latest = merged.iloc[-1]
            year = int(latest["Année"])

            value_a = float(latest[country_a])
            value_b = float(latest[country_b])

            st.markdown(f"**Dernière année commune : {year}**")

            c1, c2, c3 = st.columns(3)
            c1.metric(country_a, fmt_value(value_a, unit))
            c2.metric(country_b, fmt_value(value_b, unit))
            c3.metric(
                "Écart A − B",
                fmt_value(value_a - value_b, unit),
            )

            fig = px.line(
                merged,
                x="Année",
                y=[country_a, country_b],
                markers=True,
                title=metric,
            )

            style_chart(fig, height=400)
            fig.update_yaxes(title=unit)

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                merged.sort_values("Année", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Télécharger la comparaison CSV",
                merged.to_csv(index=False).encode("utf-8-sig"),
                file_name="comparaison_pays.csv",
                mime="text/csv",
            )

            if value_a > value_b:
                st.info(
                    f"Sur la dernière année commune, {metric.lower()} "
                    f"est numériquement plus élevé pour {country_a}. "
                    "Cela ne signifie pas automatiquement une meilleure performance."
                )

            elif value_a < value_b:
                st.info(
                    f"Sur la dernière année commune, {metric.lower()} "
                    f"est numériquement plus élevé pour {country_b}. "
                    "Cela ne suffit pas à conclure sur la performance globale."
                )

            else:
                st.info(
                    "Les deux valeurs sont identiques pour la dernière année commune."
                )

    except Exception:
        st.error(
            "Impossible de récupérer les données comparées. Réessaie plus tard."
        )

    st.caption(
        "Le moteur fournit une comparaison descriptive, "
        "pas une causalité automatique ni un conseil financier."
    )


# =========================================================
# 8. SOURCES ET MÉTHODOLOGIE
# =========================================================

else:
    st.subheader("Sources & méthodologie")

    st.markdown("### Comment lire les données")

    st.markdown("""
    - **Données macroéconomiques :** API publique de la Banque mondiale.
    - **Fréquence :** annuelle pour les indicateurs affichés ici.
    - **Dernière observation :** dernière valeur non manquante renvoyée
      par la source, pas nécessairement l’année courante.
    - **Mise à jour :** mise en cache pendant 24 heures dans l’application ;
      les organismes peuvent réviser les séries.
    - **Marchés, taux et matières premières :** liens vers les sources officielles ;
      aucun cours en direct n’est simulé.
    - **Analyse :** les écarts observés ne démontrent pas une relation de cause à effet.
    """)

    st.markdown("### Sources principales")

    sources = [
        ("Banque mondiale — données", "https://data.worldbank.org/"),
        ("API Banque mondiale", "https://api.worldbank.org/v2/"),
        ("HCP Maroc", "https://www.hcp.ma/"),
        ("Base statistique HCP", "https://bds.hcp.ma/"),
        ("Bank Al-Maghrib", "https://www.bkam.ma/"),
        ("Office des Changes", "https://www.oc.gov.ma/"),
        ("Bourse de Casablanca", "https://www.casablanca-bourse.com/"),
        ("AMMC", "https://www.ammc.ma/"),
    ]

    for name, url in sources:
        st.markdown(f"- [{name}]({url})")

    st.caption(
        "Session consultée le "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}."
    )


# =========================================================
# PIED DE PAGE
# =========================================================

st.divider()

st.markdown(
    """
    <div class="small-muted">
        🌐 Strategic Radar Maroc · Prototype académique
        · Veille → Données → Comparaison → Décision
    </div>
    """,
    unsafe_allow_html=True,
)