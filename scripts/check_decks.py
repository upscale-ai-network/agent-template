#!/usr/bin/env python3
"""Read-only deck validation — fails loud, changes nothing."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import A3_MD, B6_MD, load_b6_md, load_deck_md  # noqa: E402
from deck_validate import (  # noqa: E402
    DeckBuildError,
    fail_on_errors,
    validate_a3_build,
    validate_a3_diagram_pngs,
    validate_b6_build,
    validate_built_pptx,
)

A3_PPTX = ROOT / "dt100" / "qos-architecture.pptx"
B6_PPTX = ROOT / "dt100" / "manager-arch-vision-b6.pptx"


def main() -> int:
    a3_doc = load_deck_md(A3_MD, a3_cover_fields=True)
    b6_doc = load_b6_md()
    errors = []
    errors.extend(validate_a3_build(a3_doc))
    errors.extend(validate_a3_diagram_pngs(a3_doc))
    errors.extend(validate_b6_build(b6_doc))
    if A3_PPTX.is_file():
        errors.extend(validate_built_pptx(A3_PPTX, expected_slides=1 + len(a3_doc.slides)))
    else:
        errors.append(f"Missing built deck: {A3_PPTX.relative_to(ROOT)}")
    if B6_PPTX.is_file():
        errors.extend(validate_built_pptx(B6_PPTX, expected_slides=1 + len(b6_doc.ordered_slides())))
    else:
        errors.append(f"Missing built deck: {B6_PPTX.relative_to(ROOT)}")
    try:
        fail_on_errors(errors)
    except DeckBuildError as exc:
        print(exc, file=sys.stderr)
        return 1
    print("All deck checks passed (md, PNGs, pptx)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
