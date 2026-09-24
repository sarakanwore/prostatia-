"""Validator utilities for hypothesis testing.

Each validator implements a statistical test used to verify assumptions before a method is executed. The functions return ``True`` when the assumption holds.
"""

from typing import Dict, Any
import numpy as np
import scipy.stats as stats

def check_normality(data: np.ndarray, alpha: float = 0.05) -> bool:
    """Shapiro‑Wilk test for normality.

    Parameters
    ----------
    data : np.ndarray
        Input array (minimum 3 observations).
    alpha : float, optional
        Significance level (default 0.05).

    Returns
    -------
    bool
        True if the null hypothesis (data follows a normal distribution) cannot be rejected
        (p‑value ≥ alpha).
    """
    if len(data) < 3:
        return False
    _, p_value = stats.shapiro(data)
    return p_value >= alpha

def check_levene(data_payload: Dict[str, Any], alpha: float = 0.05) -> bool:
    """Levene test for equal variances across groups.

    Parameters
    ----------
    data_payload : Dict[str, Any]
        Mapping where each value is a ``np.ndarray`` representing a group.
    alpha : float, optional
        Significance level (default 0.05).

    Returns
    -------
    bool
        ``True`` if variances are homogeneous (p‑value ≥ ``alpha``).
    """
    groups = [v for v in data_payload.values() if isinstance(v, np.ndarray)]
    if len(groups) < 2:
        return False
    _, p_value = stats.levene(*groups)
    return p_value >= alpha

def check_homoscedasticity(*arrays: np.ndarray, alpha: float = 0.05) -> bool:
    """Wrapper for Levene test on multiple arrays."""
    if len(arrays) < 2:
        return False
    _, p_value = stats.levene(*arrays)
    return p_value >= alpha

def check_expected_frequencies(data_payload: Dict[str, Any]) -> bool:
    """Verify that all expected frequencies in a contingency table are >= 5."""
    contingency_table = data_payload.get("contingency_table")
    if contingency_table is None:
        return False
    try:
        from scipy.stats.contingency import expected_freq
        expected = expected_freq(contingency_table)
        return bool(np.all(expected >= 5))
    except Exception:
        return False

# Mapping used by the executor to call the appropriate validator
VALIDATORS_MAP = {
    "shapiro_wilk": check_normality,  # called directly with an np.ndarray
    "levene": lambda data_kwargs: check_homoscedasticity(*[v for v in data_kwargs.values() if isinstance(v, np.ndarray)]),
    "contingency_expected_freq": lambda data_kwargs: check_expected_frequencies(data_kwargs),
    "visual_check": lambda data_kwargs: True,  # visual checks validated by human
    "vif": lambda data_kwargs: True,  # placeholder for future VIF integration
}
