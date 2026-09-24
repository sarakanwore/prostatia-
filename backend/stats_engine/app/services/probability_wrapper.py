# -*- coding: utf-8 -*-
"""probability_wrapper
Provides a thin layer around scipy.stats for the probability distributions
registered in ``app.registry.methods.probability_laws``.
Each function receives a ``params`` dict (the inputs defined in the
MethodFiche) and returns a dictionary containing the requested values
(pdf, cdf, rvs, mean, variance, skewness, kurtosis).  The keys match the
output definitions in the fiches so the executor can forward them
unchanged.
"""

from typing import Dict, Any
import scipy.stats as stats

# Helper to safely fetch a parameter from the dict with a clear error
def _get(params: Dict[str, Any], key: str):
    if key not in params:
        raise ValueError(f"Missing required parameter '{key}' for probability distribution")
    return params[key]

# ---------------------------------------------------------------------------
# Generic dispatcher – each entry corresponds to the ``numerical_method``
# value stored in the MethodFiche (e.g. "probability.normal").
# ---------------------------------------------------------------------------

def _dispatch_normal(params: Dict[str, Any]) -> Dict[str, Any]:
    mu = _get(params, "mu")
    sigma = _get(params, "sigma")
    x = _get(params, "x")
    query_type = _get(params, "query_type")
    dist = stats.norm(loc=mu, scale=sigma)
    result: Dict[str, Any] = {}
    if query_type == "pdf":
        result["pdf"] = float(dist.pdf(x))
    elif query_type == "cdf":
        result["cdf"] = float(dist.cdf(x))
    elif query_type == "sf":
        result["sf"] = float(dist.sf(x))
    elif query_type == "ppf":
        result["ppf"] = float(dist.ppf(x))
    elif query_type == "interval":
        low = _get(params, "x_low")
        high = _get(params, "x_high")
        result["probability"] = float(dist.cdf(high) - dist.cdf(low))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
        result["std_dev"] = float(dist.std())
        result["skewness"] = float(dist.stats(moments="s"))
        result["kurtosis"] = float(dist.stats(moments="k"))
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for normal distribution")
    return result

def _dispatch_student_t(params: Dict[str, Any]) -> Dict[str, Any]:
    df = _get(params, "df")
    loc = _get(params, "loc")
    scale = _get(params, "scale")
    t = _get(params, "t")
    query_type = _get(params, "query_type")
    dist = stats.t(df=df, loc=loc, scale=scale)
    result: Dict[str, Any] = {}
    if query_type == "pdf":
        result["pdf"] = float(dist.pdf(t))
    elif query_type == "cdf":
        result["cdf"] = float(dist.cdf(t))
    elif query_type == "sf":
        result["sf"] = float(dist.sf(t))
    elif query_type == "ppf":
        result["ppf"] = float(dist.ppf(t))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
        result["skewness"] = float(dist.stats(moments="s"))
        result["kurtosis"] = float(dist.stats(moments="k"))
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for student_t distribution")
    return result

def _dispatch_chi2(params: Dict[str, Any]) -> Dict[str, Any]:
    df = _get(params, "df")
    x = _get(params, "x")
    query_type = _get(params, "query_type")
    dist = stats.chi2(df=df)
    result: Dict[str, Any] = {}
    if query_type == "pdf":
        result["pdf"] = float(dist.pdf(x))
    elif query_type == "cdf":
        result["cdf"] = float(dist.cdf(x))
    elif query_type == "sf":
        result["sf"] = float(dist.sf(x))
    elif query_type == "ppf":
        result["ppf"] = float(dist.ppf(x))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
        result["skewness"] = float(dist.stats(moments="s"))
        result["kurtosis"] = float(dist.stats(moments="k"))
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for chi2 distribution")
    return result

def _dispatch_binomial(params: Dict[str, Any]) -> Dict[str, Any]:
    n = _get(params, "n")
    p = _get(params, "p")
    k = _get(params, "k")
    query_type = _get(params, "query_type")
    dist = stats.binom(n=n, p=p)
    result: Dict[str, Any] = {}
    if query_type == "pmf":
        result["probability"] = float(dist.pmf(k))
    elif query_type == "cdf":
        result["probability"] = float(dist.cdf(k))
    elif query_type == "sf":
        result["probability"] = float(dist.sf(k))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
        result["std_dev"] = float(dist.std())
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for binomial distribution")
    return result

def _dispatch_poisson(params: Dict[str, Any]) -> Dict[str, Any]:
    lam = _get(params, "lam")
    k = _get(params, "k")
    query_type = _get(params, "query_type")
    dist = stats.poisson(mu=lam)
    result: Dict[str, Any] = {}
    if query_type == "pmf":
        result["probability"] = float(dist.pmf(k))
    elif query_type == "cdf":
        result["probability"] = float(dist.cdf(k))
    elif query_type == "sf":
        result["probability"] = float(dist.sf(k))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for poisson distribution")
    return result

def _dispatch_exponential(params: Dict[str, Any]) -> Dict[str, Any]:
    lam = _get(params, "lam")
    x = _get(params, "x")
    query_type = _get(params, "query_type")
    dist = stats.expon(scale=1/lam)
    result: Dict[str, Any] = {}
    if query_type == "pdf":
        result["pdf"] = float(dist.pdf(x))
    elif query_type == "cdf":
        result["cdf"] = float(dist.cdf(x))
    elif query_type == "sf":
        result["sf"] = float(dist.sf(x))
    elif query_type == "ppf":
        result["ppf"] = float(dist.ppf(x))
    elif query_type == "stats":
        result["mean"] = float(dist.mean())
        result["variance"] = float(dist.var())
    else:
        raise ValueError(f"Unsupported query_type '{query_type}' for exponential distribution")
    return result

# ---------------------------------------------------------------------------
# Registry mapping the ``numerical_method`` string to the dispatcher function.
# ---------------------------------------------------------------------------
PROBABILITY_REGISTRY: Dict[str, Any] = {
    "probability.normal": _dispatch_normal,
    "probability.student_t": _dispatch_student_t,
    "probability.chi2": _dispatch_chi2,
    "probability.binomial": _dispatch_binomial,
    "probability.poisson": _dispatch_poisson,
    "probability.exponential": _dispatch_exponential,
    # Additional distributions can be added here following the same pattern.
}

__all__ = ["PROBABILITY_REGISTRY"]
