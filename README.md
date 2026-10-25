# Strategic Radar Maroc

**Plateforme académique d'intelligence économique et financière.**

## Fonctionnalités

- Tableau de bord économique.
- Indicateurs macroéconomiques de plusieurs pays.
- PIB, croissance, inflation, chômage et population.
- Dette publique, investissement étranger et commerce, selon les données disponibles.
- Analyse historique et comparaison entre deux pays.
- Focus sur l'économie marocaine.
- Accès aux sources officielles des banques centrales.
- Accès aux sources des marchés financiers.
- Références pour les devises et les matières premières.
- Export des séries statistiques au format CSV.
- Méthodologie et limites des données documentées.

## Sources de données

Les séries macroéconomiques sont récupérées depuis l'API publique de la Banque mondiale :

https://api.worldbank.org/v2/

Sources marocaines complémentaires :

- https://www.hcp.ma/
- https://bds.hcp.ma/
- https://www.bkam.ma/
- https://www.oc.gov.ma/
- https://www.casablanca-bourse.com/
- https://www.ammc.ma/

## Transparence

Les dernières années disponibles varient selon l'indicateur. Les données peuvent être révisées par l'organisme source.

Les rubriques consacrées aux banques centrales, aux marchés financiers, aux devises et aux matières premières donnent accès aux sources de référence. Elles ne prétendent pas afficher des cours en direct sans fournisseur de données connecté.

Les comparaisons présentées sont descriptives et ne constituent pas des conclusions causales ni des conseils financiers.

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py