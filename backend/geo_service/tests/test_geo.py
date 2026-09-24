import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "geo_service"

def test_get_boundaries_togo():
    response = client.get("/api/v1/geo/boundaries/TGO")
    assert response.status_code == 200
    data = response.json()
    assert data["zone"] == "TGO"
    features = data["geojson"]["features"]
    assert len(features) == 5
    region_names = [f["properties"]["name"] for f in features]
    assert "Maritime" in region_names
    assert "Savanes" in region_names
    assert "Centrale" in region_names
    assert "Kara" in region_names
    assert "Plateaux" in region_names

def test_get_boundaries_uemoa():
    response = client.get("/api/v1/geo/boundaries/UEMOA")
    assert response.status_code == 200
    data = response.json()
    features = data["geojson"]["features"]
    assert len(features) == 8 # 8 pays membres
    country_names = [f["properties"]["name"] for f in features]
    assert "Togo" in country_names
    assert "Bénin" in country_names
    assert "Sénégal" in country_names
    assert "Côte d'Ivoire" in country_names

def test_get_boundaries_invalid():
    response = client.get("/api/v1/geo/boundaries/INVALID_ZONE")
    assert response.status_code == 400

def test_choropleth_togo():
    payload = {
        "zone": "TGO",
        "data": {
            "Maritime": 2500000.0,
            "Plateaux": 1400000.0,
            "Centrale": 650000.0,
            "Kara": 850000.0,
            "Savanes": 900000.0
        },
        "title": "Population par région au Togo",
        "palette": "Viridis"
    }
    response = client.post("/api/v1/geo/choropleth", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["zone"] == "TGO"
    assert res["legend"]["palette"] == "Viridis"
    assert res["legend"]["min"] == 650000.0
    assert res["legend"]["max"] == 2500000.0
    
    features = res["geojson"]["features"]
    maritime = next(f for f in features if f["properties"]["name"] == "Maritime")
    assert maritime["properties"]["value"] == 2500000.0
    assert "fillColor" in maritime["properties"]
    assert "tooltip" in maritime["properties"]

def test_point_in_polygon_togo():
    payload = {
        "zone": "TGO",
        "points": [
            {"id": "pt_lome", "lat": 6.13, "lon": 1.22},       # Lomé -> Maritime
            {"id": "pt_sokode", "lat": 8.98, "lon": 1.14},     # Sokodé -> Centrale
            {"id": "pt_kara", "lat": 9.55, "lon": 1.19},       # Kara -> Kara
            {"id": "pt_dapaong", "lat": 10.86, "lon": 0.20},   # Dapaong -> Savanes
            {"id": "pt_atakpame", "lat": 7.53, "lon": 1.13},   # Atakpamé -> Plateaux
            {"id": "pt_ocean", "lat": 2.0, "lon": 1.0}         # Hors zone
        ]
    }
    response = client.post("/api/v1/geo/points", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["total_points"] == 6
    assert res["located_points"] == 5

    pts = {p["id"]: p["region"] for p in res["points"]}
    assert pts["pt_lome"] == "Maritime"
    assert pts["pt_sokode"] == "Centrale"
    assert pts["pt_kara"] == "Kara"
    assert pts["pt_dapaong"] == "Savanes"
    assert pts["pt_atakpame"] == "Plateaux"
    assert pts["pt_ocean"] == "Hors zone"

    assert res["aggregates_by_region"]["Maritime"] == 1
    assert res["aggregates_by_region"]["Hors zone"] == 1

def test_density_grid():
    payload = {
        "points": [
            {"lat": 6.13, "lon": 1.22},
            {"lat": 6.14, "lon": 1.23},
            {"lat": 6.15, "lon": 1.21},
            {"lat": 8.98, "lon": 1.14}
        ],
        "grid_size": 10
    }
    response = client.post("/api/v1/geo/density", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["grid_size"] == 10
    assert len(res["density_matrix"]) == 10
    assert res["max_density"] >= 1

def test_density_empty_points():
    response = client.post("/api/v1/geo/density", json={"points": []})
    assert response.status_code == 400
