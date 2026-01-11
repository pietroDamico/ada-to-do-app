"""Tests for health endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    """Test that the health endpoint returns status code 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_ok_status():
    """Test that the health endpoint returns the expected JSON payload."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}

