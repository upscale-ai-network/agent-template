#!/usr/bin/env python3
"""Litmus checks for upscale-company-template.pptx — run before commit."""

import sys
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets/templates/upscale-company-template.pptx"

sys.path.insert(0, str(ROOT / "scripts"))
from pptx_util import (  # noqa: E402
    COLOR_GOLD,
    COLOR_NAVY_TITLE,
    RIGHT_PANEL_LEFT,
    check_zip_duplicates,
    is_footer,
)


def _run_rgb(shape):
    return shape.text_frame.paragraphs[0].runs[0].font.color.rgb


def main() -> int:
    errors = []
    if not TEMPLATE.exists():
        print(f"MISSING: {TEMPLATE}")
        return 1

    dups = check_zip_duplicates(TEMPLATE)
    if dups:
        errors.append(f"corrupt zip duplicates: {dups}")

    prs = Presentation(str(TEMPLATE))
    if len(prs.slides) != 2:
        errors.append(f"expected 2 slides, got {len(prs.slides)}")

    cover = prs.slides[0]
    has_footer = any(
        "Upscale AI" in (sh.text_frame.text if sh.has_text_frame else "")
        for sh in cover.shapes
    )
    if not has_footer:
        errors.append("cover missing Upscale footer")

    right_gold = False
    left_title = False
    for sh in cover.shapes:
        if not sh.has_text_frame or is_footer(sh):
            continue
        t = sh.text_frame.text
        if sh.left >= RIGHT_PANEL_LEFT and "[Subtitle line 1]" in t:
            if _run_rgb(sh) == COLOR_GOLD:
                right_gold = True
            else:
                errors.append(f"navy panel subtitle not gold: {_run_rgb(sh)}")
        if sh.left < RIGHT_PANEL_LEFT and "[Presentation title]" in t:
            left_title = True

    if not right_gold:
        errors.append("cover: [Subtitle line 1] on navy panel must be gold")
    if not left_title:
        errors.append("cover: missing [Presentation title] on white panel")

    content = prs.slides[1]
    title_ok = body_ok = False
    for sh in content.shapes:
        if not sh.has_text_frame or is_footer(sh):
            continue
        if sh.top < 700_000 and "[Slide title]" in sh.text_frame.text:
            if _run_rgb(sh) == COLOR_NAVY_TITLE:
                title_ok = True
            else:
                errors.append(f"content title color wrong: {_run_rgb(sh)}")
        elif sh.top > 700_000 and "[Bullet" in sh.text_frame.text:
            body_ok = True
    if not title_ok:
        errors.append("content: [Slide title] must be navy #051830")
    if not body_ok:
        errors.append("content: missing bullet placeholders")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {TEMPLATE}")
    print("  - ZIP clean, 2 slides, footer, gold on navy, navy title on content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
