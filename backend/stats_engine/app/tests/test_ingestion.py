from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_csv_ingest_success():
    payload = {
        "method_id": "csv_ingest",
        "payload": {"csv_string": "col1,col2\n1,2\n3,4"}
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "success"
    data = json_resp["data"]
    assert isinstance(data, list)
    assert data == [{"col1": 1.0, "col2": 2.0}, {"col1": 3.0, "col2": 4.0}]


def test_parquet_ingest_missing_file():
    payload = {"method_id": "parquet_ingest", "payload": {"file_path": "nonexistent.parquet"}}
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 500


def test_sql_ingest_missing_params():
    payload = {"method_id": "sql_ingest", "payload": {"connection_string": "sqlite:///:memory:"}}
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 500


def test_mongodb_ingest_missing_fields():
    payload = {"method_id": "mongodb_ingest", "payload": {"uri": "mongodb://localhost:27017"}}
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 500
