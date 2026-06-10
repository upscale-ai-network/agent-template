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
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
B6_DIR = ROOT / "assets" / "diagrams" / "b6"
B6_MD = ROOT / "dt122" / "bugatti-qos-ccc.md"
PIPELINE_SRC = ROOT / "assets" / "logical-pipeline-boss-slide.png"
MERMAID_CONFIG = B6_DIR / "mermaid-config.json"
MMDC_PKG = "@mermaid-js/mermaid-cli@11.15.0"

# stem → mmd filename (pipeline uses composite)
MERMAID_STEMS: Dict[str, str] = {
    "b6-slide04-qos-stitch": "b6-slide04-qos-stitch.mmd",
    "b6-slide04-csb-inset": "b6-slide04-csb-inset.mmd",
    "b6-slide06-boundaries": "b6-slide06-boundaries.mmd",
    "b6-slide07-next-steps": "b6-slide07-next-steps.mmd",
}

COMPOSITE_STEMS = frozenset({
    "b6-slide02-pipeline-scope-pie",
    "b6-slide03-pipeline-annotated",
    "b6-slide05-csb-ccc-tables",
})

sys.path.insert(0, str(ROOT / "scripts"))

from deck_from_md import load_b6_md  # noqa: E402
from deck_validate import fail_on_errors, validate_b6_build, validate_png  # noqa: E402

DRI_ORANGE = (239, 108, 0, 90)
DRI_STROKE = (239, 108, 0, 255)
LABEL_BG = (255, 243, 224, 220)
TEXT = (5, 24, 48, 255)
PEER = (69, 90, 100, 255)
SLICE_GRAY = (207, 216, 220, 255)
SLICE_HIGHLIGHT = (227, 242, 253, 255)
SLICE_HIGHLIGHT_EDGE = (21, 101, 192, 255)
CENTER_FILL = (255, 255, 255, 255)
CENTER_EDGE = (176, 190, 197, 255)

# Equal slices; index 5 sits at bottom (6 o'clock). (peer) = acknowledged W DRI, subtle 2nd line.
SliceLabel = str | List[str]
PipeSlice = Tuple[SliceLabel, Optional[str], bool]
PIPE_SCOPE_SLICES: List[PipeSlice] = [
    ("Port-CCC", None, False),
    ("L2/L3-CCC", "Shafi · Tilak", False),
    ("ACL-CCC", "Shrawan", False),
    ("ECMP-CCC", "Tippanna", False),
    ("Classify-CCC", "Shrawan", False),
    (["QoSMAP", "CSB buffer-carving", "QoS-CCC"], "Diwakar", True),
    ("Mirror-CCC", "Shafi", False),
    ("Others", None, False),
]
PIPE_QOS_SLICE_INDEX = 5
# Center hub — Bugatti ASIC program scope.
PIPE_HUB_LINES = ["Bugatti"]


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


def _label_lines(label: SliceLabel) -> List[str]:
    if isinstance(label, list):
        return label
    return [label]


def _draw_slice_label(
    draw,
    center: Tuple[float, float],
    label: SliceLabel,
    font,
    fill,
    *,
    peer: Optional[str] = None,
    peer_font=None,
    peer_fill=None,
    emphasis_font=None,
    emphasis_fill=None,
    emphasis_indices: Optional[set] = None,
    line_gap: int = 2,
    peer_gap: int = 3,
) -> None:
    lines = _label_lines(label)
    peer_font = peer_font or font
    peer_fill = peer_fill if peer_fill is not None else fill
    emphasis_indices = emphasis_indices or set()
    if peer:
        peer_line = peer if peer.startswith("(") else f"({peer})"
        lines = lines + [peer_line]
    if not lines:
        return
    sizes = []
    for i, line in enumerate(lines):
        if peer and i == len(lines) - 1:
            f = peer_font
        elif i in emphasis_indices and emphasis_font is not None:
            f = emphasis_font
        else:
            f = font
        bb = draw.textbbox((0, 0), line, font=f)
        sizes.append((bb[2], bb[3], f, line))
    block_h = sum(s[1] for s in sizes) + line_gap * (len(sizes) - 1)
    if peer and len(sizes) > 1:
        block_h += peer_gap - line_gap
    y = center[1] - block_h / 2
    for i, (tw, th, f, line) in enumerate(sizes):
        if peer and i == len(sizes) - 1 and i > 0:
            y += peer_gap - line_gap
        if emphasis_fill is not None and i in emphasis_indices:
            line_fill = emphasis_fill
        else:
            line_fill = peer_fill if peer and i == len(sizes) - 1 else fill
        draw.text((center[0] - tw / 2, y), line, fill=line_fill, font=f)
        y += th + line_gap


def render_pipeline_scope_pie() -> Path:
    """Donut — equal slices, QoS at bottom, Bugatti hub (not mermaid)."""
    import math

    from PIL import Image, ImageDraw, ImageFont

    w, h = 1800, 900
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2 + 20
    outer, inner = 340, 118

    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_label = font_label_sm = font_label_em = font_hub = None
    font_label_bold = None
    for path in font_paths:
        try:
            if "Bold" in path:
                if font_label_bold is None:
                    font_label_bold = ImageFont.truetype(path, 15)
                continue
            font_label = ImageFont.truetype(path, 14)
            font_label_sm = ImageFont.truetype(path, 12)
            font_label_em = ImageFont.truetype(path, 16)
            font_hub = ImageFont.truetype(path, 18)
            font_title = ImageFont.truetype(path, 22)
            if font_label_bold is None:
                bold_path = path.replace("Arial.ttf", "Arial Bold.ttf")
                if Path(bold_path).is_file():
                    font_label_bold = ImageFont.truetype(bold_path, 15)
            break
        except OSError:
            continue
    if font_label is None:
        font_label = font_label_sm = font_label_em = font_hub = font_title = ImageFont.load_default()
    if font_label_bold is None:
        font_label_bold = font_label_em or font_label

    n = len(PIPE_SCOPE_SLICES)
    sweep = 360.0 / n
    # PIL: 0° = 3 o'clock, clockwise. Bottom (6 o'clock) = 90°.
    rot = 90.0 - PIPE_QOS_SLICE_INDEX * sweep - sweep / 2.0

    for i, (label, _peer, highlight) in enumerate(PIPE_SCOPE_SLICES):
        start = rot + i * sweep
        end = rot + (i + 1) * sweep
        fill = SLICE_HIGHLIGHT if highlight else SLICE_GRAY
        outline = SLICE_HIGHLIGHT_EDGE if highlight else (120, 144, 156, 255)
        draw.pieslice(
            (cx - outer, cy - outer, cx + outer, cy + outer),
            start,
            end,
            fill=fill,
            outline=outline,
            width=3,
        )
        draw.pieslice(
            (cx - inner, cy - inner, cx + inner, cy + inner),
            start,
            end,
            fill=(0, 0, 0, 0),
            outline=(0, 0, 0, 0),
        )

    draw.ellipse(
        (cx - inner, cy - inner, cx + inner, cy + inner),
        fill=CENTER_FILL,
        outline=CENTER_EDGE,
        width=3,
    )
    hub = PIPE_HUB_LINES[0]
    tw, th = draw.textbbox((0, 0), hub, font=font_hub)[2:]
    draw.text((cx - tw / 2, cy - th / 2), hub, fill=TEXT, font=font_hub)

    mid_r = (outer + inner) / 2.0 + 8
    for i, (label, peer, _) in enumerate(PIPE_SCOPE_SLICES):
        mid_deg = rot + (i + 0.5) * sweep
        rad = mid_deg * 3.14159265 / 180.0
        tx = cx + mid_r * math.cos(rad)
        ty = cy + mid_r * math.sin(rad)
        lines = _label_lines(label)
        font = font_label_sm if len(lines) > 1 or max(len(line) for line in lines) > 16 else font_label
        emphasis = {1} if i == PIPE_QOS_SLICE_INDEX else set()
        _draw_slice_label(
            draw,
            (tx, ty),
            label,
            font,
            TEXT,
            peer=peer,
            peer_font=font_label_sm,
            peer_fill=TEXT,
            emphasis_font=font_label_bold,
            emphasis_fill=SLICE_HIGHLIGHT_EDGE,
            emphasis_indices=emphasis,
        )

    title = "QoS-CCC scope"
    tt_w = draw.textbbox((0, 0), title, font=font_title)[2]
    draw.text((cx - tt_w // 2, 36), title, fill=TEXT, font=font_title)

    out = B6_DIR / "b6-slide02-pipeline-scope-pie.png"
    B6_DIR.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG")
    return out


TABLE_HEADER = (227, 242, 253, 255)
TABLE_LANE = (227, 242, 253, 255)
TABLE_GRID = (176, 190, 197, 255)
TABLE_MUTED = (120, 144, 156, 255)

# Version 0 placeholders — refine from HW arch, RTL, c-models, use-cases.
CSB_CCC_HEADERS = ["Capabilities", "Capacities", "Constraints"]
CSB_CCC_ROWS = [
    ["Lossy / lossless pools · PFC", "CSB pool depth: TBD", "HWv1: VLAN-PRI + DSCP only"],
    ["WRED · ECN · Pause", "Queues / port: TBD", "No MPLS EXP · no IPv6 pri (v1)"],
    ["QoSMAP · TC → egress queues", "Port tiers: 200G / 400G / 800G", "Admission / headroom: TBD"],
    ["Buffer-carving · admission", "Per-TC carve: TBD", "Peer pool boundaries: TBD"],
]

FABRIC_CCC_HEADERS = ["Block", "Capabilities", "Capacities", "Constraints"]
FABRIC_CCC_ROWS = [
    ["IFP", "Ingress parse · admit", "Pool cells: TBD", "RTL: TBD"],
    ["ISB", "Ingress buffering", "Pool cells: TBD", "RTL: TBD"],
    ["CSB", "Sched · buffer-carving", "Pool cells: TBD", "RTL: TBD"],
    ["EFP", "Egress buffer · shaping", "Pool cells: TBD", "RTL: TBD"],
]


def _load_table_fonts():
    from PIL import ImageFont

    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        try:
            return (
                ImageFont.truetype(path, 20),
                ImageFont.truetype(path, 13),
                ImageFont.truetype(path, 14),
            )
        except OSError:
            continue
    default = ImageFont.load_default()
    return default, default, default


def _draw_table(
    draw,
    origin: Tuple[int, int],
    headers: List[str],
    rows: List[List[str]],
    col_widths: List[int],
    *,
    row_h: int = 44,
    header_h: int = 36,
    font_title,
    font_hdr,
    font_cell,
    title: Optional[str] = None,
    highlight_rows: Optional[set] = None,
) -> int:
    x0, y0 = origin
    highlight_rows = highlight_rows or set()
    if title:
        draw.text((x0, y0), title, fill=TEXT, font=font_title)
        y0 += 32
    table_w = sum(col_widths)
    y = y0
    # header
    x = x0
    for hdr, cw in zip(headers, col_widths):
        _box(draw, (x, y, x + cw, y + header_h), TABLE_HEADER, TABLE_GRID, 1)
        tw = draw.textbbox((0, 0), hdr, font=font_hdr)[2]
        draw.text((x + (cw - tw) // 2, y + 10), hdr, fill=TEXT, font=font_hdr)
        x += cw
    y += header_h
    for ri, row in enumerate(rows):
        x = x0
        fill = TABLE_LANE if ri in highlight_rows else (255, 255, 255, 255)
        for cell, cw in zip(row, col_widths):
            _box(draw, (x, y, x + cw, y + row_h), fill, TABLE_GRID, 1)
            draw.text((x + 8, y + 12), cell, fill=TEXT, font=font_cell)
            x += cw
        y += row_h
    return y - y0 + (32 if title else 0)


def _draw_sample_watermark(img, *, text: str = "SAMPLE") -> None:
    """Light diagonal watermark — tables are placeholders pending HW alignment."""
    from PIL import Image, ImageDraw, ImageFont

    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font = None
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, 108)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    tw = draw.textbbox((0, 0), text, font=font)[2]
    th = draw.textbbox((0, 0), text, font=font)[3]
    draw.text(((w - tw) // 2, (h - th) // 2 - 40), text, fill=(189, 189, 189, 72), font=font)
    rotated = overlay.rotate(32, resample=Image.Resampling.BICUBIC, center=(w // 2, h // 2))
    img.alpha_composite(rotated)


def render_csb_ccc_tables() -> Path:
    """CCC Cap / Cap / Con tables for CSB buffer-carving — v0 placeholders."""
    from PIL import Image, ImageDraw

    w, h = 1800, 900
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font_title, font_hdr, font_cell = _load_table_fonts()

    margin = 48
    gap = 28
    top = 52
    csb_w = [520, 420, 420]
    _draw_table(
        draw,
        (margin, top),
        CSB_CCC_HEADERS,
        CSB_CCC_ROWS,
        csb_w,
        font_title=font_title,
        font_hdr=font_hdr,
        font_cell=font_cell,
        title="CSB buffer-carving",
        highlight_rows={3},
    )
    fab_w = [100, 380, 320, 320]
    fab_x = margin
    fab_y = top + 32 + 36 + 44 * 4 + gap
    _draw_table(
        draw,
        (fab_x, fab_y),
        FABRIC_CCC_HEADERS,
        FABRIC_CCC_ROWS,
        fab_w,
        font_title=font_title,
        font_hdr=font_hdr,
        font_cell=font_cell,
        title="Fabric buffer pools (context)",
        highlight_rows={2},
    )

    _draw_sample_watermark(img)
    align = "ALIGN with HW arch"
    aw = draw.textbbox((0, 0), align, font=font_hdr)[2]
    draw.text(((w - aw) // 2, h - 44), align, fill=SLICE_HIGHLIGHT_EDGE, font=font_hdr)

    out = B6_DIR / "b6-slide05-csb-ccc-tables.png"
    B6_DIR.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG")
    return out


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
        (0.52, 0.38, 0.68, 0.62, "QoSMAP"),
        (0.70, 0.35, 0.92, 0.68, "Queue"),
    ]
    peer_labels = [
        (0.06, 0.72, "L2-CCC"),
        (0.22, 0.72, "ECMP-CCC"),
        (0.38, 0.72, "L2/L3-CCC"),
        (0.54, 0.72, "L3-CCC"),
        (0.70, 0.72, "Port-CCC"),
    ]

    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    font = font_sm = None
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, 14)
            font_sm = ImageFont.truetype(path, 12)
            break
        except OSError:
            continue
    if font is None:
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
            if stem == "b6-slide02-pipeline-scope-pie":
                render_pipeline_scope_pie()
            elif stem == "b6-slide03-pipeline-annotated":
                render_pipeline_annotated()
            elif stem == "b6-slide05-csb-ccc-tables":
                render_csb_ccc_tables()
            else:
                raise RuntimeError(f"Unknown composite stem: {stem}")
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
