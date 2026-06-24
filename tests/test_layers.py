"""Layer registry stays aligned with @pytest.mark.breadth."""

from __future__ import annotations

import subprocess
from pathlib import Path

from layer_registry import breadth_nodeids, p1_verify_nodeids


def _collected_markers(root: Path, marker: str) -> set[str]:
    proc = subprocess.run(
        ["pytest", "-m", marker, "-q", "--collect-only"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    collected = {
        ln.split()[0]
        for ln in proc.stdout.splitlines()
        if "::test_" in ln and not ln.strip().startswith("<")
    }
    assert proc.returncode == 0, proc.stderr
    return collected


def test_breadth_yaml_matches_markers():
    """layers.yaml breadth nodeids must match pytest -m breadth collection."""
    root = Path(__file__).resolve().parents[1]
    expected = set(breadth_nodeids())
    collected = _collected_markers(root, "breadth")
    assert expected == collected, (
        f"yaml vs markers mismatch\n  yaml only: {expected - collected}\n  marked only: {collected - expected}"
    )


def test_p1_verify_yaml_matches_markers():
    """P1 lock-down: exactly 2 tests in layers.yaml must match pytest -m p1_verify."""
    root = Path(__file__).resolve().parents[1]
    expected = set(p1_verify_nodeids())
    collected = _collected_markers(root, "p1_verify")
    assert len(expected) == 2, f"p1_verify must be exactly 2 tests, got {len(expected)}"
    assert expected == collected, (
        f"p1_verify yaml vs markers mismatch\n  yaml only: {expected - collected}\n  marked only: {collected - expected}"
    )
