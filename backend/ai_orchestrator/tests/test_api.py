import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai_orchestrator"

@patch("app.api.routes.get_dataset_schema", new_callable=AsyncMock)
@patch("app.api.routes.generate_detective_suggestions", new_callable=AsyncMock)
def test_detective_endpoint(mock_suggestions, mock_schema):
    mock_schema.return_value = {"dataset_id": "ds1", "columns": ["age", "salary"]}
    mock_suggestions.return_value = {
        "suggestions": ["Is salary correlated with age?"]
    }
    
    response = client.post("/api/v1/detective", json={"dataset_id": "ds1"})
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 1
