# ADR-0003 — Use React and TypeScript for the frontend

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT requires a web client that can evolve into an operational map and decision-support interface. The frontend must:

- display data quality, provenance, and freshness clearly;
- integrate 2D and 3D geospatial views in later gates;
- maintain strict typing and automated tests;
- share versioning and validation with the backend monorepo.

React with TypeScript is the provisional direction in `AGENTS.md`. Gate 0 needs a foundation UI only—project identity and backend readiness—not operational widgets or maps.

## Decision

1. Use **React 19** with **TypeScript** for the web application in `apps/web`.
2. Use **Vite** as the build and dev server.
3. Use **pnpm** workspaces for JavaScript package management.
4. Use **ESLint**, **Prettier**, **Vitest**, and **React Testing Library** for quality gates.
5. **Defer mapping libraries** — do not install **MapLibre GL** or **CesiumJS** until **Gate 1** when the common operating map is authorized.

## Consequences

### Positive

- Large ecosystem for accessible UI and future map integrations.
- TypeScript strict mode catches integration errors with API types early.
- Vite provides fast local development aligned with Gate 0 bootstrap.
- Clear Gate 0 scope boundary—no map dependencies prematurely.

### Negative

- React bundle size and complexity grow as operational features accrue.
- MapLibre and Cesium integration will require additional ADRs or gate specs for performance and licensing.

### Neutral

- No component library or design system in Gate 0; added when a gate requires it.

## Compliance

- Frontend package: `apps/web` (`@krdt/web`).
- Gate 0 page must show backend readiness and explicit not-implemented messaging.
- No fabricated operational metrics, tourism content, or map views in Gate 0.
- Node **24.18.0** and pnpm **11.14.0** pinned in root `package.json`.

## References

- Gate 0 specification — frontend non-goals
- `docs/architecture/overview.md`
- ADR-0001 — monorepo layout
