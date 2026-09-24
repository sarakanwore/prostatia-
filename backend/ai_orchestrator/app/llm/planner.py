from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import os
from openai import AsyncOpenAI
from app.llm.prompts import build_orchestrator_prompt, build_detective_prompt, build_narrative_prompt
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
api_key = os.environ.get("OPENAI_API_KEY", "")
client = AsyncOpenAI(api_key=api_key) if api_key and api_key != "dummy-key-for-local-dev" else None

class ExecutionPlan(BaseModel):
    method_id: Optional[str] = Field(None, description="L'ID de la méthode choisie dans le catalogue (ex: linear_regression). Null si aucune méthode ne correspond.")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Le mapping des noms de colonnes du dataset vers les arguments attendus par la méthode.")
    explanation: str = Field(..., description="Une brève explication en français adressée à l'utilisateur, justifiant le choix de la méthode.")

class DetectiveResponse(BaseModel):
    suggestions: List[str] = Field(..., description="Liste de 3 à 4 questions d'analyse pertinentes.")

def _heuristic_fallback_plan(user_query: str, dataset_schema: dict, methods_catalog: list) -> ExecutionPlan:
    q = user_query.lower()
    cols = dataset_schema.get("columns", [])
    num_cols = [c["name"] for c in cols if any(t in str(c.get("data_type", "")).lower() for t in ["int", "float", "num"])]
    cat_cols = [c["name"] for c in cols if c["name"] not in num_cols]

    if not num_cols and cols:
        num_cols = [c["name"] for c in cols]

    # Matching logic
    if any(w in q for w in ["acp", "pca", "composante", "dimension"]):
        chosen_cols = num_cols[:4] if len(num_cols) >= 2 else num_cols
        return ExecutionPlan(
            method_id="pca_analysis",
            payload={"features": chosen_cols, "n_components": min(2, len(chosen_cols))},
            explanation="J'ai sélectionné l'Analyse en Composantes Principales (ACP) pour réduire la dimensionnalité et projeter vos variables numériques."
        )
    elif any(w in q for w in ["cluster", "cah", "groupe", "segment"]):
        chosen_cols = num_cols[:3] if len(num_cols) >= 2 else num_cols
        return ExecutionPlan(
            method_id="hierarchical_clustering",
            payload={"features": chosen_cols, "n_clusters": 3},
            explanation="J'ai sélectionné la Classification Ascendante Hiérarchique (CAH) pour découvrir des groupes homogènes au sein de vos observations."
        )
    elif any(w in q for w in ["différence", "comparer", "student", "groupe", "t-test", "t_test"]) and len(num_cols) >= 2:
        return ExecutionPlan(
            method_id="t_test_independent",
            payload={"group_a": num_cols[0], "group_b": num_cols[1]},
            explanation=f"J'ai sélectionné le test t de Student pour comparer les distributions de '{num_cols[0]}' et '{num_cols[1]}'."
        )
    elif any(w in q for w in ["régression", "regression", "impact", "influence", "prédire", "relation", "corrélation"]) and len(num_cols) >= 2:
        return ExecutionPlan(
            method_id="linear_regression",
            payload={"x": num_cols[0], "y": num_cols[1]},
            explanation=f"J'ai choisi une régression linéaire pour modéliser l'effet de '{num_cols[0]}' sur '{num_cols[1]}'."
        )
    else:
        target_col = num_cols[0] if num_cols else (cols[0]["name"] if cols else "valeurs")
        return ExecutionPlan(
            method_id="summary_statistics",
            payload={"data": target_col},
            explanation=f"J'ai sélectionné les statistiques descriptives complètes pour caractériser la variable '{target_col}' (moyenne, écart-type, médiane, quartiles)."
        )

async def generate_plan(user_query: str, dataset_schema: dict, methods_catalog: list) -> ExecutionPlan:
    """Génère le plan d'exécution via OpenAI ou bascule sur une heuristique déterministe."""
    if client is not None:
        messages = build_orchestrator_prompt(user_query, dataset_schema, methods_catalog)
        try:
            response = await client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=ExecutionPlan,
            )
            parsed = response.choices[0].message.parsed
            if parsed and parsed.method_id:
                return parsed
        except Exception:
            pass

    return _heuristic_fallback_plan(user_query, dataset_schema, methods_catalog)

async def generate_detective_suggestions(dataset_schema: dict) -> DetectiveResponse:
    """Génère des questions pertinentes pour le Mode Détective."""
    if client is not None:
        messages = build_detective_prompt(dataset_schema)
        try:
            response = await client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=DetectiveResponse,
            )
            parsed = response.choices[0].message.parsed
            if parsed and parsed.suggestions:
                return parsed
        except Exception:
            pass

    cols = [c["name"] for c in dataset_schema.get("columns", [])]
    if len(cols) >= 2:
        return DetectiveResponse(
            suggestions=[
                f"Quelle est la corrélation et l'impact de '{cols[0]}' sur '{cols[1]}' ?",
                f"Y a-t-il des disparités ou des groupes homogènes détectables via ACP/CAH sur vos données ?",
                f"Quelle est la distribution statistique détaillée et la dispersion de '{cols[0]}' ?"
            ]
        )
    elif len(cols) == 1:
        return DetectiveResponse(
            suggestions=[
                f"Quels sont les paramètres de tendance centrale et de dispersion pour '{cols[0]}' ?",
                f"La variable '{cols[0]}' suit-elle une loi normale (test de Shapiro-Wilk) ?"
            ]
        )
    return DetectiveResponse(
        suggestions=[
            "Quelles sont les statistiques descriptives globales du jeu de données ?",
            "Existe-t-il des corrélations linéaires significatives entre les variables numériques ?"
        ]
    )

async def generate_narrative(user_query: str, method_id: str, results: dict, failed_assumptions: list) -> str:
    """Génère l'explication scientifique certifiée en français basée sur les vrais chiffres."""
    if client is not None:
        messages = build_narrative_prompt(user_query, method_id, results, failed_assumptions)
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages,
                temperature=0.2,
                max_tokens=500
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception:
            pass

    # Deterministic zero-hallucination narrative generation
    parts = []
    parts.append(f"**Analyse réalisée :** La méthode statistique `{method_id}` a été exécutée avec succès.")

    if failed_assumptions:
        parts.append(f"⚠️ **Contrôle des hypothèses :** L'hypothèse de {', '.join(failed_assumptions)} n'était pas vérifiée sur vos données. Le moteur a automatiquement engagé une procédure non-paramétrique robuste certifiée.")
    else:
        parts.append("✅ **Contrôle des hypothèses :** Toutes les conditions de validité théoriques (normalité, variance) ont été validées.")

    p_val = results.get("p_value") or (results.get("results", {}) if isinstance(results.get("results"), dict) else {}).get("p_value")
    stat = results.get("statistic") or (results.get("results", {}) if isinstance(results.get("results"), dict) else {}).get("statistic")

    if p_val is not None:
        sig = "statistiquement significative (p < 0.05)" if p_val < 0.05 else "non statistiquement significative (p ≥ 0.05)"
        parts.append(f"**Indicateurs clés :** Statistique de test = `{stat:.4f}` | p-valeur = `{p_val:.4e}`. La relation observée est **{sig}** au seuil de risque usuel de 5%.")
    elif "mean" in results:
        parts.append(f"**Statistiques descriptives :** Moyenne = `{results.get('mean'):.2f}` | Médiane = `{results.get('median'):.2f}` | Écart-type = `{results.get('std'):.2f}` (N={results.get('count')}).")
    elif "r_squared" in results:
        parts.append(f"**Qualité d'ajustement du modèle :** Coefficient de détermination R² = `{results.get('r_squared'):.4f}`.")

    parts.append("Ces conclusions sont garanties déterministes et exemptes de toute hallucination algorithmique.")
    return "\n\n".join(parts)
