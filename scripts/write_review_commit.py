#!/usr/bin/env python3
"""Record implementation and evidence commit identifiers in review metadata."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "PHASE_HANDOFF.md",
    ROOT / "docs/gates/gate-0/IMPLEMENTATION_REPORT.md",
)


def git_head(relative: str = "HEAD") -> str:
    result = subprocess.run(
        ["git", "rev-parse", relative],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def commit_exists(commit: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def replace_metadata(content: str, *, implementation: str, evidence: str) -> str:
    content = re.sub(
        r"(\| Implementation commit\s+\| )\S+( \|)",
        rf"\g<1>`{implementation}`\g<2>",
        content,
    )
    content = re.sub(
        r"(\| Evidence commit\s+\| )\S+( \|)",
        rf"\g<1>`{evidence}`\g<2>",
        content,
    )
    content = re.sub(
        r"^Implementation commit: \S+$",
        f"Implementation commit: {implementation}",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^Evidence commit: \S+$",
        f"Evidence commit: {evidence}",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"(\| Working tree\s+\| ).*?( \|)",
        r"\g<1>clean\g<2>",
        content,
        count=1,
    )
    content = re.sub(
        r"(- Implementation commit: `)[^`]+(`)",
        rf"\g<1>{implementation}\g<2>",
        content,
        count=1,
    )
    content = re.sub(
        r"(- Evidence commit: `)[^`]+(`)",
        rf"\g<1>{evidence}\g<2>",
        content,
        count=1,
    )
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--implementation",
        help="Commit containing completed Gate 0 implementation code",
    )
    parser.add_argument(
        "--evidence",
        help="Commit containing synchronized review evidence (defaults to HEAD)",
    )
    args = parser.parse_args()

    implementation = args.implementation or git_head()
    evidence = args.evidence or git_head()

    if not commit_exists(implementation):
        raise SystemExit(f"Implementation commit not found: {implementation}")
    if not commit_exists(evidence):
        raise SystemExit(f"Evidence commit not found: {evidence}")

    for path in FILES:
        updated = replace_metadata(
            path.read_text(encoding="utf-8"),
            implementation=implementation,
            evidence=evidence,
        )
        path.write_text(updated, encoding="utf-8")

    print(f"implementation={implementation}")
    print(f"evidence={evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
