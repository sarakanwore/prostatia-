# PROSTATIA Stats Engine

Bienvenue sur la documentation officielle du **PROSTATIA Stats Engine**.

Le Stats Engine est le composant central de calcul scientifique de la plateforme **PROSTATIA**. Il fournit un catalogue exhaustif de méthodes statistiques, d'inférence, de modélisation prédictive et d'analyse multivariée, encapsulé dans une architecture déterministe haute performance.

---

## Fonctionnalités principales

- **Tests d'hypothèses et validation préalable** : Vérification automatique des conditions d'application (normalité via Shapiro-Wilk, homoscédasticité via Levene, effectifs théoriques pour Chi²) et bascule automatique sur des alternatives non-paramétriques (Welch, Mann-Whitney, Kruskal-Wallis).
- **Lois de probabilité** : Calculs de densités, fonctions de répartition, quantiles et probabilités d'intervalles pour lois discrètes (Binomiale, Poisson, Hypergéométrique, Géométrique) et continues (Normale, Student, Chi², Fisher, Exponentielle, Uniforme).
- **Inférence statistique** : Intervalles de confiance (moyennes avec $\sigma$ connu ou inconnu, proportions) et tests Z.
- **Modélisation supervisée** : Régression linéaire MCO, Ridge, Lasso, Régression Logistique, SVM, Arbres de décision, Forêts Aléatoires et XGBoost.
- **Analyse multivariée & Réduction de dimension** : ACP normée, AFC, ACM, LDA, ICA, t-SNE, UMAP.
- **Clustering & Segmentation** : Classification Ascendante Hiérarchique (CAH), K-Means, DBSCAN.
- **Ingestion & Pipelines** : Ingestion native multi-formats (CSV, Parquet, bases relationnelles SQL via SQLAlchemy, bases NoSQL MongoDB) et prétraitement (imputation, standardisation, heatmaps, dendrogrammes).

---

## Démarrage rapide

### Installation locale

Le projet utilise **Poetry** pour la gestion des dépendances :

```bash
# Se placer dans le répertoire du service
cd backend/stats_engine

# Installer l'environnement virtuel et les dépendances
poetry install
```

### Lancement du serveur d'API

```bash
# Lancement avec rechargement automatique
poetry run uvicorn app.main:app --reload --port 8000
```

Le serveur sera accessible sur `http://localhost:8000`.  
La documentation interactive OpenAPI / Swagger est disponible sur `http://localhost:8000/docs`.

---

## Organisation de la documentation

- [Ingestion des données](ingestion.md) : Formats supportés, connecteurs de bases de données et pipelines.
- [Référence de l'API](api_reference.md) : Endpoints REST `/api/v1/`, schémas des requêtes et documentation du code.
- [Formules statistiques](formules.md) : Formulations mathématiques et références théoriques.
