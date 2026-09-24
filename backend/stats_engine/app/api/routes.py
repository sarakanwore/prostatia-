from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
import json
import pandas as pd
import io
from app.registry.schemas import MethodFiche
from app.registry.methods.hypothesis_testing import HYPOTHESIS_METHODS
from app.registry.methods.preprocessing import PREPROCESSING_METHODS
from app.registry.methods.regression import REGRESSION_METHODS
from app.registry.methods.descriptive import DESCRIPTIVE_METHODS
from app.registry.methods.ingestion import INGESTION_METHODS
from app.engine.data_ingestion import ingest
from app.engine.executor import executor_instance, GLOBAL_REGISTRY

router = APIRouter(prefix="/api/v1")

# Use complete global registry
METHODS_REGISTRY: Dict[str, MethodFiche] = GLOBAL_REGISTRY

@router.get("/methods", response_model=List[MethodFiche])
@router.get("/stats/methods", response_model=List[MethodFiche])
def list_methods():
    """List all available MethodFiche objects.

    Returns a list of method specifications exposed by the engine.
    """
    return list(METHODS_REGISTRY.values())

@router.get("/methods/{method_id}", response_model=MethodFiche)
@router.get("/stats/methods/{method_id}", response_model=MethodFiche)
def get_method(method_id: str):
    """
    Retourne les détails d'une fiche méthodologique spécifique.
    """
    if method_id not in METHODS_REGISTRY:
        raise HTTPException(status_code=404, detail="Method not found")
    return METHODS_REGISTRY[method_id]

from pydantic import BaseModel, Field
from fastapi import Body

class ExecuteRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "method_id": "summary_statistics",
                "payload": {
                    "data": [12.5, 14.8, 11.2, 15.6, 13.4, 18.2, 19.5, 10.8]
                }
            }
        },
        "extra": "allow"
    }

    method_id: Optional[str] = Field(None, description="Identifiant de la méthode (ex: summary_statistics, linear_regression, t_test_independent)")
    payload: Optional[Dict[str, Any]] = Field(None, description="Données d'entrée pour le calcul (ex: {'data': [...]})")
    data_payload: Optional[Dict[str, Any]] = Field(None, description="Données d'entrée alternatives")
    data: Optional[Any] = Field(None, description="Données directes")

def try_parse_json_lenient(text: str) -> Optional[Dict[str, Any]]:
    text = text.strip()
    if not text:
        return {}
    try:
        res = json.loads(text)
        if isinstance(res, dict):
            return res
    except Exception:
        pass

    # Handle accidental outer braces, e.g. "{ { ... } }" or "{ { ... } } }"
    candidate = text
    for _ in range(3):
        if candidate.startswith("{") and candidate.endswith("}"):
            candidate = candidate[1:-1].strip()
            try:
                res = json.loads(candidate)
                if isinstance(res, dict):
                    return res
            except Exception:
                pass
        else:
            break
    return None

@router.post(
    "/execute",
    openapi_extra={
        "requestBody": {
            "required": False,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "method_id": {
                                "type": "string",
                                "description": "Identifiant de la méthode (ex: summary_statistics, linear_regression, t_test_independent)"
                            },
                            "payload": {
                                "type": "object",
                                "description": "Données d'entrée pour le calcul"
                            },
                            "data_payload": {
                                "type": "object",
                                "description": "Données d'entrée alternatives"
                            },
                            "data": {
                                "description": "Données directes"
                            }
                        }
                    },
                    "examples": {
                        "summary_statistics": {
                            "summary": "Statistiques descriptives (Exemple)",
                            "description": "Calcul de la moyenne, médiane, variance, etc.",
                            "value": {
                                "method_id": "summary_statistics",
                                "payload": {
                                    "data": [12.5, 14.8, 11.2, 15.6, 13.4, 18.2, 19.5, 10.8]
                                }
                            }
                        },
                        "t_test": {
                            "summary": "Test t de Student (Exemple)",
                            "description": "Comparaison de deux groupes indépendants",
                            "value": {
                                "method_id": "t_test_independent",
                                "payload": {
                                    "group_a": [10.1, 10.2, 9.9, 10.0, 10.3, 10.1, 10.2, 9.9, 10.0, 10.3],
                                    "group_b": [12.1, 12.0, 11.9, 12.2, 12.0, 12.1, 12.0, 11.9, 12.2, 12.0]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)
@router.post("/stats/execute")
async def execute_analysis(
    request: Request,
    method_id: Optional[str] = None
):
    """Point d'entrée pour l'exécution d'un plan analytique.

    Supporte:
    - Corps JSON standard: `{"method_id": "summary_statistics", "payload": {"data": [...]}}`
    - Corps JSON direct: `{"method_id": "summary_statistics", "data": [...]}`
    - Query param + JSON: `/api/v1/execute?method_id=summary_statistics` avec `{"data": [...]}`
    """
    raw_bytes = await request.body()
    body_data = {}
    if raw_bytes:
        raw_text = raw_bytes.decode("utf-8").strip()
        parsed = try_parse_json_lenient(raw_text)
        if parsed is None:
            raise HTTPException(status_code=400, detail="Format JSON invalide. Veuillez vérifier la syntaxe de votre requête.")
        body_data = parsed

    target_method_id = body_data.get("method_id") or method_id
    if not target_method_id:
        raise HTTPException(status_code=400, detail="method_id is required either in body or as query parameter")

    if "payload" in body_data and isinstance(body_data["payload"], dict):
        target_payload = body_data["payload"]
    elif "data_payload" in body_data and isinstance(body_data["data_payload"], dict):
        target_payload = body_data["data_payload"]
    elif "data" in body_data:
        target_payload = {"data": body_data["data"]}
    else:
        target_payload = {k: v for k, v in body_data.items() if k not in ("method_id", "payload", "data_payload")}

    try:
        result = executor_instance.execute(target_method_id, target_payload)
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

@router.post("/preprocess")
@router.post("/stats/preprocess")
async def run_preprocess(request: Request):
    """Execute a preprocessing pipeline.
    Expects JSON payload with:
        - method_id: identifier of the preprocessing method (e.g., "basic_pipeline")
        - csv: CSV string representing the input DataFrame
    Returns processed DataFrame (as CSV string) and optional visualizations (base64 PNG).
    """
    payload = await request.json()
    method_id = payload.get("method_id")
    csv_data = payload.get("csv")
    if method_id is None or csv_data is None:
        raise HTTPException(status_code=400, detail="method_id and csv are required")
    df = pd.read_csv(io.StringIO(csv_data))
    result = executor_instance.execute(method_id, {"df": df})
    return JSONResponse(content=result)

@router.post("/ingest")
async def run_ingest(request: Request):
    """Ingest data from CSV, Parquet, SQL or MongoDB.

    The request body must contain:
    - ``method_id``: one of ``csv_ingest``, ``parquet_ingest``, ``sql_ingest`` or ``mongodb_ingest``.
    - ``payload``: a dictionary with the required keys for the chosen method (see ``data_ingestion.py``).

    Returns the ingested data as a JSON‑serialisable representation (list of records).
    """
    payload = await request.json()
    method_id = payload.get("method_id")
    data_payload = payload.get("payload", {})
    if not method_id:
        raise HTTPException(status_code=400, detail="method_id is required")
    try:
        df = ingest(method_id, data_payload)
        # Convert DataFrame to list of dicts for JSON response
        return JSONResponse(content={"status": "success", "data": df.to_dict(orient="records")})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
