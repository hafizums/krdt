# KRDT Risk Register

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | ACTIVE                                   |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

Likelihood and impact use a 1–5 scale (1 = low, 5 = high). Status values: **OPEN**, **MITIGATING**, **ACCEPTED**, **CLOSED**.

Owners are organizational roles. Use **UNASSIGNED** where ownership is not yet confirmed. This register does not invent agency commitments.

---

## Risk summary

| ID       | Title                                 | Likelihood | Impact | Owner               | Status     |
| -------- | ------------------------------------- | ---------: | -----: | ------------------- | ---------- |
| RISK-001 | Source-data access                    |          4 |      5 | UNASSIGNED          | OPEN       |
| RISK-002 | Coordinate-system mismatch            |          4 |      5 | UNASSIGNED          | MITIGATING |
| RISK-003 | Stale data presented as current       |          4 |      5 | UNASSIGNED          | OPEN       |
| RISK-004 | Sensor failure or drift               |          3 |      4 | UNASSIGNED          | OPEN       |
| RISK-005 | Intermittent field connectivity       |          4 |      4 | UNASSIGNED          | OPEN       |
| RISK-006 | False operational confidence          |          4 |      5 | Human owner         | MITIGATING |
| RISK-007 | Analytical-model misuse               |          3 |      5 | UNASSIGNED          | MITIGATING |
| RISK-008 | Sensitive-data exposure               |          3 |      5 | UNASSIGNED          | MITIGATING |
| RISK-009 | Dependency or supply-chain compromise |          3 |      4 | UNASSIGNED          | MITIGATING |
| RISK-010 | Insufficient agency or data ownership |          4 |      5 | UNASSIGNED          | OPEN       |
| RISK-011 | Inadequate backup and recovery        |          3 |      5 | UNASSIGNED          | OPEN       |
| RISK-012 | AI context loss between sessions      |          4 |      3 | Cursor / gatekeeper | MITIGATING |
| RISK-013 | Gate scope creep                      |          3 |      4 | Gatekeeper          | MITIGATING |
| RISK-014 | Local development secret leakage      |          2 |      4 | UNASSIGNED          | MITIGATING |

---

## Detailed risks

### RISK-001 — Source-data access

| Field           | Value                                                                                                                                                                                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Required government, infrastructure, environmental, and sensor datasets may need formal agreements, licensing fees, restricted access paths, or legal review before ingestion. Without confirmed access, gates depending on real data cannot proceed on schedule.    |
| **Likelihood**  | 4                                                                                                                                                                                                                                                                    |
| **Impact**      | 5                                                                                                                                                                                                                                                                    |
| **Mitigation**  | Maintain a dataset catalogue with licence and owner metadata; use synthetic labelled fixtures in development; document access blockers in gate specifications; do not commit restricted files; escalate unresolved access before gate planning assumes availability. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                                                                                           |
| **Status**      | OPEN                                                                                                                                                                                                                                                                 |

### RISK-002 — Coordinate-system mismatch

| Field           | Value                                                                                                                                                                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Source datasets may use different projected or geographic coordinate reference systems, axis orders, or elevation datums. Silent assumptions can misplace assets by hundreds of metres.                                                        |
| **Likelihood**  | 4                                                                                                                                                                                                                                              |
| **Impact**      | 5                                                                                                                                                                                                                                              |
| **Mitigation**  | ADR-0006 defers authoritative project CRS to Gate 1; require explicit CRS metadata on every dataset; test transformations and boundary cases; never assume incoming coordinates; select project CRS from actual source requirements in Gate 1. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                                                                     |
| **Status**      | MITIGATING                                                                                                                                                                                                                                     |

### RISK-003 — Stale data presented as current

| Field           | Value                                                                                                                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Description** | Observations, imagery, or asset registries may age without visible indicators. Users may treat outdated state as live operational truth during rainfall or slope events.                                                       |
| **Likelihood**  | 4                                                                                                                                                                                                                              |
| **Impact**      | 5                                                                                                                                                                                                                              |
| **Mitigation**  | Separate observation time and ingestion time; implement STALE and MISSING quality states; display timestamps and sources on operational views; reject silent overwrite of history; test late-arriving data behavior in Gate 2. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                                                     |
| **Status**      | OPEN                                                                                                                                                                                                                           |

### RISK-004 — Sensor failure or drift

| Field           | Value                                                                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Physical sensors may fail, lose calibration, lose power, or report plausible but wrong values. Single-sensor reliance can create false confidence in slope or rainfall conditions. |
| **Likelihood**  | 3                                                                                                                                                                                  |
| **Impact**      | 4                                                                                                                                                                                  |
| **Mitigation**  | Device health monitoring in Gate 4; quality states SUSPECT and REJECTED; redundant sources where feasible; maintenance ownership recorded per sensor; field validation workflows.  |
| **Owner**       | UNASSIGNED                                                                                                                                                                         |
| **Status**      | OPEN                                                                                                                                                                               |

### RISK-005 — Intermittent field connectivity

| Field           | Value                                                                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Kundasang field connectivity may drop for extended periods. Observations and inspections may arrive late or fail to sync, creating gaps in situational awareness.                 |
| **Likelihood**  | 4                                                                                                                                                                                 |
| **Impact**      | 4                                                                                                                                                                                 |
| **Mitigation**  | Design ingestion for buffering and idempotent resubmission in Gate 4; visible sync status; distinguish MISSING from zero; offline behavior defined only in gates that require it. |
| **Owner**       | UNASSIGNED                                                                                                                                                                        |
| **Status**      | OPEN                                                                                                                                                                              |

### RISK-006 — False operational confidence

| Field           | Value                                                                                                                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Polished maps, 3D views, or green health indicators may be mistaken for authoritative, complete, or current operational pictures even when data is partial, synthetic, or foundation-only.                                         |
| **Likelihood**  | 4                                                                                                                                                                                                                                  |
| **Impact**      | 5                                                                                                                                                                                                                                  |
| **Mitigation**  | Charter and UI must state limitations; Gate 0 frontend shows explicit not-implemented message; expose quality states and provenance in later gates; prohibit fabricated live metrics; distinguish Observed vs Derived vs Forecast. |
| **Owner**       | Human owner                                                                                                                                                                                                                        |
| **Status**      | MITIGATING                                                                                                                                                                                                                         |

### RISK-007 — Analytical-model misuse

| Field           | Value                                                                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Description** | Risk scores, forecasts, or simulations may be treated as observations or as instructions to close roads or evacuate without human review.                                                              |
| **Likelihood**  | 3                                                                                                                                                                                                      |
| **Impact**      | 5                                                                                                                                                                                                      |
| **Mitigation**  | Version 1 prohibits autonomous safety actions; model outputs labelled with model name, version, inputs, and validation status; Gate 5 governance for analytics; no unsupported AI hazard declarations. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                             |
| **Status**      | MITIGATING                                                                                                                                                                                             |

### RISK-008 — Sensitive-data exposure

| Field           | Value                                                                                                                                                                                                                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | RESTRICTED infrastructure detail, PERSONAL identifiers, or SAFETY_CRITICAL operational state may leak through public APIs, logs, exports, or repository commits.                                                      |
| **Likelihood**  | 3                                                                                                                                                                                                                     |
| **Impact**      | 5                                                                                                                                                                                                                     |
| **Mitigation**  | `DATA_CLASSIFICATION.md` and `SECURITY_MODEL.md`; deny-by-default access in future gates; secret scanning; log redaction; localhost-only dev database; no real operational data in Gate 0; security review at Gate 7. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                                            |
| **Status**      | MITIGATING                                                                                                                                                                                                            |

### RISK-009 — Dependency or supply-chain compromise

| Field           | Value                                                                                                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Compromised or unmaintained dependencies in Python, Node, container images, or CI actions could introduce vulnerabilities or supply-chain attacks.                                                      |
| **Likelihood**  | 3                                                                                                                                                                                                       |
| **Impact**      | 4                                                                                                                                                                                                       |
| **Mitigation**  | Lockfiles (`uv.lock`, `pnpm-lock.yaml`); Dependabot; pinned CI actions; version constraints; documented update process; no unpinned Git dependencies; validate frozen installs in canonical validation. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                              |
| **Status**      | MITIGATING                                                                                                                                                                                              |

### RISK-010 — Insufficient agency or data ownership

| Field           | Value                                                                                                                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Without clear operational ownership from responsible organizations, datasets may lack maintenance, incident response paths, or authority to act on system outputs.                                |
| **Likelihood**  | 4                                                                                                                                                                                                 |
| **Impact**      | 5                                                                                                                                                                                                 |
| **Mitigation**  | Record UNASSIGNED owners explicitly in metadata; escalate before production reliance; charter avoids unconfirmed participation claims; gatekeeper challenges unsupported operational assumptions. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                        |
| **Status**      | OPEN                                                                                                                                                                                              |

### RISK-011 — Inadequate backup and recovery

| Field           | Value                                                                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Database, object storage, or configuration loss without tested restore could destroy historical observations, audit trails, and incident records needed after an event.                            |
| **Likelihood**  | 3                                                                                                                                                                                                  |
| **Impact**      | 5                                                                                                                                                                                                  |
| **Mitigation**  | Defer production backup architecture to Gate 7; use named Docker volumes locally with documented reset procedure; require backup/restore runbooks and tested recovery before production readiness. |
| **Owner**       | UNASSIGNED                                                                                                                                                                                         |
| **Status**      | OPEN                                                                                                                                                                                               |

### RISK-012 — AI context loss between sessions

| Field           | Value                                                                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Coding agents starting fresh chats may contradict prior decisions, re-open settled ADRs, or implement out-of-scope features without reading project memory.                                                   |
| **Likelihood**  | 4                                                                                                                                                                                                             |
| **Impact**      | 3                                                                                                                                                                                                             |
| **Mitigation**  | `AGENTS.md`, `PROJECT_MEMORY.md`, `PHASE_HANDOFF.md`; gate specifications in `docs/gates/`; `scripts/check_memory.py` in canonical validation; bootstrap prompt for new chats; Cursor must not approve gates. |
| **Owner**       | Cursor / gatekeeper                                                                                                                                                                                           |
| **Status**      | MITIGATING                                                                                                                                                                                                    |

### RISK-013 — Gate scope creep

| Field           | Value                                                                                                                                                                                                           |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Foundation or feature work may expand into maps, domain entities, or integrations before prior gates pass, creating untested operational surface area.                                                          |
| **Likelihood**  | 3                                                                                                                                                                                                               |
| **Impact**      | 4                                                                                                                                                                                                               |
| **Mitigation**  | Strict gate specifications; implementation reports; scope guard in Gate 0 validation culture; gatekeeper review; explicit non-goals in each gate; Cursor stops when acceptance criteria cannot be demonstrated. |
| **Owner**       | Gatekeeper                                                                                                                                                                                                      |
| **Status**      | MITIGATING                                                                                                                                                                                                      |

### RISK-014 — Local development secret leakage

| Field           | Value                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Description** | Developers may commit `.env` files, paste credentials into issues, or log connection strings during debugging.                                                                |
| **Likelihood**  | 2                                                                                                                                                                             |
| **Impact**      | 4                                                                                                                                                                             |
| **Mitigation**  | `.env` in `.gitignore`; placeholders only in `.env.example`; logging redaction tests; SECURITY.md reporting path; no production secret defaults; education in DEVELOPMENT.md. |
| **Owner**       | UNASSIGNED                                                                                                                                                                    |
| **Status**      | MITIGATING                                                                                                                                                                    |

---

## Review and escalation

| Trigger                   | Action                                        |
| ------------------------- | --------------------------------------------- |
| New data source connected | Assess classification and add risks if needed |
| Gate PASS                 | Review mitigations for gate-specific risks    |
| Security or data incident | Open incident record; update status and owner |
| Owner or scope change     | Re-evaluate RISK-010 and RISK-001             |

Next scheduled review: Gate 0 gatekeeper review and upon Gate 1 specification approval.
