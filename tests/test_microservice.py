"""Tests for the FastAPI microservice (advanced task #1)."""

import pytest
from fastapi.testclient import TestClient

from lab8.microservice import app, reset_items

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store() -> None:
    """Give every test an empty item store."""
    reset_items()


def test_health_returns_ok() -> None:
    """GET /health answers 200 with the documented body."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_items_start_empty() -> None:
    """GET /items answers 200 with an empty list."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_then_fetch_item() -> None:
    """POST /items stores an item retrievable by identifier."""
    created = client.post(
        "/items", json={"name": "mouse", "price": 29.9}
    )
    assert created.status_code == 201
    body = created.json()
    assert body["id"] == 1
    assert body["name"] == "mouse"
    assert body["in_stock"] is True
    fetched = client.get("/items/1")
    assert fetched.status_code == 200
    assert fetched.json() == body
    listed = client.get("/items")
    assert listed.json() == [body]


def test_missing_item_returns_404() -> None:
    """GET /items/{id} answers 404 for an unknown identifier."""
    response = client.get("/items/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "item not found"


def test_invalid_payload_returns_422() -> None:
    """Pydantic rejects a payload without the price field."""
    response = client.post("/items", json={"name": "x"})
    assert response.status_code == 422


def test_negative_price_returns_422() -> None:
    """The Item schema rejects negative prices."""
    response = client.post(
        "/items", json={"name": "x", "price": -1}
    )
    assert response.status_code == 422
