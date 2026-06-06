"""
Workflow pipeline regression — md → mermaid → png → pptx.

Fast tests: parse / validate structure (no npx).
@workflow tests: full render + build (needs npx on PATH).

Future git gate: uv run pytest tests/ -m workflow
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import load_deck_md  # noqa: E402
from deck_render import render_mermaid_diagram  # noqa: E402
from deck_validate import DeckBuildError, fail_on_errors, validate_png  # noqa: E402
from workflow_testkit import (  # noqa: E402
    CANARY_MD,
    build_deck_from_md,
    diagram_stems,
    extract_visible_text,
    slide_count,
)

from conftest import requires_npx, requires_uv, workflow  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
CANARY_DIAGRAMS = FIXTURES / "diagrams" / "canary"


# --- Fast tier (no npx) ---


def test_tc01_parse_canary_md_structure():
    doc = load_deck_md(CANARY_MD)
    assert doc.cover.title == "Workflow canary"
    slides = doc.ordered_slides()
    assert len(slides) == 3
    assert slides[0].diagram == "canary-slide01-boxes"
    assert slides[1].diagram == "canary-slide02-flow"
    assert slides[2].diagram == ""


def test_tc02_diagram_stems_declared():
    doc = load_deck_md(CANARY_MD)
    assert diagram_stems(doc) == ["canary-slide01-boxes", "canary-slide02-flow"]


def test_tc08_missing_mmd_fails_loud(tmp_path):
    diagram_dir = tmp_path / "diagrams"
    diagram_dir.mkdir()
    with pytest.raises(FileNotFoundError):
        render_mermaid_diagram(diagram_dir, "canary-slide99-missing")


# --- Full workflow tier (npx) ---


@workflow
@requires_npx
def test_tc03_render_produces_valid_pngs(canary_paths):
    md_path, diagram_dir, _ = canary_paths
    doc = load_deck_md(md_path)
    config = diagram_dir / "mermaid-config.json"
    for stem in diagram_stems(doc):
        render_mermaid_diagram(diagram_dir, stem, config_path=config)
        fail_on_errors(
            validate_png(diagram_dir / f"{stem}.png", min_width=150, min_height=50)
        )


@workflow
@requires_npx
def test_tc04_build_pptx_slide_count(canary_paths):
    md_path, diagram_dir, out_pptx = canary_paths
    config = diagram_dir / "mermaid-config.json"
    doc = build_deck_from_md(
        md_path, out_pptx, diagram_dir, config_path=config, render=True
    )
    assert slide_count(out_pptx) == 1 + len(doc.ordered_slides())
    text = "\n".join(extract_visible_text(out_pptx))
    assert "MARKER_CANARY_BOXES" in text
    assert "MARKER_CANARY_TEXT" in text


@workflow
@requires_npx
def test_tc05_md_title_change_without_mmd_touch(canary_paths):
    md_path, diagram_dir, out_pptx = canary_paths
    config = diagram_dir / "mermaid-config.json"
    png_before = None
    build_deck_from_md(md_path, out_pptx, diagram_dir, config_path=config)
    png_before = (diagram_dir / "canary-slide01-boxes.png").read_bytes()

    body = md_path.read_text(encoding="utf-8").replace(
        "Canary color boxes", "Canary color boxes REV2"
    )
    md_path.write_text(body, encoding="utf-8")
    out2 = out_pptx.with_name("canary-rev2.pptx")
    build_deck_from_md(md_path, out2, diagram_dir, config_path=config, render=False)

    png_after = (diagram_dir / "canary-slide01-boxes.png").read_bytes()
    assert png_before == png_after
    text = "\n".join(extract_visible_text(out2))
    assert "REV2" in text


@workflow
@requires_npx
def test_tc06_duplicate_slide_increments_count(canary_paths):
    md_path, diagram_dir, out_pptx = canary_paths
    config = diagram_dir / "mermaid-config.json"
    extra = """

## Slide 4

**Title:** Duplicate diagram slide
**Diagram:** canary-slide01-boxes

**Bullets:**
- MARKER_CANARY_DUP
"""
    md_path.write_text(md_path.read_text(encoding="utf-8") + extra, encoding="utf-8")
    doc = build_deck_from_md(
        md_path, out_pptx, diagram_dir, config_path=config, render=True
    )
    assert len(doc.ordered_slides()) == 4
    assert slide_count(out_pptx) == 5


@workflow
@requires_npx
def test_tc07_mmd_color_change_changes_png_hash(canary_paths):
    md_path, diagram_dir, _ = canary_paths
    config = diagram_dir / "mermaid-config.json"
    doc = load_deck_md(md_path)
    stem = diagram_stems(doc)[0]
    render_mermaid_diagram(diagram_dir, stem, config_path=config)
    h1 = hashlib.sha256((diagram_dir / f"{stem}.png").read_bytes()).hexdigest()

    mmd = diagram_dir / f"{stem}.mmd"
    mmd.write_text(
        mmd.read_text(encoding="utf-8").replace("#EF6C00", "#1565C0"),
        encoding="utf-8",
    )
    render_mermaid_diagram(diagram_dir, stem, config_path=config)
    h2 = hashlib.sha256((diagram_dir / f"{stem}.png").read_bytes()).hexdigest()
    assert h1 != h2


@workflow
@requires_npx
def test_tc10_idempotent_build_same_slide_count(canary_paths):
    md_path, diagram_dir, out_pptx = canary_paths
    config = diagram_dir / "mermaid-config.json"
    build_deck_from_md(md_path, out_pptx, diagram_dir, config_path=config)
    n1 = slide_count(out_pptx)
    build_deck_from_md(md_path, out_pptx, diagram_dir, config_path=config)
    n2 = slide_count(out_pptx)
    assert n1 == n2 == 4


@workflow
@requires_uv
def test_tc09_production_check_decks_subprocess():
    subprocess.run(["uv", "run", "check-decks"], check=True, timeout=120, cwd=ROOT)
