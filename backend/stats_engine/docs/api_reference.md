# Référence de l'API & Documentation du Code

Cette page présente les routes de l'API REST exposées par le Stats Engine ainsi que les docstrings des modules Python.

---

## Endpoints de l'API REST

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/health` | Vérification de l'état de santé du service. |
| `GET` | `/api/v1/methods` | Liste l'ensemble des fiches méthodologiques enregistrées (`MethodFiche`). |
| `GET` | `/api/v1/methods/{method_id}` | Récupère le détail d'une méthode spécifique (entrées, hypothèses, fallbacks, sorties). |
| `POST` | `/api/v1/execute` | Exécute un calcul statistique en appliquant la validation d'hypothèses et les fallbacks. |
| `POST` | `/api/v1/preprocess` | Exécute un pipeline de prétraitement (imputation, normalisation, heatmaps, dendrogrammes). |
| `POST` | `/api/v1/ingest` | Charge et valide des données depuis une source CSV, Parquet, SQL ou MongoDB. |

---

## Modules Python

### Moteur d'exécution & validation

::: app.engine.executor
    options:
      show_root_heading: true

::: app.engine.validators
    options:
      show_root_heading: true

---

### Wrappers de calculs statistiques

::: app.services.scipy_wrapper
    options:
      show_root_heading: true

---

### Modélisation & Apprentissage

::: app.services.modeling
    options:
      show_root_heading: true

---

### Méthodes multivariées étendues

::: app.services.multivariate_extended
    options:
      show_root_heading: true

---

### Ingestion des données

::: app.services.data_ingestion
    options:
      show_root_heading: true
