"""Layer registry stays aligned with @pytest.mark.breadth."""

from __future__ import annotations

import subprocess
from pathlib import Path

from layer_registry import breadth_nodeids


def test_breadth_yaml_matches_markers():
    """layers.yaml breadth nodeids must match pytest -m breadth collection."""
    root = Path(__file__).resolve().parents[1]
    expected = set(breadth_nodeids())

    proc = subprocess.run(
        ["pytest", "-m", "breadth", "-q", "--collect-only"],
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
    assert expected == collected, (
        f"yaml vs markers mismatch\n  yaml only: {expected - collected}\n  marked only: {collected - expected}"
    )
