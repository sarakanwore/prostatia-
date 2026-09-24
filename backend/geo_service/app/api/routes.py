from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import (
    ChoroplethRequest,
    ChoroplethResponse,
    PointsRequest,
    PointsResponse,
    DensityRequest,
    DensityResponse
)
from app.core.boundaries import get_boundaries
from app.core.spatial import (
    build_choropleth_feature_collection,
    locate_points_in_regions,
    compute_density_grid
)

router = APIRouter(prefix="/api/v1/geo", tags=["geospatial"])

@router.get("/boundaries/{zone}")
def get_administrative_boundaries(zone: str):
    """
    Retourne la collection GeoJSON native pour la zone demandée (TGO ou UEMOA).
    """
    try:
        boundaries = get_boundaries(zone)
        return {
            "status": "success",
            "zone": zone.upper(),
            "geojson": boundaries
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des limites: {str(e)}")

@router.post("/choropleth", response_model=ChoroplethResponse)
def create_choropleth(req: ChoroplethRequest):
    """
    Génère une carte choroplèthe : fusion des données numériques
    avec les polygones administratifs de la zone (TGO / UEMOA) et attribution de styles colorés.
    """
    try:
        boundaries = get_boundaries(req.zone)
        styled_geojson, legend = build_choropleth_feature_collection(
            geojson=boundaries,
            data=req.data,
            palette_name=req.palette or "Blues",
            title=req.title or "Carte thématique choroplèthe"
        )
        return ChoroplethResponse(
            zone=req.zone,
            title=req.title or "Carte thématique choroplèthe",
            geojson=styled_geojson,
            legend=legend
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la carte: {str(e)}")

@router.post("/points", response_model=PointsResponse)
def analyze_points(req: PointsRequest):
    """
    Rattache une liste de points GPS à leur région administrative d'appartenance
    par l'algorithme Point-in-Polygon et calcule les statistiques par zone.
    """
    try:
        boundaries = get_boundaries(req.zone)
        points_data = [p.model_dump() for p in req.points]
        located, aggregates = locate_points_in_regions(points_data, boundaries)

        located_count = sum(v for k, v in aggregates.items() if k != "Hors zone")

        return PointsResponse(
            total_points=len(req.points),
            located_points=located_count,
            points=located,
            aggregates_by_region=aggregates
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse des points: {str(e)}")

@router.post("/density", response_model=DensityResponse)
def analyze_density(req: DensityRequest):
    """
    Calcule la matrice de densité géographique 2D pour affichage en heatmap.
    """
    try:
        points_data = [p.model_dump() for p in req.points]
        grid_size = req.grid_size or 20
        density_matrix, lat_bounds, lon_bounds, max_density = compute_density_grid(
            points_data, grid_size=grid_size
        )
        return DensityResponse(
            grid_size=grid_size,
            lat_bounds=lat_bounds,
            lon_bounds=lon_bounds,
            density_matrix=density_matrix,
            max_density=max_density
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul de densité: {str(e)}")
