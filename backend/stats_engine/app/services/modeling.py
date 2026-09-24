"""Thin wrappers around scikit‑learn and XGBoost models for the PROSTATIA backend.
Each function receives a ``params`` dict, fits the model, and returns a dict
with predictions, optional coefficients, and a basic performance metric.
"""
from typing import Dict, Any
import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge, Lasso, LinearRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def _as_array(x):
    return np.array(x, dtype=float)

def logistic_regression(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste un modèle de régression logistique binaire ou multi-classes.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Vecteur de cibles catégorielles/binaires (1D array-like).
            - "C" (optionnel): Inverse de la force de régularisation (défaut: 1.0).
            - "max_iter" (optionnel): Nombre maximal d'itérations du solveur (défaut: 100).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Liste des classes prédites pour chaque observation.
            - "coefficients": Coefficients du modèle ajusté.
            - "intercept": Constante (biais) du modèle.
            - "accuracy": Score d'exactitude (accuracy) sur les données d'entraînement.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    C = params.get("C", 1.0)
    max_iter = params.get("max_iter", 100)
    model = LogisticRegression(C=C, max_iter=max_iter, solver="lbfgs")
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_.tolist(),
        "accuracy": float(model.score(X, y)),
    }

def glm(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste un modèle linéaire généralisé standard (régression linéaire par MCO).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice des variables explicatives (2D array-like).
            - "y": Vecteur de la variable continue cible (1D array-like).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Prédictions continues du modèle.
            - "coefficients": Coefficients estimés pour chaque variable explicative.
            - "intercept": Ordonnée à l'origine (intercept).
            - "r2": Coefficient de détermination R² d'ajustement.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"])
    model = LinearRegression()
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_.tolist(),
        "r2": float(model.score(X, y)),
    }

def ridge(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste une régression régularisée Ridge (pénalité L2).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice des variables explicatives (2D array-like).
            - "y": Vecteur cible continu (1D array-like).
            - "alpha" (optionnel): Paramètre de pénalité L2 (défaut: 1.0).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Prédictions du modèle régularisé.
            - "coefficients": Coefficients régularisés Ridge.
            - "intercept": Ordonnée à l'origine.
            - "r2": Coefficient de détermination R².
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"])
    alpha = params.get("alpha", 1.0)
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_.tolist(),
        "r2": float(model.score(X, y)),
    }

def lasso(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste une régression régularisée Lasso (pénalité L1 pour parcimonie).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice des variables explicatives (2D array-like).
            - "y": Vecteur cible continu (1D array-like).
            - "alpha" (optionnel): Paramètre de pénalité L1 (défaut: 1.0).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Prédictions du modèle Lasso.
            - "coefficients": Coefficients estimés (potentiellement nuls).
            - "intercept": Ordonnée à l'origine.
            - "r2": Coefficient de détermination R².
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"])
    alpha = params.get("alpha", 1.0)
    model = Lasso(alpha=alpha)
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_.tolist(),
        "r2": float(model.score(X, y)),
    }

def svm(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste un classifieur à vecteurs de support (Support Vector Classifier - C-SVC).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Vecteur de cibles catégorielles (1D array-like).
            - "C" (optionnel): Paramètre de régularisation (défaut: 1.0).
            - "kernel" (optionnel): Type de noyau, ex: 'rbf', 'linear', 'poly' (défaut: 'rbf').

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Classes prédites.
            - "probabilities": Probabilités estimées pour chaque classe.
            - "accuracy": Score d'exactitude (accuracy).
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    C = params.get("C", 1.0)
    kernel = params.get("kernel", "rbf")
    model = SVC(C=C, kernel=kernel, probability=True)
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "probabilities": model.predict_proba(X).tolist(),
        "accuracy": float(model.score(X, y)),
    }

def decision_tree(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste un arbre de décision pour la classification.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Vecteur des classes (1D array-like).
            - "max_depth" (optionnel): Profondeur maximale de l'arbre (défaut: None).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Classes prédites.
            - "accuracy": Exactitude globale du modèle sur les données fournies.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    max_depth = params.get("max_depth")
    model = DecisionTreeClassifier(max_depth=max_depth)
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "accuracy": float(model.score(X, y)),
    }

def random_forest(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste une forêt aléatoire de classifieurs (Random Forest Classifier).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Vecteur des classes (1D array-like).
            - "n_estimators" (optionnel): Nombre d'arbres dans la forêt (défaut: 100).
            - "max_depth" (optionnel): Profondeur maximale autorisée par arbre (défaut: None).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Classes prédites par vote d'ensemble.
            - "accuracy": Exactitude globale de la classification.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    n_estimators = params.get("n_estimators", 100)
    max_depth = params.get("max_depth")
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "accuracy": float(model.score(X, y)),
    }

def xgboost_boosting(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ajuste un modèle de gradient boosting optimisé avec XGBoost (XGBClassifier).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Vecteur des classes (1D array-like).
            - "n_estimators" (optionnel): Nombre d'arbres de boosting (défaut: 100).
            - "learning_rate" (optionnel): Taux d'apprentissage de descente (défaut: 0.1).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "predictions": Classes prédites.
            - "accuracy": Exactitude globale obtenue sur l'échantillon.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    n_estimators = params.get("n_estimators", 100)
    learning_rate = params.get("learning_rate", 0.1)
    model = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate, eval_metric="logloss")
    model.fit(X, y)
    return {
        "predictions": model.predict(X).tolist(),
        "accuracy": float(model.score(X, y)),
    }

