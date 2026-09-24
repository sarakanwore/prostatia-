from sklearn.datasets import load_iris, make_regression
from app.services.modeling import (
    logistic_regression,
    glm,
    ridge,
    lasso,
    svm,
    decision_tree,
    random_forest,
    xgboost_boosting,
)

def test_logistic_regression():
    data = load_iris()
    X, y = data.data, data.target
    res = logistic_regression({"X": X, "y": y, "C": 1.0, "max_iter": 200})
    assert len(res["predictions"]) == len(y)
    assert 0.0 <= res["accuracy"] <= 1.0

def test_glm():
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1)
    res = glm({"X": X, "y": y})
    assert len(res["predictions"]) == len(y)
    assert -1.0 <= res["r2"] <= 1.0

def test_ridge():
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1)
    res = ridge({"X": X, "y": y, "alpha": 1.0})
    assert len(res["predictions"]) == len(y)
    assert -1.0 <= res["r2"] <= 1.0

def test_lasso():
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1)
    res = lasso({"X": X, "y": y, "alpha": 0.5})
    assert len(res["predictions"]) == len(y)
    assert -1.0 <= res["r2"] <= 1.0

def test_svm():
    data = load_iris()
    X, y = data.data, data.target
    res = svm({"X": X, "y": y, "C": 1.0, "kernel": "linear"})
    assert len(res["predictions"]) == len(y)
    assert 0.0 <= res["accuracy"] <= 1.0

def test_decision_tree():
    data = load_iris()
    X, y = data.data, data.target
    res = decision_tree({"X": X, "y": y, "max_depth": 3})
    assert len(res["predictions"]) == len(y)
    assert 0.0 <= res["accuracy"] <= 1.0

def test_random_forest():
    data = load_iris()
    X, y = data.data, data.target
    res = random_forest({"X": X, "y": y, "n_estimators": 50, "max_depth": 4})
    assert len(res["predictions"]) == len(y)
    assert 0.0 <= res["accuracy"] <= 1.0

def test_xgboost_boosting():
    data = load_iris()
    X, y = data.data, data.target
    res = xgboost_boosting({"X": X, "y": y, "n_estimators": 30, "learning_rate": 0.1})
    assert len(res["predictions"]) == len(y)
    assert 0.0 <= res["accuracy"] <= 1.0
