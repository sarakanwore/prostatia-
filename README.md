# STATIA – PROSTATIA Backend

## Présentation

**PROSTATIA** est une plateforme d'analyse statistique micro‑service qui regroupe :
- **Stats Engine** (Python / FastAPI) : calculs statistiques, modèles de machine‑learning, ingestion de données.
- **Data Service** (Rust) : ingestion rapide de fichiers, stockage et pré‑traitement.
- **AI Orchestrator** (Python) : traduction des requêtes naturelles en plans d'exécution, appels aux différents services.
- **Gateway** (Rust / Axum) : point d’entrée unique, authentification JWT et routage vers les services internes.

Le tout est orchestré via Docker‑Compose pour faciliter le déploiement local et en production.

## Architecture

```
+-------------------+        +-------------------+        +-------------------+
|  Stats Engine     | <---► |  AI Orchestrator  | <---► |  Gateway (API)   |
|  (FastAPI)        |        |  (FastAPI)        |        |  (Axum)          |
+-------------------+        +-------------------+        +-------------------+
        ▲                                 ▲
        │                                 │
        │                                 │
        ▼                                 ▼
+-------------------+        +-------------------+
|  Data Service     |        |  PostgreSQL DB    |
|  (Rust)           |        |  (users, stats)   |
+-------------------+        +-------------------+
```

## Prérequis

- **Docker Desktop** (ou Docker Engine) ≥ 20.10
- **Python** 3.11 + `poetry`
- **Rust** 1.76 + `cargo`
- **Make** (facultatif, pour les scripts d’aide)

## Installation & lancement

```powershell
# cloner le dépôt
git clone https://github.com/your/repo.git
cd PROSTATIA/backend

# créer les fichiers .env (exemple fourni)
cp stats_engine/.env.example stats_engine/.env
cp ai_orchestrator/.env.example ai_orchestrator/.env

# démarrer les containers
docker compose up --build
```

Les services seront exposés :
- Stats Engine : `http://localhost:8000`
- Data Service : `http://localhost:8001`
- AI Orchestrator : `http://localhost:8002`
- Gateway : `http://localhost:8080`

## Tests

```bash
# depuis le répertoire du stats_engine
cd stats_engine
poetry install
poetry run pytest -v
```

## Documentation

- **README** – ce fichier.
- **docs/formules.md** – formules statistiques utilisées.
- Les docstrings présentes dans le code permettent de générer la documentation via MkDocs (`mkdocs build`).

## Contribution

1. Fork du dépôt.
2. Créez une branche `feature/…`.
3. Respectez le formatage (`black`, `ruff`, `cargo fmt`).
4. Ajoutez ou mettez à jour les tests.
5. Ouvrez une Pull Request.

## Licence

MIT – voir le fichier `LICENSE`.

---

*Ce README a été généré automatiquement pour offrir un point d’entrée clair aux développeurs et aux utilisateurs.*
# prostatia-
