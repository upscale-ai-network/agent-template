#!/usr/bin/env python3
"""
Build DT100 A3/B6 PPTX from manager-arch-vision-a3.md and manager-arch-vision-b6.md.
"""

import shutil
import sys
from pathlib import Path
from typing import List, Optional

from pptx import Presentation
from pptx.util import Inches

ROOT = Path(__file__).resolve().parents[1]
DT100 = ROOT / "dt100"
sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import A3_MD, B6_MD, load_b6_md, load_deck_md  # noqa: E402
from pptx_util import (  # noqa: E402
    DSBM_TITLE_LINES,
    assert_pptx_valid,
    fill_content_diagram_slide,
    fill_cover_slide,
    save_presentation,
    trim_to_slides,
)

DSBM_SUBLINE = "\n".join(DSBM_TITLE_LINES)
PIPELINE_IMG = ROOT / "assets" / "logical-pipeline-boss-slide.png"
A3_DIAGRAMS = ROOT / "assets" / "diagrams" / "a3"
RENDER_A3 = ROOT / "scripts" / "render-a3-diagrams.py"

STYLE_DOWNLOAD = Path.home() / "Downloads" / "Mirror-Sflow-Bugatti-ASIC-CCC.pptx"
STYLE_REF = ROOT / "assets/templates/upscale-ccc-style-reference.pptx"

IDX_COVER = 0
IDX_CONTENT = 2


def ensure_style_reference() -> Path:
    if STYLE_REF.exists():
        return STYLE_REF
    if STYLE_DOWNLOAD.exists():
        STYLE_REF.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(STYLE_DOWNLOAD, STYLE_REF)
        return STYLE_REF
    raise FileNotFoundError(
        f"Company style deck not found. Download CCC PPTX to {STYLE_DOWNLOAD} "
        f"or copy to {STYLE_REF}"
    )


class StyledDeck:
    def __init__(self, out_path: Path, num_content_slides: int):
        ref = ensure_style_reference()
        shutil.copy2(ref, out_path)
        self.path = out_path
        self.prs = Presentation(str(out_path))
        keep = [IDX_COVER] + list(range(IDX_CONTENT, IDX_CONTENT + num_content_slides))
        if keep[-1] >= len(self.prs.slides):
            raise ValueError(f"CCC deck needs {keep[-1] + 1} slides, has {len(self.prs.slides)}")
        trim_to_slides(self.prs, keep)
        self._slide_i = 1

    def add_cover(self, headline, subline, meta, tag, notes=None):
        fill_cover_slide(self.prs.slides[0], headline, subline, meta, tag)
        if notes:
            self.prs.slides[0].notes_slide.notes_text_frame.text = notes

    def add_content(
        self,
        title,
        bullets,
        subtitle=None,
        notes=None,
        diagram: Optional[Path] = None,
        title_lines: Optional[List[str]] = None,
    ):
        slide = self.prs.slides[self._slide_i]
        self._slide_i += 1
        if diagram and diagram.is_file():
            fill_content_diagram_slide(
                slide,
                title,
                diagram,
                title_lines=title_lines,
                lead_line=subtitle,
                slide_width=self.prs.slide_width,
            )
        else:
            from pptx_util import fill_content_slide

            fill_content_slide(slide, title, bullets, subtitle=subtitle, title_lines=title_lines)
        if notes:
            slide.notes_slide.notes_text_frame.text = notes
        return slide

    def add_image_slide(self, title, image_path: Path, caption: Optional[str] = None, notes=None):
        slide = self.add_content(
            title,
            [caption] if caption else [],
            diagram=image_path if image_path.is_file() else None,
            notes=notes,
        )
        return slide

    def save(self):
        save_presentation(self.prs, self.path)
        assert_pptx_valid(self.path)
        print(f"OK: {self.path.name}")
        return self.path


def ensure_a3_diagrams() -> None:
    if RENDER_A3.is_file():
        import subprocess

        subprocess.run([sys.executable, str(RENDER_A3)], check=True, cwd=str(ROOT))


def _a3_png(name: str) -> Path:
    return A3_DIAGRAMS / f"{name}.png"


def _join_notes(*parts: str) -> Optional[str]:
    text = "\n\n".join(p.strip() for p in parts if p and p.strip())
    return text or None


def build_a3() -> Path:
    ensure_a3_diagrams()
    doc = load_deck_md(A3_MD, a3_cover_fields=True)
    out = DT100 / "manager-arch-vision-a3.pptx"
    deck = StyledDeck(out, num_content_slides=len(doc.slides))

    cov = doc.cover
    right = cov.right_lines if cov.right_lines else DSBM_TITLE_LINES
    deck.add_cover(
        cov.left_title,
        "\n".join(right),
        cov.left_subtitle,
        cov.tag,
        notes=cov.notes or None,
    )

    before = doc.extra_notes.get("before-1", "")
    into_b6 = doc.extra_notes.get("into-b6", "")
    after_b6 = doc.extra_notes.get("after-b6", "")

    for s in doc.ordered_slides():
        notes = s.notes
        if s.number == 1:
            notes = _join_notes(before, notes, into_b6)
        elif s.number == 3:
            notes = _join_notes(notes, after_b6)
        kwargs = dict(
            title=s.title,
            bullets=[],
            subtitle=s.subtitle or None,
            notes=notes,
        )
        if s.diagram:
            kwargs["diagram"] = _a3_png(s.diagram)
        if s.number == 1:
            kwargs["title_lines"] = DSBM_TITLE_LINES
        deck.add_content(**kwargs)

    return deck.save()


def build_b6() -> Path:
    doc = load_b6_md()
    slides = doc.ordered_slides()
    out = DT100 / "manager-arch-vision-b6.pptx"
    deck = StyledDeck(out, num_content_slides=len(slides))

    cov = doc.cover
    deck.add_cover(cov.title, cov.subtitle, cov.meta, cov.tag, notes=cov.notes or None)

    for s in slides:
        if s.image:
            img = PIPELINE_IMG if s.image == "logical-pipeline-boss-slide.png" else ROOT / "assets" / s.image
            deck.add_image_slide(s.title, img, caption=s.caption or None, notes=s.notes or None)
        else:
            deck.add_content(
                s.title,
                s.bullets,
                subtitle=s.subtitle or None,
                notes=s.notes or None,
            )

    return deck.save()


def main():
    ref = ensure_style_reference()
    print(f"Style reference: {ref}")
    a3 = build_a3()
    b6 = build_b6()
    print(f"Wrote {a3} ({len(Presentation(a3).slides)} slides, company chrome)")
    print(f"Wrote {b6} ({len(Presentation(b6).slides)} slides, company chrome)")


if __name__ == "__main__":
    main()
