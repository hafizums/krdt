# KRDT Data Classification Policy

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | APPROVED FOR IMPLEMENTATION              |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

This policy defines how KRDT classifies information, what metadata every dataset must carry, and how classifications affect storage, access, logging, and public release. It applies to repository content, ingested datasets, derived products, and operational records.

**Important:** The Apache 2.0 licence on KRDT source code and original documentation does **not** grant rights to external datasets. External datasets retain their original ownership, licensing, and usage restrictions. Restricted government, commercial, or personal datasets must not be committed to the repository.

---

## 1. Purpose

KRDT handles geospatial, operational, and potentially sensitive information. Consistent classification prevents:

- accidental public release of restricted infrastructure detail;
- treatment of analytical outputs as authoritative observations;
- uncontrolled retention of personal information;
- unsafe use of stale or unverified data in decision support;
- licence violations when mixing code and third-party data.

Every dataset, export, API response, and log stream must be assignable to a classification and handled accordingly.

---

## 2. Classification levels

| Classification      | Definition                                                                                                                | Examples in KRDT context                                                                                                                                                                                 | Default handling                                                                                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PUBLIC**          | Information approved for unrestricted public release after licence and accuracy review                                    | Published open-government boundaries released for reuse; anonymized aggregate statistics explicitly approved for publication; project README and open-source code                                        | May be exposed through public interfaces after licence review; still requires source attribution and freshness metadata                                                               |
| **INTERNAL**        | Non-public project or operational information that is not individually sensitive and not safety-critical on its own       | Development notes; CI logs without secrets; internal architecture docs; non-sensitive configuration templates; foundation health status in Gate 0                                                        | Authenticated project or operational access; not committed if it contains embedded secrets                                                                                            |
| **RESTRICTED**      | Non-public operational or infrastructure information whose disclosure could aid misuse, targeting, or unauthorized access | Detailed bridge structural identifiers; non-public utility routing; unpublished inspection findings; credentials or connection details; precise critical-facility layouts not cleared for public release | Role-limited access; encryption in transit and at rest where supported; audit access; no public API exposure without explicit reclassification                                        |
| **PERSONAL**        | Information that identifies or could reasonably identify a natural person                                                 | Inspector names; contact details; free-text field notes naming individuals; device identifiers tied to a person                                                                                          | Collect only when necessary; minimize fields; restrict access; audit reads and exports; define retention and deletion rules; never use for surveillance excluded from Version 1 scope |
| **SAFETY_CRITICAL** | Information relied upon during emergency or time-sensitive safety decisions                                               | Active incident status used for coordination; road closure recommendations under human review; alert states; scenario outputs presented to authorized decision staff during an event                     | Strongest access controls; full audit trail; explicit quality and freshness indicators; human review before external action; never trigger autonomous Version 1 prohibited actions    |

### Handling rules by classification

| Action                            | PUBLIC                    | INTERNAL           | RESTRICTED                                 | PERSONAL                        | SAFETY_CRITICAL                                 |
| --------------------------------- | ------------------------- | ------------------ | ------------------------------------------ | ------------------------------- | ----------------------------------------------- |
| Commit to git                     | Only when licence permits | Yes, if no secrets | No unless explicitly approved and redacted | No                              | No                                              |
| Include in public API             | After review              | No                 | No                                         | No                              | No                                              |
| Log in application logs           | Summary only              | Yes, avoid secrets | Minimal, redacted                          | Avoid; hash or omit identifiers | Structured audit events only                    |
| Cache in CDN or public bucket     | Yes, when approved        | No                 | No                                         | No                              | No                                              |
| Display without quality indicator | Yes, if verified          | Contextual         | Never without auth                         | Never without auth and purpose  | Never without auth, freshness, and review state |

When multiple classifications apply, use the **most restrictive** classification that applies to any field in the dataset or record.

---

## 3. Required dataset metadata

Every dataset ingested or published by KRDT must receive a metadata record before operational use. At minimum:

| Field                          | Requirement                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------ |
| **Classification**             | One of PUBLIC, INTERNAL, RESTRICTED, PERSONAL, SAFETY_CRITICAL                 |
| **Owner**                      | Responsible role or organization unit; use `UNASSIGNED` until confirmed        |
| **Source**                     | Producing system, agency, sensor, or document reference                        |
| **Licence**                    | SPDX identifier, contract reference, or `UNKNOWN_PENDING_REVIEW`               |
| **Retention rule**             | Minimum and maximum retention; archival or deletion trigger                    |
| **Allowed users**              | Roles or groups permitted to read, write, or export                            |
| **Public-release status**      | `NOT_APPROVED`, `APPROVED`, or `NEVER_PUBLIC`                                  |
| **Coordinate reference**       | CRS of supplied geometry; `EPSG:4326` for exchange unless otherwise documented |
| **Effective date**             | When the data applies spatially or temporally                                  |
| **Acquisition or ingest date** | When the data was collected or first ingested                                  |
| **Quality status**             | Controlled value such as VALID, SUSPECT, STALE, MISSING, REJECTED, UNVERIFIED  |
| **Update cadence**             | Expected refresh interval or event-driven note                                 |
| **Provenance chain**           | Transformations applied since source acquisition                               |

Gate 0 does not implement a dataset catalogue service. This section defines the contract for future ingestion gates.

---

## 4. External datasets and licensing

Third-party and government datasets remain subject to their **original** terms:

- KRDT code licence does not transfer data rights.
- Ingestion adapters must store licence text or a durable reference.
- Restricted or commercial datasets must not be copied into the repository.
- Synthetic or sample data must be clearly labelled and isolated from operational stores.
- Mixing open and restricted layers in one export requires review against the highest applicable classification.

Before operational use, the data owner or gatekeeper must confirm that intended system use complies with the source licence.

---

## 5. Derived and analytical data

Derived products inherit constraints from inputs and add:

| Field                         | Requirement                                                         |
| ----------------------------- | ------------------------------------------------------------------- |
| **Derivation type**           | Observed, Derived, Estimated, Forecast, Simulated, Operator-entered |
| **Model name and version**    | When produced by analytics                                          |
| **Input dataset versions**    | References to inputs at execution time                              |
| **Execution timestamp**       | UTC                                                                 |
| **Validation status**         | Whether the output passed approved validation                       |
| **Uncertainty or confidence** | When supported by the model                                         |

Analytical outputs must not be stored or displayed as observations. SAFETY_CRITICAL classification requires explicit human review workflows before reliance in operational decisions.

---

## 6. Gate 0 repository content

The Gate 0 foundation repository contains:

- source code and tests under Apache 2.0;
- original documentation classified as **INTERNAL** or **PUBLIC** as appropriate;
- development placeholders in `.env.example` only;
- **no** real Kundasang operational datasets;
- **no** restricted government files;
- **no** personal data.

Foundation health endpoints expose service availability only, not domain operational data.

---

## 7. Logging and export restrictions

Application and audit logs must:

- never include database passwords or complete connection strings;
- redact RESTRICTED and PERSONAL fields unless writing to a dedicated audited store;
- use correlation identifiers instead of duplicating full request payloads;
- record classification-aware access to RESTRICTED, PERSONAL, and SAFETY_CRITICAL data when such access is implemented in later gates.

Exports (CSV, GeoJSON, reports) must embed classification and licence metadata and respect the recipient's authorized role.

---

## 8. Reclassification and downgrade

Reclassification to a less restrictive level requires:

- documented approval from the data owner or human owner;
- licence verification for PUBLIC release;
- audit record of the decision;
- update to dataset metadata and dependent derived products.

Automatic downgrade is prohibited.

---

## 9. Related documents

| Document                  | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| `docs/SECURITY_MODEL.md`  | Trust boundaries and secret handling         |
| `docs/RISK_REGISTER.md`   | Risks including sensitive-data exposure      |
| `docs/PROJECT_CHARTER.md` | Scope and safety boundaries                  |
| `SECURITY.md`             | Vulnerability reporting                      |
| `LICENSE`                 | Code and original documentation licence only |

---

## 10. Review cycle

Review this policy:

- at each gate that introduces new data types or public interfaces;
- when a new external data source is connected;
- after any suspected classification or licence incident;
- at Gate 7 operational hardening as part of production readiness.
