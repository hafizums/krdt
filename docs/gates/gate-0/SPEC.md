# Gate 0 — Repository and Governance Foundation

## Specification Status

**APPROVED FOR IMPLEMENTATION**

This file is the authoritative Gate 0 specification for the Kundasang Resilience Digital Twin (KRDT).

| Field                 | Value                               |
| --------------------- | ----------------------------------- |
| Project               | Kundasang Resilience Digital Twin   |
| Short name            | KRDT                                |
| Gate                  | 0                                   |
| Repository name       | `kundasang-resilience-digital-twin` |
| Implementation branch | `gate-0-foundation`                 |

## Objective

Create a reproducible, testable and documented repository foundation for KRDT without implementing digital-twin domain features.

## Approved Technical Baseline

| Component         |         Required version |
| ----------------- | -----------------------: |
| Python            |                `3.13.14` |
| uv                |                `0.11.32` |
| Node.js           |                `24.18.0` |
| pnpm              |                `11.14.0` |
| PostgreSQL        |                     `18` |
| PostGIS           |                    `3.6` |
| PostGIS container | `postgis/postgis:18-3.6` |
| FastAPI           |                `0.139.x` |
| Ruff              |                `0.15.22` |

## Required Backend Behavior

- `GET /health/live` — no database, HTTP 200, explicit schema
- `GET /health/ready` — verifies PostgreSQL and PostGIS, HTTP 200 or 503
- Empty versioned router at `/api/v1`
- OpenAPI identifies service as KRDT API

## Required Frontend Behavior

Foundation page showing project identity, environment, backend status (`Checking` / `Available` / `Unavailable`), and message that operational features are not implemented.

## Canonical Validation

```bash
uv run --frozen python scripts/validate.py
```

Fast validation:

```bash
uv run --frozen python scripts/validate.py --fast
```

## Explicit Non-Goals

No maps, spatial domain entities, sensors, incidents, external ingestion, authentication, analytics, MapLibre, Cesium, TimescaleDB, or production deployment.

## Authorization

Cursor is authorized to implement Gate 0 only. Only the gatekeeper may issue `PASS` and authorize Gate 1.

---

The full approved specification was provided in the Gate 0 implementation prompt and governs all deliverables, acceptance criteria, repository structure, tests, CI, governance documents, ADRs, and evidence requirements for this gate.
