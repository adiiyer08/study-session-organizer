from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app, sessions


@pytest.fixture
def client():
    sessions.clear()

    with TestClient(app) as test_client:
        yield test_client

    sessions.clear()


@pytest.fixture
def valid_payload():
    return {
        "title": "  Midterm review  ",
        "course": "ECS 36A",
        "location": "Shields Library",
        "starts_at": (
            datetime.now(timezone.utc) + timedelta(days=1)
        ).isoformat(),
        "capacity": 5,
    }


def test_list_sessions_starts_empty(client):
    response = client.get("/sessions")

    assert response.status_code == 200
    assert response.json() == []


def test_create_session_then_list_it(client, valid_payload):
    create_response = client.post("/sessions", json=valid_payload)

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["id"]
    assert created["title"] == "Midterm review"
    assert created["course"] == valid_payload["course"]
    assert created["location"] == valid_payload["location"]
    assert created["capacity"] == valid_payload["capacity"]

    list_response = client.get("/sessions")

    assert list_response.status_code == 200
    assert list_response.json() == [created]


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("title", "   "),
        ("capacity", 1),
        ("capacity", 51),
        ("capacity", "5"),
        ("starts_at", "2000-01-01T12:00:00+00:00"),
        ("starts_at", "2099-01-01T12:00:00"),
    ],
)
def test_invalid_session_is_not_stored(
    client, valid_payload, field, invalid_value
):
    valid_payload[field] = invalid_value

    response = client.post("/sessions", json=valid_payload)

    assert response.status_code == 422
    assert any(
        error["loc"] == ["body", field]
        for error in response.json()["detail"]
    )

    list_response = client.get("/sessions")

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_created_sessions_have_distinct_ids(client, valid_payload):
    first_response = client.post("/sessions", json=valid_payload)
    second_response = client.post("/sessions", json=valid_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["id"] != second_response.json()["id"]

    list_response = client.get("/sessions")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 2