# KRDT Project Charter

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | APPROVED FOR IMPLEMENTATION              |
| Gate         | 0 — Repository and Governance Foundation |
| Last updated | 2026-07-24                               |

This charter defines why KRDT exists, who it serves, what Version 1 includes and excludes, and how the project is governed. It does not claim formal participation from any government agency, utility operator, or other external organization unless that participation has been independently confirmed and documented elsewhere.

---

## 1. Problem statement

Kundasang, Ranau, Sabah, Malaysia sits in a high-relief environment where terrain, rainfall, slope instability, road access, and settlement exposure interact in ways that affect community safety and operational response. Operational information about these conditions is often fragmented across maps, spreadsheets, sensor systems, inspection records, and informal channels.

Decision-makers and field personnel need a single, trustworthy representation of:

- what assets and communities exist in the pilot area;
- what is happening now and what has changed;
- which areas and infrastructure are affected by hazards or incidents;
- what response options are available and what actions were taken.

Without a persistent digital twin that preserves provenance, quality states, and historical context, teams risk acting on incomplete, stale, or visually convincing but unverified information.

---

## 2. Mission

Build a trusted and maintainable digital representation of Kundasang that helps **authorized users** answer:

1. What exists?
2. What is happening now?
3. What changed?
4. Which assets and communities are affected?
5. What may happen next?
6. Which response options are available?
7. What action was taken?
8. What was the outcome?

KRDT prioritizes operational usefulness, traceability, data quality, safety, maintainability, and human-reviewed decision support over visual spectacle. A map or 3D view alone is not a digital twin.

---

## 3. Initial users

The first intended user groups are described by role, not by named organizations:

| User group                             | Primary need                                                                              |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| Local resilience coordinators          | Situational awareness across terrain, access routes, settlements, and critical facilities |
| Field inspection and maintenance staff | Record inspections, link findings to assets, and track follow-up work                     |
| Sensor and data operators              | Monitor ingestion health, data quality, and observation freshness                         |
| Analysts and planners                  | Review derived risk outputs with explicit model provenance and uncertainty                |
| Authorized decision support staff      | Compare scenarios and response options without autonomous system action                   |
| Project engineers and maintainers      | Extend the twin through gated delivery with auditable changes                             |

Access to operational data will be role-limited. Public-facing views, if any, must respect data classification and licensing rules defined in `DATA_CLASSIFICATION.md`.

---

## 4. Version 1 scope

Version 1 focuses on **resilience management** for the Kundasang pilot domain. Planned capabilities across the gate sequence include:

- administrative and pilot boundaries;
- terrain and elevation metadata;
- roads, bridges, and accessibility context;
- slope zones and known landslides;
- buildings, settlements, and critical facilities;
- weather and rainfall observations;
- environmental sensors and time-series observations;
- incidents, inspections, alerts, and work orders;
- response actions and historical playback;
- provenance, auditability, and data-quality states;
- human-reviewed decision support and scenario analysis.

Gate 0 establishes repository, governance, and foundation services only. Domain features begin in Gate 1 and later gates.

---

## 5. Explicit exclusions (Version 1)

The following are out of scope for Version 1 unless approved through a scope gate or Architecture Decision Record:

- autonomous evacuation orders;
- autonomous road closures;
- autonomous dispatch of emergency services;
- publication of official public hazard declarations without human authorization;
- direct control of physical infrastructure (barriers, sirens, machinery);
- modification of authoritative government records;
- facial recognition or individual resident tracking;
- tourist surveillance or commercial tourism analytics;
- complete building-interior BIM;
- full agriculture management;
- unsupported AI-generated hazard declarations presented as facts;
- public disclosure of sensitive infrastructure detail beyond authorized roles.

---

## 6. Safety boundaries

Version 1 may **support** human decisions but must **not autonomously**:

- order evacuations;
- close roads;
- dispatch emergency services;
- publish official hazard declarations;
- activate barriers, sirens, or machinery;
- alter authoritative government records.

Additional safety rules:

- Observed, derived, estimated, forecast, simulated, and operator-entered information must remain distinguishable in storage and presentation.
- Unvalidated analytical models must not trigger operational actions.
- Alerts must remain reviewable by authorized personnel.
- Safety-critical information must be handled according to `DATA_CLASSIFICATION.md` and `SECURITY_MODEL.md`.

---

## 7. Definition of project success

KRDT Version 1 is successful when authorized users can reliably:

| Success criterion                                                                     | Evidence type                                |
| ------------------------------------------------------------------------------------- | -------------------------------------------- |
| Identify registered assets, observations, and relationships within the pilot boundary | Queryable registry with provenance           |
| Distinguish current state from historical state                                       | Timestamped records and playback             |
| See data quality and source for operational displays                                  | Quality states and source metadata visible   |
| Trace incidents through inspection and response workflows                             | Audit trail and linked entities              |
| Review analytical outputs without mistaking them for observations                     | Model name, version, inputs, and uncertainty |
| Operate within documented security and classification rules                           | Security model compliance                    |
| Onboard a new developer from repository documentation alone                           | Reproducible bootstrap and validation        |

Gate 0 success is narrower: a new developer can clone the repository, install pinned tools, start foundation services, run canonical validation, and understand project rules without prior chat history. Gate 0 does **not** by itself make KRDT an operational digital twin.

---

## 8. Governance and gatekeeper workflow

KRDT uses a strict gate-based delivery model:

```text
Human intent
    ↓
Gate specification
    ↓
Cursor implementation
    ↓
Automated and manual evidence
    ↓
Independent gatekeeper review
    ↓
PASS, CONDITIONAL PASS, or FAIL
    ↓
Next authorized gate
```

### Roles

| Role                                                                | Responsibility                                                                          |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Human owner                                                         | Product intent, scope approval, policy decisions, acceptance of operational risk        |
| Cursor                                                              | Implementation within the active gate only; tests and evidence; implementation report   |
| Gatekeeper                                                          | Independent review of repository state, diff, tests, and evidence; issues gate decision |
| Repository                                                          | Persistent technical source of truth                                                    |
| Memory files (`AGENTS.md`, `PROJECT_MEMORY.md`, `PHASE_HANDOFF.md`) | Persistent conversational and decision context                                          |

### Gate decision meanings

- **PASS** — All acceptance criteria satisfied; evidence complete; no unresolved blocker in gate scope.
- **CONDITIONAL PASS** — Objective achieved with a bounded, documented follow-up that does not block the next gate.
- **FAIL** — One or more criteria not met, evidence missing, scope violated, or material risk unresolved. The next gate must not start.

### Rules binding all participants

- Cursor must not approve its own gate.
- Cursor must not begin the next gate without explicit authorization after a gatekeeper **PASS**.
- Implementation agents implement only the active gate specification.
- The gatekeeper reviews evidence independently; summaries and screenshots alone are insufficient.
- Scope expansion requires human owner approval and, where applicable, an ADR.

### Current gate status

**Gate 0 — Repository and Governance Foundation** is in progress. It is **not** marked passed until the gatekeeper issues an explicit **PASS** decision.

---

## 9. Related documents

| Document                      | Purpose                                                                |
| ----------------------------- | ---------------------------------------------------------------------- |
| `AGENTS.md`                   | Agent roles, gate rules, testing honesty, implementation report format |
| `PROJECT_MEMORY.md`           | Durable approved decisions and completed gates                         |
| `PHASE_HANDOFF.md`            | Active working context for the current gate                            |
| `docs/DATA_CLASSIFICATION.md` | Data handling classes and metadata requirements                        |
| `docs/RISK_REGISTER.md`       | Identified project risks and mitigations                               |
| `docs/SECURITY_MODEL.md`      | Trust boundaries and security practices                                |
| `docs/DEFINITION_OF_DONE.md`  | Completion criteria for all gate work                                  |
| `docs/gates/gate-0/SPEC.md`   | Active Gate 0 implementation contract                                  |

---

## 10. Charter maintenance

Update this charter when:

- Version 1 scope or exclusions change with owner approval;
- safety boundaries change;
- the mission or primary user groups change materially;
- governance roles or gate workflow change.

Minor clarifications may be made during Gate 0 foundation work. Material scope changes require owner approval and gatekeeper acknowledgment before implementation proceeds.
