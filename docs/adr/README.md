# Architecture Decision Records (ADR)

## Purpose

Architecture Decision Records capture significant, durable technical decisions for the Kundasang Resilience Digital Twin (KRDT). They provide context for future developers and AI agents when the rationale would otherwise be lost.

Create an ADR when a decision is:

- difficult to reverse;
- cross-cutting;
- security-sensitive;
- operationally significant;
- likely to affect multiple future gates.

Cursor may **draft** ADRs but must not mark them **ACCEPTED** without approval from the human owner or an approved gate specification.

---

## ADR states

| State          | Meaning                           |
| -------------- | --------------------------------- |
| **PROPOSED**   | Under discussion; not yet binding |
| **ACCEPTED**   | Approved and in effect            |
| **SUPERSEDED** | Replaced by a newer ADR           |
| **REJECTED**   | Considered and not adopted        |

When superseding an ADR, update the old record's status and link to the replacement.

---

## File naming

```text
docs/adr/NNNN-short-title-in-kebab-case.md
```

- `NNNN` — four-digit sequence starting at `0001`
- Use lowercase words separated by hyphens
- Title in the document header may use natural casing

---

## Template

Each ADR should include:

```markdown
# ADR-NNNN — Title

## Status

ACCEPTED | PROPOSED | SUPERSEDED | REJECTED

## Date

YYYY-MM-DD

## Context

What problem or constraint led to this decision?

## Decision

What was decided?

## Consequences

Positive, negative, and neutral outcomes.

## Compliance

How gates and code must respect this decision.
```

---

## Process

1. Identify a decision that meets the ADR threshold.
2. Draft ADR as **PROPOSED** (or include in gate specification for batch approval).
3. Human owner or gatekeeper reviews with gate evidence.
4. On approval, set status to **ACCEPTED** and record in `PROJECT_MEMORY.md` section 14.
5. Implement within the authorized gate scope.
6. Reference ADR number in code comments, docs, or gate reports only when it aids traceability—not excessively.

Gate 0 approved six foundation ADRs through the Gate 0 specification. Later gates may add ADRs without modifying accepted Gate 0 records except to supersede with explicit replacement.

---

## Index

| ADR                                           | Title                                     | Status   | Date       |
| --------------------------------------------- | ----------------------------------------- | -------- | ---------- |
| [0001](0001-use-a-monorepo.md)                | Use a monorepo                            | ACCEPTED | 2026-07-24 |
| [0002](0002-use-python-fastapi-backend.md)    | Use Python and FastAPI for the backend    | ACCEPTED | 2026-07-24 |
| [0003](0003-use-react-typescript-frontend.md) | Use React and TypeScript for the frontend | ACCEPTED | 2026-07-24 |
| [0004](0004-use-postgresql-postgis.md)        | Use PostgreSQL and PostGIS                | ACCEPTED | 2026-07-24 |
| [0005](0005-use-utc-for-persistence.md)       | Persist timestamps in UTC                 | ACCEPTED | 2026-07-24 |
| [0006](0006-defer-project-crs-selection.md)   | Defer project CRS selection               | ACCEPTED | 2026-07-24 |

---

## Related documents

- `AGENTS.md` — section 30 (Architecture Decision Records)
- `PROJECT_MEMORY.md` — accepted ADR table
- `docs/gates/gate-0/SPEC.md` — Gate 0 ADR requirements
