"""Core execution engine for the PROSTATIA Stats Engine.

This module defines the global method registry and the `StatsExecutor` class responsible for:
- Validating input data against hypothesis validators.
- Dispatching the call to the appropriate computational function (SciPy, scikit‑learn, custom wrappers, etc.).
- Handling fall‑backs when hypotheses fail.
"""

from typing import Dict, Any, List
import numpy as np

from app.registry.schemas import MethodFiche
from app.registry.methods.hypothesis_testing import HYPOTHESIS_METHODS
from app.registry.methods.regression import REGRESSION_METHODS
from app.registry.methods.descriptive import DESCRIPTIVE_METHODS
from app.registry.methods.multivariate import MULTIVARIATE_METHODS
from app.registry.methods.multivariate_extra import MULTIVARIATE_EXTRA_METHODS
from app.registry.methods.probability_laws import PROBABILITY_METHODS
from app.registry.methods.inference import INFERENCE_METHODS
from app.engine.validators import VALIDATORS_MAP
from app.registry.methods.advanced_stats import ADVANCED_STATS_METHODS
from app.services.scipy_wrapper import SCIPY_REGISTRY
from app.registry.methods.multivariate_extended import MULTIVARIATE_EXTENDED_METHODS
from app.registry.methods.modeling import MULTIVARIATE_MODELING_METHODS
from app.registry.methods.ingestion import INGESTION_METHODS
from app.registry.methods.preprocessing import PREPROCESSING_METHODS
# Registre global — Encyclopédie Statistique Complète
GLOBAL_REGISTRY = {
    **HYPOTHESIS_METHODS,
    **REGRESSION_METHODS,
    **DESCRIPTIVE_METHODS,
    **MULTIVARIATE_METHODS,
    **MULTIVARIATE_EXTRA_METHODS,
    **PROBABILITY_METHODS,
    **INFERENCE_METHODS,
    **ADVANCED_STATS_METHODS,
    **MULTIVARIATE_EXTENDED_METHODS,
    **MULTIVARIATE_MODELING_METHODS,
    **INGESTION_METHODS,
    **PREPROCESSING_METHODS,
}

class StatsExecutor:
    """Core execution engine for the PROSTATIA Stats Engine.

    The executor receives a method identifier and input data, validates any hypothesis assumptions,
    and dispatches the call to the appropriate computational function (or a fallback when needed).
    """

    def __init__(self):
        self.registry = GLOBAL_REGISTRY
        self.validators = VALIDATORS_MAP
        self.functions = SCIPY_REGISTRY

    def execute(self, method_id: str, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la méthode statistique demandée après vérification des hypothèses.

        Args:
            method_id: Identifiant unique de la fiche méthodologique enregistrée.
            data_payload: Dictionnaire contenant les paramètres et vecteurs/matrices d'entrée.

        Returns:
            Dict[str, Any]: Dictionnaire contenant:
                - "method_used": Identifiant de la fonction de calcul appelée (ou fallback).
                - "failed_assumptions": Liste des hypothèses statistiques invalidées.
                - "robustness": Évaluation de la robustesse (score, couleur, taille d'échantillon).
                - "results": Résultats numériques retournés par la méthode.

        Raises:
            ValueError: Si `method_id` n'existe pas dans le registre global.
            NotImplementedError: Si la méthode numérique n'est pas implémentée.
        """
        if method_id not in self.registry:
            raise ValueError(f"Method {method_id} not found in registry")
            
        fiche: MethodFiche = self.registry[method_id]
        
        # 1. Préparation des données (conversion en numpy arrays si nécessaire)
        prepared_data = {}
        for key, val in data_payload.items():
            if isinstance(val, list):
                prepared_data[key] = np.array(val, dtype=float)
            else:
                prepared_data[key] = val

        # 2. Vérification des hypothèses
        failed_assumptions: List[str] = []
        
        for assumption in fiche.assumptions:
            validator_func = self.validators.get(assumption.test_method)
            if not validator_func:
                # Si le validateur n'est pas critique ou manquant, on ignore pour le proto
                continue
            
            if assumption.test_method == "shapiro_wilk":
                for key, val in prepared_data.items():
                    if isinstance(val, np.ndarray):
                        # Gérer le cas d'une matrice (ex: groups pour ANOVA)
                        if val.ndim > 1:
                            for sub_val in val:
                                if not validator_func(sub_val):
                                    failed_assumptions.append(assumption.id)
                                    break
                        else:
                            if not validator_func(val):
                                failed_assumptions.append(assumption.id)
                                break
            elif assumption.test_method in ["levene", "contingency_expected_freq"]:
                # Ces validateurs prennent tout le payload
                if not validator_func(prepared_data):
                    failed_assumptions.append(assumption.id)

        # 3. Gestion des fallbacks
        method_to_call = fiche.numerical_method
        kwargs = prepared_data.copy()
        
        if failed_assumptions:
            for fallback in fiche.fallback_if_assumptions_fail:
                if fallback.failed_assumption in failed_assumptions:
                    if fallback.fallback_method == "welch_t_test":
                        kwargs["equal_var"] = False
                    elif fallback.fallback_method == "mann_whitney_u":
                        method_to_call = "scipy.stats.mannwhitneyu"
                    elif fallback.fallback_method == "kruskal_wallis":
                        method_to_call = "scipy.stats.kruskal"
                    break # On prend le premier fallback pertinent

        # 4. Exécution
        func = self.functions.get(method_to_call)
        if not func:
            raise NotImplementedError(f"Function {method_to_call} not implemented in wrappers")
            
        result = func(**kwargs)

        # 5. Calcul de la robustesse
        # Simplification:
        # 100 si aucune assomption n'échoue et N >= 30
        # 75 si aucune assomption n'échoue mais N < 30
        # 50 si une assomption échoue mais qu'un fallback a été utilisé
        # 25 si plus d'une assomption échoue ou pas de fallback
        
        # Trouver la taille minimum d'échantillon (N)
        min_n = float('inf')
        for val in prepared_data.values():
            if isinstance(val, np.ndarray):
                min_n = min(min_n, len(val))
        
        if min_n == float('inf'):
            min_n = 0
            
        robustness_score = 100
        robustness_color = "green"
        
        if len(failed_assumptions) == 0:
            if min_n < 30:
                robustness_score = 75
                robustness_color = "orange"
        else:
            fallback_used = method_to_call != fiche.numerical_method
            if len(failed_assumptions) == 1 and fallback_used:
                robustness_score = 50
                robustness_color = "orange"
            else:
                robustness_score = 25
                robustness_color = "red"
        
        return {
            "method_used": method_to_call,
            "failed_assumptions": failed_assumptions,
            "robustness": {
                "score": robustness_score,
                "color": robustness_color,
                "sample_size_used": min_n
            },
            "results": result
        }

executor_instance = StatsExecutor()
