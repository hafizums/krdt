"""Tests for persistent memory validation."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_check(root: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if root is not None:
        env["KRDT_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(ROOT / "check_memory.py")],
        cwd=ROOT.parent,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_missing_memory_file_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("AGENTS.md", "PROJECT_MEMORY.md", "PHASE_HANDOFF.md"):
        (tmp_path / name).write_text("# test\n", encoding="utf-8")
    (tmp_path / "PROJECT_MEMORY.md").unlink()
    monkeypatch.chdir(tmp_path)
    result = run_check(tmp_path)
    assert result.returncode != 0
    assert "PROJECT_MEMORY.md" in result.stderr


def test_contradictory_gate_values_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (tmp_path / "PROJECT_MEMORY.md").write_text(
        "Current gate: Gate 0\nGate 0 status: READY FOR GATEKEEPER REVIEW\n",
        encoding="utf-8",
    )
    (tmp_path / "PHASE_HANDOFF.md").write_text(
        "Current gate: Gate 1\nStatus: READY FOR GATEKEEPER REVIEW\nCommit: abc123\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    result = run_check(tmp_path)
    assert result.returncode != 0


def test_valid_gate0_review_ready_memory_passes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (tmp_path / "PROJECT_MEMORY.md").write_text(
        "\n".join(
            [
                "# PROJECT_MEMORY.md",
                "Current gate: Gate 0",
                "Gate 0 status: READY FOR GATEKEEPER REVIEW",
                "## 14. Accepted Architecture Decisions",
                "| ADR | Title | Status | Date |",
                "| --- | ----- | ------ | ---- |",
                "| 0001 | Use a monorepo | ACCEPTED | 2026-07-24 |",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "PHASE_HANDOFF.md").write_text(
        "\n".join(
            [
                "# PHASE_HANDOFF.md",
                "Current gate: Gate 0",
                "Status: READY FOR GATEKEEPER REVIEW",
                "Implementation commit: deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                "Evidence commit: deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                "Next authorized action: Independent Gate 0 review",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    result = run_check(tmp_path)
    assert result.returncode == 0, result.stderr
