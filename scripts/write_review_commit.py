#!/usr/bin/env python3
"""Write the current git HEAD into review metadata files."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "PHASE_HANDOFF.md",
    ROOT / "docs/gates/gate-0/IMPLEMENTATION_REPORT.md",
)


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def replace_commit(content: str, commit: str) -> str:
    content = re.sub(
        r"(\| Commit\s+\| )\S+( \|)",
        rf"\g<1>{commit}\g<2>",
        content,
        count=1,
    )
    content = re.sub(r"^Commit: \S+$", f"Commit: {commit}", content, flags=re.MULTILINE)
    content = re.sub(
        r"(- Commit: `)[^`]+(`)",
        rf"\g<1>{commit}\g<2>",
        content,
        count=1,
    )
    return content


def main() -> int:
    commit = git_head()
    for path in FILES:
        updated = replace_commit(path.read_text(encoding="utf-8"), commit)
        path.write_text(updated, encoding="utf-8")
    print(commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
