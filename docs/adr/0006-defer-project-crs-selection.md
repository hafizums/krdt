# ADR-0006 — Defer project CRS selection

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT will ingest data from sources that may use WGS 84 geographic coordinates, legacy projected systems, or local surveying references. Choosing an authoritative **project coordinate reference system (CRS)** too early—without real source datasets and accuracy requirements—risks:

- systematic positional error after transformation;
- incompatible mixing of precision claims;
- costly reprojection when the wrong CRS is locked;
- silent assumptions by developers or AI agents.

Gate 0 establishes PostGIS but does not ingest pilot geometry. Gate 1 will introduce the pilot boundary and entity registry and must select CRS using actual data requirements.

## Decision

1. **Do not select an authoritative projected CRS in Gate 0.**
2. External web API exchange may use **WGS 84 (EPSG:4326)** where appropriate, with explicit CRS metadata on stored geometry once ingestion begins.
3. **Gate 1 must select** the authoritative project CRS based on:
   - source dataset CRS and accuracy;
   - pilot boundary data availability;
   - required measurement units and distortion tolerance;
   - PostGIS transformation testing results.
4. **No agent or developer may silently assume** a projected CRS (e.g. arbitrary UTM zone) in code, fixtures, or documentation presented as decided.

Until Gate 1 completes CRS ADR or specification approval, store CRS as `UNKNOWN_PENDING_GATE1` in metadata where needed.

## Consequences

### Positive

- Avoids premature wrong commitment.
- Forces Gate 1 to include CRS evidence and transformation tests.
- Aligns with `RISK-002` mitigation in the risk register.

### Negative

- Gate 1 planning must budget time for CRS analysis.
- Gate 0 spatial tests limited to extension availability, not domain geometry.

### Neutral

- PostGIS remains available for future geometry columns once CRS is chosen.

## Compliance

- Gate 0 migrations must not create geometry columns for domain entities.
- Documentation and code must not state a project CRS as finalized.
- Ingestion gates must validate incoming CRS, axis order, and transformation explicitly.
- Low-resolution data must not be presented as high-precision property measurements.

## References

- `docs/RISK_REGISTER.md` — RISK-002
- `AGENTS.md` — spatial data rules
- Gate 0 specification — ADR-0006 and Gate 1 dependency
- Gate 1 (future) — pilot boundary and CRS selection gate
