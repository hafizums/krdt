# KRDT Security Model

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | APPROVED FOR IMPLEMENTATION              |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

This document defines security boundaries for KRDT during foundation development and establishes constraints for later gates. Gate 0 intentionally exposes **no authentication** because it contains no operational domain data and no mutation endpoints beyond local development infrastructure.

---

## 1. Security objectives

KRDT must:

- protect restricted, personal, and safety-critical information by default;
- prevent accidental secret commit and log exposure;
- validate all untrusted input at system boundaries;
- preserve auditability for material operational changes;
- fail safely when dependencies are unavailable;
- avoid creating false confidence through insecure or unauthenticated demo behavior.

---

## 2. Trust boundaries

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Untrusted zone                            │
│  Browsers, external APIs, sensor gateways, future public users   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS / validated input only
┌────────────────────────────▼────────────────────────────────────┐
│                     Application boundary                         │
│  FastAPI (Gate 0: health only) │ React frontend │ future auth   │
└────────────────────────────┬────────────────────────────────────┘
                             │ parameterized queries, no secrets in logs
┌────────────────────────────▼────────────────────────────────────┐
│                   Operational data boundary                      │
│  PostgreSQL/PostGIS │ object storage │ message queues (future)   │
└────────────────────────────┬────────────────────────────────────┘
                             │ role-limited access (future)
┌────────────────────────────▼────────────────────────────────────┐
│              Restricted / personal / safety-critical             │
│  Incident detail │ inspections │ restricted infra │ audit logs   │
└─────────────────────────────────────────────────────────────────┘
```

| Boundary                     | Gate 0 state                                              | Future requirement                                        |
| ---------------------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| Public internet → API        | Localhost dev only; CORS restricted to configured origins | Authenticated APIs, rate limits, TLS termination          |
| API → database               | Readiness check with bounded timeout                      | Least-privilege DB roles, connection pooling limits       |
| API → external systems       | Not implemented                                           | Adapter timeouts, retries, circuit breaking per AGENTS.md |
| Developer workstation → repo | Trust developer machine; validate commits                 | Pre-commit hooks, secret scanning in CI                   |
| CI → repository              | Read-only checkout; least-privilege workflow permissions  | Scoped tokens if secrets required in later gates          |

---

## 3. Local development assumptions

Gate 0 local development assumes:

| Assumption                                   | Implication                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| WSL2 on Windows is the primary environment   | Authoritative bootstrap and validation paths use Linux scripts                |
| Docker Compose runs on the developer machine | PostgreSQL bound to `127.0.0.1:5432` only                                     |
| Developers are project participants          | `.env` is not committed but may contain dev placeholders on disk              |
| No production data in Gate 0                 | Absence of auth is acceptable only for foundation scope                       |
| Single-user local database                   | Default credentials in `.env.example` are placeholders, not production values |

**Not assumed:** production deployment safety, multi-tenant isolation, or public internet exposure of the dev stack.

---

## 4. Secret handling

| Rule                            | Implementation                                                      |
| ------------------------------- | ------------------------------------------------------------------- |
| Never commit secrets            | `.env` ignored; `.env.example` placeholders only                    |
| No production defaults          | Production secrets must not have fallback values in code            |
| Fail on missing required config | Typed settings reject invalid or missing critical values in tests   |
| Redact in logs                  | Passwords and full connection strings must not appear in log output |
| Rotate on exposure              | Document rotation in runbooks (Gate 7); report via SECURITY.md      |
| CI without secrets              | Gate 0 CI requires no repository secrets                            |

Store secrets in environment variables or an approved secret manager in later environments—not in source control, issue comments, or chat logs.

---

## 5. Public versus operational data

| Category                | Gate 0                                                    | Operational phase                                          |
| ----------------------- | --------------------------------------------------------- | ---------------------------------------------------------- |
| Source code             | Apache 2.0; may be public if repository visibility allows | Same                                                       |
| Documentation           | Internal/project governance                               | Classification per DATA_CLASSIFICATION.md                  |
| Health endpoints        | Non-sensitive availability                                | Still non-domain; no version leakage                       |
| Domain entities         | Not implemented                                           | RESTRICTED or higher by default                            |
| Aggregated public views | Not implemented                                           | Requires explicit PUBLIC classification and licence review |

Operational data must not appear in public responses without classification review. Gate 0 frontend must not fabricate operational metrics.

---

## 6. Application input boundaries

All external input must be validated at the boundary:

| Input channel                      | Gate 0                | Rules                                                        |
| ---------------------------------- | --------------------- | ------------------------------------------------------------ |
| HTTP headers (e.g. correlation ID) | Validated or replaced | Reject or replace malformed values per documented behavior   |
| Query parameters                   | Health routes only    | Typed response models                                        |
| Request bodies                     | None in Gate 0        | Future: Pydantic schemas, size limits, content types         |
| File uploads                       | Not implemented       | Future: virus scan, format validation, CRS checks            |
| Geospatial payloads                | Not implemented       | Geometry validation, CRS verification, pilot boundary checks |

Errors must use consistent structures without stack traces or credential details in client responses.

---

## 7. Dependency and supply-chain controls

| Control                  | Gate 0 implementation                                                    |
| ------------------------ | ------------------------------------------------------------------------ |
| Lockfiles                | `uv.lock`, `pnpm-lock.yaml` committed                                    |
| Version pinning          | Python 3.13.14, uv 0.11.32, Node 24.18.0, pnpm 11.14.0                   |
| Dependabot               | `.github/dependabot.yml`                                                 |
| CI action pinning        | Immutable SHA with version comment in workflow                           |
| Licence compatibility    | Apache 2.0 for project code; review third-party licences before adoption |
| No unpinned Git installs | Package manifests use version constraints                                |
| Container images         | Approved `postgis/postgis:18-3.6` only in Gate 0                         |

New dependencies require justification, licence check, and validation pass before merge.

---

## 8. Logging restrictions

Structured logs may include:

- timestamp (UTC);
- level;
- service and environment;
- HTTP method, path, status, duration;
- correlation ID.

Logs must **not** include by default:

- database passwords or complete `KRDT_DATABASE_URL`;
- request or response bodies;
- PERSONAL identifiers;
- RESTRICTED operational payload;
- stack traces sent to clients (server-side logging of errors may be restricted in production).

Accept incoming correlation IDs only after validation; generate when absent; return in response headers.

---

## 9. Future authentication boundary

Gate 0 does not implement authentication or authorization.

Future gates must:

- deny access by default to operational endpoints;
- separate public information from operational views;
- enforce role-based access aligned with DATA_CLASSIFICATION.md;
- avoid frontend-only authorization;
- record security-relevant actions in immutable audit records;
- use authenticated service-to-service communication between components.

The introduction of identity providers, session handling, or API keys requires an ADR and gate specification.

---

## 10. Prohibited practices

The following are prohibited across the programme:

| Practice                                                | Reason                                   |
| ------------------------------------------------------- | ---------------------------------------- |
| Committing `.env`, keys, tokens, or certificates        | Credential exposure                      |
| Committing restricted government or commercial datasets | Licence and classification violation     |
| Wildcard CORS in any environment                        | Cross-origin abuse                       |
| Publicly exposing the development database              | Data breach and misuse                   |
| Logging secrets or full connection strings              | Log aggregation leakage                  |
| Presenting synthetic data as live operational fact      | False confidence                         |
| Disabling validation to accept bad geometry or input    | Silent data corruption                   |
| Frontend-only security checks                           | Trivial bypass                           |
| Autonomous Version 1 prohibited safety actions          | Safety boundary violation                |
| Infinite retries on external calls                      | Amplification and duplicate side effects |
| Unbounded queries or unpaginated high-volume endpoints  | DoS and data exfiltration risk           |

---

## 11. Vulnerability reporting

See [SECURITY.md](../SECURITY.md) for coordinated disclosure expectations. Do not open public issues for unresolved security vulnerabilities affecting operational deployments.

---

## 12. Gate 0 security evidence

Gate 0 must demonstrate:

- no committed secrets;
- ignored `.env`;
- localhost-only database binding;
- bounded database connect timeout;
- restricted CORS (no wildcard);
- safe readiness failure responses (HTTP 503 without stack traces or credentials);
- credential redaction in logging tests;
- frozen lockfiles and CI least-privilege permissions.

---

## 13. Related documents

| Document                      | Purpose                      |
| ----------------------------- | ---------------------------- |
| `docs/DATA_CLASSIFICATION.md` | Data handling classes        |
| `docs/RISK_REGISTER.md`       | RISK-008, RISK-009, RISK-014 |
| `AGENTS.md`                   | Security and privacy section |
| `SECURITY.md`                 | Reporting process            |

Review this model at Gate 7 and whenever authentication, public APIs, or new data classes are introduced.
