# Strategic Radar Maroc

**Prototype académique Streamlit d’intelligence économique multisectorielle.**

## Fonctionnalités

- Analyse économique de plusieurs pays.
- Comparaison des indicateurs entre pays.
- Graphiques et tableaux statistiques.
- Export des données disponibles en CSV.
- Rubriques consacrées aux villes, régions et entreprises.
- Accès aux sources institutionnelles officielles.
- Simulateur pédagogique et analyse sectorielle.

## Déploiement

- **Branche :** `main`
- **Fichier principal :** `app.py`
- **Dépendances :** `requirements.txt`

## Transparence des données

Les graphiques de démonstration sectorielle utilisent des valeurs fictives, clairement signalées.

La rubrique « Pays » interroge l’API publique de la Banque mondiale pour récupérer les indicateurs disponibles. Les années et les données disponibles varient selon l’indicateur et peuvent être révisées par la source.

Les rubriques « Villes & régions » et « Entreprises » donnent accès aux sources officielles. Elles ne prétendent pas automatiser la récupération des données locales et financières lorsqu'aucune connexion n'est configurée.

## Lancement local

```bash
pip install -r requirements.txt
streamlit run app.py