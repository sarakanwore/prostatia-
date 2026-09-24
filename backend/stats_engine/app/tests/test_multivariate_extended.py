import numpy as np
from sklearn.datasets import load_iris
from app.services.multivariate_extended import pca, ica, lda, tsne, umap_embed, dbscan

def test_pca():
    X = np.random.rand(50, 5)
    res = pca({"X": X, "n_components": 2})
    assert len(res["components"][0]) == 2
    assert len(res["explained_variance"]) == 2

def test_ica():
    X = np.random.rand(50, 3)
    res = ica({"X": X, "n_components": 2})
    assert len(res["sources"][0]) == 2
    assert len(res["mixing_matrix"]) == 3

def test_lda():
    data = load_iris()
    X = data.data
    y = data.target
    res = lda({"X": X, "y": y, "n_components": 2})
    assert len(res["components"][0]) == 2
    assert len(res["explained_variance_ratio"]) == 2

def test_tsne():
    X = np.random.rand(30, 4)
    res = tsne({"X": X, "n_components": 2})
    assert len(res["embedding"][0]) == 2

def test_umap():
    X = np.random.rand(30, 4)
    res = umap_embed({"X": X, "n_components": 2})
    assert len(res["embedding"][0]) == 2

def test_dbscan():
    X = np.random.rand(100, 2)
    res = dbscan({"X": X, "eps": 0.2, "min_samples": 5})
    assert len(res["labels"]) == 100
