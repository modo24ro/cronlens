from fastapi.testclient import TestClient

from cronlens.api import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_explain_returns_description_and_runs():
    response = client.post(
        "/api/explain",
        json={"expression": "0 9 * * MON", "count": 2, "after": "2026-01-01T00:00:00Z"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "At 09:00, on Monday."
    assert body["next_runs"] == ["2026-01-05T09:00:00Z", "2026-01-12T09:00:00Z"]
    assert body["fields"][4] == {"name": "day_of_week", "source": "MON", "values": [1]}


def test_explain_reports_syntax_errors_with_field():
    response = client.post("/api/explain", json={"expression": "61 * * * *"})
    assert response.status_code == 422
    assert response.json()["detail"]["field"] == "minute"


def test_count_is_bounded():
    response = client.post("/api/explain", json={"expression": "* * * * *", "count": 1000})
    assert response.status_code == 422
