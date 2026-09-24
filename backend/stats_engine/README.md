# PROSTATIA Stats Engine

## Overview
The **PROSTATIA Stats Engine** is a deterministic, high‑performance backend service that provides a comprehensive suite of statistical methods, machine‑learning models, data‑preprocessing pipelines, visualisation utilities, and data‑ingestion capabilities. It is designed to be consumed by the AI Orchestrator and other micro‑services in the PROSTATIA platform.

## Features
- **Multivariate methods**: PCA, ICA, LDA, t‑SNE, UMAP, DBSCAN, etc.
- **Supervised modeling**: Logistic regression, GLM, Ridge, Lasso, SVM, decision trees, Random Forest, XGBoost.
- **Statistical inference**: Classical hypothesis tests, confidence intervals, Bayesian inference.
- **Pre‑processing pipelines**: Imputation, scaling, heatmap & dendrogram visualisations.
- **Data ingestion**: CSV, Parquet, SQL (via SQLAlchemy), MongoDB (via PyMongo).
- **Rich documentation**: `README.md`, `docs/formules.md`, comprehensive docstrings throughout the codebase.

## Installation
```bash
# From the project root (PROSTATIA/backend/stats_engine)
poetry install   # installs all dependencies defined in pyproject.toml
```

## Running the API
```bash
uvicorn app.main:app --reload   # start the FastAPI server on http://localhost:8000
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/methods` | List all available method fiches. |
| `GET` | `/api/v1/methods/{method_id}` | Retrieve details of a specific method. |
| `POST` | `/api/v1/execute` | Execute a statistical or modelling method. |
| `POST` | `/api/v1/preprocess` | Run a preprocessing pipeline (e.g., `basic_pipeline`). |
| `POST` | `/api/v1/ingest` | Ingest data from CSV, Parquet, SQL, or MongoDB. |

## Contributing
- Follow the existing code style (PEP8, Black, Ruff). 
- Add new `MethodFiche` entries for any new statistical method.
- Update `docs/formules.md` with any new formulas or algorithm descriptions.
- Ensure every public function/class has a clear docstring.

## License
Apache‑2.0 © PROSTATIA Team
