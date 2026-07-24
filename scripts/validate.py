#!/usr/bin/env python3
"""Canonical Gate 0 validation runner."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".python-version",
    "pyproject.toml",
    "uv.lock",
    "package.json",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
    "infra/compose.yaml",
    "apps/api/pyproject.toml",
    "apps/web/package.json",
    "docs/gates/gate-0/SPEC.md",
    "scripts/check_memory.py",
    "scripts/validate.py",
]

REQUIRED_VERSIONS = {
    "python": "3.13.14",
    "uv": "0.11.32",
    "node": "v24.18.0",
    "pnpm": "11.14.0",
}


@dataclass
class StepResult:
    name: str
    ok: bool
    detail: str = ""


def resolve_executable(name: str) -> str | None:
    direct = shutil.which(name) or shutil.which(f"{name}.cmd")
    if direct:
        return direct
    if name == "pnpm":
        corepack = shutil.which("corepack") or shutil.which("corepack.cmd")
        if corepack:
            return corepack
    return None


def build_command(command: list[str]) -> list[str]:
    executable = command[0]
    resolved = resolve_executable(executable)
    if resolved is None:
        return command
    if executable == "pnpm" and Path(resolved).name.lower().startswith("corepack"):
        return [resolved, "pnpm", *command[1:]]
    return [resolved, *command[1:]]


def run_command(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    command = build_command(command)
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def step_required_files() -> StepResult:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        return StepResult("required-file validation", False, ", ".join(missing))
    return StepResult("required-file validation", True)


def step_memory() -> StepResult:
    result = run_command([sys.executable, "scripts/check_memory.py"])
    return StepResult(
        "memory consistency validation",
        result.returncode == 0,
        result.stderr.strip() or result.stdout.strip(),
    )


def parse_version(command: list[str], pattern: str) -> str | None:
    if resolve_executable(command[0]) is None:
        return None
    result = run_command(build_command(command))
    if result.returncode != 0:
        return None
    match = re.search(pattern, result.stdout.strip())
    return match.group(0) if match else result.stdout.strip()


def step_toolchain() -> StepResult:
    actual = {
        "python": parse_version([sys.executable, "--version"], r"3\.\d+\.\d+"),
        "uv": parse_version(["uv", "--version"], r"0\.\d+\.\d+"),
        "node": parse_version(["node", "--version"], r"v\d+\.\d+\.\d+"),
        "pnpm": parse_version(["pnpm", "--version"], r"\d+\.\d+\.\d+"),
    }
    mismatches = []
    for tool, expected in REQUIRED_VERSIONS.items():
        value = actual.get(tool)
        if value is None:
            mismatches.append(f"{tool}: missing")
            continue
        normalized = value.lstrip("v")
        expected_normalized = expected.lstrip("v")
        if normalized != expected_normalized:
            mismatches.append(f"{tool}: expected {expected}, got {value}")
    if mismatches:
        return StepResult("toolchain-version validation", False, "; ".join(mismatches))
    return StepResult("toolchain-version validation", True)


def step_python_lockfile() -> StepResult:
    result = run_command(["uv", "lock", "--check"], cwd=ROOT)
    return StepResult("Python lockfile verification", result.returncode == 0, result.stderr.strip())


def step_js_lockfile() -> StepResult:
    result = run_command(["pnpm", "install", "--frozen-lockfile"], cwd=ROOT)
    return StepResult(
        "JavaScript lockfile verification", result.returncode == 0, result.stderr.strip()
    )


def step_python_format() -> StepResult:
    result = run_command(["uv", "run", "ruff", "format", "--check", "apps/api", "scripts"])
    return StepResult("Python formatting check", result.returncode == 0, result.stderr.strip())


def step_python_lint() -> StepResult:
    result = run_command(["uv", "run", "ruff", "check", "apps/api", "scripts"])
    return StepResult("Python lint", result.returncode == 0, result.stderr.strip())


def step_python_typecheck() -> StepResult:
    result = run_command(["uv", "run", "mypy"])
    return StepResult("Python type checking", result.returncode == 0, result.stderr.strip())


def step_python_unit_tests() -> StepResult:
    result = run_command(
        ["uv", "run", "pytest", "apps/api/tests/unit", "scripts/tests", "-q"],
        env={"KRDT_DATABASE_URL": "postgresql+psycopg://unused:unused@127.0.0.1:1/unused"},
    )
    return StepResult("Python unit tests", result.returncode == 0, result.stdout.strip())


def step_frontend_format() -> StepResult:
    result = run_command(["pnpm", "format:check"])
    return StepResult("frontend formatting check", result.returncode == 0, result.stderr.strip())


def step_frontend_lint() -> StepResult:
    result = run_command(["pnpm", "web:lint"])
    return StepResult("frontend lint", result.returncode == 0, result.stderr.strip())


def step_frontend_typecheck() -> StepResult:
    result = run_command(["pnpm", "web:typecheck"])
    return StepResult("frontend type checking", result.returncode == 0, result.stderr.strip())


def step_frontend_tests() -> StepResult:
    result = run_command(["pnpm", "web:test"])
    return StepResult("frontend tests", result.returncode == 0, result.stdout.strip())


def step_frontend_build() -> StepResult:
    result = run_command(["pnpm", "web:build"])
    return StepResult("frontend production build", result.returncode == 0, result.stderr.strip())


def step_compose_config() -> StepResult:
    if shutil.which("docker") is None:
        return StepResult("Docker Compose configuration validation", False, "docker not available")
    result = run_command(["docker", "compose", "-f", "infra/compose.yaml", "config"])
    return StepResult(
        "Docker Compose configuration validation",
        result.returncode == 0,
        result.stderr.strip(),
    )


def docker_available() -> bool:
    return shutil.which("docker") is not None


def step_database_startup() -> StepResult:
    if not docker_available():
        return StepResult("database startup and health wait", False, "docker not available")
    run_command(["docker", "compose", "-f", "infra/compose.yaml", "up", "-d"])
    for _ in range(30):
        result = run_command(
            ["docker", "compose", "-f", "infra/compose.yaml", "ps", "--format", "json"]
        )
        if result.returncode == 0 and "healthy" in result.stdout.lower():
            return StepResult("database startup and health wait", True)
        time.sleep(2)
    return StepResult("database startup and health wait", False, "database did not become healthy")


def migration_env() -> dict[str, str]:
    return {
        "KRDT_DATABASE_URL": "postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt",
        "KRDT_ENVIRONMENT": "development",
        "KRDT_LOG_LEVEL": "INFO",
        "KRDT_API_HOST": "0.0.0.0",
        "KRDT_API_PORT": "8000",
        "KRDT_DATABASE_CONNECT_TIMEOUT_SECONDS": "5",
        "KRDT_CORS_ORIGINS": "http://localhost:5173",
    }


def step_migration(action: str) -> StepResult:
    if not docker_available():
        return StepResult(f"migration {action}", False, "docker not available")
    result = run_command(
        ["uv", "run", "--project", "apps/api", "alembic", action],
        cwd=ROOT / "apps/api",
        env=migration_env(),
    )
    return StepResult(f"migration {action}", result.returncode == 0, result.stderr.strip())


def step_backend_integration_tests() -> StepResult:
    if not docker_available():
        return StepResult("backend integration tests", False, "docker not available")
    result = run_command(
        ["uv", "run", "pytest", "apps/api/tests/integration", "-q"],
        env=migration_env(),
    )
    return StepResult("backend integration tests", result.returncode == 0, result.stdout.strip())


def step_postgis_checks() -> StepResult:
    if not docker_available():
        return StepResult("PostGIS extension checks", False, "docker not available")
    result = run_command(
        [
            "docker",
            "compose",
            "-f",
            "infra/compose.yaml",
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            "krdt",
            "-d",
            "krdt",
            "-tAc",
            (
                "SELECT PostGIS_Version(); "
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname='postgis_topology');"
            ),
        ]
    )
    ok = result.returncode == 0 and bool(result.stdout.strip())
    return StepResult("PostGIS extension checks", ok, result.stdout.strip())


def step_working_tree() -> StepResult:
    if shutil.which("git") is None:
        return StepResult("working-tree generated-file check", True, "git unavailable")
    result = run_command(["git", "status", "--porcelain"])
    generated = [
        line for line in result.stdout.splitlines() if "pnpm-lock.yaml" in line or "uv.lock" in line
    ]
    if generated:
        return StepResult(
            "working-tree generated-file check",
            False,
            "unexpected lockfile changes: " + ", ".join(generated),
        )
    return StepResult("working-tree generated-file check", True)


def ensure_toolchain_path() -> None:
    """Ensure common Node installation paths are available to subprocesses."""

    extra_paths: list[str] = []
    for key in ("NVM_HOME", "NVM_SYMLINK"):
        value = os.environ.get(key)
        if value:
            extra_paths.append(value)
    extra_paths.extend(
        [
            r"C:\nvm4w\nodejs",
            str(Path.home() / ".local" / "bin"),
        ]
    )
    current = os.environ.get("PATH", "")
    for entry in extra_paths:
        if entry and entry not in current:
            current = f"{entry};{current}"
    os.environ["PATH"] = current


def main() -> int:
    ensure_toolchain_path()
    parser = argparse.ArgumentParser(description="Run KRDT Gate 0 validation")
    parser.add_argument("--fast", action="store_true", help="Skip live database integration")
    args = parser.parse_args()

    steps = [
        step_required_files,
        step_memory,
        step_toolchain,
        step_python_lockfile,
        step_js_lockfile,
        step_python_format,
        step_python_lint,
        step_python_typecheck,
        step_python_unit_tests,
        step_frontend_format,
        step_frontend_lint,
        step_frontend_typecheck,
        step_frontend_tests,
        step_frontend_build,
    ]

    if not args.fast:
        steps.extend(
            [
                step_compose_config,
                step_database_startup,
                lambda: step_migration("upgrade head"),
                lambda: step_migration("downgrade base"),
                lambda: step_migration("upgrade head"),
                step_backend_integration_tests,
                step_postgis_checks,
                step_working_tree,
            ]
        )

    results: list[StepResult] = []
    for step in steps:
        result = step()
        results.append(result)
        status = "PASS" if result.ok else "FAIL"
        detail = f" ({result.detail})" if result.detail else ""
        print(f"[{status}] {result.name}{detail}")

    summary = {
        "passed": sum(1 for r in results if r.ok),
        "failed": sum(1 for r in results if not r.ok),
    }
    print(json.dumps({"summary": summary}))
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
