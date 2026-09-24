# AI Orchestrator
Service gérant les LLM et la planification de l'exécution.

## Probabilités & Statistiques avancées
PROSTATIA expose désormais un large catalogue de lois de probabilité (normale, Student‑t, chi‑carré, binomiale, Poisson, etc.) et des fonctions statistiques avancées (skewness, kurtosis, test de proportion, ANOVA).  Les méthodes sont disponibles via le registre global et peuvent être appelées directement avec l'endpoint `/api/v1/multivariate` ou via le nouveau point `/api/v1/advanced_stats`.

### Exemple d’utilisation (cURL)
```bash
curl -X POST http://localhost:8000/api/v1/multivariate \
  -H "Content-Type: application/json" \
  -d '{
        "method_id": "probability.normal",
        "params": {
            "mu": 0,
            "sigma": 1,
            "x": 0.5,
            "query_type": "pdf"
        }
    }'
```
Le corps de la réponse contient `pdf`, `cdf`, `mean`, `variance`, etc., ainsi que `execution_time_ms`.

### Fonctions avancées
```bash
curl -X POST http://localhost:8000/api/v1/advanced_stats \
  -H "Content-Type: application/json" \
  -d '{
        "method_id": "skewness",
        "params": {"data": [1,2,3,4,5], "bias": false}
    }'
```
Renvoie `{ "skewness": 0.0 }`.

