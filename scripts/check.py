#!/usr/bin/env python3
"""Run all local validation checks, including Node-based function tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLED_NODE = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "node"
    / "bin"
    / ("node.exe" if sys.platform.startswith("win") else "node")
)


def find_node() -> str:
    node = shutil.which("node")
    if node:
        return node
    if BUNDLED_NODE.exists():
        return str(BUNDLED_NODE)
    raise RuntimeError("Node.js not found. Install Node.js or run inside Codex Desktop with bundled Node.")


def run(args: list[str]) -> None:
    print(f"\n$ {' '.join(args)}")
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    node = find_node()
    commands = [
        [sys.executable, "scripts/validate.py"],
        [sys.executable, "web/scripts/build-data.py"],
        [sys.executable, "web/scripts/smoke-test.py"],
        [node, "scripts/test-functions.mjs"],
        [node, "scripts/test-liuyao-engine.mjs"],
        [sys.executable, "scripts/predeploy_check.py"],
    ]

    try:
        for command in commands:
            run(command)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\nCheck failed: {error}", file=sys.stderr)
        return 1

    print("\nAll checks ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
