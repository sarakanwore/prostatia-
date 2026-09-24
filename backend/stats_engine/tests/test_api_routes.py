from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "stats_engine"}


def test_list_methods():
    response = client.get("/api/v1/methods")
    assert response.status_code == 200
    methods = response.json()
    assert isinstance(methods, list)
    assert len(methods) > 10
    method_ids = [m["id"] for m in methods]
    assert "t_test_independent" in method_ids
    assert "summary_statistics" in method_ids


def test_get_method_found():
    response = client.get("/api/v1/methods/t_test_independent")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "t_test_independent"
    assert "assumptions" in data
    assert "outputs" in data


def test_get_method_not_found():
    response = client.get("/api/v1/methods/non_existent_method_xyz")
    assert response.status_code == 404
    assert response.json()["detail"] == "Method not found"


def test_execute_with_json_body():
    payload = {
        "method_id": "summary_statistics",
        "data_payload": {"data": [10.0, 20.0, 30.0, 40.0, 50.0]}
    }
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert res["data"]["results"]["mean"] == 30.0
    assert res["data"]["results"]["count"] == 5


def test_execute_with_query_param():
    data = {"data": [2.0, 4.0, 6.0, 8.0]}
    response = client.post("/api/v1/execute?method_id=summary_statistics", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert res["data"]["results"]["mean"] == 5.0


def test_execute_t_test_hypothesis_validation():
    payload = {
        "method_id": "t_test_independent",
        "data_payload": {
            "group_a": [10.1, 10.2, 9.9, 10.0, 10.3] * 10,
            "group_b": [12.1, 12.0, 11.9, 12.2, 12.0] * 10,
        }
    }
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert "robustness" in res["data"]
    assert "statistic" in res["data"]["results"]
    assert "p_value" in res["data"]["results"]


def test_execute_missing_method_id():
    response = client.post("/api/v1/execute", json={"data_payload": {"x": 1}})
    assert response.status_code == 400


def test_execute_unknown_method():
    payload = {
        "method_id": "unknown_calculation_method",
        "data_payload": {"data": [1, 2, 3]}
    }
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 400
