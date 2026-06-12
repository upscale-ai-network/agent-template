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

# Fixed canvas — native resolution matches PPTX diagram band (no upscale blur).
CANVAS_W, CANVAS_H = 1800, 720
BOX_W, BOX_H = 280, 72
BOX_R = 8
BOX_GAP = 44
ARROW_COLOR = (69, 90, 100, 255)

# Legacy mermaid (unused by current deck — kept for ad-hoc .mmd experiments).
MERMAID_STEMS: Dict[str, str] = {}

COMPOSITE_STEMS = frozenset({
    "b6-slide02-pipeline-scope-pie",
    "b6-slide03-pipeline-blocks",
    "b6-slide03-pipeline-annotated",
    "b6-slide04-qos-stitch",
    "b6-slide04-csb-inset",
    "b6-slide05-csb-ccc-tables",
    "b6-slide06-scope-deliverable",
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
QOS_ORANGE_FILL = (255, 224, 178, 255)
QOS_ORANGE_STROKE = (239, 108, 0, 255)
QOS_DETACH_GAP_DEG = 5.0
QOS_EXPLODE_PX = 44
PIE_CENTER_Y_OFFSET = -28
PIE_OUTER_R = 318
PIE_INNER_R = 108
QOS_LABEL_R_EXTRA = 20
SHADOW_FILL = (176, 190, 197, 90)
SHADOW_OFFSET = (5, 6)
CENTER_FILL = (255, 255, 255, 255)
CENTER_EDGE = (176, 190, 197, 255)
LANE_GLOW = (255, 243, 224, 180)

# Equal slices; index 5 sits at bottom (6 o'clock). (peer) = acknowledged W DRI, subtle 2nd line.
SliceLabel = str | List[str]
PipeSlice = Tuple[SliceLabel, Optional[str], bool]
PIPE_SCOPE_SLICES: List[PipeSlice] = [
    ("Port-CCC", None, False),
    ("L2/L3-CCC", "Shafi · Tilak", False),
    ("ACL-CCC", "Shrawan", False),
    ("ECMP-CCC", "Tippanna", False),
    ("Classify-CCC", "Shrawan", False),
    (["QoSMAP", "CSB Buffer Carving", "csb-buffer-carving-ccc"], "Diwakar", True),
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


PEER_BOX = ((236, 239, 241, 255), (69, 90, 100, 255))
LANE_BOX = ((227, 242, 253, 255), (21, 101, 192, 255))
QOS_BLOCK = (QOS_ORANGE_FILL, QOS_ORANGE_STROKE)
MUTED_BOX = ((245, 245, 245, 255), (144, 164, 174, 255))


def _load_flow_font(size: int = 14):
    from PIL import ImageFont

    for path in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _load_flow_font_bold(size: int = 14):
    from PIL import ImageFont

    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return _load_flow_font(size)


def _save_flow_canvas(img, out: Path) -> Path:
    from PIL import Image

    out.parent.mkdir(parents=True, exist_ok=True)
    if img.size != (CANVAS_W, CANVAS_H):
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
        ox = (CANVAS_W - img.width) // 2
        oy = (CANVAS_H - img.height) // 2
        canvas.paste(img, (ox, oy), img if img.mode == "RGBA" else None)
        img = canvas
    img.convert("RGB").save(out, "PNG", dpi=(192, 192))
    return out


def _draw_labeled_box(
    draw,
    x: int,
    y: int,
    lines: List[str],
    style: Tuple,
    font,
    *,
    box_w: Optional[int] = None,
    box_h: Optional[int] = None,
    shadow: bool = False,
    glow: bool = False,
    line_h: Optional[int] = None,
    sub_font=None,
    sub_fill=None,
    stroke_w: int = 2,
) -> None:
    fill, stroke = style
    bw = box_w or BOX_W
    bh = box_h or BOX_H
    if glow:
        draw.rounded_rectangle(
            (x - 4, y - 4, x + bw + 4, y + bh + 4),
            radius=BOX_R + 2,
            fill=LANE_GLOW,
            outline=None,
        )
    if shadow:
        ox, oy = SHADOW_OFFSET
        draw.rounded_rectangle(
            (x + ox, y + oy, x + bw + ox, y + bh + oy),
            radius=BOX_R,
            fill=SHADOW_FILL,
            outline=None,
        )
    draw.rounded_rectangle(
        (x, y, x + bw, y + bh), radius=BOX_R, fill=fill, outline=stroke, width=stroke_w
    )
    lh = line_h or 18
    block_h = len(lines) * lh
    ty = y + (bh - block_h) // 2
    for i, line in enumerate(lines):
        f = sub_font if sub_font is not None and i > 0 else font
        line_fill = sub_fill if sub_fill is not None and i > 0 else TEXT
        tw = draw.textbbox((0, 0), line, font=f)[2]
        draw.text((x + (bw - tw) // 2, ty), line, fill=line_fill, font=f)
        ty += lh


def _arrow_h(draw, x1: int, y: int, x2: int) -> None:
    draw.line((x1, y, x2 - 10, y), fill=ARROW_COLOR, width=2)
    draw.polygon([(x2, y), (x2 - 12, y - 6), (x2 - 12, y + 6)], fill=ARROW_COLOR)


def _arrow_v(draw, x: int, y1: int, y2: int) -> None:
    draw.line((x, y1, x, y2 - 10), fill=ARROW_COLOR, width=2)
    draw.polygon([(x, y2), (x - 6, y2 - 12), (x + 6, y2 - 12)], fill=ARROW_COLOR)


def _render_lr_chain(
    items: List[Tuple[List[str], Tuple]],
    out_name: str,
) -> Path:
    """Horizontal chain — uniform box size, fixed canvas."""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_flow_font()
    n = len(items)
    span = n * BOX_W + (n - 1) * BOX_GAP
    x = (CANVAS_W - span) // 2
    y = (CANVAS_H - BOX_H) // 2
    xs: List[int] = []
    for lines, style in items:
        _draw_labeled_box(draw, x, y, lines, style, font)
        xs.append(x)
        x += BOX_W + BOX_GAP
    mid_y = y + BOX_H // 2
    for i in range(n - 1):
        _arrow_h(draw, xs[i] + BOX_W, mid_y, xs[i + 1])
    return _save_flow_canvas(img, B6_DIR / out_name)


def render_qos_stitch() -> Path:
    return _render_lr_chain(
        [
            (["Ingress", "VLAN · DSCP · ESUN · UFH"], PEER_BOX),
            (["TC"], PEER_BOX),
            (["Remark · policer · ECN"], PEER_BOX),
            (["Queue · QoSMAP"], LANE_BOX),
            (["Buffer-carving", "at CSB"], LANE_BOX),
        ],
        "b6-slide04-qos-stitch.png",
    )


# Guru kickoff blocks — same names, deck-native styling (shadows · QoS highlight).
PIPE_LOOKUP_BLOCKS = [
    "Port",
    "Parser",
    "MyMAC",
    "VLAN",
    "L2-FBD",
    "UFH",
    "VRF",
    "L3-FIB",
    "ESUN FDB",
]
PIPE_FWD_BLOCKS = [
    "ECMP",
    "QoSMAP",
    "NH",
    "LAG",
    "IACL",
    "Queue",
    "Egress",
    "EgrNH",
    "EACL",
]
PIPE_QOS_HIGHLIGHT = frozenset({"QoSMAP", "Queue"})


def render_pipeline_blocks() -> Path:
    """Guru logical pipeline — block diagram with shadows; QoS blocks highlighted."""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_flow_font(11)
    font_lane = _load_flow_font_bold(12)

    sm_w, sm_h = 108, 48
    gap = 16
    lane_pad = 28
    lane_h = sm_h + lane_pad * 2
    row1_y = 118
    row2_y = row1_y + lane_h + 56

    def _row_span(n: int) -> int:
        return n * sm_w + (n - 1) * gap

    def _draw_lane_band(y: int, label: str, blocks: List[str]) -> List[int]:
        span = _row_span(len(blocks))
        band_x = (CANVAS_W - span - 120) // 2 + 100
        band_w = span + 24
        band_y = y - lane_pad
        draw.rounded_rectangle(
            (band_x - 12, band_y, band_x + band_w, band_y + lane_h),
            radius=12,
            fill=(248, 250, 252, 255),
            outline=(207, 216, 220, 255),
            width=1,
        )
        draw.text((48, y + sm_h // 2 - 8), label, fill=PEER, font=font_lane)
        xs: List[int] = []
        x = band_x
        for name in blocks:
            style = QOS_BLOCK if name in PIPE_QOS_HIGHLIGHT else PEER_BOX
            highlight = name in PIPE_QOS_HIGHLIGHT
            _draw_labeled_box(
                draw,
                x,
                y,
                [name],
                style,
                font,
                box_w=sm_w,
                box_h=sm_h,
                shadow=True,
                glow=highlight,
            )
            xs.append(x)
            x += sm_w + gap
        mid_y = y + sm_h // 2
        for i in range(len(xs) - 1):
            _arrow_h(draw, xs[i] + sm_w, mid_y, xs[i + 1])
        return xs

    xs1 = _draw_lane_band(row1_y, "Ingress · lookup", PIPE_LOOKUP_BLOCKS)
    xs2 = _draw_lane_band(row2_y, "Forward · egress", PIPE_FWD_BLOCKS)
    _arrow_v(draw, xs1[-1] + sm_w // 2, row1_y + sm_h, row2_y)

    callout = "QoSMAP · Queue = bugatti-qos-ccc scope"
    font_callout = _load_flow_font(12)
    tw = draw.textbbox((0, 0), callout, font=font_callout)[2]
    draw.text((CANVAS_W // 2 - tw // 2, row2_y + sm_h + lane_pad + 8), callout, fill=QOS_ORANGE_STROKE, font=font_callout)

    return _save_flow_canvas(img, B6_DIR / "b6-slide03-pipeline-blocks.png")


def render_csb_inset() -> Path:
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_flow_font()
    inner_w = BOX_W + 80
    inner_h = 3 * BOX_H + 2 * BOX_GAP + 48
    ix = (CANVAS_W - inner_w) // 2
    iy = (CANVAS_H - inner_h - BOX_H - BOX_GAP) // 2
    draw.rounded_rectangle(
        (ix - 20, iy - 36, ix + inner_w + 20, iy + inner_h + 12),
        radius=12,
        fill=(250, 250, 250, 255),
        outline=(176, 190, 197, 255),
        width=2,
    )
    title = "CSB buffer-carving"
    tw = draw.textbbox((0, 0), title, font=_load_flow_font_bold())[2]
    draw.text((CANVAS_W // 2 - tw // 2, iy - 28), title, fill=TEXT, font=_load_flow_font_bold())
    labels = [
        ["Port-speed tiers", "200G · 400G · 800G"],
        ["Lossy / lossless · PFC · queues"],
        ["QoSMAP · TC · egress queues"],
    ]
    bx = ix + (inner_w - BOX_W) // 2
    by = iy + 8
    prev_bottom: Optional[int] = None
    for lines in labels:
        _draw_labeled_box(draw, bx, by, lines, LANE_BOX, font)
        if prev_bottom is not None:
            _arrow_v(draw, bx + BOX_W // 2, prev_bottom, by)
        prev_bottom = by + BOX_H
        by += BOX_H + BOX_GAP
    out_y = iy + inner_h + BOX_GAP
    _draw_labeled_box(
        draw,
        (CANVAS_W - BOX_W) // 2,
        out_y,
        ["buffer-carving plan"],
        LANE_BOX,
        font,
    )
    _arrow_v(draw, CANVAS_W // 2, iy + inner_h - 8, out_y)
    return _save_flow_canvas(img, B6_DIR / "b6-slide04-csb-inset.png")


def render_scope_deliverable() -> Path:
    """Closing — Scope (top half) · Deliverable qos-arch-ccc · full Datapath band."""
    from PIL import Image, ImageDraw

    # 2× supersample → downscale for crisp type and edges in PPTX
    scale = 2
    W, H = CANVAS_W * scale, CANVAS_H * scale

    def sc(v: float) -> int:
        return int(round(v * scale))

    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_section = _load_flow_font_bold(sc(20))
    font_title = _load_flow_font_bold(sc(17))
    font_cap = _load_flow_font(sc(15))
    font_det_title = _load_flow_font_bold(sc(14))
    font_det_sub = _load_flow_font(sc(13))
    font_plan = _load_flow_font(sc(13))
    font_dp = _load_flow_font_bold(sc(16))
    font_qos = _load_flow_font_bold(sc(14))

    margin = sc(52)
    mid_y = sc(328)
    stroke = 3 if scale >= 2 else 2

    draw.rounded_rectangle(
        (margin - sc(8), sc(8), W - margin + sc(8), mid_y - sc(10)),
        radius=sc(10),
        fill=(248, 250, 252, 255),
        outline=(176, 190, 197, 255),
        width=stroke,
    )
    draw.rounded_rectangle(
        (margin - sc(8), mid_y + sc(6), W - margin + sc(8), H - sc(12)),
        radius=sc(10),
        fill=(252, 252, 252, 255),
        outline=(176, 190, 197, 255),
        width=stroke,
    )
    draw.line((margin, mid_y, W - margin, mid_y), fill=(120, 144, 156, 255), width=stroke)

    draw.text((margin, sc(16)), "Scope", fill=TEXT, font=font_section)
    scope_y = sc(46)
    scope_w, scope_h = sc(400), sc(56)
    scope_x = W // 2 - scope_w // 2
    _draw_labeled_box(
        draw,
        scope_x,
        scope_y,
        ["bugatti-qos-ccc"],
        LANE_BOX,
        font_title,
        box_w=scope_w,
        box_h=scope_h,
        shadow=True,
        stroke_w=stroke,
    )

    cap_w, cap_h = sc(228), sc(52)
    cap_gap = sc(34)
    cap_row = 3 * cap_w + 2 * cap_gap
    cap_x0 = (W - cap_row) // 2
    cap_y = scope_y + scope_h + sc(24)
    for i, label in enumerate(["Capabilities", "Capacities", "Constraints"]):
        x = cap_x0 + i * (cap_w + cap_gap)
        _draw_labeled_box(
            draw, x, cap_y, [label], LANE_BOX, font_cap,
            box_w=cap_w, box_h=cap_h, stroke_w=stroke,
        )
        _arrow_v(draw, x + cap_w // 2, scope_y + scope_h, cap_y)

    scope_sub = "QoSMAP → CSB Buffer Carving"
    stw = draw.textbbox((0, 0), scope_sub, font=font_qos)[2]
    draw.text(
        (W // 2 - stw // 2, cap_y + cap_h + sc(12)),
        scope_sub,
        fill=TEXT,
        font=font_qos,
    )

    draw.text((margin, mid_y + sc(14)), "Deliverable", fill=TEXT, font=font_section)
    del_y = mid_y + sc(44)
    del_w, del_h = sc(440), sc(58)
    del_x = W // 2 - del_w // 2
    _draw_labeled_box(
        draw,
        del_x,
        del_y,
        ["qos-arch-ccc"],
        LANE_BOX,
        font_title,
        box_w=del_w,
        box_h=del_h,
        shadow=True,
        glow=True,
        stroke_w=stroke,
    )

    det_w, det_h = sc(268), sc(66)
    det_gap = sc(28)
    det_row = 3 * det_w + 2 * det_gap
    det_x0 = (W - det_row) // 2
    det_y = del_y + del_h + sc(20)
    details = [
        ["Capabilities", "classify · remark · policer"],
        ["Capacities", "CSB carve · pools · tiers"],
        ["Constraints", "CSB tables · gates v0"],
    ]
    for i, lines in enumerate(details):
        x = det_x0 + i * (det_w + det_gap)
        _draw_labeled_box(
            draw,
            x,
            det_y,
            lines,
            PEER_BOX,
            font_det_title,
            box_w=det_w,
            box_h=det_h,
            shadow=True,
            line_h=sc(20),
            sub_font=font_det_sub,
            sub_fill=PEER,
            stroke_w=stroke,
        )
        _arrow_v(draw, del_x + del_w // 2, del_y + del_h, det_y)

    plan_y = det_y + det_h + sc(16)
    plan_items = ["buffer-carving plan", "validation gates v0", "Architecture docs"]
    plan_w, plan_h = sc(210), sc(48)
    plan_gap = sc(22)
    plan_row = 3 * plan_w + 2 * plan_gap
    plan_x0 = (W - plan_row) // 2
    for i, label in enumerate(plan_items):
        x = plan_x0 + i * (plan_w + plan_gap)
        _draw_labeled_box(
            draw, x, plan_y, [label], MUTED_BOX, font_plan,
            box_w=plan_w, box_h=plan_h, stroke_w=stroke,
        )

    _arrow_v(draw, W // 2, cap_y + cap_h + sc(34), mid_y + sc(4))

    dp_y = plan_y + plan_h + sc(18)
    dp_h = sc(48)
    dp_w = W - 2 * margin
    _draw_labeled_box(
        draw,
        margin,
        dp_y,
        ["full Datapath"],
        MUTED_BOX,
        font_dp,
        box_w=dp_w,
        box_h=dp_h,
        shadow=True,
        stroke_w=stroke,
    )
    _arrow_v(draw, W // 2, plan_y + plan_h, dp_y)

    sharp = img.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    out = B6_DIR / "b6-slide06-scope-deliverable.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sharp.convert("RGB").save(out, "PNG", dpi=(192, 192))
    return out


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


def _draw_donut_slice(
    draw,
    cx: float,
    cy: float,
    outer: float,
    inner: float,
    start: float,
    end: float,
    fill,
    outline,
    *,
    width: int = 3,
    inner_fill=(0, 0, 0, 0),
) -> None:
    draw.pieslice(
        (cx - outer, cy - outer, cx + outer, cy + outer),
        start,
        end,
        fill=fill,
        outline=outline,
        width=width,
    )
    if inner > 0:
        draw.pieslice(
            (cx - inner, cy - inner, cx + inner, cy + inner),
            start,
            end,
            fill=inner_fill,
            outline=(0, 0, 0, 0),
        )


def _fill_annulus_sector(
    draw,
    cx: float,
    cy: float,
    inner: float,
    outer: float,
    start: float,
    end: float,
    fill,
    *,
    steps: int = 24,
) -> None:
    import math

    def _arc(cx, cy, r, a0, a1, reverse=False):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            a = math.radians(a0 + (a1 - a0) * t)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return list(reversed(pts)) if reverse else pts

    outer_pts = _arc(cx, cy, outer, start, end)
    inner_pts = _arc(cx, cy, inner, start, end, reverse=True)
    draw.polygon(outer_pts + inner_pts, fill=fill)


def _exploded_slice_points(
    arc_cx: float,
    arc_cy: float,
    outer: float,
    inner: float,
    start: float,
    end: float,
    *,
    steps: int = 40,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    import math

    def _arc(cx, cy, r, a0, a1, n, reverse=False):
        pts = []
        for i in range(n + 1):
            t = i / n
            a = math.radians(a0 + (a1 - a0) * t)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return list(reversed(pts)) if reverse else pts

    outer_pts = _arc(arc_cx, arc_cy, outer, start, end, steps)
    inner_pts = _arc(arc_cx, arc_cy, inner, start, end, steps, reverse=True)
    return outer_pts, inner_pts


def _draw_exploded_donut_slice(
    draw,
    arc_cx: float,
    arc_cy: float,
    outer: float,
    inner: float,
    start: float,
    end: float,
    fill,
    outline,
    *,
    steps: int = 40,
    stroke_w: int = 3,
    shadow: bool = False,
) -> None:
    """Exploded ring segment — inner and outer arcs share exploded center."""
    outer_pts, inner_pts = _exploded_slice_points(
        arc_cx, arc_cy, outer, inner, start, end, steps=steps
    )
    if shadow:
        ox, oy = SHADOW_OFFSET
        shadow_pts = [(x + ox, y + oy) for x, y in outer_pts + inner_pts]
        draw.polygon(shadow_pts, fill=SHADOW_FILL)
    draw.polygon(outer_pts + inner_pts, fill=fill)
    for i in range(len(outer_pts) - 1):
        draw.line([outer_pts[i], outer_pts[i + 1]], fill=outline, width=stroke_w)
    for i in range(len(inner_pts) - 1):
        draw.line([inner_pts[i], inner_pts[i + 1]], fill=outline, width=stroke_w)


def render_pipeline_scope_pie() -> Path:
    """Donut — equal slices, QoS exploded at bottom (6 o'clock), Bugatti hub."""
    import math

    from PIL import Image, ImageDraw, ImageFont

    w, h = CANVAS_W, CANVAS_H
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2 + PIE_CENTER_Y_OFFSET
    outer, inner = PIE_OUTER_R, PIE_INNER_R

    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_label = font_label_sm = font_label_em = font_hub = font_hub_sub = None
    font_label_bold = None
    for path in font_paths:
        try:
            if "Bold" in path:
                if font_label_bold is None:
                    font_label_bold = ImageFont.truetype(path, 17)
                continue
            font_label = ImageFont.truetype(path, 14)
            font_label_sm = ImageFont.truetype(path, 11)
            font_label_em = ImageFont.truetype(path, 16)
            font_hub = ImageFont.truetype(path, 22)
            font_hub_sub = ImageFont.truetype(path, 11)
            font_title = ImageFont.truetype(path, 22)
            if font_label_bold is None:
                bold_path = path.replace("Arial.ttf", "Arial Bold.ttf")
                if Path(bold_path).is_file():
                    font_label_bold = ImageFont.truetype(bold_path, 17)
            break
        except OSError:
            continue
    if font_label is None:
        font_label = font_label_sm = font_label_em = font_hub = font_hub_sub = font_title = ImageFont.load_default()
    if font_label_bold is None:
        font_label_bold = font_label_em or font_label

    # Soft plate behind donut
    draw.ellipse(
        (cx - outer - 36, cy - outer - 36, cx + outer + 36, cy + outer + 36),
        fill=(248, 250, 252, 255),
        outline=(224, 230, 234, 255),
        width=1,
    )

    n = len(PIPE_SCOPE_SLICES)
    sweep = 360.0 / n
    # PIL: 0° = 3 o'clock, clockwise. Bottom (6 o'clock) = 90°.
    rot = 90.0 - PIPE_QOS_SLICE_INDEX * sweep - sweep / 2.0
    gap = QOS_DETACH_GAP_DEG
    qos_i = PIPE_QOS_SLICE_INDEX
    qos_start = rot + qos_i * sweep + gap / 2.0
    qos_end = rot + (qos_i + 1) * sweep - gap / 2.0
    qos_mid_deg = rot + (qos_i + 0.5) * sweep
    qos_rad = qos_mid_deg * math.pi / 180.0
    qos_cx = cx + QOS_EXPLODE_PX * math.cos(qos_rad)
    qos_cy = cy + QOS_EXPLODE_PX * math.sin(qos_rad)

    gray_outline = (120, 144, 156, 255)
    for i, (_label, _peer, highlight) in enumerate(PIPE_SCOPE_SLICES):
        if highlight:
            continue
        start = rot + i * sweep
        end = rot + (i + 1) * sweep
        if i == qos_i - 1:
            end -= gap / 2.0
        elif i == (qos_i + 1) % n:
            start += gap / 2.0
        _draw_donut_slice(
            draw, cx, cy, outer, inner, start, end, SLICE_GRAY, gray_outline,
            inner_fill=(0, 0, 0, 0),
        )

    # White out detach gaps before orange wedge (clears inner-ring stroke artifacts)
    gap_a = gap
    for gs, ge in (
        (rot + qos_i * sweep - gap_a / 2, rot + qos_i * sweep + gap_a / 2),
        (rot + (qos_i + 1) * sweep - gap_a / 2, rot + (qos_i + 1) * sweep + gap_a / 2),
    ):
        _fill_annulus_sector(draw, cx, cy, inner - 2, outer + 2, gs, ge, CENTER_FILL)

    _draw_exploded_donut_slice(
        draw,
        qos_cx,
        qos_cy,
        outer,
        inner,
        qos_start,
        qos_end,
        QOS_ORANGE_FILL,
        QOS_ORANGE_STROKE,
        shadow=True,
    )

    draw.ellipse(
        (cx - inner, cy - inner, cx + inner, cy + inner),
        fill=CENTER_FILL,
        outline=None,
    )
    # Hub ring stroke — skip QoS detach slot so gray arc doesn't read as a black spot
    hub_bb = (cx - inner, cy - inner, cx + inner, cy + inner)
    skip_start = rot + qos_i * sweep - gap
    skip_end = rot + (qos_i + 1) * sweep + gap
    draw.arc(hub_bb, skip_end, skip_start, fill=CENTER_EDGE, width=3)
    hub_lines = PIPE_HUB_LINES + ["program scope"]
    block_h = 0
    sizes = []
    for i, line in enumerate(hub_lines):
        f = font_hub if i == 0 else font_hub_sub
        bb = draw.textbbox((0, 0), line, font=f)
        sizes.append((bb[2], bb[3], f, line, PEER if i else TEXT))
        block_h += bb[3] + (2 if i == 0 else 0)
    hy = cy - block_h / 2
    for tw, th, f, line, fill in sizes:
        draw.text((cx - tw / 2, hy), line, fill=fill, font=f)
        hy += th + 2

    mid_r = (outer + inner) / 2.0 + 8
    for i, (label, peer, highlight) in enumerate(PIPE_SCOPE_SLICES):
        mid_deg = rot + (i + 0.5) * sweep
        rad = mid_deg * math.pi / 180.0
        r = mid_r + (QOS_LABEL_R_EXTRA if highlight else 0)
        if highlight:
            tx = qos_cx + r * math.cos(rad)
            ty = qos_cy + r * math.sin(rad)
        else:
            tx = cx + r * math.cos(rad)
            ty = cy + r * math.sin(rad)
        lines = _label_lines(label)
        font = font_label_sm if len(lines) > 1 or max(len(line) for line in lines) > 16 else font_label
        emphasis = {1} if i == PIPE_QOS_SLICE_INDEX else set()
        _draw_slice_label(
            draw,
            (tx, ty),
            label,
            font,
            TEXT if highlight else (84, 110, 122, 255),
            peer=peer,
            peer_font=font_label_sm,
            peer_fill=PEER,
            emphasis_font=font_label_bold,
            emphasis_fill=TEXT,
            emphasis_indices=emphasis,
        )

    out = B6_DIR / "b6-slide02-pipeline-scope-pie.png"
    B6_DIR.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", dpi=(192, 192))
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

    regular_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_title = font_hdr = font_cell = font_title_bold = None
    for path in regular_paths:
        try:
            font_title = ImageFont.truetype(path, 20)
            font_hdr = ImageFont.truetype(path, 13)
            font_cell = ImageFont.truetype(path, 14)
            break
        except OSError:
            continue
    for path in bold_paths:
        try:
            font_title_bold = ImageFont.truetype(path, 20)
            break
        except OSError:
            continue
    if font_title is None:
        default = ImageFont.load_default()
        return default, default, default, default
    return font_title, font_hdr, font_cell, font_title_bold or font_title


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
    title_font=None,
) -> int:
    x0, y0 = origin
    highlight_rows = highlight_rows or set()
    tfont = title_font or font_title
    if title:
        draw.text((x0, y0), title, fill=TEXT, font=tfont)
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
    font_title, font_hdr, font_cell, font_title_bold = _load_table_fonts()

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
        title_font=font_title_bold,
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
        title="Fabric pools",
        highlight_rows={2},
    )

    _draw_sample_watermark(img)

    out = B6_DIR / "b6-slide05-csb-ccc-tables.png"
    B6_DIR.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", dpi=(192, 192))
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
            dispatch = {
                "b6-slide02-pipeline-scope-pie": render_pipeline_scope_pie,
                "b6-slide03-pipeline-blocks": render_pipeline_blocks,
                "b6-slide03-pipeline-annotated": render_pipeline_annotated,
                "b6-slide04-qos-stitch": render_qos_stitch,
                "b6-slide04-csb-inset": render_csb_inset,
                "b6-slide05-csb-ccc-tables": render_csb_ccc_tables,
                "b6-slide06-scope-deliverable": render_scope_deliverable,
            }
            fn = dispatch.get(stem)
            if fn is None:
                raise RuntimeError(f"Unknown composite stem: {stem}")
            fn()
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
