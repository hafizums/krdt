"""Integration tests requiring PostgreSQL and PostGIS."""

from __future__ import annotations

import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from krdt_api.config import Settings
from krdt_api.main import create_app


def _database_available() -> bool:
    url = os.environ.get(
        "KRDT_TEST_DATABASE_URL",
        "postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt",
    )
    try:
        engine = create_engine(url, connect_args={"connect_timeout": 2})
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _database_available(), reason="PostgreSQL is unavailable")


@pytest.fixture
def integration_settings() -> Settings:
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
def integration_client(integration_settings: Settings) -> TestClient:
    app = create_app(integration_settings)
    with TestClient(app) as test_client:
        yield test_client


def test_readiness_succeeds_with_available_postgis(integration_client: TestClient) -> None:
    response = integration_client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "available",
        "postgis": "available",
    }


def test_alembic_upgrade_downgrade_upgrade(integration_settings: Settings) -> None:
    config = Config("apps/api/alembic.ini")
    os.environ["KRDT_DATABASE_URL"] = integration_settings.database_url
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    engine = create_engine(integration_settings.database_url)
    with engine.connect() as connection:
        postgis = connection.execute(text("SELECT PostGIS_Version()")).scalar_one()
        topology = connection.execute(
            text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'postgis_topology')")
        ).scalar_one()
        revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()

    assert postgis
    assert topology is True
    assert revision == "0001_gate0_baseline"
