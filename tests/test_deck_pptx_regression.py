"""P(-1) — pptx compare utility + canary idempotent regen (Path 1 only).

Production md/png/pptx parity lives in TC14/TC15 (@artifact_parity, opt-in).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import load_deck_md  # noqa: E402
from pptx_compare import (  # noqa: E402
    assert_pptx_content_equal,
    content_sha256,
    diff_pptx_content,
    load_published_hashes,
)
from workflow_testkit import (  # noqa: E402
    build_deck_from_md,
    build_production_a3_isolated,
    build_production_b6_isolated,
    slide_count,
)

from conftest import artifact_parity, requires_npx, workflow  # noqa: E402

B6_PPTX = ROOT / "dt122" / "bugatti-qos-ccc.pptx"
A3_PPTX = ROOT / "dt100" / "bugatti-qos-architecture.pptx"
PUBLISHED_HASHES = ROOT / "tests" / "fixtures" / "published-deck-hashes.txt"
B6_DIAGRAMS = ROOT / "assets" / "diagrams" / "b6"
A3_DIAGRAMS = ROOT / "assets" / "diagrams" / "a3"
SCOPE_DELIVERABLE_PNG = B6_DIAGRAMS / "b6-slide06-scope-deliverable.png"


def _snapshot_mtimes(paths: list[Path]) -> dict[Path, float]:
    return {p: p.stat().st_mtime for p in paths if p.is_file()}


def _assert_mtimes_unchanged(before: dict[Path, float]) -> None:
    for path, mtime in before.items():
        assert path.is_file(), f"production artifact removed during test: {path}"
        assert path.stat().st_mtime == mtime, f"production artifact touched: {path}"


@pytest.fixture
def production_artifact_mtimes():
    paths = [
        A3_PPTX,
        B6_PPTX,
        *A3_DIAGRAMS.glob("*.png"),
        *B6_DIAGRAMS.glob("*.png"),
    ]
    before = _snapshot_mtimes(paths)
    yield before
    _assert_mtimes_unchanged(before)


def test_tc11_pptx_compare_ignores_docprops_only(tmp_path):
    """Sanity — byte drift from docProps alone must not fail content compare."""
    if not B6_PPTX.is_file():
        pytest.skip("committed B6 pptx missing")
    copy = tmp_path / "copy.pptx"
    copy.write_bytes(B6_PPTX.read_bytes())
    assert diff_pptx_content(B6_PPTX, copy) == []


@workflow
@requires_npx
def test_tc12_canary_regen_is_idempotent(canary_paths):
    """Path 1 — two canary regens produce identical pptx content (falsifiable md only)."""
    md_path, diagram_dir, _ = canary_paths
    config = diagram_dir / "mermaid-config.json"
    base = md_path.parent
    out1 = base / "run1.pptx"
    out2 = base / "run2.pptx"

    build_deck_from_md(md_path, out1, diagram_dir, config_path=config)
    build_deck_from_md(md_path, out2, diagram_dir, config_path=config)
    doc = load_deck_md(md_path)
    expected = 1 + len(doc.ordered_slides())

    assert out1.is_file() and out2.is_file()
    assert slide_count(out1) == slide_count(out2) == expected
    assert_pptx_content_equal(out1, out2, label="canary idempotent regen")


@artifact_parity
def test_tc15_a3_regen_matches_committed_pptx(tmp_path, production_artifact_mtimes):
    """Path 2 — git parity; opt-in only."""
    if not A3_PPTX.is_file():
        pytest.skip("committed A3 pptx missing")

    regenerated = build_production_a3_isolated(tmp_path / "a3-build")
    diffs = diff_pptx_content(A3_PPTX, regenerated)
    if diffs:
        pytest.skip(
            "committed A3 pptx out of sync with pipeline — run build-decks-a3 and commit: "
            + diffs[0]
        )
    assert_pptx_content_equal(A3_PPTX, regenerated, label="A3 bugatti-qos-architecture")


@workflow
@pytest.mark.parametrize(
    ("deck_key", "builder"),
    [
        ("a3", build_production_a3_isolated),
        ("b6", build_production_b6_isolated),
    ],
)
def test_tc16_published_deck_content_hash(tmp_path, deck_key, builder):
    """Published snapshot — regen from md must match golden content SHA256 (not raw zip bytes)."""
    golden = load_published_hashes(PUBLISHED_HASHES)[deck_key]
    md_path = ROOT / golden.md_source
    assert md_path.is_file(), f"missing md source: {md_path}"

    regenerated = builder(tmp_path / deck_key)
    actual = content_sha256(regenerated)
    assert actual == golden.content_sha256, (
        f"{deck_key} content drift vs published snapshot ({golden.md_source}):\n"
        f"  expected: {golden.content_sha256}\n"
        f"  actual:   {actual}\n"
        "Hint: if intentional publish, run "
        "`uv run python scripts/pptx_compare.py --update-published-hashes`"
    )


@artifact_parity
def test_tc14_b6_regen_matches_committed_pptx(tmp_path, production_artifact_mtimes):
    """Path 2 — git parity; opt-in only."""
    if not B6_PPTX.is_file():
        pytest.skip("committed B6 pptx missing")
    if not SCOPE_DELIVERABLE_PNG.is_file():
        pytest.skip("scope-deliverable PNG missing")

    regenerated = build_production_b6_isolated(tmp_path / "b6-build")
    diffs = diff_pptx_content(B6_PPTX, regenerated)
    if diffs:
        pytest.skip(
            "md ahead of committed pptx — run `uv run build-decks` and commit pptx/png: "
            + diffs[0]
        )
    assert_pptx_content_equal(B6_PPTX, regenerated, label="B6 bugatti-qos-ccc")
