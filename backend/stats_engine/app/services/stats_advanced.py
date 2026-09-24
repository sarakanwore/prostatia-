# -*- coding: utf-8 -*-
"""stats_advanced
Provides additional statistical utilities beyond the basic hypothesis tests.
Implemented functions:
- skewness: compute sample skewness (Fisher's definition)
- kurtosis: compute sample excess kurtosis (Fisher's definition)
- proportion_test: two‑sided test for difference of proportions (using normal approximation)
- anova_oneway: one‑way ANOVA (scipy.stats.f_oneway)
Each function receives a dict of parameters matching the MethodFiche definition and
returns a dict of results (statistic, p_value, confidence_interval when applicable).
"""

from typing import Dict, Any
import numpy as np
import scipy.stats as stats

def _get(params: Dict[str, Any], key: str):
    if key not in params:
        raise ValueError(f"Missing required parameter '{key}' for advanced stats function")
    return params[key]

# ---------------------------------------------------------------------------
# Skewness – Fisher (biased) definition via scipy.stats.skew
# ---------------------------------------------------------------------------
def skewness(params: Dict[str, Any]) -> Dict[str, Any]:
    """Calcule le coefficient d'asymétrie (skewness) d'un échantillon.

    Args:
        params: Dictionnaire contenant:
            - "data": Vecteur de données numériques (1D array-like).
            - "bias" (optionnel): Si True, calcul biaisé ; si False, correction de Fisher (défaut: False).

    Returns:
        Dict[str, Any]: Dictionnaire avec la clé "skewness".
    """
    data = np.array(_get(params, "data"), dtype=float)
    bias = params.get("bias", False)  # default unbiased (Fisher) = False
    value = float(stats.skew(data, bias=bias))
    return {"skewness": value}

# ---------------------------------------------------------------------------
# Kurtosis – excess kurtosis (Fisher) via scipy.stats.kurtosis
# ---------------------------------------------------------------------------
def kurtosis(params: Dict[str, Any]) -> Dict[str, Any]:
    """Calcule le coefficient d'aplatissement (excess kurtosis de Fisher) d'un échantillon.

    Args:
        params: Dictionnaire contenant:
            - "data": Vecteur de données numériques (1D array-like).
            - "bias" (optionnel): Si True, calcul biaisé ; si False, non-biaisé (défaut: False).

    Returns:
        Dict[str, Any]: Dictionnaire avec la clé "kurtosis" (0 pour une loi normale).
    """
    data = np.array(_get(params, "data"), dtype=float)
    bias = params.get("bias", False)
    value = float(stats.kurtosis(data, bias=bias, fisher=True))
    return {"kurtosis": value}

# ---------------------------------------------------------------------------
# Two‑sample proportion test (normal approximation)
# ---------------------------------------------------------------------------
def proportion_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute un test de comparaison de deux proportions par approximation normale.

    Args:
        params: Dictionnaire contenant:
            - "success_a": Nombre de succès dans l'échantillon A.
            - "n_a": Taille de l'échantillon A.
            - "success_b": Nombre de succès dans l'échantillon B.
            - "n_b": Taille de l'échantillon B.
            - "alternative" (optionnel): 'two-sided', 'larger', 'smaller' (défaut: 'two-sided').

    Returns:
        Dict[str, Any]: Dictionnaire avec la statistique "z" et la "p_value".
    """
    # Expected keys: success_a, n_a, success_b, n_b, alternative ('two-sided', 'larger', 'smaller')
    a = _get(params, "success_a")
    n_a = _get(params, "n_a")
    b = _get(params, "success_b")
    n_b = _get(params, "n_b")
    alt = params.get("alternative", "two-sided")
    p1 = a / n_a
    p2 = b / n_b
    p_pool = (a + b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (p1 - p2) / se
    if alt == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif alt == "larger":  # p1 > p2
        p_value = 1 - stats.norm.cdf(z)
    else:  # smaller
        p_value = stats.norm.cdf(z)
    return {"z": float(z), "p_value": float(p_value)}

# ---------------------------------------------------------------------------
# One‑way ANOVA (scipy.stats.f_oneway)
# ---------------------------------------------------------------------------
def anova_oneway(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une ANOVA à un facteur à partir des clés 'group_*' du dictionnaire.

    Args:
        params: Dictionnaire associant chaque nom de groupe ('group_1', 'group_2', ...)
            à sa série d'échantillons numériques.

    Returns:
        Dict[str, Any]: Dictionnaire avec la statistique "F" et la "p_value".
    """
    # Expect a dict where each key is a group name and value is an array‑like of samples
    groups = [_get(params, key) for key in params if key.startswith("group_")]
    # Convert each to numpy array
    arrays = [np.asarray(g, dtype=float) for g in groups]
    f_stat, p_val = stats.f_oneway(*arrays)
    return {"F": float(f_stat), "p_value": float(p_val)}

__all__ = ["skewness", "kurtosis", "proportion_test", "anova_oneway"]
