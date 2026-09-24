import math
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import copy

COLOR_PALETTES = {
    "Blues": ["#eff6ff", "#bfdbfe", "#60a5fa", "#2563eb", "#1e40af"],
    "Greens": ["#f0fdf4", "#bbf7d0", "#4ade80", "#16a34a", "#166534"],
    "Oranges": ["#fff7ed", "#fed7aa", "#fb923c", "#ea580c", "#9a3412"],
    "Purples": ["#faf5ff", "#e9d5ff", "#c084fc", "#9333ea", "#581c87"],
    "Viridis": ["#440154", "#3b528b", "#21908d", "#5dc863", "#fde725"]
}

def point_in_polygon(lon: float, lat: float, polygon_coords: List[List[float]]) -> bool:
    """
    Algorithme de Ray-Casting (Théorème de Jordan) pour tester
    si le point (lon, lat) est à l'intérieur du polygone.
    polygon_coords est une liste de paires [lon, lat].
    """
    n = len(polygon_coords)
    inside = False
    
    p1x, p1y = polygon_coords[0][0], polygon_coords[0][1]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n][0], polygon_coords[i % n][1]
        if lat > min(p1y, p2y):
            if lat <= max(p1y, p2y):
                if lon <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or lon <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def _normalize_name(name: str) -> str:
    """Normalise une chaîne pour comparaison souple (sans accents, minuscules)."""
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', name)
    cleaned = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return cleaned.lower().strip()

def build_choropleth_feature_collection(
    geojson: Dict[str, Any],
    data: Dict[str, float],
    palette_name: str = "Blues",
    title: str = "Choroplèthe"
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Associe les métriques utilisateur aux polygones GeoJSON et génère
    les attributs de style (fillColor, fillOpacity) et la légende.
    """
    palette = COLOR_PALETTES.get(palette_name, COLOR_PALETTES["Blues"])
    result_geojson = copy.deepcopy(geojson)

    # Dictionnaire normalisé pour les données utilisateur
    normalized_data = {_normalize_name(k): v for k, v in data.items()}

    values_found: List[float] = []
    for feature in result_geojson["features"]:
        props = feature["properties"]
        name = props.get("name", "")
        code = props.get("code", "")
        feat_id = feature.get("id", "")

        val = None
        for key in [name, code, feat_id]:
            if key and _normalize_name(key) in normalized_data:
                val = normalized_data[_normalize_name(key)]
                break

        props["value"] = val
        if val is not None:
            values_found.append(val)

    if not values_found:
        min_v, max_v = 0.0, 1.0
        breaks = [0.0, 0.25, 0.5, 0.75, 1.0]
    else:
        min_v = float(min(values_found))
        max_v = float(max(values_found))
        if min_v == max_v:
            breaks = [min_v] * 5
        else:
            breaks = np.linspace(min_v, max_v, num=len(palette) + 1).tolist()

    # Attribution des couleurs
    for feature in result_geojson["features"]:
        props = feature["properties"]
        val = props.get("value")
        if val is None:
            props["fillColor"] = "#cbd5e1" # Gris clair si non renseigné
            props["fillOpacity"] = 0.4
            props["tooltip"] = f"{props.get('name')}: Donnée non renseignée"
        else:
            # Recherche de la classe
            assigned_color = palette[-1]
            for i in range(len(palette)):
                if val <= breaks[i + 1]:
                    assigned_color = palette[i]
                    break
            props["fillColor"] = assigned_color
            props["fillOpacity"] = 0.8
            props["tooltip"] = f"{props.get('name')}: {val:,.2f}"

        props["strokeColor"] = "#ffffff"
        props["strokeWidth"] = 1.5

    legend = {
        "title": title,
        "palette": palette_name,
        "min": min_v,
        "max": max_v,
        "breaks": breaks,
        "colors": palette
    }

    return result_geojson, legend

def locate_points_in_regions(
    points: List[Dict[str, Any]],
    geojson: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Rattache chaque point GPS à la région administrative qui le contient
    par l'algorithme Point-in-Polygon.
    """
    located_points: List[Dict[str, Any]] = []
    aggregates: Dict[str, int] = {}

    for p in points:
        lat = float(p["lat"])
        lon = float(p["lon"])
        p_id = p.get("id")
        meta = p.get("metadata", {})

        assigned_region = "Hors zone"
        assigned_code = None

        for feature in geojson["features"]:
            coords = feature["geometry"]["coordinates"][0]
            if point_in_polygon(lon, lat, coords):
                assigned_region = feature["properties"]["name"]
                assigned_code = feature["properties"]["code"]
                break

        located_points.append({
            "id": p_id,
            "lat": lat,
            "lon": lon,
            "region": assigned_region,
            "code": assigned_code,
            "metadata": meta
        })

        aggregates[assigned_region] = aggregates.get(assigned_region, 0) + 1

    return located_points, aggregates

def compute_density_grid(
    points: List[Dict[str, Any]],
    grid_size: int = 20
) -> Tuple[List[List[int]], List[float], List[float], int]:
    """
    Calcule une grille de densité spatiale 2D à partir d'un ensemble de coordonnées.
    """
    if not points:
        raise ValueError("La liste de points ne peut pas être vide")

    lats = [float(p["lat"]) for p in points]
    lons = [float(p["lon"]) for p in points]

    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)

    # Padding léger si un seul point ou tous identiques
    if lat_min == lat_max:
        lat_min -= 0.1
        lat_max += 0.1
    if lon_min == lon_max:
        lon_min -= 0.1
        lon_max += 0.1

    h, xedges, yedges = np.histogram2d(
        lons, lats,
        bins=grid_size,
        range=[[lon_min, lon_max], [lat_min, lat_max]]
    )

    density_matrix = h.astype(int).tolist()
    max_density = int(h.max())

    lat_bounds = [float(lat_min), float(lat_max)]
    lon_bounds = [float(lon_min), float(lon_max)]

    return density_matrix, lat_bounds, lon_bounds, max_density
