# KRDT Definition of Done

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | APPROVED FOR IMPLEMENTATION              |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

This document defines when work is **done** for KRDT gates. It aligns with `AGENTS.md` section 37 (Definition of Done) and the gatekeeper workflow. **Writing code is necessary but not sufficient.**

---

## 1. Core principle

A task or gate is done only when its behavior is implemented **and** verified **and** documented **and** reviewable by an independent gatekeeper.

Cursor must not treat its own implementation report as gate approval.

---

## 2. Task-level definition of done

Every behavior introduced by a gate must satisfy **all** of the following:

| Criterion                 | Requirement                                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| **Behavior implemented**  | Matches the active gate specification; no silent scope expansion                               |
| **Tests**                 | Appropriate unit, integration, API, migration, or domain tests cover success and failure paths |
| **Tests pass**            | Reported with exact commands and exit codes—not assumed                                        |
| **Validation**            | Required gate validation commands pass locally and in CI where applicable                      |
| **Error handling**        | Failures classified; no swallowed exceptions; no unsafe defaults                               |
| **Security reviewed**     | Impact on secrets, input validation, logging, and classification considered                    |
| **Provenance preserved**  | Data and entity rules respected where applicable                                               |
| **Documentation updated** | User-facing and developer docs describe **current** behavior only                              |
| **Memory current**        | `PHASE_HANDOFF.md` updated; `PROJECT_MEMORY.md` updated when durable decisions change          |
| **Working tree clean**    | No unexplained generated files; lockfiles intentional                                          |
| **Evidence recorded**     | Implementation report with reproducible command output                                         |

If any row is incomplete, the task is **not done**.

---

## 3. Gate-level definition of done

A gate is done **only** when the gatekeeper issues an explicit:

```text
PASS
```

or a documented **CONDITIONAL PASS** with bounded follow-up.

Until then, the gate status must remain something like:

```text
READY FOR GATEKEEPER REVIEW
```

—not passed, not closed, not authorized for the next gate.

### Gate completion checklist

| Step                        | Owner       | Done when                                                        |
| --------------------------- | ----------- | ---------------------------------------------------------------- |
| Gate specification approved | Human owner | Written spec with acceptance criteria                            |
| Implementation within scope | Cursor      | Matches spec; stop conditions respected                          |
| Canonical validation        | Cursor      | Full validation exit code `0` with evidence                      |
| Implementation report       | Cursor      | Submitted per AGENTS.md format                                   |
| Independent review          | Gatekeeper  | Repository, diff, tests, and evidence verified                   |
| Gate decision recorded      | Gatekeeper  | PASS / CONDITIONAL PASS / FAIL documented                        |
| Memory updated after PASS   | Cursor      | Completed gate in PROJECT_MEMORY; handoff prepared for next gate |

---

## 4. What does not count as done

| Anti-pattern                                        | Why it fails             |
| --------------------------------------------------- | ------------------------ |
| Code merged without tests                           | Behavior unverified      |
| Tests that mock the function under test exclusively | No meaningful validation |
| Hard-coded demo success for integrations            | False evidence           |
| Skipped tests without explanation                   | Unknown coverage gap     |
| Assertions removed to pass CI                       | Dishonest validation     |
| Screenshot-only evidence                            | Not reproducible         |
| Cursor self-declaring PASS                          | Violates governance      |
| Starting the next gate after FAIL                   | Bypasses gatekeeper      |
| Placeholder dates in memory files                   | Breaks memory validation |
| Undocumented strictness exceptions                  | Hidden quality debt      |

---

## 5. Evidence requirements

Evidence must be **exact** and ** reproducible**:

```text
Command:
<exact command>

Result:
<stdout/stderr summary and exit code>
```

Required evidence types by gate are defined in each gate specification. Gate 0 requires, among other items:

- toolchain version output;
- canonical validation output;
- migration upgrade/downgrade/upgrade;
- PostGIS extension verification;
- test counts;
- CI run reference;
- memory consistency check;
- confirmation of no Gate 1 features.

Screenshots may supplement but cannot replace command output.

---

## 6. Documentation and memory obligations

| Artifact                       | When to update                                                          |
| ------------------------------ | ----------------------------------------------------------------------- |
| `PHASE_HANDOFF.md`             | After every implementation or review cycle                              |
| `PROJECT_MEMORY.md`            | After gate PASS, ADR acceptance, scope change, or durable risk/decision |
| `README.md` / `DEVELOPMENT.md` | When bootstrap, commands, or prerequisites change                       |
| ADRs                           | When cross-cutting decisions are made                                   |
| Gate implementation report     | Before gatekeeper review                                                |

Provisional items must be labelled PROVISIONAL. Do not record unverified assumptions as VERIFIED.

---

## 7. Roles and authority

| Role        | May declare task done?               | May declare gate PASS?                |
| ----------- | ------------------------------------ | ------------------------------------- |
| Cursor      | No ( submits READY FOR REVIEW )      | **No**                                |
| Human owner | Accepts product risk; approves scope | No (unless also acting as gatekeeper) |
| Gatekeeper  | N/A                                  | **Yes**                               |

Cursor must stop after submitting implementation evidence. Only the gatekeeper authorizes the next gate.

---

## 8. Conditional pass

A **CONDITIONAL PASS** must document:

- remaining action;
- responsible owner;
- why it does not block progression;
- deadline or target gate for resolution.

Unresolved blockers inside gate scope still yield **FAIL**.

---

## 9. Alignment with AGENTS.md

This definition incorporates AGENTS.md requirements including:

- test honesty;
- no fabricated live data;
- migration testing on empty database;
- security and privacy review;
- implementation report format (section 34);
- stop conditions when acceptance criteria cannot be demonstrated.

When instructions conflict, follow source-of-truth priority in AGENTS.md section 6.

---

## 10. Gate 0 current status

Gate 0 foundation work may reach **READY FOR GATEKEEPER REVIEW** when implementation and validation are complete.

Gate 0 is **not done** until the gatekeeper records **PASS** and updates authorization for Gate 1.

---

## Related documents

- `AGENTS.md` — authoritative agent and gate rules
- `docs/PROJECT_CHARTER.md` — governance workflow
- `docs/gates/gate-0/SPEC.md` — Gate 0 acceptance criteria
- `scripts/validate.py` — canonical validation command
