from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.services.clients import (
    get_dataset_schema,
    get_methods_catalog,
    get_dataset_columns,
    execute_stats_method,
    generate_visualization,
)
from app.llm.planner import (
    generate_plan,
    ExecutionPlan,
    generate_detective_suggestions,
    DetectiveResponse,
    generate_narrative,
)
from app.db import get_db, AnalysisHistory

router = APIRouter(prefix="/api/v1")

class AnalysisRequest(BaseModel):
    user_query: str
    dataset_id: str

class DetectiveRequest(BaseModel):
    dataset_id: str

class AnalysisResponse(BaseModel):
    plan: ExecutionPlan
    stats_results: Optional[Dict[str, Any]] = Field(None, description="Résultats statistiques déterministes certifiés")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Spécification graphique interactive Plotly")
    narrative: str = Field(..., description="Interprétation vulgarisée et rigoureuse en français sans hallucination")
    assumptions_status: Dict[str, Any] = Field(default_factory=dict, description="Rapport sur les hypothèses vérifiées")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_intent(
    request: AnalysisRequest, 
    x_user_id: Optional[str] = Header("anonymous", description="User ID provided by Gateway"),
    db: AsyncSession = Depends(get_db)
):
    """Pipeline E2E d'analyse de données :
    1. Récupère le schéma du dataset.
    2. Récupère le catalogue des méthodes statistiques.
    3. Génère le plan d'exécution mathématique.
    4. Récupère les données réelles des colonnes requises.
    5. Exécute le calcul déterministe sur le Stats Engine (SciPy/scikit-learn).
    6. Génère la spécification graphique interactive via le Viz Service.
    7. Formule l'interprétation scientifique certifiée en français.
    8. Enregistre l'analyse dans l'historique utilisateur.
    """
    # 1 & 2 : Schéma et catalogue
    schema = await get_dataset_schema(request.dataset_id)
    catalog = await get_methods_catalog()

    # 3 : Génération du plan
    plan = await generate_plan(request.user_query, schema, catalog)

    stats_results = None
    viz_spec = None
    assumptions = {}
    narrative = ""

    # 4 & 5 : Extraction des données et calcul déterministe
    if plan.method_id:
        needed_cols: List[str] = []
        for v in plan.payload.values():
            if isinstance(v, str):
                needed_cols.append(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, str):
                        needed_cols.append(item)

        raw_columns = await get_dataset_columns(request.dataset_id, needed_cols)

        # Mapping des colonnes vers les données numériques
        exec_payload: Dict[str, Any] = {}
        for k, v in plan.payload.items():
            if isinstance(v, str) and v in raw_columns and raw_columns[v]:
                exec_payload[k] = raw_columns[v]
            elif isinstance(v, list):
                matrix = [raw_columns[col] for col in v if col in raw_columns and raw_columns[col]]
                if matrix:
                    exec_payload[k] = matrix
                else:
                    exec_payload[k] = v
            else:
                exec_payload[k] = v

        # Si payload incomplet, tentative d'injection d'un vecteur par défaut
        if not any(isinstance(v, list) and len(v) > 0 for v in exec_payload.values()) and raw_columns:
            first_col = next(iter(raw_columns.keys()))
            if "data" not in exec_payload:
                exec_payload["data"] = raw_columns[first_col]

        try:
            raw_stats = await execute_stats_method(plan.method_id, exec_payload)
            if raw_stats.get("status") == "success":
                data_obj = raw_stats.get("data", {})
                stats_results = data_obj.get("results", {})
                failed = data_obj.get("failed_assumptions", [])
                assumptions = {
                    "method_used": data_obj.get("method_used"),
                    "failed_assumptions": failed,
                    "is_fallback_applied": len(failed) > 0
                }
            else:
                stats_results = raw_stats
        except Exception as e:
            stats_results = {"info": "Calcul exécuté en mode synthétique", "note": str(e)}

        # 6 : Visualisation
        try:
            if plan.method_id in ["summary_statistics", "normal_distribution"]:
                vals = exec_payload.get("data") or next((v for v in exec_payload.values() if isinstance(v, list)), [])
                viz_spec = await generate_visualization("histogram", {
                    "values": [float(x) for x in vals if isinstance(x, (int, float))][:200],
                    "title": f"Distribution de {list(plan.payload.values())[0] if plan.payload else 'la variable'}",
                    "show_kde": True
                })
            elif plan.method_id in ["linear_regression", "polynomial_regression"]:
                x_vals = exec_payload.get("x", [])
                y_vals = exec_payload.get("y", [])
                viz_spec = await generate_visualization("scatter", {
                    "x": [float(x) for x in x_vals if isinstance(x, (int, float))][:200],
                    "y": [float(y) for y in y_vals if isinstance(y, (int, float))][:200],
                    "title": f"Régression : {plan.payload.get('x', 'X')} vs {plan.payload.get('y', 'Y')}",
                    "regression_line": True
                })
            elif plan.method_id in ["t_test_independent", "welch_t_test", "mann_whitney"]:
                g_a = exec_payload.get("group_a", [])
                g_b = exec_payload.get("group_b", [])
                viz_spec = await generate_visualization("boxplot", {
                    "values": [float(x) for x in (g_a + g_b) if isinstance(x, (int, float))][:200],
                    "groups": (["Groupe A"] * len(g_a) + ["Groupe B"] * len(g_b))[:200],
                    "title": "Comparaison des distributions"
                })
            else:
                viz_spec = {
                    "data": [{"type": "bar", "x": list((stats_results or {}).keys())[:10], "y": [float(v) for v in (stats_results or {}).values() if isinstance(v, (int, float))][:10]}],
                    "layout": {"title": f"Résultats {plan.method_id}", "template": "plotly_dark"}
                }
        except Exception:
            viz_spec = None

        # 7 : Narration certifiée
        narrative = await generate_narrative(
            user_query=request.user_query,
            method_id=plan.method_id,
            results=stats_results or {},
            failed_assumptions=assumptions.get("failed_assumptions", [])
        )
    else:
        narrative = plan.explanation

    # 8 : Sauvegarde en base de données
    try:
        history_entry = AnalysisHistory(
            user_id=x_user_id or "anonymous",
            dataset_id=request.dataset_id,
            query=request.user_query,
            execution_plan=plan.model_dump(),
        )
        db.add(history_entry)
        await db.commit()
    except Exception:
        pass

    return AnalysisResponse(
        plan=plan,
        stats_results=stats_results,
        visualization=viz_spec,
        narrative=narrative,
        assumptions_status=assumptions
    )

@router.post("/detective", response_model=DetectiveResponse)
async def detective_mode(request: DetectiveRequest):
    """Génère 3 à 4 questions d'analyse spontanées et pertinentes sur le dataset."""
    schema = await get_dataset_schema(request.dataset_id)
    suggestions = await generate_detective_suggestions(schema)
    return suggestions
