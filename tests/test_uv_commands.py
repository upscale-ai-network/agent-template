"""Subprocess smoke for uv entry points — must not write deliverables under dt100/ or dt122/."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import artifact_parity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import A3_MD, load_deck_md  # noqa: E402
from workflow_testkit import _load_build_module, slide_count  # noqa: E402

A3_PPTX = ROOT / "dt100" / "bugatti-qos-architecture.pptx"


@artifact_parity
@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not on PATH")
def test_check_decks_uv_run():
    subprocess.run(["uv", "run", "check-decks"], check=True, timeout=120)


@artifact_parity
def test_build_a3_isolated(tmp_path):
    """A3 build regression — all artifacts under tmp_path only."""
    deliverable_mtime = A3_PPTX.stat().st_mtime if A3_PPTX.is_file() else None

    diagram_dir = tmp_path / "diagrams"
    out_pptx = tmp_path / "a3-test.pptx"
    build = _load_build_module()
    path = build.build_a3(out_path=out_pptx, diagram_dir=diagram_dir)

    assert path == out_pptx
    assert out_pptx.is_file()
    doc = load_deck_md(A3_MD, a3_cover_fields=True)
    assert slide_count(out_pptx) == 1 + len(doc.slides)
    for s in doc.ordered_slides():
        if s.diagram:
            assert (diagram_dir / f"{s.diagram}.png").is_file()

    if deliverable_mtime is not None:
        assert A3_PPTX.stat().st_mtime == deliverable_mtime
