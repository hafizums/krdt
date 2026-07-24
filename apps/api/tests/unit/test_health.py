"""Unit tests for health endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_live_returns_expected_response(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "krdt-api"}


def test_live_does_not_require_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_check(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("database should not be queried for liveness")

    monkeypatch.setattr("krdt_api.api.health.check_database_health", fail_check)
    response = client.get("/health/live")
    assert response.status_code == 200


def test_readiness_returns_503_when_database_unavailable(unavailable_client: TestClient) -> None:
    response = unavailable_client.get("/health/ready")
    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "not_ready"
    assert payload["database"] == "unavailable"
    assert payload["postgis"] == "unavailable"
    assert "password" not in response.text
    assert "postgresql" not in response.text


def test_correlation_id_is_returned(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Correlation-ID": "abc12345-test-id"})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == "abc12345-test-id"


def test_malformed_correlation_id_is_replaced(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Correlation-ID": "bad id"})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") != "bad id"
    assert response.headers.get("X-Correlation-ID")
