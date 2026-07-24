# KRDT Development Guide

## Document status

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Project      | Kundasang Resilience Digital Twin (KRDT) |
| Version      | 1.0 (Gate 0 foundation)                  |
| Status       | APPROVED FOR IMPLEMENTATION              |
| Gate         | 0                                        |
| Last updated | 2026-07-24                               |

This guide describes how to set up a local KRDT development environment. **WSL2 on Windows is the authoritative development environment for Windows users.** Native Windows paths are documented where helpers exist, but bootstrap and validation expectations follow the Linux/WSL scripts.

---

## 1. Supported environments

### Primary (Windows)

| Requirement    | Version / note                                    |
| -------------- | ------------------------------------------------- |
| Windows        | 10 or newer                                       |
| WSL2           | Ubuntu 22.04 or newer                             |
| Docker Desktop | WSL2 backend enabled                              |
| Editor         | Visual Studio Code or Cursor with WSL integration |

Clone and run all commands inside the WSL filesystem (e.g. `~/projects/kundasang-resilience-digital-twin`), not under `/mnt/c/`, for best file-watcher and I/O performance.

### Secondary (Linux)

| Requirement   | Version / note                 |
| ------------- | ------------------------------ |
| OS            | Native Ubuntu 22.04 or newer   |
| Docker Engine | With Docker Compose v2         |
| Editor        | VS Code, Cursor, or equivalent |

---

## 2. Prerequisites (pinned versions)

Install these exact versions before bootstrap:

| Tool    | Required version  | Verification command          |
| ------- | ----------------- | ----------------------------- |
| Python  | **3.13.14**       | `python3 --version`           |
| uv      | **0.11.32**       | `uv --version`                |
| Node.js | **24.18.0**       | `node --version` → `v24.18.0` |
| pnpm    | **11.14.0**       | `pnpm --version`              |
| Docker  | Docker Compose v2 | `docker compose version`      |
| Git     | Recent stable     | `git --version`               |

Recorded in repository:

- `.python-version` → `3.13.14`
- Root `package.json` `engines` → Node `24.18.0`, pnpm `11.14.0`
- `uv.lock` / `pnpm-lock.yaml` → dependency lockfiles

### Installing Python 3.13.14

Use pyenv, uv-managed Python, or your distribution's supported method. The bootstrap script rejects version mismatches.

### Installing uv 0.11.32

```bash
curl -LsSf https://astral.sh/uv/0.11.32/install.sh | sh
```

Or upgrade/downgrade an existing install to match `0.11.32`.

### Installing Node.js 24.18.0

Use nvm, fnm, or NodeSource. Enable Corepack for pnpm:

```bash
corepack enable
corepack prepare pnpm@11.14.0 --activate
```

### Docker

Ensure the Docker daemon is running before bootstrap. On Windows, start Docker Desktop and confirm WSL integration for your Ubuntu distribution.

---

## 3. WSL2 setup (Windows)

1. Install WSL2 and Ubuntu:

   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

2. Install Docker Desktop; enable **Use the WSL 2 based engine** and integration for your Ubuntu distro.

3. Open the project in WSL:

   ```bash
   git clone <repository-url> ~/projects/kundasang-resilience-digital-twin
   cd ~/projects/kundasang-resilience-digital-twin
   ```

4. Open the folder from WSL in Cursor/VS Code (`\\wsl$\Ubuntu\...` or `code .` from WSL).

5. Install prerequisites inside WSL (section 2), not in Windows PowerShell, for bootstrap/validation parity.

---

## 4. Bootstrap

Bootstrap verifies toolchain versions, installs locked dependencies, starts PostgreSQL/PostGIS, and runs migrations.

### Linux / WSL

```bash
chmod +x scripts/bootstrap.sh scripts/validate.sh
./scripts/bootstrap.sh
```

### Windows PowerShell (secondary)

```powershell
.\scripts\bootstrap.ps1
```

Bootstrap will:

1. Verify required commands and pinned versions;
2. Copy `.env.example` → `.env` **only if** `.env` does not exist;
3. Run `uv sync --frozen` and `pnpm install --frozen-lockfile`;
4. Start `docker compose -f infra/compose.yaml up -d`;
5. Wait for database health;
6. Run Alembic `upgrade head`.

It will **not** overwrite an existing `.env`.

### Database image

PostgreSQL **18** with PostGIS **3.6**:

```text
postgis/postgis:18-3.6
```

Extensions enabled via `infra/postgres/init/001-extensions.sql`:

- `postgis`
- `postgis_topology`

---

## 5. Configuration

Copy or allow bootstrap to create `.env` from `.env.example`:

```dotenv
KRDT_ENVIRONMENT=development
KRDT_LOG_LEVEL=INFO
KRDT_API_HOST=0.0.0.0
KRDT_API_PORT=8000
KRDT_DATABASE_URL=postgresql+psycopg://krdt:change-me@localhost:5432/krdt
KRDT_DATABASE_CONNECT_TIMEOUT_SECONDS=5
KRDT_CORS_ORIGINS=http://localhost:5173

POSTGRES_DB=krdt
POSTGRES_USER=krdt
POSTGRES_PASSWORD=change-me
```

Rules:

- Never commit `.env`;
- Change placeholders for shared environments;
- Wildcard CORS is not supported;
- Tests use explicit environment overrides, not your personal `.env`.

---

## 6. Run commands

### Start backend (FastAPI)

```bash
uv run --project apps/api uvicorn krdt_api.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints (Gate 0):

| Method | Path            | Purpose                                  |
| ------ | --------------- | ---------------------------------------- |
| GET    | `/health/live`  | Liveness (no database)                   |
| GET    | `/health/ready` | Readiness (database + PostGIS)           |
| GET    | `/api/v1`       | Versioned router root (no domain routes) |

OpenAPI: `http://localhost:8000/docs`

### Start frontend (Vite + React)

```bash
pnpm --filter @krdt/web dev
```

Default URL: `http://localhost:5173`

The Gate 0 page shows project identity, environment, backend readiness status, and an explicit message that operational digital-twin features are not implemented.

### Database management

```bash
# Status
docker compose -f infra/compose.yaml ps

# Stop
docker compose -f infra/compose.yaml down

# Stop and remove volume (destructive)
docker compose -f infra/compose.yaml down -v
```

### Migrations

```bash
KRDT_DATABASE_URL="postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt" \
  uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

---

## 7. Validation

### Fast validation (no live database integration)

```bash
uv run --frozen python scripts/validate.py --fast
```

Skips Docker startup, migration cycle, integration tests, and PostGIS checks.

### Full canonical validation (authoritative)

```bash
uv run --frozen python scripts/validate.py
```

Or via wrapper:

```bash
./scripts/validate.sh
```

Full validation runs, in order:

1. Required-file validation
2. Memory consistency (`scripts/check_memory.py`)
3. Toolchain version checks
4. Python and JavaScript lockfile verification
5. Python format, lint, mypy, unit tests
6. Frontend format, lint, typecheck, tests, production build
7. Docker Compose config
8. Database startup and health wait
9. Migration upgrade → downgrade → upgrade
10. Backend integration tests
11. PostGIS extension checks
12. Working-tree lockfile check

Exit code `0` means all steps passed. Non-zero indicates failure—do not report success without running the command.

### Individual checks

```bash
# Python format / lint
uv run ruff format --check apps/api scripts
uv run ruff check apps/api scripts

# Python types and tests
uv run mypy
uv run pytest apps/api/tests/unit scripts/tests -q

# Frontend
pnpm format:check
pnpm web:lint
pnpm web:typecheck
pnpm web:test
pnpm web:build
```

---

## 8. Repository layout (development focus)

```text
apps/api/          FastAPI backend, Alembic, tests
apps/web/          React + Vite frontend
infra/             Docker Compose and Postgres init
scripts/           bootstrap, validate, check_memory
docs/              Governance, ADRs, architecture
AGENTS.md          Agent and gate policy
PROJECT_MEMORY.md  Durable decisions
PHASE_HANDOFF.md   Active gate context
```

Domain packages (`domain/`, `application/`) exist as empty boundaries for Gate 1+. Do not add domain entities during Gate 0.

---

## 9. Troubleshooting

| Issue                      | Likely cause                       | Action                                   |
| -------------------------- | ---------------------------------- | ---------------------------------------- |
| Bootstrap version mismatch | Wrong Python/Node/uv/pnpm          | Install exact pinned versions            |
| Docker not healthy         | Daemon stopped or port conflict    | Start Docker; check `5432` not in use    |
| Migration failure          | DB not ready                       | `docker compose ... ps`; retry bootstrap |
| WSL file watch issues      | Project on `/mnt/c/`               | Move clone to WSL home directory         |
| validate.py memory fail    | Placeholder dates or gate mismatch | Update memory files per gate spec        |
| CORS errors                | Origin not in `KRDT_CORS_ORIGINS`  | Add frontend URL to `.env`               |

Stop and report per gate stop conditions when behavior materially differs from the specification—do not silently substitute tools.

---

## 10. Related documents

| Document                     | Purpose                          |
| ---------------------------- | -------------------------------- |
| `README.md`                  | Project overview and quick start |
| `docs/gates/gate-0/SPEC.md`  | Gate 0 contract                  |
| `docs/SECURITY_MODEL.md`     | Local security assumptions       |
| `docs/DEFINITION_OF_DONE.md` | Completion criteria              |
| `docs/adr/`                  | Accepted architecture decisions  |

---

## 11. Data warning

This repository contains **no real Kundasang operational datasets**. Do not add restricted government, commercial, or personal data to the working tree.
