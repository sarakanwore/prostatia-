"""Preprocessing utilities and pipelines for PROSTATIA.
Provides functions that return sklearn Pipeline objects and visualization helpers.
"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def build_basic_pipeline() -> Pipeline:
    """Simple pipeline: impute missing values then scale numeric columns."""
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler()),
    ])
    return Pipeline([("numeric", numeric_transformer)])

def preprocess_dataframe(df: pd.DataFrame, pipeline: Pipeline) -> pd.DataFrame:
    """Apply a sklearn Pipeline to a pandas DataFrame and return the transformed DataFrame."""
    transformed = pipeline.fit_transform(df)
    if isinstance(transformed, np.ndarray):
        return pd.DataFrame(transformed, columns=df.columns, index=df.index)
    return transformed

def heatmap(df: pd.DataFrame) -> str:
    """Return a base64‑encoded PNG heatmap of the correlation matrix."""
    corr = df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="viridis", fmt=".2f")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

def dendrogram(df: pd.DataFrame) -> str:
    """Return a base64‑encoded PNG dendrogram based on hierarchical clustering of rows."""
    from scipy.cluster.hierarchy import dendrogram, linkage
    linked = linkage(df.values, method="ward")
    plt.figure(figsize=(10, 5))
    dendrogram(linked, labels=df.index.astype(str).tolist())
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()
