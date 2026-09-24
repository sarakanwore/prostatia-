# STATIA Visualization Service (viz_service)

Version 1.0.0

Le **viz_service** est le microservice de restitution visuelle de la plateforme **STATIA**.
Il transforme les données brutes et les résultats d'analyses statistiques (tests, régressions, distributions, corrélations) en spécifications graphiques déclaratives interactives prêtes pour le frontend :
- **Plotly JSON** (data, layout, config)
- **Vega-Lite JSON** (spécification $schema v5)

## Types de graphiques supportés
- **Histogram & Density** : Répartition univariée, découpage automatique de classes, KDE optionnel.
- **Boxplot & Outliers** : Boîte à moustaches avec détection d'outliers 1.5x IQR.
- **Scatter plot & Trendline** : Nuage de points avec droite de régression linéaire OLS optionnelle.
- **Correlation Heatmap** : Matrice de corrélation interactive.
- **Bar Chart** : Histogrammes catégoriels et moyennes comparées.
- **Line Chart** : Séries temporelles et tendances.
- **Residuals Plot** : Diagnostic de régression linéaire (résidus vs prédictions).

## Démarrage local
```bash
poetry install
poetry run uvicorn app.main:app --port 8003 --reload
```
