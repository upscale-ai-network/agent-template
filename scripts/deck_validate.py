"""Pre- and post-build checks for DT100 decks. Fail loud; no silent fallbacks."""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence

from deck_from_md import DeckDocument, DeckSlide, load_b6_md, load_deck_md

ROOT = Path(__file__).resolve().parents[1]
A3_MD = ROOT / "dt100" / "qos-architecture.md"
B6_MD = ROOT / "dt100" / "manager-arch-vision-b6.md"
A3_DIAGRAMS = ROOT / "assets" / "diagrams" / "a3"
PIPELINE_IMG = ROOT / "assets" / "logical-pipeline-boss-slide.png"
STYLE_REF = ROOT / "assets/templates/upscale-ccc-style-reference.pptx"

MIN_PNG_BYTES = 500


class DeckBuildError(Exception):
    """One or more validation errors — build must not continue."""

    def __init__(self, errors: Sequence[str]):
        self.errors = list(errors)
        super().__init__(self._format())

    def _format(self) -> str:
        lines = ["Deck validation failed:"]
        lines.extend(f"  - {e}" for e in self.errors)
        return "\n".join(lines)


def fail_on_errors(errors: Sequence[str]) -> None:
    if errors:
        raise DeckBuildError(errors)


def _a3_png(stem: str) -> Path:
    return A3_DIAGRAMS / f"{stem}.png"


def validate_style_reference() -> List[str]:
    errors: List[str] = []
    if not STYLE_REF.is_file():
        errors.append(f"Missing company style template: {STYLE_REF}")
    elif STYLE_REF.stat().st_size < 10_000:
        errors.append(f"Style template looks corrupt or empty: {STYLE_REF}")
    return errors


def _validate_slide_layout(s: DeckSlide) -> List[str]:
    errors: List[str] = []
    if s.number == 1:
        if len(s.stack_groups) < 2:
            errors.append(
                f"Slide {s.number}: diagram needs two *group* blocks in {A3_MD.name}"
            )
    elif s.number == 2:
        if len(s.columns) < 3:
            errors.append(f"Slide {s.number}: diagram needs three Column blocks in {A3_MD.name}")
        if not s.branch_yes:
            errors.append(f"Slide {s.number}: missing Outcome in {A3_MD.name}")
    elif s.number in (3, 4):
        if not s.stack:
            errors.append(f"Slide {s.number}: diagram needs On-slide (stack) nodes in {A3_MD.name}")
    return errors


def validate_a3_md(doc: DeckDocument | None = None) -> List[str]:
    doc = doc or load_deck_md(A3_MD, a3_cover_fields=True)
    errors: List[str] = []

    if not doc.cover.left_title.strip():
        errors.append("A3 cover missing Left title")
    if not doc.cover.left_subtitle.strip():
        errors.append("A3 cover missing Left subtitle")
    if not doc.cover.right_lines:
        errors.append("A3 cover missing Right (navy, 3 lines)")
    if not doc.cover.tag.strip():
        errors.append("A3 cover missing Tag")

    slides = doc.ordered_slides()
    if len(slides) != 4:
        errors.append(f"A3 deck must have exactly 4 content slides (found {len(slides)})")

    for s in slides:
        if not s.title.strip():
            errors.append(f"Slide {s.number} missing Title")
        if not s.diagram.strip():
            errors.append(f"Slide {s.number} missing Diagram field")
            continue
        errors.extend(_validate_slide_layout(s))

    return errors


def validate_a3_renderers(doc: DeckDocument | None = None) -> List[str]:
    from a3_aligned_render import diagram_stems_for_doc

    doc = doc or load_deck_md(A3_MD, a3_cover_fields=True)
    errors: List[str] = []
    expected = {s.diagram for s in doc.ordered_slides() if s.diagram}
    available = set(diagram_stems_for_doc(doc))
    missing = sorted(expected - available)
    if missing:
        errors.append(
            f"No Python diagram renderer for: {', '.join(missing)} "
            f"(edit scripts/a3_aligned_render.py — not Mermaid)"
        )
    return errors


def validate_png(path: Path) -> List[str]:
    errors: List[str] = []
    if not path.is_file():
        errors.append(f"Diagram PNG missing: {path.relative_to(ROOT)}")
        return errors
    size = path.stat().st_size
    if size < MIN_PNG_BYTES:
        errors.append(f"Diagram PNG too small ({size} B): {path.relative_to(ROOT)}")
        return errors
    try:
        from PIL import Image

        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            w, h = img.size
            if w < 200 or h < 80:
                errors.append(
                    f"Diagram PNG dimensions too small ({w}x{h}): {path.relative_to(ROOT)}"
                )
    except Exception as exc:
        errors.append(f"Diagram PNG unreadable ({path.relative_to(ROOT)}): {exc}")
    return errors


def validate_a3_diagram_pngs(doc: DeckDocument | None = None) -> List[str]:
    doc = doc or load_deck_md(A3_MD, a3_cover_fields=True)
    errors: List[str] = []
    for s in doc.ordered_slides():
        if s.diagram:
            errors.extend(validate_png(_a3_png(s.diagram)))
    return errors


def validate_b6_md(doc: DeckDocument | None = None) -> List[str]:
    doc = doc or load_b6_md()
    errors: List[str] = []

    if not doc.cover.title.strip():
        errors.append("B6 cover missing Title")
    if not doc.cover.subtitle.strip():
        errors.append("B6 cover missing Subtitle")

    slides = doc.ordered_slides()
    if not slides:
        errors.append("B6 deck has no content slides")

    for s in slides:
        if not s.title.strip():
            errors.append(f"B6 slide {s.number} missing Title")
        if s.image:
            if s.image == "logical-pipeline-boss-slide.png":
                img = PIPELINE_IMG
            else:
                img = ROOT / "assets" / s.image
            if not img.is_file():
                errors.append(f"B6 slide {s.number} image missing: {img.relative_to(ROOT)}")
        elif not s.bullets:
            errors.append(f"B6 slide {s.number} has no bullets and no image")

    return errors


def validate_built_pptx(path: Path, *, expected_slides: int) -> List[str]:
    from pptx_util import assert_pptx_valid

    errors: List[str] = []
    try:
        assert_pptx_valid(path)
    except ValueError as exc:
        errors.append(f"{path.name}: {exc}")
        return errors

    from pptx import Presentation

    prs = Presentation(str(path))
    count = len(prs.slides)
    if count != expected_slides:
        errors.append(f"{path.name}: expected {expected_slides} slides, got {count}")
    return errors


def validate_a3_build(doc: DeckDocument | None = None) -> List[str]:
    doc = doc or load_deck_md(A3_MD, a3_cover_fields=True)
    errors: List[str] = []
    errors.extend(validate_style_reference())
    errors.extend(validate_a3_md(doc))
    errors.extend(validate_a3_renderers(doc))
    return errors


def validate_b6_build(doc: DeckDocument | None = None) -> List[str]:
    doc = doc or load_b6_md()
    errors: List[str] = []
    errors.extend(validate_style_reference())
    errors.extend(validate_b6_md(doc))
    return errors
