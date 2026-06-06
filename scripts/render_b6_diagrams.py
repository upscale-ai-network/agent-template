#!/usr/bin/env python3
"""
Render B6 diagram PNGs for bugatti-qos-ccc.md.

- Mermaid sources: assets/diagrams/b6/*.mmd  → mmdc via npx
- Pipeline annotate: Pillow overlay on logical-pipeline-boss-slide.png
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
B6_DIR = ROOT / "assets" / "diagrams" / "b6"
B6_MD = ROOT / "dt122" / "bugatti-qos-ccc.md"
PIPELINE_SRC = ROOT / "assets" / "logical-pipeline-boss-slide.png"
MERMAID_CONFIG = B6_DIR / "mermaid-config.json"
MMDC_PKG = "@mermaid-js/mermaid-cli@11.15.0"

# stem → mmd filename (pipeline uses composite)
MERMAID_STEMS: Dict[str, str] = {
    "b6-slide01-process-ribbon": "b6-slide01-process-ribbon.mmd",
    "b6-slide02-validation-stack": "b6-slide02-validation-stack.mmd",
    "b6-slide04-csb-inset": "b6-slide04-csb-inset.mmd",
    "b6-slide05-gate-alignment": "b6-slide05-gate-alignment.mmd",
    "b6-slide06-boundaries": "b6-slide06-boundaries.mmd",
    "b6-slide07-next-steps": "b6-slide07-next-steps.mmd",
}

COMPOSITE_STEMS = frozenset({"b6-slide03-pipeline-annotated"})

sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import load_b6_md  # noqa: E402
from deck_validate import fail_on_errors, validate_b6_build, validate_png  # noqa: E402

DRI_ORANGE = (239, 108, 0, 90)
DRI_STROKE = (239, 108, 0, 255)
LABEL_BG = (255, 243, 224, 220)
TEXT = (5, 24, 48, 255)
PEER = (69, 90, 100, 255)


def _require_npx() -> str:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("npx not on PATH — install node or render on Mac Lepton primary")
    return npx


def render_mermaid(stem: str, mmd_name: str) -> Path:
    mmd = B6_DIR / mmd_name
    out = B6_DIR / f"{stem}.png"
    if not mmd.is_file():
        raise FileNotFoundError(f"Missing mermaid source: {mmd}")
    B6_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        _require_npx(),
        "--yes",
        MMDC_PKG,
        "-i",
        str(mmd),
        "-o",
        str(out),
        "-b",
        "white",
        "-w",
        "1800",
        "-H",
        "900",
    ]
    if MERMAID_CONFIG.is_file():
        cmd.extend(["-c", str(MERMAID_CONFIG)])
    subprocess.run(cmd, check=True, cwd=ROOT)
    return out


def _box(draw, xy: Tuple[int, int, int, int], fill, outline, width: int = 3) -> None:
    draw.rectangle(xy, fill=fill, outline=outline, width=width)


def render_pipeline_annotated() -> Path:
    from PIL import Image, ImageDraw, ImageFont

    if not PIPELINE_SRC.is_file():
        raise FileNotFoundError(f"Missing pipeline base: {PIPELINE_SRC}")

    img = Image.open(PIPELINE_SRC).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size

    # Fractional regions on boss slide (1024×575 typical)
    highlights = [
        (0.52, 0.38, 0.68, 0.62, "QoSMAP · Diwakar"),
        (0.70, 0.35, 0.92, 0.68, "Queue / carve · Diwakar"),
    ]
    peer_labels = [
        (0.08, 0.72, "Parser · Rupa"),
        (0.22, 0.72, "L2 · Shafi / Tilak"),
        (0.38, 0.72, "L3 · Girish"),
        (0.52, 0.72, "ECMP/LAG · Tippanna"),
    ]

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    for x1f, y1f, x2f, y2f, _ in highlights:
        x1, y1, x2, y2 = int(x1f * w), int(y1f * h), int(x2f * w), int(y2f * h)
        _box(draw, (x1, y1, x2, y2), DRI_ORANGE, DRI_STROKE, 4)

    for x1f, y1f, x2f, y2f, label in highlights:
        x1, y1, x2, y2 = int(x1f * w), int(y1f * h), int(x2f * w), int(y2f * h)
        tw, th = draw.textbbox((0, 0), label, font=font)[2:]
        tx = x1 + (x2 - x1 - tw) // 2
        ty = max(0, y1 - th - 4)
        _box(draw, (tx - 4, ty - 2, tx + tw + 4, ty + th + 2), LABEL_BG, DRI_STROKE, 2)
        draw.text((tx, ty), label, fill=TEXT, font=font)

    for xf, yf, label in peer_labels:
        x, y = int(xf * w), int(yf * h)
        draw.text((x, y), label, fill=PEER, font=font_sm)

    composed = Image.alpha_composite(img, overlay).convert("RGB")
    out = B6_DIR / "b6-slide03-pipeline-annotated.png"
    B6_DIR.mkdir(parents=True, exist_ok=True)
    composed.save(out, "PNG")
    return out


def stems_for_doc(doc=None) -> List[str]:
    doc = doc or load_b6_md()
    return [s.diagram for s in doc.ordered_slides() if s.diagram]


def render_all_b6_diagrams(doc=None) -> List[str]:
    doc = doc or load_b6_md()
    fail_on_errors(validate_b6_build(doc))
    rendered: List[str] = []

    for stem in stems_for_doc(doc):
        if stem in COMPOSITE_STEMS:
            render_pipeline_annotated()
        elif stem in MERMAID_STEMS:
            render_mermaid(stem, MERMAID_STEMS[stem])
        elif (B6_DIR / f"{stem}.mmd").is_file():
            render_mermaid(stem, f"{stem}.mmd")
        else:
            raise RuntimeError(f"No B6 renderer for diagram stem: {stem}")
        fail_on_errors(validate_png(B6_DIR / f"{stem}.png"))
        rendered.append(stem)

    return rendered


def main() -> int:
    doc = load_b6_md()
    stems = render_all_b6_diagrams(doc)
    print(f"Rendered {len(stems)} B6 diagrams from {B6_MD.name}")
    for stem in stems:
        print(f"OK: {(B6_DIR / f'{stem}.png').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
