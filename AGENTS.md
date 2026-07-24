# AGENTS.md

## 1. Project Identity

**Project:** Kundasang Resilience Digital Twin
**Short name:** KRDT
**Repository status:** Pre-foundation
**Primary location:** Kundasang, Ranau, Sabah, Malaysia

KRDT is an operational digital twin for understanding and managing conditions affecting Kundasang.

The first implementation focuses on:

- terrain and slope conditions;
- rainfall and weather observations;
- landslide risk;
- roads, bridges and accessibility;
- settlements and critical facilities;
- incidents, inspections and response actions;
- historical playback;
- operational decision support.

KRDT is not merely a 3D map, dashboard or GIS viewer.

A capability may be described as part of the digital twin only when it contributes to a persistent representation of real entities, observations, relationships, historical state, analysis or operational workflows.

---

## 2. Mission

Build a trusted and maintainable digital representation of Kundasang that helps authorized users answer:

1. What exists?
2. What is happening now?
3. What changed?
4. Which assets and communities are affected?
5. What may happen next?
6. Which response options are available?
7. What action was taken?
8. What was the outcome?

The system must prioritize reliability, traceability and operational usefulness over visual spectacle.

---

## 3. Current Scope

The initial project scope is the **Kundasang resilience domain**.

### Included

- administrative and pilot boundaries;
- terrain and elevation;
- roads and bridges;
- slope zones;
- known landslides;
- buildings;
- settlements;
- critical facilities;
- weather observations;
- rainfall observations;
- environmental sensors;
- incidents;
- inspections;
- alerts;
- work orders;
- response actions;
- historical state;
- provenance and data quality.

### Excluded from Version 1

- autonomous evacuation orders;
- autonomous road closures;
- individual resident tracking;
- facial recognition;
- tourist surveillance;
- complete building-interior BIM;
- full agriculture management;
- commercial tourism analytics;
- unsupported AI-generated hazard declarations;
- direct control of physical infrastructure;
- public disclosure of sensitive infrastructure data.

Scope may only expand through an approved gate or Architecture Decision Record.

---

## 4. Working Model

This repository uses a strict gate-based development model.

```text
Intent
  ↓
Gate specification
  ↓
Cursor implementation
  ↓
Automated and manual evidence
  ↓
Independent gatekeeper review
  ↓
PASS, CONDITIONAL PASS or FAIL
  ↓
Next gate
```

Implementation agents must not declare their own gate approved.

A gate is complete only after the gatekeeper explicitly returns **PASS**.

---

## 5. Agent Roles

## 5.1 Human Owner

The human owner:

- defines project intent;
- makes product and policy decisions;
- approves major scope changes;
- resolves organizational questions;
- accepts operational risk;
- decides whether the project proceeds after gatekeeper findings.

The human owner has final authority.

## 5.2 Gatekeeper

The gatekeeper:

- defines or reviews gate specifications;
- evaluates implementation evidence;
- checks scope compliance;
- challenges unsupported claims;
- identifies missing tests and risks;
- issues PASS, CONDITIONAL PASS or FAIL;
- does not assume that implementation reports are correct;
- does not approve based only on screenshots or summaries.

The gatekeeper should review the repository state, diff, tests and evidence whenever access is available.

## 5.3 Cursor Coding Agent

Cursor is the implementation agent.

Cursor must:

- work on only the active gate;
- read this file before making changes;
- inspect existing code before proposing architecture;
- follow the active gate specification;
- make the smallest coherent change that satisfies the gate;
- write or update tests;
- run required validation;
- report exact evidence;
- disclose failures and incomplete work;
- stop after submitting the implementation report.

Cursor must not:

- approve its own work;
- silently expand scope;
- begin the next gate;
- hide failing tests;
- claim commands were run when they were not;
- replace production behavior with hard-coded demonstrations;
- invent unavailable datasets or API responses;
- weaken security or validation to make tests pass.

---

## 6. Source-of-Truth Order

When instructions conflict, use this priority:

1. Explicit instruction from the human owner.
2. Active gate specification.
3. Approved Architecture Decision Records.
4. This `AGENTS.md`.
5. Existing tests and API contracts.
6. Existing implementation.
7. Comments, examples and informal notes.

A lower-priority source must not override a higher-priority source.

When a conflict remains unresolved, stop and report it instead of guessing.

---

## 7. Gate Rules

Every gate must define:

- objective;
- context;
- included scope;
- excluded scope;
- required deliverables;
- acceptance criteria;
- required tests;
- required evidence;
- explicit non-goals;
- rollback considerations;
- known risks.

Cursor must implement only what is required to pass the active gate.

### Scope discipline

A change is permitted when it is:

- required by the gate;
- necessary to keep the project buildable;
- necessary to test the gate;
- a small refactor directly enabling the gate;
- a security correction discovered while implementing the gate.

A change is not permitted when it is:

- speculative future architecture;
- unrelated cleanup;
- a new feature outside the gate;
- a large dependency upgrade without approval;
- a UI redesign not required by the gate;
- an optimization without measured need;
- a replacement of an approved technology without an ADR.

Unexpected issues must be reported separately.

---

## 8. Gate Decision Definitions

### PASS

All acceptance criteria are satisfied.

Required evidence is complete and credible.

No unresolved blocker remains inside the gate scope.

### CONDITIONAL PASS

The gate objective is achieved, but a clearly bounded non-blocking action remains.

A conditional pass must state:

- the remaining action;
- the owner;
- why it does not block progression;
- the deadline or future gate where it must be resolved.

### FAIL

One or more acceptance criteria are not satisfied, evidence is missing, tests fail, scope was violated, or material risk remains unresolved.

A failed gate must not be bypassed by starting the next gate.

---

## 9. Provisional Technical Direction

These are provisional defaults until replaced by an approved ADR.

### Backend

- Python 3.12 or newer
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Data

- PostgreSQL
- PostGIS
- TimescaleDB where time-series behavior is required
- object storage compatible with the S3 API

### Messaging and ingestion

- MQTT for sensor messaging
- REST APIs for system integrations
- scheduled ingestion for external datasets
- asynchronous workers for expensive processing

### Geospatial services

- OGC API Features where practical
- OGC SensorThings-compatible data structures where practical
- GeoJSON for small vector responses
- Cloud-Optimized GeoTIFF for raster products
- 3D Tiles for large 3D datasets
- STAC-compatible metadata for imagery and derived raster assets

### Frontend

- TypeScript
- React
- MapLibre GL for 2D
- CesiumJS for 3D

### Local development

The first development environment should be simple and reproducible.

Use Docker Compose only when the active gate requires multiple infrastructure services. Do not introduce Kubernetes during the foundation gates.

---

## 10. Architecture Boundaries

The initial system should preserve these logical boundaries:

```text
API layer
Application services
Domain model
Repositories
Integrations
Ingestion workers
Analytics
Geospatial processing
Persistence
Observability
Frontend applications
```

### Required direction of dependencies

```text
API → Application → Domain
Application → Repository interfaces
Integrations → External systems
Repositories → Persistence implementations
Workers → Application services
```

The domain layer must not depend directly on:

- FastAPI;
- SQLAlchemy models;
- MQTT clients;
- cloud SDKs;
- Cesium;
- external agency APIs.

External systems must be accessed through explicit integration adapters.

---

## 11. Domain Integrity

Every persistent real-world entity must have:

- a stable internal identifier;
- an entity type;
- a lifecycle state where applicable;
- a creation timestamp;
- an update timestamp;
- a source or responsible owner;
- provenance;
- an effective time where applicable.

Example identifiers:

```text
KDT-AREA-000001
KDT-SLOPE-000127
KDT-ROAD-000042
KDT-BRIDGE-000008
KDT-BUILDING-004918
KDT-SENSOR-000231
KDT-INCIDENT-2026-000017
```

Display names, external identifiers and database primary keys must not be treated as interchangeable.

Changing the source dataset must not silently change the identity of an existing physical entity.

---

## 12. Core Domain Entities

Expected domain concepts include:

```text
AdministrativeArea
TerrainDataset
ImageryDataset
LandParcel
SlopeZone
Landslide
RoadSegment
Bridge
DrainageAsset
Building
Settlement
CriticalFacility
UtilityAsset
Sensor
Observation
WeatherEvent
Alert
Incident
Inspection
WorkOrder
Scenario
ResponseAction
DataSource
DataQualityResult
```

This list is not permission to implement every entity immediately.

Only active-gate entities should be created.

---

## 13. Relationship Requirements

The twin must represent meaningful relationships between entities.

Examples:

```text
SlopeZone threatens RoadSegment
RoadSegment providesAccessTo Settlement
Building locatedWithin AdministrativeArea
Building exposedTo SlopeZone
Sensor monitors SlopeZone
Observation producedBy Sensor
WeatherEvent affects AdministrativeArea
Incident affects RoadSegment
Inspection evaluates SlopeZone
WorkOrder respondsTo Incident
CriticalFacility serves Settlement
ResponseAction addresses Incident
```

Relationships must be explicit and queryable. They must not exist only as text descriptions.

---

## 14. Spatial Data Rules

All geospatial data must include:

- coordinate reference system;
- source;
- acquisition or effective date;
- spatial accuracy where known;
- processing history;
- licensing or usage restrictions;
- data-quality status.

### Coordinate systems

- Store authoritative geometry in an explicitly chosen project coordinate reference system.
- Use WGS 84 longitude and latitude for external web API exchange where appropriate.
- Never assume that incoming coordinates use the expected coordinate system.
- Coordinate transformations must be explicit and tested.
- Axis order must be verified.
- Elevation datum must be recorded when elevation is used.

### Geometry validation

Incoming geometry must be checked for:

- null geometry;
- invalid geometry;
- unexpected geometry type;
- self-intersection;
- empty geometry;
- coordinates outside the pilot boundary where relevant;
- invalid altitude values;
- duplicate entities;
- unreasonable precision.

Invalid geometry must not be silently accepted.

### Spatial uncertainty

Do not present spatial data as more precise than its source.

A low-resolution satellite product must not be displayed or described as a property-level measurement.

---

## 15. Observation and Time-Series Rules

Every observation must include:

- observation identifier;
- source;
- sensor or producing system;
- observed property;
- value;
- unit;
- observation time;
- ingestion time;
- quality status;
- provenance;
- location or monitored entity;
- raw source reference where available.

Observation time and ingestion time must remain separate.

Late-arriving data must not overwrite history without an audit trail.

Missing data, stale data and rejected data must be distinguishable from valid zero values.

Units must be explicit. Unit conversion must be tested.

---

## 16. Data Quality

Every data ingestion path must define:

- schema validation;
- type validation;
- range validation;
- timestamp validation;
- duplicate detection;
- coordinate validation;
- unit handling;
- missing-value handling;
- provenance;
- failure handling;
- retry behavior.

Quality states should use controlled values such as:

```text
VALID
SUSPECT
STALE
MISSING
REJECTED
UNVERIFIED
```

The frontend must not display suspect or unverified data as confirmed without a visible quality indicator.

---

## 17. Simulation and Prediction Rules

A calculated risk score, forecast or simulation is not an observed fact.

Every analytical output must include:

- model name;
- model version;
- input dataset versions;
- execution timestamp;
- spatial and temporal scope;
- confidence or uncertainty where supported;
- validation status;
- explanation or contributing factors where practical.

The system must distinguish:

```text
Observed
Derived
Estimated
Forecast
Simulated
Operator-entered
```

Unvalidated models must not trigger autonomous operational actions.

No model may be described as operationally reliable until it passes an approved validation gate.

---

## 18. Safety-Critical Boundaries

The system may support human decisions, but Version 1 must not autonomously:

- order evacuations;
- close roads;
- dispatch emergency services;
- publish public hazard declarations;
- operate barriers, sirens or machinery;
- alter official government records.

Alerts must be reviewable by authorized personnel.

Operational actions must record:

- responsible user;
- decision time;
- evidence available;
- action taken;
- affected entities;
- result;
- notes.

---

## 19. Security and Privacy

Apply least privilege.

Required principles:

- deny access by default;
- separate public and operational information;
- protect sensitive infrastructure data;
- validate all untrusted input;
- avoid exposing internal identifiers unnecessarily;
- keep secrets outside source control;
- log security-relevant actions;
- rotate credentials through documented procedures;
- use authenticated service-to-service communication;
- rate-limit externally accessible ingestion endpoints.

Never commit:

- passwords;
- API keys;
- database credentials;
- private certificates;
- production tokens;
- personal datasets;
- restricted agency files.

Example environment files must contain placeholders only.

---

## 20. Auditability

Material changes must be auditable.

Audit records should capture:

- actor;
- action;
- entity;
- previous state where appropriate;
- new state where appropriate;
- timestamp;
- source application;
- reason or correlation identifier.

Audit records must not be modified through ordinary application operations.

Logs are not a substitute for domain audit records.

---

## 21. Reliability

All external integrations must define:

- timeout;
- retry policy;
- maximum retry count;
- backoff behavior;
- idempotency behavior;
- error classification;
- circuit-breaking strategy where justified;
- observability;
- fallback behavior.

No outbound request may wait indefinitely.

Retries must not duplicate incidents, observations, work orders or side effects.

Background jobs must be restart-safe or explicitly report that they are not.

---

## 22. Offline and Connectivity Considerations

Kundasang field connectivity may be intermittent.

Field and sensor workflows should be designed to support, where required:

- local buffering;
- delayed synchronization;
- idempotent resubmission;
- visible synchronization status;
- conflict handling;
- device health reporting;
- timestamps generated at the observation source.

Offline behavior must be implemented only in a gate that defines its required behavior and tests.

---

## 23. API Rules

APIs must:

- use versioned routes;
- use explicit request and response schemas;
- validate all input;
- return consistent error structures;
- support correlation identifiers;
- document authentication requirements;
- document pagination;
- document time and coordinate formats;
- avoid leaking stack traces;
- preserve backward compatibility within a published API version.

Recommended route structure:

```text
/api/v1/areas
/api/v1/roads
/api/v1/slopes
/api/v1/sensors
/api/v1/observations
/api/v1/incidents
/api/v1/inspections
/api/v1/work-orders
/api/v1/scenarios
```

Routes must not be implemented merely because they appear in this example.

---

## 24. Database and Migration Rules

All schema changes must use migrations.

A migration must be:

- deterministic;
- reviewable;
- reversible where practical;
- tested on an empty database;
- tested against the previous application revision;
- safe for existing data.

Do not:

- edit an already released migration;
- silently drop data;
- use application startup as an undocumented migration mechanism;
- depend on manually changing production tables.

Destructive migrations require explicit gatekeeper attention.

---

## 25. Testing Requirements

Every behavior introduced by a gate must have appropriate tests.

Expected test categories:

- unit tests;
- domain tests;
- repository tests;
- API tests;
- migration tests;
- integration tests;
- geospatial validation tests;
- ingestion tests;
- security tests;
- end-to-end tests where required.

Tests must cover both successful and failing behavior.

For spatial logic, include edge cases such as:

- boundary intersections;
- invalid geometry;
- different coordinate systems;
- empty geometry;
- points exactly on boundaries;
- antimeridian behavior if relevant;
- elevation absence;
- duplicate source features.

For time-series logic, include:

- duplicate observations;
- out-of-order observations;
- stale observations;
- future timestamps;
- daylight-saving assumptions;
- timezone conversion;
- missing readings;
- late ingestion.

Sabah timestamps should be handled explicitly using the `Asia/Kuching` timezone when local time is required. Persist event timestamps in UTC unless an approved ADR specifies otherwise.

---

## 26. Test Honesty

A test must validate meaningful behavior.

Do not:

- assert only that a route returns any response;
- mock the exact function being tested;
- replace integration behavior with hard-coded success;
- mark tests skipped without explanation;
- remove assertions to obtain a passing suite;
- reduce coverage requirements without approval.

When a real external service cannot be used, tests must use a controlled adapter, fixture or recorded contract that preserves the expected interface and failure behavior.

---

## 27. Quality Checks

The repository should eventually provide one canonical validation command, for example:

```bash
make validate
```

Until that command exists, each gate specification must state the exact commands to run.

Validation should eventually include:

```text
format check
lint
static type checking
unit tests
integration tests
migration validation
dependency validation
security checks
build verification
```

Cursor must report exact commands and exit results.

“Tests pass” is not sufficient evidence.

---

## 28. Dependencies

Before adding a dependency, verify:

- active maintenance;
- license compatibility;
- security posture;
- Python or Node version support;
- whether an existing dependency already provides the capability;
- operational cost;
- vendor lock-in;
- upgrade impact.

Dependencies must be version constrained.

Large framework or infrastructure changes require an ADR.

---

## 29. Documentation

Code behavior and documentation must change together.

Required documentation may include:

- README;
- architecture overview;
- local setup;
- environment variables;
- API contract;
- migration procedure;
- dataset catalogue;
- data dictionary;
- operational runbook;
- incident runbook;
- backup and restore procedure;
- ADRs.

Documentation must describe the current system, not a planned future system, unless clearly labelled as proposed.

---

## 30. Architecture Decision Records

Create an ADR for decisions that are:

- difficult to reverse;
- cross-cutting;
- security-sensitive;
- operationally significant;
- likely to affect multiple future gates.

Examples:

- project coordinate reference system;
- primary database;
- sensor protocol;
- identity provider;
- 2D and 3D rendering stack;
- event architecture;
- tenancy model;
- deployment platform;
- public-data boundary;
- analytical model governance.

ADR states:

```text
PROPOSED
ACCEPTED
SUPERSEDED
REJECTED
```

Cursor may draft an ADR but may not mark it accepted without approval.

---

## 31. Repository Practices

Use focused commits.

Recommended commit format:

```text
feat(gate-1): add spatial entity registry
fix(gate-2): reject duplicate sensor observations
test(gate-1): cover invalid road geometries
docs(adr): propose project coordinate system
chore(dev): add local PostGIS service
```

Do not combine unrelated work into one commit.

Do not rewrite shared history without explicit authorization.

Do not create releases or production deployments unless the active gate requires them.

---

## 32. Prohibited Shortcuts

The following are not acceptable:

- fabricated live data presented as real;
- sample data mixed into production datasets without labelling;
- fake integrations that always return success;
- credentials committed to the repository;
- disabled validation to accept malformed geospatial data;
- swallowed exceptions;
- broad `except` blocks without classification and logging;
- infinite retries;
- unbounded queries;
- unpaginated high-volume endpoints;
- frontend-only authorization;
- production schema creation through test fixtures;
- using screenshots as the only evidence;
- claiming a digital twin exists when only a static map exists.

Synthetic data is permitted only when visibly identified and isolated from operational data.

---

## 33. Stop Conditions

Cursor must stop and report before continuing when:

- an active gate requirement is contradictory;
- required source data is unavailable;
- a legal or licensing restriction is discovered;
- credentials or restricted information appear in the repository;
- a destructive migration is required;
- an architectural change outside the gate becomes necessary;
- tests reveal a safety-critical defect outside the active gate;
- implementation would require weakening an approved security control;
- acceptance criteria cannot be objectively demonstrated.

The report must state what was discovered and what decision is required.

---

## 34. Implementation Report Format

At the end of every gate, Cursor must submit the following report.

````markdown
# Gate <number> Implementation Report

## Status

READY FOR GATEKEEPER REVIEW | BLOCKED | PARTIAL

## Gate Objective

<Exact objective from the gate specification>

## Scope Implemented

- <Implemented item>
- <Implemented item>

## Files Changed

| File         | Change      |
| ------------ | ----------- |
| path/to/file | Description |

## Architecture Notes

- <Important design decision>
- <Boundary or trade-off>

## Database Changes

- Migration:
- Tables or columns:
- Upgrade behavior:
- Downgrade behavior:
- Existing-data impact:

## API Changes

| Method | Route       | Purpose |
| ------ | ----------- | ------- |
| GET    | /api/v1/... | ...     |

## Security and Privacy

- Authentication impact:
- Authorization impact:
- Input validation:
- Sensitive data impact:
- Secrets introduced: NONE or explanation

## Tests Added or Updated

| Test      | Behavior Verified |
| --------- | ----------------- |
| test_name | Description       |

## Validation Commands

### Command

```bash
<exact command>
```
````

### Result

```text
<exact result and exit status>
```

Repeat for every command.

## Manual Validation

1. <Step>
2. <Step>
3. <Observed result>

## Acceptance Criteria Evidence

| Criterion   | Result    | Evidence                        |
| ----------- | --------- | ------------------------------- |
| Criterion 1 | PASS/FAIL | Test, command or file reference |

## Known Limitations

- <Limitation>
- NONE if none are known

## Risks Discovered

- <Risk and impact>
- NONE if none were discovered

## Scope Deviations

- <Deviation and reason>
- NONE if there were no deviations

## Deferred Work

- <Explicitly deferred item>
- NONE if nothing was deferred

## Git Evidence

- Branch:
- Commit:
- Working tree status:
- Diff summary:

## Final Declaration

I implemented only the active gate scope.

I did not begin the next gate.

I have disclosed all known failures, skipped tests, limitations and deviations.

````

Reports must contain evidence, not only conclusions.

---

## 35. Gatekeeper Review Format

The gatekeeper should respond using:

```markdown
# Gate <number> Review

## Decision

PASS | CONDITIONAL PASS | FAIL

## Verified Evidence

- <Evidence independently reviewed>

## Acceptance Criteria

| Criterion | Result | Notes |
|---|---|---|
| Criterion | PASS/FAIL | Explanation |

## Findings

### Blockers

- <Finding>
- NONE

### Major Findings

- <Finding>
- NONE

### Minor Findings

- <Finding>
- NONE

## Required Corrections

1. <Correction>
2. <Correction>

## Deferred Items

- <Approved deferred item>
- NONE

## Authorization

AUTHORIZED TO BEGIN GATE <next number>

or

NOT AUTHORIZED TO BEGIN THE NEXT GATE
````

---

## 36. Initial Gate Sequence

The provisional delivery sequence is:

### Gate 0 — Repository and Governance Foundation

- project charter;
- repository structure;
- contribution rules;
- local-development baseline;
- initial ADRs;
- risk register;
- data-classification model;
- definition of done.

### Gate 1 — Common Operating Map Foundation

- pilot boundary;
- spatial database;
- entity registry;
- terrain metadata;
- roads;
- bridges;
- settlements;
- critical facilities;
- initial 2D map;
- provenance.

### Gate 2 — Observation Platform

- sensors;
- observations;
- time-series storage;
- ingestion validation;
- data-quality states;
- historical playback.

### Gate 3 — Incident and Inspection Workflow

- incidents;
- field reports;
- inspections;
- assignments;
- work orders;
- audit trail.

### Gate 4 — Instrumented Slope Pilot

- physical sensor adapters;
- device health;
- gateway buffering;
- synchronization;
- field validation.

### Gate 5 — Risk Analytics

- rainfall accumulation;
- risk scoring;
- exposure analysis;
- model versioning;
- confidence reporting;
- historical validation.

### Gate 6 — Scenario and Decision Support

- road closure scenarios;
- settlement isolation analysis;
- alternative routing;
- resource-positioning scenarios.

### Gate 7 — Operational Hardening

- security;
- performance;
- backup and restore;
- disaster recovery;
- observability;
- operational runbooks;
- production readiness.

This sequence may be changed only through an approved project decision.

---

## 37. Definition of Done

A task is done only when:

- behavior is implemented;
- tests cover the behavior;
- tests pass;
- validation commands pass;
- error behavior is handled;
- security impact is reviewed;
- data provenance is preserved;
- documentation is updated;
- no unexplained generated files remain;
- working-tree changes are understood;
- evidence is included in the implementation report.

A gate is done only when the gatekeeper issues PASS.

---

## 38. Current Instruction to Coding Agents

Do not implement KRDT application features yet.

The next authorized activity is **Gate 0 specification and repository foundation**.

Before coding, obtain the Gate 0 brief containing:

- exact repository technology;
- repository name;
- required development environments;
- project structure;
- required foundation files;
- validation commands;
- Gate 0 acceptance criteria.

Until that brief is approved, this `AGENTS.md` is the controlling project-development policy.

## Persistent Project Memory

This repository uses Markdown memory files so a new AI chat can recover project context without relying on previous conversations.

The required files are:

```text
PROJECT_MEMORY.md
PHASE_HANDOFF.md
```

### PROJECT_MEMORY.md

`PROJECT_MEMORY.md` contains durable project knowledge:

- project identity and purpose;
- approved architecture;
- accepted ADRs;
- technology decisions;
- domain terminology;
- important constraints;
- repository conventions;
- completed gates;
- long-term risks;
- decisions that future agents must not reconsider without approval.

It must not contain:

- temporary debugging notes;
- unverified assumptions;
- copied chat transcripts;
- secrets;
- credentials;
- detailed command output;
- obsolete implementation plans.

### PHASE_HANDOFF.md

`PHASE_HANDOFF.md` contains the active working context:

- current gate;
- gate objective;
- current repository state;
- work completed;
- work remaining;
- latest validation results;
- blockers;
- known failures;
- files changed;
- decisions needed;
- exact next action;
- instructions for the next chat.

This file is replaced or substantially updated after every implementation or review cycle.

### Agent responsibilities

Before starting work, every coding or reviewing agent must read:

1. `AGENTS.md`
2. `PROJECT_MEMORY.md`
3. `PHASE_HANDOFF.md`
4. the active gate specification;
5. relevant accepted ADRs.

At the end of every implementation cycle, Cursor must update `PHASE_HANDOFF.md`.

After a gate receives `PASS`, Cursor must:

1. record the completed gate in `PROJECT_MEMORY.md`;
2. copy only durable decisions from `PHASE_HANDOFF.md` into `PROJECT_MEMORY.md`;
3. remove obsolete temporary information;
4. prepare `PHASE_HANDOFF.md` for the next gate;
5. include the memory-file changes in the implementation report.

Cursor must not rewrite previously approved facts without explicitly identifying the change.

### Truth and verification rules

Every memory item must be marked as one of:

```text
VERIFIED
APPROVED
PROVISIONAL
UNVERIFIED
SUPERSEDED
```

Definitions:

- `VERIFIED` — directly supported by repository state, command output or external evidence.
- `APPROVED` — explicitly accepted by the human owner or gatekeeper.
- `PROVISIONAL` — currently used but not yet formally approved.
- `UNVERIFIED` — reported but not independently confirmed.
- `SUPERSEDED` — previously valid but replaced by a newer decision.

Do not record assumptions as verified facts.

Every completed gate entry must include:

- gate number;
- decision;
- decision date;
- reviewed commit;
- validation summary;
- important decisions;
- deferred work;
- remaining risks.

### New-chat bootstrap instruction

When beginning a new AI chat, provide:

```text
Read the attached AGENTS.md, PROJECT_MEMORY.md and PHASE_HANDOFF.md.

Treat them as the project context and source of truth according to the
priority rules in AGENTS.md.

Do not start implementation yet.

First:
1. identify the current gate;
2. summarize the verified repository state;
3. list unresolved blockers and decisions;
4. state the exact next authorized action;
5. identify any contradictions or missing evidence.

Do not assume that an implementation report is accurate unless its evidence
has been verified.
```
