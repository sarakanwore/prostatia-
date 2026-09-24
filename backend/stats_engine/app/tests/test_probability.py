import numpy as np
from app.services.probability_wrapper import (
    PROBABILITY_REGISTRY,
)
import scipy.stats as stats

# Helper to call dispatcher
def call_dispatcher(method_key: str, params: dict):
    if method_key not in PROBABILITY_REGISTRY:
        raise KeyError(f"Dispatcher for {method_key} not found")
    return PROBABILITY_REGISTRY[method_key](params)

# --------------------- Normal distribution ---------------------
def test_normal_pdf_cdf():
    params = {
        "mu": 0.0,
        "sigma": 1.0,
        "x": 0.5,
        "query_type": "pdf",
    }
    res = call_dispatcher("probability.normal", params)
    expected = stats.norm(loc=0.0, scale=1.0).pdf(0.5)
    assert np.isclose(res["pdf"], expected)

    params["query_type"] = "cdf"
    res = call_dispatcher("probability.normal", params)
    expected = stats.norm(loc=0.0, scale=1.0).cdf(0.5)
    assert np.isclose(res["cdf"], expected)

    params["query_type"] = "stats"
    res = call_dispatcher("probability.normal", params)
    dist = stats.norm(loc=0.0, scale=1.0)
    assert np.isclose(res["mean"], dist.mean())
    assert np.isclose(res["variance"], dist.var())
    assert np.isclose(res["skewness"], dist.stats(moments="s"))
    assert np.isclose(res["kurtosis"], dist.stats(moments="k"))

# --------------------- Binomial distribution ---------------------
def test_binomial_pmf_cdf_stats():
    params = {
        "n": 10,
        "p": 0.3,
        "k": 3,
        "query_type": "pmf",
    }
    res = call_dispatcher("probability.binomial", params)
    expected = stats.binom(n=10, p=0.3).pmf(3)
    assert np.isclose(res["probability"], expected)

    params["query_type"] = "cdf"
    res = call_dispatcher("probability.binomial", params)
    expected = stats.binom(n=10, p=0.3).cdf(3)
    assert np.isclose(res["probability"], expected)

    params["query_type"] = "stats"
    res = call_dispatcher("probability.binomial", params)
    dist = stats.binom(n=10, p=0.3)
    assert np.isclose(res["mean"], dist.mean())
    assert np.isclose(res["variance"], dist.var())
    assert np.isclose(res["std_dev"], dist.std())

# --------------------- Poisson distribution ---------------------
def test_poisson_pmf_cdf_stats():
    params = {
        "lam": 4.0,
        "k": 2,
        "query_type": "pmf",
    }
    res = call_dispatcher("probability.poisson", params)
    expected = stats.poisson(mu=4.0).pmf(2)
    assert np.isclose(res["probability"], expected)

    params["query_type"] = "cdf"
    res = call_dispatcher("probability.poisson", params)
    expected = stats.poisson(mu=4.0).cdf(2)
    assert np.isclose(res["probability"], expected)

    params["query_type"] = "stats"
    res = call_dispatcher("probability.poisson", params)
    dist = stats.poisson(mu=4.0)
    assert np.isclose(res["mean"], dist.mean())
    assert np.isclose(res["variance"], dist.var())

# --------------------- Exponential distribution ---------------------
def test_exponential_pdf_cdf_stats():
    params = {
        "lam": 2.0,
        "x": 0.5,
        "query_type": "pdf",
    }
    res = call_dispatcher("probability.exponential", params)
    expected = stats.expon(scale=1/2.0).pdf(0.5)
    assert np.isclose(res["pdf"], expected)

    params["query_type"] = "cdf"
    res = call_dispatcher("probability.exponential", params)
    expected = stats.expon(scale=1/2.0).cdf(0.5)
    assert np.isclose(res["cdf"], expected)

    params["query_type"] = "stats"
    res = call_dispatcher("probability.exponential", params)
    dist = stats.expon(scale=1/2.0)
    assert np.isclose(res["mean"], dist.mean())
    assert np.isclose(res["variance"], dist.var())

# --------------------- Chi2 distribution ---------------------
def test_chi2_pdf_cdf_stats():
    params = {
        "df": 5,
        "x": 2.5,
        "query_type": "pdf",
    }
    res = call_dispatcher("probability.chi2", params)
    expected = stats.chi2(df=5).pdf(2.5)
    assert np.isclose(res["pdf"], expected)

    params["query_type"] = "cdf"
    res = call_dispatcher("probability.chi2", params)
    expected = stats.chi2(df=5).cdf(2.5)
    assert np.isclose(res["cdf"], expected)

    params["query_type"] = "stats"
    res = call_dispatcher("probability.chi2", params)
    dist = stats.chi2(df=5)
    assert np.isclose(res["mean"], dist.mean())
    assert np.isclose(res["variance"], dist.var())
    assert np.isclose(res["skewness"], dist.stats(moments="s"))
    assert np.isclose(res["kurtosis"], dist.stats(moments="k"))
