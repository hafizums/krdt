# PROJECT_MEMORY.md

## 1. Memory Metadata

| Field             | Value                             |
| ----------------- | --------------------------------- |
| Project           | Kundasang Resilience Digital Twin |
| Short name        | KRDT                              |
| Memory version    | 0.2.0                             |
| Last updated      | 2026-07-24                        |
| Updated by        | Cursor                            |
| Repository        | kundasang-resilience-digital-twin |
| Current lifecycle | Foundation                        |
| Current gate      | Gate 0                            |
| Overall status    | READY FOR GATEKEEPER REVIEW       |

Current gate: Gate 0
Gate 0 status: READY FOR GATEKEEPER REVIEW

This file contains durable project knowledge.

Temporary implementation context belongs in `PHASE_HANDOFF.md`.

---

## 2. Project Identity

**Status:** APPROVED

KRDT stands for **Kundasang Resilience Digital Twin**.

KRDT is intended to become an operational digital twin for Kundasang, Ranau, Sabah, Malaysia.

---

## 3. Approved Technical Baseline

**Status:** APPROVED (Gate 0)

| Component  | Version |
| ---------- | ------- |
| Python     | 3.13.14 |
| uv         | 0.11.32 |
| Node.js    | 24.18.0 |
| pnpm       | 11.14.0 |
| PostgreSQL | 18      |
| PostGIS    | 3.6     |
| FastAPI    | 0.139.2 |
| Ruff       | 0.15.22 |

Repository model: monorepo on branch `gate-0-foundation`.

---

## 4. Working Model

**Status:** APPROVED

Gatekeeper workflow remains authoritative. Cursor cannot approve gates.

---

## 5. Completed Gates

No gates have been completed.

| Gate | Decision | Date | Commit | Summary |
| ---- | -------- | ---- | ------ | ------- |
| —    | —        | —    | —      | —       |

---

## 6. Accepted Architecture Decisions

## 14. Accepted Architecture Decisions

| ADR  | Title                             | Status   | Date       |
| ---- | --------------------------------- | -------- | ---------- |
| 0001 | Use a monorepo                    | ACCEPTED | 2026-07-24 |
| 0002 | Use Python and FastAPI backend    | ACCEPTED | 2026-07-24 |
| 0003 | Use React and TypeScript frontend | ACCEPTED | 2026-07-24 |
| 0004 | Use PostgreSQL and PostGIS        | ACCEPTED | 2026-07-24 |
| 0005 | Persist timestamps in UTC         | ACCEPTED | 2026-07-24 |
| 0006 | Defer project CRS selection       | ACCEPTED | 2026-07-24 |

---

## 7. Deferred Decisions

**Status:** APPROVED

- Authoritative project CRS — deferred to Gate 1 (ADR-0006)
- TimescaleDB — deferred until observation-platform need is demonstrated
- MapLibre GL and CesiumJS — deferred to Gate 1
- Authentication — deferred until operational domain data exists

---

## 8. Known Long-Term Risks

See `docs/RISK_REGISTER.md` for the authoritative risk register.

Summary:

- source-data access;
- coordinate-system mismatch;
- stale data;
- sensor failure;
- intermittent connectivity;
- false operational confidence;
- analytical-model misuse;
- sensitive-data exposure;
- dependency compromise;
- insufficient agency ownership;
- inadequate backup and recovery;
- AI context loss.

---

## 9. Project Memory Rules

Update this file when a gate passes, an ADR is accepted, or durable constraints change.

Do not mark Gate 0 complete until the gatekeeper issues `PASS`.
