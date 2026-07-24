# Security Policy

## Supported versions

KRDT is in **Gate 0 — Repository and Governance Foundation**. There is no production deployment. Security reporting is welcome during foundation development and will become more formal before any operational deployment.

| Version / gate      | Supported               |
| ------------------- | ----------------------- |
| Gate 0 (foundation) | Active development      |
| Pre-release         | Not for operational use |

---

## Reporting a vulnerability

If you believe you have found a security vulnerability in KRDT:

1. **Do not** open a public GitHub issue for unresolved vulnerabilities that could affect deployments handling sensitive or operational data.
2. Contact the project maintainers through the channel designated by the human owner (email or private advisory channel—update this section when a contact address is assigned).
3. Include:
   - description of the issue;
   - steps to reproduce;
   - affected components (API, frontend, CI, dependencies);
   - potential impact;
   - suggested fix if available.

We aim to acknowledge reports within a reasonable timeframe during active development. Coordinated disclosure details will expand at Gate 7 operational hardening.

---

## Scope

In scope for reports:

- committed secrets or credentials in the repository;
- injection or validation flaws in API boundaries;
- dependency vulnerabilities in locked packages;
- CI workflow permission or supply-chain weaknesses;
- information disclosure through logs, health endpoints, or error responses;
- misconfiguration that exposes the development database beyond localhost.

Out of scope for Gate 0:

- vulnerabilities in third-party services not used by the repository;
- social engineering;
- issues requiring operational data not present in Gate 0;
- missing authentication on Gate 0 health endpoints alone (documented accepted risk for foundation scope—still report if combined with sensitive data exposure).

---

## Secrets and repository hygiene

**Never commit:**

- passwords, API keys, or tokens;
- private keys or certificates;
- production database credentials;
- `.env` files;
- restricted government, commercial, or personal datasets.

The repository provides `.env.example` with **development placeholders only**. Copy to `.env` locally; `.env` is gitignored.

If you accidentally commit a secret:

1. Rotate the credential immediately.
2. Notify maintainers.
3. Do not rely on git history deletion alone without coordinated rotation.

See `docs/SECURITY_MODEL.md` for trust boundaries and logging restrictions.

---

## Dependency security

- Python dependencies locked in `uv.lock`.
- JavaScript dependencies locked in `pnpm-lock.yaml`.
- Dependabot configured in `.github/dependabot.yml`.
- Run canonical validation after dependency updates:

  ```bash
  uv run --frozen python scripts/validate.py
  ```

Report supply-chain concerns via the same private channel.

---

## Safe development practices

- Bind local PostgreSQL to `127.0.0.1` only.
- Do not expose the dev stack to the public internet.
- Do not add real Kundasang operational or restricted data to the repository.
- Do not disable validation to accept malformed input.
- Review `docs/DATA_CLASSIFICATION.md` before adding datasets.

---

## Related documents

| Document                                                   | Purpose                         |
| ---------------------------------------------------------- | ------------------------------- |
| [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md)           | Trust boundaries and controls   |
| [docs/DATA_CLASSIFICATION.md](docs/DATA_CLASSIFICATION.md) | Data handling classes           |
| [docs/RISK_REGISTER.md](docs/RISK_REGISTER.md)             | RISK-008, RISK-009              |
| [AGENTS.md](AGENTS.md)                                     | Security and privacy principles |

---

## Licence note

KRDT source code and original documentation are licensed under Apache 2.0 (see [LICENSE](LICENSE)). That licence does not grant rights to third-party datasets. External data retains its original licensing and restrictions.
