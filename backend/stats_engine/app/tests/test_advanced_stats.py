import numpy as np
from app.services.stats_advanced import (
    skewness,
    kurtosis,
    proportion_test,
    anova_oneway,
)

# --------------------- Skewness ---------------------
def test_skewness():
    data = np.array([1, 2, 3, 4, 5])
    res = skewness({"data": data, "bias": False})
    expected = float(__import__('scipy').stats.skew(data, bias=False))
    assert np.isclose(res["skewness"], expected)

# --------------------- Kurtosis ---------------------
def test_kurtosis():
    data = np.array([1, 2, 3, 4, 5])
    res = kurtosis({"data": data, "bias": False})
    expected = float(__import__('scipy').stats.kurtosis(data, bias=False, fisher=True))
    assert np.isclose(res["kurtosis"], expected)

# --------------------- Proportion test ---------------------
def test_proportion_test_two_sided():
    params = {"success_a": 30, "n_a": 100, "success_b": 20, "n_b": 80, "alternative": "two-sided"}
    res = proportion_test(params)
    # Compute expected using manual formula
    p1 = params["success_a"] / params["n_a"]
    p2 = params["success_b"] / params["n_b"]
    p_pool = (params["success_a"] + params["success_b"]) / (params["n_a"] + params["n_b"])
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / params["n_a"] + 1 / params["n_b"]))
    z = (p1 - p2) / se
    expected_p = 2 * (1 - __import__('scipy').stats.norm.cdf(abs(z)))
    assert np.isclose(res["z"], float(z))
    assert np.isclose(res["p_value"], float(expected_p))

# --------------------- One‑way ANOVA ---------------------
def test_anova_oneway():
    params = {
        "group_1": [1.0, 2.0, 3.0],
        "group_2": [2.0, 3.0, 4.0],
        "group_3": [5.0, 6.0, 7.0],
    }
    res = anova_oneway(params)
    f_stat, p_val = __import__('scipy').stats.f_oneway(params["group_1"], params["group_2"], params["group_3"])
    assert np.isclose(res["F"], float(f_stat))
    assert np.isclose(res["p_value"], float(p_val))
