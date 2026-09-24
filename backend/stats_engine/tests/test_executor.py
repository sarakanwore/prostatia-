import pytest
import numpy as np
from app.engine.executor import StatsExecutor

@pytest.fixture
def executor():
    return StatsExecutor()

def test_t_test_independent_normal(executor):
    """
    Test avec des données qui respectent la normalité et l'homoscédasticité.
    On s'attend à ce que scipy.stats.ttest_ind soit appelé sans fallback.
    """
    # Génère des données normales similaires (H0 vraie)
    np.random.seed(42)
    group_a = np.random.normal(loc=10, scale=2, size=50).tolist()
    group_b = np.random.normal(loc=10, scale=2, size=50).tolist()
    
    payload = {
        "group_a": group_a,
        "group_b": group_b
    }
    
    result = executor.execute("t_test_independent", payload)
    
    assert result["method_used"] == "scipy.stats.ttest_ind"
    assert len(result["failed_assumptions"]) == 0
    assert "statistic" in result["results"]
    assert "p_value" in result["results"]
    assert result["results"]["degrees_of_freedom"] == 98.0

def test_t_test_independent_non_normal(executor):
    """
    Test avec des données fortement non-normales (Pareto).
    Shapiro-Wilk doit échouer, déclenchant le fallback vers Mann-Whitney.
    """
    np.random.seed(0)
    # Distribution de Pareto très asymétrique → garantit non-normalité
    group_a = (np.random.pareto(a=0.5, size=50) + 1).tolist()
    group_b = (np.random.pareto(a=0.5, size=50) + 1).tolist()

    payload = {
        "group_a": group_a,
        "group_b": group_b
    }

    result = executor.execute("t_test_independent", payload)

    assert "normality" in result["failed_assumptions"]
    assert result["method_used"] == "scipy.stats.mannwhitneyu"
    assert "statistic" in result["results"]
    assert "p_value" in result["results"]

def test_t_test_independent_unequal_variance(executor):
    """
    Test avec des données normales mais de variances différentes.
    Levene devrait échouer, déclenchant le test de Welch.
    """
    np.random.seed(42)
    # Moyennes égales mais variances très différentes
    group_a = np.random.normal(loc=10, scale=1, size=50).tolist()
    group_b = np.random.normal(loc=10, scale=10, size=50).tolist()
    
    payload = {
        "group_a": group_a,
        "group_b": group_b
    }
    
    result = executor.execute("t_test_independent", payload)
    
    assert "homoscedasticity" in result["failed_assumptions"]
    # La méthode appelée est toujours ttest_ind mais avec equal_var=False (Welch)
    # Dans notre implémentation, on l'appelle toujours scipy.stats.ttest_ind mais
    # le comportement interne sera testé via les degrés de liberté
    assert result["method_used"] == "scipy.stats.ttest_ind"
    # Pour Welch, les df ne sont plus n1+n2-2 (98), ils seront fractionnaires ou plus petits
    assert result["results"]["degrees_of_freedom"] < 98.0

def test_summary_stats(executor):
    """
    Test pour les statistiques descriptives de base.
    """
    payload = {
        "data": [1, 2, 3, 4, 5, float('nan')]
    }
    
    result = executor.execute("summary_statistics", payload)
    
    assert result["method_used"] == "app.engine.executor.calculate_summary_stats"
    res = result["results"]
    assert res["mean"] == 3.0
    assert res["median"] == 3.0
    assert res["min"] == 1.0
    assert res["max"] == 5.0
    assert res["count"] == 5
    assert np.isclose(res["std_dev"], 1.5811388300841898)

def test_multiple_linear_regression(executor):
    """
    Test pour la régression linéaire multiple.
    """
    np.random.seed(42)
    # y = 2*x1 + 3*x2 + 5 + noise
    x1 = np.random.rand(100)
    x2 = np.random.rand(100)
    X = np.column_stack((x1, x2)).tolist()
    y = (2 * x1 + 3 * x2 + 5 + np.random.randn(100) * 0.1).tolist()
    
    payload = {
        "X": X,
        "y": y
    }
    
    result = executor.execute("multiple_linear_regression", payload)
    
    assert result["method_used"] == "statsmodels.api.OLS"
    res = result["results"]
    assert "r_squared" in res
    assert "coefficients" in res
    assert len(res["coefficients"]) == 2
    assert np.isclose(res["coefficients"][0], 2.0, atol=0.1)
    assert np.isclose(res["coefficients"][1], 3.0, atol=0.1)
    assert np.isclose(res["intercept"], 5.0, atol=0.1)
