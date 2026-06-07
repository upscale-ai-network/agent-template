#!/usr/bin/env python3
"""
Render A3 diagram PNGs from bugatti-qos-architecture.md via a3_aligned_render.py.

Source of truth: the .md file (labels, layout). Rasterizer: PyMuPDF only.
No Mermaid, mmdc, Chrome, or Puppeteer.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A3_DIR = ROOT / "assets" / "diagrams" / "a3"

sys.path.insert(0, str(ROOT / "scripts"))

from a3_aligned_render import render_all_diagrams  # noqa: E402
from deck_from_md import A3_MD, load_deck_md  # noqa: E402
from deck_validate import (  # noqa: E402
    fail_on_errors,
    validate_a3_build,
    validate_a3_diagram_pngs,
    validate_png,
)


def _preflight_pymupdf() -> None:
    try:
        from pymupdf_util import load_fitz

        load_fitz()
    except ImportError as exc:
        raise SystemExit("PyMuPDF required. Run: uv sync") from exc


def render_all_a3_diagrams(doc=None, diagram_dir: Path | None = None) -> list[str]:
    """Render every diagram declared in A3 md. Returns diagram stems rendered."""
    doc = doc or load_deck_md(A3_MD, a3_cover_fields=True)
    fail_on_errors(validate_a3_build(doc))

    stems = [s.diagram for s in doc.ordered_slides() if s.diagram]
    if not stems:
        raise RuntimeError(f"No diagrams declared in {A3_MD.name}")

    out_dir = diagram_dir or A3_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    render_all_diagrams(out_dir, doc=doc)
    for stem in stems:
        fail_on_errors(validate_png(out_dir / f"{stem}.png"))

    return stems


def main() -> int:
    _preflight_pymupdf()
    if not A3_DIR.is_dir() and not A3_MD.is_file():
        print(f"Missing {A3_DIR} and {A3_MD}", file=sys.stderr)
        return 1

    doc = load_deck_md(A3_MD, a3_cover_fields=True)
    stems = render_all_a3_diagrams(doc)
    print(f"Rendered {len(stems)} A3 diagrams from {A3_MD.name} (PyMuPDF)")
    for stem in stems:
        print(f"OK: {(A3_DIR / f'{stem}.png').relative_to(ROOT)}")

    fail_on_errors(validate_a3_diagram_pngs(doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
