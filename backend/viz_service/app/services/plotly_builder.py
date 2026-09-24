import math
import numpy as np
from typing import List, Dict, Any, Optional, Union

def _base_layout(title: str, x_label: Optional[str] = None, y_label: Optional[str] = None) -> Dict[str, Any]:
    return {
        "title": {"text": title, "font": {"family": "Inter, sans-serif", "size": 16, "color": "#1e293b"}},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(248,250,252,0.6)",
        "xaxis": {
            "title": {"text": x_label or "", "font": {"size": 13, "color": "#475569"}},
            "gridcolor": "#e2e8f0",
            "zerolinecolor": "#cbd5e1"
        },
        "yaxis": {
            "title": {"text": y_label or "", "font": {"size": 13, "color": "#475569"}},
            "gridcolor": "#e2e8f0",
            "zerolinecolor": "#cbd5e1"
        },
        "margin": {"l": 50, "r": 30, "t": 60, "b": 50},
        "hovermode": "closest",
        "font": {"family": "Inter, sans-serif"}
    }

def _default_config() -> Dict[str, Any]:
    return {
        "responsive": True,
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"]
    }

def build_histogram(
    values: List[float],
    title: str = "Distribution des valeurs",
    x_label: Optional[str] = "Valeur",
    nbins: Optional[int] = None,
    show_kde: bool = True
) -> Dict[str, Any]:
    if not values:
        raise ValueError("La liste de valeurs ne peut pas être vide")

    arr = np.array([v for v in values if not math.isnan(v)], dtype=float)
    if len(arr) == 0:
        raise ValueError("Aucune valeur valide")

    traces: List[Dict[str, Any]] = []

    # Trace d'histogramme
    hist_trace: Dict[str, Any] = {
        "type": "histogram",
        "x": arr.tolist(),
        "name": "Fréquence",
        "marker": {"color": "#3b82f6", "opacity": 0.75, "line": {"color": "#1d4ed8", "width": 1}},
        "histnorm": "probability density" if show_kde else ""
    }
    if nbins and nbins > 0:
        hist_trace["nbinsx"] = nbins

    traces.append(hist_trace)

    # Calcul de courbe KDE gaussienne si demandé et n >= 3
    if show_kde and len(arr) >= 3:
        std = float(np.std(arr, ddof=1))
        if std > 1e-8:
            n = len(arr)
            # Règle de Silverman
            iqr = float(np.subtract(*np.percentile(arr, [75, 25])))
            silverman_scale = min(std, iqr / 1.34) if iqr > 1e-8 else std
            bandwidth = 1.06 * silverman_scale * (n ** (-0.2))

            x_grid = np.linspace(arr.min() - 0.5 * std, arr.max() + 0.5 * std, 100)
            # Évaluation KDE
            u = (x_grid[:, None] - arr[None, :]) / bandwidth
            kde_y = (np.exp(-0.5 * u**2) / (math.sqrt(2 * math.pi) * bandwidth)).mean(axis=1)

            kde_trace = {
                "type": "scatter",
                "mode": "lines",
                "x": x_grid.tolist(),
                "y": kde_y.tolist(),
                "name": "Densité (KDE)",
                "line": {"color": "#dc2626", "width": 2.5}
            }
            traces.append(kde_trace)

    layout = _base_layout(title, x_label, "Densité" if show_kde else "Fréquence")
    return {"data": traces, "layout": layout, "config": _default_config()}

def build_boxplot(
    values: Optional[List[float]] = None,
    groups: Optional[Dict[str, List[float]]] = None,
    title: str = "Boîte à moustaches",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    traces: List[Dict[str, Any]] = []

    palette = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"]

    if groups and len(groups) > 0:
        for idx, (grp_name, grp_values) in enumerate(groups.items()):
            color = palette[idx % len(palette)]
            traces.append({
                "type": "box",
                "y": grp_values,
                "name": grp_name,
                "boxpoints": "outliers",
                "jitter": 0.3,
                "marker": {"color": color, "size": 5},
                "line": {"width": 1.5}
            })
    elif values is not None and len(values) > 0:
        traces.append({
            "type": "box",
            "y": values,
            "name": "Série",
            "boxpoints": "outliers",
            "marker": {"color": "#3b82f6", "size": 5},
            "line": {"width": 1.5}
        })
    else:
        raise ValueError("Veuillez fournir soit 'values' soit 'groups' non vide")

    layout = _base_layout(title, "Groupe" if groups else "", y_label)
    return {"data": traces, "layout": layout, "config": _default_config()}

def build_scatter(
    x: List[float],
    y: List[float],
    title: str = "Nuage de points",
    x_label: Optional[str] = "X",
    y_label: Optional[str] = "Y",
    show_trendline: bool = True
) -> Dict[str, Any]:
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Les listes x et y doivent être de même longueur et non vides")

    traces: List[Dict[str, Any]] = [{
        "type": "scatter",
        "mode": "markers",
        "x": x,
        "y": y,
        "name": "Observations",
        "marker": {"color": "#2563eb", "size": 8, "opacity": 0.8, "line": {"color": "#1d4ed8", "width": 0.5}}
    }]

    if show_trendline and len(x) >= 2:
        x_arr = np.array(x, dtype=float)
        y_arr = np.array(y, dtype=float)
        x_mean = np.mean(x_arr)
        y_mean = np.mean(y_arr)
        denom = np.sum((x_arr - x_mean) ** 2)
        if denom > 1e-10:
            slope = float(np.sum((x_arr - x_mean) * (y_arr - y_mean)) / denom)
            intercept = float(y_mean - slope * x_mean)
            
            x_min, x_max = float(x_arr.min()), float(x_arr.max())
            trend_x = [x_min, x_max]
            trend_y = [intercept + slope * x_min, intercept + slope * x_max]
            
            traces.append({
                "type": "scatter",
                "mode": "lines",
                "x": trend_x,
                "y": trend_y,
                "name": f"Tendance (y={slope:.2f}x + {intercept:.2f})",
                "line": {"color": "#ef4444", "width": 2, "dash": "solid"}
            })

    layout = _base_layout(title, x_label, y_label)
    return {"data": traces, "layout": layout, "config": _default_config()}

def build_correlation_heatmap(
    matrix: List[List[float]],
    labels: List[str],
    title: str = "Matrice de corrélation"
) -> Dict[str, Any]:
    if not matrix or not labels or len(matrix) != len(labels):
        raise ValueError("La matrice doit être carrée et correspondre aux labels")

    # Arrondir pour affichage textuel
    text_matrix = [[f"{val:.2f}" for val in row] for row in matrix]

    trace = {
        "type": "heatmap",
        "z": matrix,
        "x": labels,
        "y": labels,
        "text": text_matrix,
        "texttemplate": "%{text}",
        "textfont": {"size": 11},
        "colorscale": [
            [0.0, "#b91c1c"],   # -1 (Fortement négatif -> Rouge)
            [0.5, "#f8fafc"],   #  0 (Neutre -> Blanc cassé)
            [1.0, "#1d4ed8"]    # +1 (Fortement positif -> Bleu)
        ],
        "zmin": -1.0,
        "zmax": 1.0,
        "colorbar": {"title": "r", "titleside": "right"}
    }

    layout = _base_layout(title, None, None)
    layout["yaxis"]["autorange"] = "reversed" # Standard heatmap orientation
    return {"data": [trace], "layout": layout, "config": _default_config()}

def build_bar_chart(
    categories: List[str],
    values: List[float],
    title: str = "Diagramme en barres",
    x_label: Optional[str] = "Catégorie",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    if len(categories) != len(values) or len(categories) == 0:
        raise ValueError("categories et values doivent avoir la même longueur et être non vides")

    trace = {
        "type": "bar",
        "x": categories,
        "y": values,
        "marker": {
            "color": "#3b82f6",
            "opacity": 0.9,
            "line": {"color": "#1d4ed8", "width": 1}
        }
    }

    layout = _base_layout(title, x_label, y_label)
    return {"data": [trace], "layout": layout, "config": _default_config()}

def build_line_chart(
    x: List[Union[float, str]],
    y: List[float],
    title: str = "Courbe d'évolution",
    x_label: Optional[str] = "Temps",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("x et y doivent avoir la même longueur et être non vides")

    trace = {
        "type": "scatter",
        "mode": "lines+markers",
        "x": x,
        "y": y,
        "line": {"color": "#0284c7", "width": 2.5},
        "marker": {"size": 6, "color": "#0369a1"}
    }

    layout = _base_layout(title, x_label, y_label)
    return {"data": [trace], "layout": layout, "config": _default_config()}

def build_residuals(
    predictions: List[float],
    residuals: List[float],
    title: str = "Diagnostic des résidus vs prédictions"
) -> Dict[str, Any]:
    if len(predictions) != len(residuals) or len(predictions) == 0:
        raise ValueError("predictions et residuals doivent avoir la même longueur et être non vides")

    traces: List[Dict[str, Any]] = [
        {
            "type": "scatter",
            "mode": "markers",
            "x": predictions,
            "y": residuals,
            "name": "Résidus",
            "marker": {"color": "#4f46e5", "size": 7, "opacity": 0.75}
        }
    ]

    p_min, p_max = min(predictions), max(predictions)
    # Ligne horizontale à 0
    traces.append({
        "type": "scatter",
        "mode": "lines",
        "x": [p_min, p_max],
        "y": [0.0, 0.0],
        "name": "Ligne zéro (référence)",
        "line": {"color": "#dc2626", "width": 2, "dash": "dash"}
    })

    layout = _base_layout(title, "Valeurs prédites (ŷ)", "Résidus (e = y - ŷ)")
    return {"data": traces, "layout": layout, "config": _default_config()}
