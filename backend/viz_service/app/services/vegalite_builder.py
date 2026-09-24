from typing import List, Dict, Any, Optional, Union

SCHEMA_URL = "https://vega.github.io/schema/vega-lite/v5.json"

def build_vega_histogram(
    values: List[float],
    title: str = "Distribution des valeurs",
    x_label: Optional[str] = "Valeur",
    nbins: Optional[int] = None
) -> Dict[str, Any]:
    if not values:
        raise ValueError("La liste de valeurs ne peut pas être vide")

    data = [{"val": v} for v in values]
    bin_spec = {"maxbins": nbins} if nbins else True

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": {"type": "bar", "color": "#3b82f6"},
        "encoding": {
            "x": {"bin": bin_spec, "field": "val", "type": "quantitative", "title": x_label or "Valeur"},
            "y": {"aggregate": "count", "type": "quantitative", "title": "Effectif"}
        }
    }

def build_vega_boxplot(
    values: Optional[List[float]] = None,
    groups: Optional[Dict[str, List[float]]] = None,
    title: str = "Boîte à moustaches",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    data: List[Dict[str, Any]] = []

    if groups:
        for grp_name, grp_values in groups.items():
            for v in grp_values:
                data.append({"group": grp_name, "val": v})
        encoding = {
            "x": {"field": "group", "type": "nominal", "title": "Groupe"},
            "y": {"field": "val", "type": "quantitative", "title": y_label or "Valeur"},
            "color": {"field": "group", "type": "nominal"}
        }
    elif values:
        for v in values:
            data.append({"val": v})
        encoding = {
            "y": {"field": "val", "type": "quantitative", "title": y_label or "Valeur"}
        }
    else:
        raise ValueError("Fournir values ou groups")

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": {"type": "boxplot", "extent": 1.5},
        "encoding": encoding
    }

def build_vega_scatter(
    x: List[float],
    y: List[float],
    title: str = "Nuage de points",
    x_label: Optional[str] = "X",
    y_label: Optional[str] = "Y"
) -> Dict[str, Any]:
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("x et y doivent avoir la même longueur et être non vides")

    data = [{"x": x_i, "y": y_i} for x_i, y_i in zip(x, y)]

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": {"type": "point", "filled": True, "color": "#2563eb", "size": 60},
        "encoding": {
            "x": {"field": "x", "type": "quantitative", "title": x_label or "X"},
            "y": {"field": "y", "type": "quantitative", "title": y_label or "Y"}
        }
    }

def build_vega_bar_chart(
    categories: List[str],
    values: List[float],
    title: str = "Diagramme en barres",
    x_label: Optional[str] = "Catégorie",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    if len(categories) != len(values) or len(categories) == 0:
        raise ValueError("categories et values doivent avoir la même taille")

    data = [{"category": c, "val": v} for c, v in zip(categories, values)]

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": {"type": "bar", "color": "#3b82f6"},
        "encoding": {
            "x": {"field": "category", "type": "nominal", "title": x_label or "Catégorie"},
            "y": {"field": "val", "type": "quantitative", "title": y_label or "Valeur"}
        }
    }

def build_vega_line_chart(
    x: List[Union[float, str]],
    y: List[float],
    title: str = "Courbe d'évolution",
    x_label: Optional[str] = "Temps",
    y_label: Optional[str] = "Valeur"
) -> Dict[str, Any]:
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("x et y doivent avoir la même taille")

    data = [{"x": str(x_i), "val": y_i} for x_i, y_i in zip(x, y)]

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": {"type": "line", "point": True, "color": "#0284c7"},
        "encoding": {
            "x": {"field": "x", "type": "ordinal", "title": x_label or "Temps"},
            "y": {"field": "val", "type": "quantitative", "title": y_label or "Valeur"}
        }
    }

def build_vega_heatmap(
    matrix: List[List[float]],
    labels: List[str],
    title: str = "Matrice de corrélation"
) -> Dict[str, Any]:
    if not matrix or not labels or len(matrix) != len(labels):
        raise ValueError("Matrice invalide")

    data = []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            data.append({"var1": labels[i], "var2": labels[j], "corr": val})

    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "mark": "rect",
        "encoding": {
            "x": {"field": "var1", "type": "nominal", "title": "Variable 1"},
            "y": {"field": "var2", "type": "nominal", "title": "Variable 2"},
            "color": {
                "field": "corr",
                "type": "quantitative",
                "scale": {"domain": [-1, 1], "scheme": "redblue"}
            }
        }
    }

def build_vega_residuals(
    predictions: List[float],
    residuals: List[float],
    title: str = "Résidus vs prédictions"
) -> Dict[str, Any]:
    data = [{"pred": p, "res": r} for p, r in zip(predictions, residuals)]
    return {
        "$schema": SCHEMA_URL,
        "title": title,
        "data": {"values": data},
        "layer": [
            {
                "mark": {"type": "point", "color": "#4f46e5"},
                "encoding": {
                    "x": {"field": "pred", "type": "quantitative", "title": "Valeurs prédites"},
                    "y": {"field": "res", "type": "quantitative", "title": "Résidus"}
                }
            },
            {
                "mark": {"type": "rule", "color": "#dc2626", "strokeDash": [4, 4]},
                "encoding": {
                    "y": {"datum": 0}
                }
            }
        ]
    }
