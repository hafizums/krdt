# ADR-0002 — Use Python and FastAPI for the backend

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT requires a backend that supports:

- versioned REST APIs with explicit schemas;
- geospatial and time-series persistence in later gates;
- strict validation and testability;
- structured logging and health checks;
- clear separation between HTTP transport and domain logic.

Python is widely used in geospatial and data engineering workflows. FastAPI provides OpenAPI generation, Pydantic v2 integration, and async-capable request handling while keeping HTTP concerns in the API layer.

The Gate 0 specification pins **Python 3.13.14** (conservative baseline versus the newer 3.14 line) and **FastAPI 0.139.x** with locked dependencies via `uv.lock`.

## Decision

1. Use **Python 3.13.14** as the sole supported backend runtime for Gate 0 and the initial programme baseline.
2. Use **FastAPI** as the HTTP/API framework.
3. Use **Pydantic v2** for settings and request/response schemas.
4. Use **SQLAlchemy 2**, **Alembic**, and **Psycopg 3** for database access and migrations.
5. Use **Ruff** (format + lint) and **mypy** (strict) for quality gates.
6. Preserve **domain isolation** — the `domain` package must not import FastAPI, SQLAlchemy, or other infrastructure frameworks.

## Consequences

### Positive

- Strong typing and schema validation at API boundaries.
- Mature ecosystem for PostGIS, geospatial libraries, and scientific tooling in later gates.
- OpenAPI documentation generated from code for contract review.
- Fast iteration for foundation health endpoints and future CRUD APIs.

### Negative

- Python async and ORM patterns require discipline to avoid leaking persistence into domain code.
- Strict mypy imposes upfront typing cost.
- GIL-bound CPU work may need worker offload in later analytics gates.

### Neutral

- Uvicorn remains the ASGI server; production deployment details deferred to Gate 7.

## Compliance

- Backend code lives under `apps/api/src/krdt_api/`.
- Domain rules implemented in Gate 1+ must remain framework-free and tested without FastAPI where practical.
- Dependency versions controlled by `uv.lock`; Gate 0 freezes FastAPI 0.139.x line at project creation.
- Health and future domain routes use `/api/v1` versioning prefix.

## References

- `docs/DEVELOPMENT.md` — pinned Python and uv versions
- `docs/architecture/overview.md` — dependency direction
- Gate 0 specification — backend baseline
