"""Database connectivity helpers."""

from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from krdt_api.config import Settings


@dataclass(frozen=True)
class DatabaseHealth:
    """Result of a database readiness probe."""

    available: bool
    postgis_available: bool
    error: str | None = None


def create_db_engine(settings: Settings) -> Engine:
    """Create a SQLAlchemy engine with bounded connect timeout."""

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": settings.database_connect_timeout_seconds},
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a session factory bound to the given engine."""

    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db_session(session_factory: sessionmaker[Session]) -> Generator[Session]:
    """Yield a database session for request scope."""

    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def check_database_health(engine: Engine) -> DatabaseHealth:
    """Verify database connectivity and PostGIS availability."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            postgis_row = connection.execute(
                text(
                    "SELECT PostGIS_Version(), EXISTS("
                    "SELECT 1 FROM pg_extension WHERE extname = 'postgis_topology')"
                )
            ).one()
            postgis_version = postgis_row[0]
            topology_available = bool(postgis_row[1])
            if not postgis_version:
                return DatabaseHealth(
                    available=False,
                    postgis_available=False,
                    error="PostGIS is not available",
                )
            if not topology_available:
                return DatabaseHealth(
                    available=False,
                    postgis_available=False,
                    error="postgis_topology extension is not available",
                )
            return DatabaseHealth(available=True, postgis_available=True)
    except Exception as exc:  # noqa: BLE001 - readiness must not leak internals
        return DatabaseHealth(
            available=False,
            postgis_available=False,
            error=str(exc.__class__.__name__),
        )
