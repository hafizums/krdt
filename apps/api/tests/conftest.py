"""Shared pytest fixtures."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from krdt_api.config import Settings
from krdt_api.main import create_app


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        environment="test",
        log_level="INFO",
        api_host="127.0.0.1",
        api_port=8000,
        database_url=os.environ.get(
            "KRDT_TEST_DATABASE_URL",
            "postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt",
        ),
        database_connect_timeout_seconds=5,
        cors_origins=["http://localhost:5173"],
    )


@pytest.fixture
def client(test_settings: Settings) -> TestClient:
    app = create_app(test_settings)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def unavailable_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    settings = Settings(
        environment="test",
        log_level="INFO",
        api_host="127.0.0.1",
        api_port=8000,
        database_url="postgresql+psycopg://invalid:invalid@127.0.0.1:1/nodb",
        database_connect_timeout_seconds=1,
        cors_origins=["http://localhost:5173"],
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
