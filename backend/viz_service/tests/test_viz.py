import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "viz_service"

def test_histogram_plotly():
    payload = {
        "values": [12.5, 14.2, 11.8, 15.0, 13.9, 16.2, 12.1, 14.8, 15.5],
        "title": "Distribution des âges",
        "show_kde": True,
        "format": "plotly"
    }
    response = client.post("/api/v1/chart/histogram", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["chart_type"] == "histogram"
    assert res["format"] == "plotly"
    assert "data" in res["spec"]
    assert "layout" in res["spec"]
    # Vérifie qu'on a au moins l'histogramme et la trace KDE
    assert len(res["spec"]["data"]) >= 1

def test_histogram_vegalite():
    payload = {
        "values": [10.0, 20.0, 30.0, 40.0, 50.0],
        "format": "vega_lite"
    }
    response = client.post("/api/v1/chart/histogram", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["format"] == "vega_lite"
    assert res["spec"]["mark"]["type"] == "bar"
    assert "data" in res["spec"]

def test_boxplot_single_and_multi():
    # Mono-groupe
    res_single = client.post("/api/v1/chart/boxplot", json={"values": [10, 15, 12, 18, 14, 25], "format": "plotly"})
    assert res_single.status_code == 200
    assert len(res_single.json()["spec"]["data"]) == 1

    # Multi-groupes
    res_multi = client.post("/api/v1/chart/boxplot", json={
        "groups": {
            "Groupe A": [10, 12, 14, 15],
            "Groupe B": [20, 22, 24, 25]
        },
        "format": "vega_lite"
    })
    assert res_multi.status_code == 200
    assert res_multi.json()["format"] == "vega_lite"

def test_scatter_with_trendline():
    payload = {
        "x": [1.0, 2.0, 3.0, 4.0, 5.0],
        "y": [2.1, 3.9, 6.2, 8.0, 10.1],
        "show_trendline": True,
        "format": "plotly"
    }
    response = client.post("/api/v1/chart/scatter", json=payload)
    assert response.status_code == 200
    res = response.json()
    # 2 traces: points + droite de tendance
    assert len(res["spec"]["data"]) == 2
    assert "Tendance" in res["spec"]["data"][1]["name"]

def test_correlation_heatmap():
    payload = {
        "matrix": [
            [1.0, 0.85, -0.2],
            [0.85, 1.0, -0.15],
            [-0.2, -0.15, 1.0]
        ],
        "labels": ["Ventes", "Pub", "Prix"],
        "format": "plotly"
    }
    response = client.post("/api/v1/chart/correlation_heatmap", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["spec"]["data"][0]["type"] == "heatmap"

def test_bar_chart():
    payload = {
        "categories": ["Nord", "Sud", "Est", "Ouest"],
        "values": [1200.0, 2400.0, 1800.0, 950.0],
        "format": "plotly"
    }
    response = client.post("/api/v1/chart/bar", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["spec"]["data"][0]["type"] == "bar"

def test_line_chart():
    payload = {
        "x": ["2026-01", "2026-02", "2026-03"],
        "y": [100.5, 112.3, 125.8],
        "format": "vega_lite"
    }
    response = client.post("/api/v1/chart/line", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["spec"]["mark"]["type"] == "line"

def test_residuals_plot():
    payload = {
        "predictions": [10.0, 20.0, 30.0, 40.0],
        "residuals": [0.5, -1.2, 0.8, -0.1],
        "format": "plotly"
    }
    response = client.post("/api/v1/chart/residuals", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert len(res["spec"]["data"]) == 2 # résidus + ligne zéro

def test_generic_dispatcher():
    payload = {
        "chart_type": "scatter",
        "format": "plotly",
        "data": {
            "x": [10, 20, 30],
            "y": [15, 25, 35]
        },
        "config": {"title": "Test Dispatcher"}
    }
    response = client.post("/api/v1/chart/generate", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["chart_type"] == "scatter"
    assert res["spec"]["layout"]["title"]["text"] == "Test Dispatcher"

def test_error_handling_empty_values():
    response = client.post("/api/v1/chart/histogram", json={"values": []})
    assert response.status_code == 400

def test_error_handling_mismatched_lengths():
    response = client.post("/api/v1/chart/scatter", json={"x": [1, 2], "y": [1]})
    assert response.status_code == 400
