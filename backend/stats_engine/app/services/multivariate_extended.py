"""Thin wrappers around scikit‑learn / umap‑learn for extended multivariate methods.
Each function receives a ``params`` dictionary, converts inputs to ``np.ndarray``
and returns a plain ``dict`` suitable for the ``StatsExecutor``.
"""
from typing import Dict, Any
import numpy as np
from sklearn.decomposition import PCA, FastICA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
import umap


def _as_array(x: Any) -> np.ndarray:
    return np.array(x, dtype=float)


def pca(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une Analyse en Composantes Principales (ACP) sur une matrice de données.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de données (2D array-like).
            - "n_components" (optionnel): Nombre de composantes à conserver (défaut: min(n_samples, n_features)).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "components": Coordonnées projetées des observations sur les composantes.
            - "explained_variance": Variance expliquée par chaque composante.
            - "explained_variance_ratio": Ratio de variance expliquée par composante.
    """
    X = _as_array(params["X"])
    n = params.get("n_components", min(X.shape))
    model = PCA(n_components=n)
    components = model.fit_transform(X)
    return {
        "components": components.tolist(),
        "explained_variance": model.explained_variance_.tolist(),
        "explained_variance_ratio": model.explained_variance_ratio_.tolist(),
    }


def ica(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une Analyse en Composantes Indépendantes (FastICA).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice des signaux observés (2D array-like).
            - "n_components" (optionnel): Nombre de composantes indépendantes (défaut: min(n_samples, n_features)).
            - "max_iter" (optionnel): Nombre maximal d'itérations d'estimation (défaut: 200).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "sources": Signaux sources estimés indépendants.
            - "mixing_matrix": Matrice de mélange estimée.
            - "unmixing_matrix": Matrice de démélange.
    """
    X = _as_array(params["X"])
    n = params.get("n_components", min(X.shape))
    max_iter = params.get("max_iter", 200)
    model = FastICA(n_components=n, max_iter=max_iter)
    sources = model.fit_transform(X)
    return {
        "sources": sources.tolist(),
        "mixing_matrix": model.mixing_.tolist(),
        "unmixing_matrix": model.components_.tolist(),
    }


def lda(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une Analyse Discriminante Linéaire (LDA) supervisée.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de caractéristiques (2D array-like).
            - "y": Classes associées aux observations (1D array-like).
            - "n_components" (optionnel): Nombre de composantes discriminantes.

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "components": Données projetées dans l'espace discriminant.
            - "explained_variance_ratio": Ratio de variance expliquée entre les classes.
    """
    X = _as_array(params["X"])
    y = _as_array(params["y"]).astype(int)
    n = params.get("n_components", None)
    model = LinearDiscriminantAnalysis(n_components=n)
    X_red = model.fit_transform(X, y)
    return {
        "components": X_red.tolist(),
        "explained_variance_ratio": model.explained_variance_ratio_.tolist(),
    }


def tsne(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une réduction de dimension non-linéaire t-SNE pour visualisation.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de données (2D array-like).
            - "n_components" (optionnel): Dimension de l'espace projeté (défaut: 2).
            - "perplexity" (optionnel): Perplexité t-SNE (défaut: 30.0).
            - "learning_rate" (optionnel): Taux d'apprentissage de l'optimisation (défaut: 200.0).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "embedding": Coordonnées de projection dans l'espace réduit (ex: 2D).
    """
    X = _as_array(params["X"])
    n = params.get("n_components", 2)
    # perplexity must be strictly less than n_samples
    perplexity = min(params.get("perplexity", 30.0), X.shape[0] - 1)
    lr = params.get("learning_rate", 200.0)
    model = TSNE(n_components=n, perplexity=perplexity, learning_rate=lr)
    embedding = model.fit_transform(X)
    return {"embedding": embedding.tolist()}


def umap_embed(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute une réduction dimensionnelle UMAP (Uniform Manifold Approximation and Projection).

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de données (2D array-like).
            - "n_components" (optionnel): Nombre de dimensions de sortie (défaut: 2).
            - "n_neighbors" (optionnel): Nombre de voisins pris en compte (défaut: 15).
            - "min_dist" (optionnel): Distance minimale entre points projetés (défaut: 0.1).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "embedding": Coordonnées plongées dans le sous-espace.
    """
    X = _as_array(params["X"])
    n = params.get("n_components", 2)
    n_neighbors = params.get("n_neighbors", 15)
    min_dist = params.get("min_dist", 0.1)
    reducer = umap.UMAP(n_components=n, n_neighbors=n_neighbors, min_dist=min_dist)
    embedding = reducer.fit_transform(X)
    return {"embedding": embedding.tolist()}


def dbscan(params: Dict[str, Any]) -> Dict[str, Any]:
    """Exécute un partitionnement DBSCAN basé sur la densité spatiale.

    Args:
        params: Dictionnaire contenant:
            - "X": Matrice de données (2D array-like).
            - "eps" (optionnel): Rayon maximal de voisinage epsilon (défaut: 0.5).
            - "min_samples" (optionnel): Nombre minimum de voisins pour constituer un point cœur (défaut: 5).

    Returns:
        Dict[str, Any]: Dictionnaire contenant:
            - "labels": Liste des clusters attribués à chaque point (-1 pour le bruit).
            - "core_sample_indices": Indices des échantillons cœurs identifiés.
    """
    X = _as_array(params["X"])
    eps = params.get("eps", 0.5)
    min_samples = params.get("min_samples", 5)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    return {"labels": labels.tolist(), "core_sample_indices": model.core_sample_indices_.tolist()}

