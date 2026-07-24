# KRDT Architecture Overview

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Scope        | Foundation only — no domain entities     |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

This document describes the **logical architecture** approved for KRDT. Gate 0 implements scaffolding and health behavior only. Domain entities, spatial registry, maps, sensors, and workflows appear in later gates.

---

## 1. Purpose

KRDT is an operational digital twin—not merely a map or dashboard. Architecture must preserve:

- clear boundaries between layers;
- testable domain logic isolated from frameworks;
- explicit integration adapters for external systems;
- traceable data and audit paths as features are added;
- safe failure modes during foundation and operations.

---

## 2. Gate 0 foundation scope

Gate 0 delivers:

| Component             | Gate 0 behavior                                                                   |
| --------------------- | --------------------------------------------------------------------------------- |
| `apps/api`            | FastAPI app, config, structured logging, health endpoints, empty `/api/v1` router |
| `apps/web`            | React status page, backend readiness check                                        |
| `infra/compose.yaml`  | Local PostgreSQL 18 + PostGIS 3.6                                                 |
| `apps/api/migrations` | Alembic baseline; no domain tables                                                |
| `scripts/validate.py` | Canonical validation                                                              |
| Governance docs       | Charter, classification, risks, security, ADRs                                    |

Gate 0 explicitly does **not** deliver entity registry, maps, ingestion, auth, or analytics.

---

## 3. Logical boundaries

From `AGENTS.md`, the initial system preserves these layers:

```text
┌──────────────────────────────────────────────────────────────┐
│                  Frontend applications                        │
│         apps/web (Gate 0: foundation status page)             │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP
┌────────────────────────────▼─────────────────────────────────┐
│                        API layer                              │
│    FastAPI routes, schemas, correlation ID, health checks     │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                  Application services                         │
│         Use cases orchestrating domain + repositories           │
│              (packages present; empty in Gate 0)              │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                       Domain model                            │
│    Entities, value objects, domain rules (Gate 1+ entities)     │
│              (package present; empty in Gate 0)               │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│              Repository interfaces / adapters                 │
│         Persistence abstractions (future gates)                 │
└────────────────────────────┬─────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  Persistence  │  │  Integrations   │  │ Ingestion workers │
│ PostgreSQL/   │  │ External APIs,  │  │ MQTT, scheduled   │
│ PostGIS       │  │ agency adapters │  │ jobs (future)     │
└───────────────┘  └─────────────────┘  └──────────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
              ┌──────────────────────────┐
              │ Analytics & geospatial   │
              │ processing (future)      │
              └──────────────────────────┘
                             │
              ┌──────────────▼─────────────┐
              │      Observability         │
              │  Logging (Gate 0); metrics │
              │  tracing (later gates)     │
              └────────────────────────────┘
```

---

## 4. Dependency direction

Required dependency flow:

```text
API → Application → Domain
Application → Repository interfaces
Integrations → External systems
Repositories → Persistence implementations
Workers → Application services
```

The **domain layer must not depend on**:

- FastAPI;
- SQLAlchemy ORM models;
- MQTT clients;
- cloud SDKs;
- Cesium or MapLibre;
- external government APIs.

External access goes through explicit integration adapters in later gates.

---

## 5. Monorepo layout

ADR-0001 places backend, frontend, infrastructure, scripts, documentation, and memory files in one repository during the initial programme:

```text
kundasang-resilience-digital-twin/
├── apps/
│   ├── api/                 Backend service
│   └── web/                 Frontend application
├── docs/                    Governance, ADRs, gate specs
├── infra/                   Docker Compose, DB init
├── scripts/                 Bootstrap, validation, memory check
├── .github/                 CI, Dependabot, PR template
├── AGENTS.md
├── PROJECT_MEMORY.md
└── PHASE_HANDOFF.md
```

Atomic changes across API contracts, frontend, migrations, and docs reduce gate delivery risk.

---

## 6. Backend structure (Gate 0)

```text
apps/api/src/krdt_api/
├── api/                     HTTP layer (health, v1 router)
├── application/             Use cases (empty)
├── domain/                  Domain model (empty)
├── infrastructure/          DB session, logging
├── config.py                Typed settings from environment
└── main.py                  Application factory
```

Health endpoints:

- **Liveness** — process up; no database call.
- **Readiness** — database connectivity and PostGIS availability with bounded timeout.

---

## 7. Frontend structure (Gate 0)

```text
apps/web/src/
├── App.tsx                  Foundation status page
├── main.tsx                 Entry point
└── test/                    Vitest setup
```

No map libraries (MapLibre, Cesium) in Gate 0—deferred to Gate 1 per ADR-0003.

---

## 8. Data and persistence (Gate 0)

| Decision             | ADR      | Gate 0 state                                  |
| -------------------- | -------- | --------------------------------------------- |
| PostgreSQL + PostGIS | ADR-0004 | Local container only                          |
| UTC persistence      | ADR-0005 | Log timestamps UTC                            |
| Project CRS          | ADR-0006 | **Deferred** — no authoritative projected CRS |
| TimescaleDB          | —        | Deferred until observation gate               |

Baseline migration verifies extensions; it does not create KRDT domain tables.

---

## 9. Cross-cutting concerns

| Concern        | Gate 0 approach                           | Future gates                       |
| -------------- | ----------------------------------------- | ---------------------------------- |
| Configuration  | Environment variables + Pydantic settings | Environment-specific secret stores |
| Logging        | Structured JSON, correlation ID           | Centralized aggregation (Gate 7)   |
| Authentication | None (documented exception)               | Role-based access, ADR required    |
| API versioning | `/api/v1` prefix                          | Domain routes under v1             |
| Testing        | pytest, Vitest, integration with PostGIS  | Expanded per gate                  |
| Validation     | `scripts/validate.py`                     | Same canonical command in CI       |

---

## 10. Planned evolution by gate (not implemented)

| Gate   | Architectural addition                                          |
| ------ | --------------------------------------------------------------- |
| Gate 1 | Pilot boundary, entity registry, spatial types, MapLibre 2D map |
| Gate 2 | Sensors, observations, time-series, quality states              |
| Gate 3 | Incidents, inspections, work orders, audit                      |
| Gate 4 | Physical sensor adapters, buffering, sync                       |
| Gate 5 | Risk analytics, model versioning                                |
| Gate 6 | Scenarios and decision support                                  |
| Gate 7 | Production hardening, backup, observability                     |

This table is **planning context** only. Implementation requires each gate's specification and gatekeeper PASS.

---

## 11. Domain entities

No domain entities are implemented in Gate 0.

Expected future concepts (from programme scope) include AdministrativeArea, RoadSegment, Bridge, SlopeZone, Sensor, Observation, Incident, and others listed in `AGENTS.md` and `PROJECT_MEMORY.md`. They must not be created until the gate that authorizes them.

Each future entity requires stable internal identifiers (e.g. `KDT-ROAD-000042`), provenance, timestamps, and explicit relationships—not display names alone.

---

## 12. Related documents

| Document                                       | Purpose                            |
| ---------------------------------------------- | ---------------------------------- |
| `docs/adr/README.md`                           | ADR index and process              |
| `docs/adr/0001-use-a-monorepo.md`              | Repository model                   |
| `docs/adr/0004-use-postgresql-postgis.md`      | Database direction                 |
| `docs/adr/0006-defer-project-crs-selection.md` | CRS deferral                       |
| `AGENTS.md`                                    | Full architecture and domain rules |
| `docs/gates/gate-0/SPEC.md`                    | Gate 0 deliverables                |

Update this overview when an ADR or passed gate materially changes boundaries.
