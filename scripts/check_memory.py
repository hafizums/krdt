#!/usr/bin/env python3
"""Validate persistent AI memory file consistency."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("KRDT_ROOT", str(Path(__file__).resolve().parents[1])))
REQUIRED_FILES = ("AGENTS.md", "PROJECT_MEMORY.md", "PHASE_HANDOFF.md")
REQUIRED_HEADINGS = {
    "PROJECT_MEMORY.md": ("# PROJECT_MEMORY.md",),
    "PHASE_HANDOFF.md": ("# PHASE_HANDOFF.md",),
}
PLACEHOLDER_PATTERN = re.compile(r"YYYY-MM-DD|Not (yet )?created|Not available")
CURRENT_GATE_PATTERN = re.compile(r"^Current gate:\s*(.+)$", re.MULTILINE)
STATUS_PATTERN = re.compile(r"^Status:\s*(.+)$", re.MULTILINE)
GATE0_STATUS_PATTERN = re.compile(r"^Gate 0 status:\s*(.+)$", re.MULTILINE)
IMPLEMENTATION_COMMIT_PATTERN = re.compile(r"^Implementation commit:\s*(.+)$", re.MULTILINE)
EVIDENCE_COMMIT_PATTERN = re.compile(r"^Evidence commit:\s*(.+)$", re.MULTILINE)
NEXT_ACTION_PATTERN = re.compile(r"^Next authorized action:\s*(.+)$", re.MULTILINE)
PASSED_GATE_PATTERN = re.compile(r"Gate 0.*\bPASS\b", re.IGNORECASE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def git_head(relative: str = "HEAD") -> str:
    result = subprocess.run(
        ["git", "rev-parse", relative],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def commit_exists(commit: str) -> bool:
    if not commit or commit.lower() in {"not available", "none", "n/a", "pending"}:
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def normalize_commit(value: str) -> str:
    return value.strip().strip("`")


def main() -> int:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.exists():
            return fail(f"Missing required memory file: {name}")
        content = read_text(path)
        for heading in REQUIRED_HEADINGS.get(name, ()):
            if heading not in content:
                return fail(f"Missing required heading in {name}: {heading}")
        if PLACEHOLDER_PATTERN.search(content):
            return fail(f"Placeholder value remains in {name}")

    memory = read_text(ROOT / "PROJECT_MEMORY.md")
    handoff = read_text(ROOT / "PHASE_HANDOFF.md")

    memory_gate = CURRENT_GATE_PATTERN.search(memory)
    handoff_gate = CURRENT_GATE_PATTERN.search(handoff)
    if not memory_gate or not handoff_gate:
        return fail("Current gate metadata is missing")
    if memory_gate.group(1).strip() != handoff_gate.group(1).strip():
        return fail("Current gate values contradict each other")

    handoff_status = STATUS_PATTERN.search(handoff)
    if not handoff_status:
        return fail("Handoff status metadata is missing")

    status_value = handoff_status.group(1).strip()
    if status_value.upper().startswith("PASS") and "Gate 0 status: PASS" not in memory:
        return fail("Handoff claims a gate passed without a recorded gatekeeper decision")

    if "READY FOR GATEKEEPER REVIEW" in status_value:
        implementation = IMPLEMENTATION_COMMIT_PATTERN.search(handoff)
        evidence = EVIDENCE_COMMIT_PATTERN.search(handoff)
        if not implementation or not evidence:
            return fail("Implementation and evidence commit metadata are required for review")
        implementation_commit = normalize_commit(implementation.group(1))
        evidence_commit = normalize_commit(evidence.group(1))
        if not commit_exists(implementation_commit):
            return fail("Implementation commit is missing or not present in git history")
        if not commit_exists(evidence_commit):
            return fail("Evidence commit is missing or not present in git history")
        head = git_head()
        if head and evidence_commit not in {head, git_head("HEAD~1")}:
            return fail(
                "Evidence commit must match HEAD or the metadata sync commit "
                "while status is ready for review"
            )

    if PASSED_GATE_PATTERN.search(handoff) and "Gate 0 status: PASS" not in memory:
        return fail("Handoff indicates Gate 0 passed without gatekeeper decision in memory")

    next_action = NEXT_ACTION_PATTERN.search(handoff)
    if not next_action:
        return fail("Next authorized action metadata is missing")

    gate0_status = GATE0_STATUS_PATTERN.search(memory)
    if gate0_status and "PASS" in gate0_status.group(1) and "Gate 0 status: PASS" not in memory:
        return fail("Gate 0 marked passed without gatekeeper metadata")

    print("Memory consistency validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
