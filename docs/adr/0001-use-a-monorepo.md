# ADR-0001 — Use a monorepo

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT delivers coordinated backend APIs, frontend applications, database migrations, infrastructure definitions, governance documentation, and AI memory files through a gate-based programme. Splitting these across multiple repositories at foundation stage would increase synchronization cost and make gate evidence harder to verify atomically.

The Gate 0 specification requires a single reproducible validation command, shared lockfiles, and consistent toolchain pins across all components.

## Decision

Use **one monorepo** named `kundasang-resilience-digital-twin` containing at minimum:

- `apps/api` — Python/FastAPI backend;
- `apps/web` — React/TypeScript frontend;
- `infra/` — Docker Compose and database initialization;
- `docs/` — governance, ADRs, gate specifications;
- `scripts/` — bootstrap, validation, memory checks;
- root toolchain files and persistent memory (`AGENTS.md`, `PROJECT_MEMORY.md`, `PHASE_HANDOFF.md`).

Multiple repositories are not used for the initial programme unless a future ADR supersedes this decision.

## Consequences

### Positive

- **Coordinated gate delivery** — a gate can change API, UI, migrations, and docs in one reviewable changeset.
- **Shared documentation** — governance and architecture live beside the code they describe.
- **Atomic changes** — no cross-repo version skew during foundation gates.
- **Easier context recovery** — AI agents and developers clone one repository to understand the full foundation.
- **Simplified validation** — one canonical command verifies backend, frontend, infra, and memory consistency.

### Negative

- Clone size grows as geospatial assets and history accumulate (mitigated later with Git LFS or external object storage if needed).
- Access control is repository-wide unless path-based policies are added at hosting level.
- CI must orchestrate multiple languages in one workflow.

### Neutral

- pnpm workspaces and uv workspaces organize packages inside the monorepo without separate git remotes.

## Compliance

- New applications and services default inside `apps/` unless an ADR approves extraction.
- Gate implementation reports must list files across the monorepo when relevant.
- CI and `scripts/validate.py` remain the single validation entry point for Gate 0.

## References

- Gate 0 specification — repository structure section
- `docs/architecture/overview.md`
