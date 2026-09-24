from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import BaseModel, Field

ZoneType = Literal["TGO", "UEMOA"]

class PointItem(BaseModel):
    id: Optional[Union[str, int]] = Field(None, description="Identifiant unique optionnel")
    lat: float = Field(..., description="Latitude WGS84 (-90 à 90)")
    lon: float = Field(..., description="Longitude WGS84 (-180 à 180)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Attributs additionnels")

class ChoroplethRequest(BaseModel):
    zone: ZoneType = Field("TGO", description="Zone géographique (TGO pour Régions du Togo, UEMOA pour pays membres)")
    data: Dict[str, float] = Field(..., description="Dictionnaire nom_entite -> valeur numerique")
    title: Optional[str] = Field("Carte thématique choroplèthe", description="Titre de la carte")
    palette: Optional[str] = Field("Blues", description="Palette de couleurs (Blues, Greens, Oranges, Purples, Viridis)")

class PointsRequest(BaseModel):
    zone: ZoneType = Field("TGO", description="Zone géographique de référence pour le rattachement Point-in-Polygon")
    points: List[PointItem] = Field(..., description="Liste des coordonnées GPS à analyser et rattacher")

class DensityRequest(BaseModel):
    points: List[PointItem] = Field(..., description="Points géolocalisés pour calcul de la grille de densité")
    grid_size: Optional[int] = Field(20, description="Résolution de la grille (ex: 20x20)")

class ChoroplethResponse(BaseModel):
    zone: str
    title: str
    geojson: Dict[str, Any]
    legend: Dict[str, Any]
    status: str = "success"

class PointsResponse(BaseModel):
    total_points: int
    located_points: int
    points: List[Dict[str, Any]]
    aggregates_by_region: Dict[str, int]
    status: str = "success"

class DensityResponse(BaseModel):
    grid_size: int
    lat_bounds: List[float]
    lon_bounds: List[float]
    density_matrix: List[List[int]]
    max_density: int
    status: str = "success"
