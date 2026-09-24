import httpx
import os
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional

DATA_SERVICE_URL = os.environ.get("DATA_SERVICE_URL", "http://localhost:8001/api/v1")
STATS_ENGINE_URL = os.environ.get("STATS_ENGINE_URL", "http://localhost:8000/api/v1")
VIZ_SERVICE_URL = os.environ.get("VIZ_SERVICE_URL", "http://localhost:8003/api/v1")
GEO_SERVICE_URL = os.environ.get("GEO_SERVICE_URL", "http://localhost:8004/api/v1")

# Fallback local paths for dev if microservices are local
LOCAL_UPLOAD_DIRS = [
    Path("./uploads"),
    Path("../data_service/uploads"),
    Path("backend/data_service/uploads"),
    Path("c:/Users/HP/Downloads/PROSTATIA/backend/data_service/uploads"),
]

def _read_csv_fallback(dataset_id: str, columns: Optional[List[str]] = None) -> Dict[str, List[Any]]:
    for up_dir in LOCAL_UPLOAD_DIRS:
        csv_file = up_dir / f"{dataset_id}.csv"
        if csv_file.exists():
            with open(csv_file, mode="r", encoding="utf-8-sig", errors="replace") as f:
                reader = csv.DictReader(f)
                res: Dict[str, List[Any]] = {col: [] for col in (columns or reader.fieldnames or [])}
                for row in reader:
                    for c in res.keys():
                        val = row.get(c)
                        if val is None or val.strip() == "":
                            continue
                        try:
                            # Try float conversion
                            float_val = float(val)
                            res[c].append(int(float_val) if float_val.is_integer() else float_val)
                        except ValueError:
                            res[c].append(val)
                return res
    return {}

async def get_dataset_schema(dataset_id: str) -> dict:
    """Appelle le Data Service (Rust) pour récupérer le schéma d'un dataset."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{DATA_SERVICE_URL}/data/schema/{dataset_id}")
            if response.status_code == 200:
                return response.json().get("schema", {})
    except Exception:
        pass

    # Fallback to local parsing if data_service is offline
    cols_data = _read_csv_fallback(dataset_id)
    if cols_data:
        cols_schema = [
            {"name": k, "data_type": "Float64" if all(isinstance(v, (int, float)) for v in vals[:10]) else "Utf8", "null_count": 0}
            for k, vals in cols_data.items()
        ]
        return {
            "dataset_id": dataset_id,
            "row_count": len(next(iter(cols_data.values()))) if cols_data else 0,
            "columns": cols_schema
        }
    return {"dataset_id": dataset_id, "row_count": 0, "columns": []}

async def get_methods_catalog() -> list:
    """Appelle le Stats Engine (Python) pour récupérer le catalogue des méthodes."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{STATS_ENGINE_URL}/methods")
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return []

async def get_dataset_preview(dataset_id: str, limit: int = 100) -> list:
    """Récupère un échantillon de lignes pour affichage dans la table."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{DATA_SERVICE_URL}/data/preview/{dataset_id}?limit={limit}")
            if response.status_code == 200:
                return response.json().get("data", [])
    except Exception:
        pass
    
    # Fallback local
    cols_data = _read_csv_fallback(dataset_id)
    if cols_data:
        rows = []
        keys = list(cols_data.keys())
        n = min(limit, len(next(iter(cols_data.values()))) if cols_data else 0)
        for i in range(n):
            rows.append({k: cols_data[k][i] if i < len(cols_data[k]) else None for k in keys})
        return rows
    return []

async def get_dataset_columns(dataset_id: str, columns: List[str]) -> Dict[str, List[Any]]:
    """Extrait les colonnes sous forme de listes de valeurs pour le calcul statistique."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{DATA_SERVICE_URL}/data/columns/{dataset_id}",
                json={"columns": columns}
            )
            if response.status_code == 200:
                return response.json().get("data", {})
    except Exception:
        pass

    return _read_csv_fallback(dataset_id, columns)

async def execute_stats_method(method_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute la méthode statistique déterministe sur le Stats Engine."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{STATS_ENGINE_URL}/execute",
            json={"method_id": method_id, "payload": payload}
        )
        response.raise_for_status()
        return response.json()

async def generate_visualization(chart_type: str, chart_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Demande la génération de spécification graphique (Plotly) au Viz Service."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{VIZ_SERVICE_URL}/chart/{chart_type}",
                json=chart_payload
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("spec", {})
    except Exception:
        pass

    # Direct fallback Plotly spec
    return {
        "data": [{"type": chart_type, "values": chart_payload.get("values", [])}],
        "layout": {"title": chart_payload.get("title", "Visualisation PROSTATIA"), "template": "plotly_dark"}
    }
