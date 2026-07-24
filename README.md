# Kundasang Resilience Digital Twin (KRDT)

Operational digital twin foundation for understanding and managing resilience conditions affecting Kundasang, Ranau, Sabah, Malaysia.

---

## Status warning

**KRDT is not yet an operational digital twin.**

The project is in **Gate 0 — Repository and Governance Foundation**. The repository provides reproducible tooling, governance documents, health-checked API and frontend scaffolds, and local PostGIS infrastructure only.

There are:

- no pilot-area map;
- no entity registry or spatial domain data;
- no sensors, observations, incidents, or analytics;
- no authentication system;
- **no real Kundasang operational datasets** in this repository.

Do not use Gate 0 outputs for operational or emergency decisions.

Gate 0 is **not passed** until an independent gatekeeper issues an explicit **PASS** decision.

---

## Purpose

KRDT aims to help **authorized users** answer:

1. What exists?
2. What is happening now?
3. What changed?
4. Which assets and communities are affected?
5. What may happen next?
6. Which response options are available?
7. What action was taken?
8. What was the outcome?

The programme prioritizes traceability, data quality, safety, and human-reviewed decision support over visual spectacle. See [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) for mission, scope, and exclusions.

---

## Gate 0 scope

Gate 0 establishes:

| Area                | Delivered in Gate 0                                                |
| ------------------- | ------------------------------------------------------------------ |
| Monorepo structure  | `apps/api`, `apps/web`, `infra`, `docs`, `scripts`                 |
| Backend foundation  | FastAPI health endpoints, config, logging, Alembic baseline        |
| Frontend foundation | React status page with backend readiness check                     |
| Database            | PostgreSQL 18 + PostGIS 3.6 via Docker Compose                     |
| Governance          | Charter, classification, risks, security model, definition of done |
| ADRs                | Six accepted foundation decisions in `docs/adr/`                   |
| Validation          | `scripts/validate.py` canonical command                            |
| CI                  | GitHub Actions validation workflow                                 |
| Memory workflow     | `AGENTS.md`, `PROJECT_MEMORY.md`, `PHASE_HANDOFF.md`               |

Gate 0 explicitly excludes maps, domain entities, ingestion, MQTT, authentication, and production deployment. See [docs/gates/gate-0/SPEC.md](docs/gates/gate-0/SPEC.md) when present.

---

## Architecture summary

Logical layers (foundation only—domain packages empty):

```text
Frontend (apps/web) → API (apps/api) → Application → Domain → Repositories → PostgreSQL/PostGIS
```

External integrations, ingestion workers, and analytics are planned for later gates. Details: [docs/architecture/overview.md](docs/architecture/overview.md).

Accepted foundation decisions:

| ADR  | Decision                                        |
| ---- | ----------------------------------------------- |
| 0001 | Monorepo                                        |
| 0002 | Python 3.13 + FastAPI                           |
| 0003 | React + TypeScript (maps deferred to Gate 1)    |
| 0004 | PostgreSQL + PostGIS                            |
| 0005 | UTC persistence; Asia/Kuching for local display |
| 0006 | Project CRS deferred to Gate 1                  |

---

## Prerequisites

Pinned toolchain (exact versions required):

| Tool           | Version                        |
| -------------- | ------------------------------ |
| Python         | 3.13.14                        |
| uv             | 0.11.32                        |
| Node.js        | 24.18.0                        |
| pnpm           | 11.14.0                        |
| Docker Compose | v2 (Docker Desktop on Windows) |

Full setup: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

## WSL2 development (Windows)

**WSL2 is the authoritative Windows development environment.**

1. Install WSL2 with Ubuntu 22.04+.
2. Enable Docker Desktop WSL integration.
3. Clone inside WSL (e.g. `~/projects/`), not `/mnt/c/`.
4. Install pinned tools inside WSL.
5. Run bootstrap and validation from WSL bash.

Native Windows PowerShell scripts exist (`scripts/bootstrap.ps1`, `scripts/validate.ps1`) but Linux/WSL paths define expected behavior.

---

## Bootstrap

```bash
git clone <repository-url>
cd kundasang-resilience-digital-twin
chmod +x scripts/bootstrap.sh scripts/validate.sh
./scripts/bootstrap.sh
```

Bootstrap verifies versions, installs locked dependencies, starts PostGIS, and runs migrations. It creates `.env` from `.env.example` only when `.env` is absent.

---

## Run commands

**Backend** (port 8000):

```bash
uv run --project apps/api uvicorn krdt_api.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (port 5173):

```bash
pnpm --filter @krdt/web dev
```

**Health checks:**

- Liveness: `GET http://localhost:8000/health/live`
- Readiness: `GET http://localhost:8000/health/ready`

---

## Validation

**Full canonical validation** (required before gatekeeper review):

```bash
uv run --frozen python scripts/validate.py
```

**Fast validation** (skips live database integration):

```bash
uv run --frozen python scripts/validate.py --fast
```

Exit code must be `0` for success. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full step list.

---

## Repository structure

```text
.
├── apps/
│   ├── api/              FastAPI backend, migrations, tests
│   └── web/              React frontend, tests
├── docs/
│   ├── adr/              Architecture decision records
│   ├── architecture/     Architecture overview
│   ├── gates/            Gate specifications and reports
│   ├── PROJECT_CHARTER.md
│   ├── DATA_CLASSIFICATION.md
│   ├── RISK_REGISTER.md
│   ├── SECURITY_MODEL.md
│   ├── DEFINITION_OF_DONE.md
│   └── DEVELOPMENT.md
├── infra/
│   ├── compose.yaml      PostGIS container
│   └── postgres/init/    Extension initialization
├── scripts/
│   ├── bootstrap.sh
│   ├── validate.py       Canonical validation
│   └── check_memory.py   Memory consistency
├── AGENTS.md             Agent and gate policy
├── PROJECT_MEMORY.md     Durable approved decisions
├── PHASE_HANDOFF.md      Active gate context
├── SECURITY.md           Vulnerability reporting
└── LICENSE               Apache 2.0
```

---

## Memory workflow

Persistent AI and developer context lives in:

| File                | Role                                       |
| ------------------- | ------------------------------------------ |
| `AGENTS.md`         | Roles, gate rules, safety, report formats  |
| `PROJECT_MEMORY.md` | Approved decisions, ADRs, completed gates  |
| `PHASE_HANDOFF.md`  | Current gate status, blockers, next action |

New chats should read all three before implementing. `scripts/check_memory.py` enforces consistency during validation.

**Rules:**

- Cursor must not approve its own gate.
- Do not mark Gate 0 passed without gatekeeper **PASS**.
- Update `PHASE_HANDOFF.md` after each implementation cycle.

---

## Gate workflow

```text
Human intent → Gate spec → Cursor implementation → Evidence → Gatekeeper review → PASS / FAIL → Next gate
```

Implementation reports use the format in `AGENTS.md` section 34. Definition of done: [docs/DEFINITION_OF_DONE.md](docs/DEFINITION_OF_DONE.md).

Only the gatekeeper may authorize Gate 1 after Gate 0 **PASS**.

---

## Security

Report vulnerabilities per [SECURITY.md](SECURITY.md). Summary:

- no secrets in the repository;
- `.env` gitignored;
- localhost-only database in development;
- restricted CORS;
- no real operational or personal data in Gate 0.

Full model: [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md)

---

## Data and licensing

- **Code and original documentation:** [Apache License 2.0](LICENSE)
- **External datasets:** retain original ownership and licensing. Do not commit restricted government or commercial datasets.
- **This repository:** contains **no real Kundasang operational data**. Synthetic data must be clearly labelled and isolated when introduced in tests or fixtures.

See [docs/DATA_CLASSIFICATION.md](docs/DATA_CLASSIFICATION.md).

---

## Documentation index

| Document                                                       | Description                |
| -------------------------------------------------------------- | -------------------------- |
| [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)             | Mission, scope, governance |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)                     | Setup and commands         |
| [docs/DATA_CLASSIFICATION.md](docs/DATA_CLASSIFICATION.md)     | Data classes               |
| [docs/RISK_REGISTER.md](docs/RISK_REGISTER.md)                 | Project risks              |
| [docs/architecture/overview.md](docs/architecture/overview.md) | Logical architecture       |
| [docs/adr/README.md](docs/adr/README.md)                       | ADR index                  |

---

## Contributing

Gate-based delivery applies. Implement only the active gate specification. Pull requests should pass canonical validation and include evidence per the implementation report format.

---

## Licence

Apache License 2.0 — see [LICENSE](LICENSE). Data licensing is separate; see [Data and licensing](#data-and-licensing).
