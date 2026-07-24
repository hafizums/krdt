# ADR-0004 — Use PostgreSQL and PostGIS

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT is inherently geospatial: pilot boundaries, roads, slopes, settlements, sensor locations, and incidents require reliable spatial querying, integrity constraints, and transactional consistency with operational records.

The programme needs:

- an authoritative operational relational store;
- PostGIS for geometry types, spatial indexes, and topology where required;
- migration-managed schema evolution;
- local development parity with future production.

PostgreSQL 18 and PostGIS 3.6 are supported together. The official PostGIS container recommendation for new projects is `postgis/postgis:18-3.6`.

TimescaleDB may help time-series workloads but is not required for Gate 0 foundation.

## Decision

1. Use **PostgreSQL 18** as the authoritative operational database.
2. Use **PostGIS 3.6** for spatial persistence and querying.
3. Run local development database via **Docker Compose** with image `postgis/postgis:18-3.6`.
4. Enable **`postgis`** and **`postgis_topology`** extensions in development initialization.
5. Use **Alembic** for schema migrations; baseline Gate 0 migration must not create domain tables.
6. **Defer TimescaleDB** until the observation-platform gate demonstrates concrete need.

Volume mount for PostgreSQL 18 containers must use `/var/lib/postgresql`, not the legacy `/var/lib/postgresql/data` path.

## Consequences

### Positive

- Mature spatial SQL and ecosystem compatibility with OGC-oriented workflows.
- Single database for relational and geospatial data simplifies transactions and audit.
- Docker Compose gives reproducible PostGIS for developers and CI on Ubuntu.

### Negative

- Operational hosting requires DBA skills, backup, and upgrade planning (Gate 7).
- PostGIS topology and CRS choices add complexity—CRS selection deferred separately (ADR-0006).
- Container resource usage on developer machines.

### Neutral

- Object storage for rasters and tiles remains separate in later gates (S3-compatible store per programme direction).

## Compliance

- Connection via typed settings (`KRDT_DATABASE_URL`); credentials not in `alembic.ini`.
- Readiness endpoint verifies database and PostGIS availability.
- Migrations must support upgrade → downgrade → upgrade on empty database in validation.
- Database bound to localhost in development.

## References

- `infra/compose.yaml`
- `infra/postgres/init/001-extensions.sql`
- ADR-0006 — project CRS deferral
- Gate 0 specification — database requirements
