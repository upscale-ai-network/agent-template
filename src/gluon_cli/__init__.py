"""Gluon workbench CLI entry points — uv run build-decks, check-decks."""

from __future__ import annotations

import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_script(script: str, *argv: str) -> None:
    path = ROOT / "scripts" / script
    sys.argv = [str(path), *argv]
    runpy.run_path(str(path), run_name="__main__")


def build_decks() -> None:
    _run_script("build-dt100-decks.py")


def build_decks_a3() -> None:
    _run_script("build-dt100-decks.py", "--a3-only")


def check_decks() -> None:
    _run_script("check_decks.py")


def pytest_breadth() -> None:
    """Breadth layer (Q1–Q5): pytest -m breadth."""
    extra = sys.argv[1:] if len(sys.argv) > 1 else ["-v", "--tb=line"]
    raise SystemExit(
        subprocess.run(
            ["pytest", "-m", "breadth", *extra],
            cwd=ROOT,
            check=False,
        ).returncode
    )


def pytest_p1_verify() -> None:
    """P1 lock-down gate: pytest -m p1_verify (exactly 2 tests)."""
    extra = sys.argv[1:] if len(sys.argv) > 1 else ["-v", "--tb=line"]
    raise SystemExit(
        subprocess.run(
            ["pytest", "-m", "p1_verify", *extra],
            cwd=ROOT,
            check=False,
        ).returncode
    )
