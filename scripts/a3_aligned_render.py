"""Aligned A3 diagram renderer — reads labels from manager-arch-vision-a3.md."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from deck_from_md import A3_MD, load_deck_md


def _a3():
    return load_deck_md(A3_MD, a3_cover_fields=True)

STYLES: Dict[str, Dict[str, str]] = {
    "program": {"fill": "#E3F2FD", "stroke": "#1565C0", "color": "#051830"},
    "lane": {"fill": "#FFF3E0", "stroke": "#EF6C00", "color": "#051830"},
    "peer": {"fill": "#ECEFF1", "stroke": "#455A64", "color": "#051830"},
    "gate": {"fill": "#F3E5F5", "stroke": "#7B1FA2", "color": "#051830"},
    "step": {"fill": "#E8F5E9", "stroke": "#2E7D32", "color": "#051830"},
    "doc": {"fill": "#E3F2FD", "stroke": "#1565C0", "color": "#051830"},
    "ask": {"fill": "#FFF3E0", "stroke": "#EF6C00", "color": "#051830"},
    "act": {"fill": "#F3E5F5", "stroke": "#7B1FA2", "color": "#051830"},
    "muted": {"fill": "#F5F5F5", "stroke": "#BDBDBD", "color": "#9E9E9E"},
}

FLOW_ARROW = "#B0BEC5"
FLOW_ARROW_WIDTH = 1.25

# On-slide read path — Guru asked how to read; must be visible in PPTX (not hairlines).
GUIDE_COLOR = "#455A64"
GUIDE_WIDTH = 2.5
GUIDE_MARKER = "read-guide-head"

# Unified box/font — TARGET_SCALE maps BOX_W to on-slide pixels across slides.
BOX_W = 192
BOX_H = 50
YES_BOX_W = BOX_W * 1.12
YES_BOX_H = BOX_H * 1.08
FONT = "Arial, Helvetica, sans-serif"
FONT_SIZE = 12
FONT_SIZE_SG = 11
FONT_SIZE_NOTE = 10
LINE_H = 13
LABEL_MAX_CHARS = 22

MARGIN = 20.0
H_GAP = 30.0
H_GAP_SLIDE1 = 10.0
ROW_GAP = 26.0
ROW_GAP_SLIDE2 = 18.0
COL_GAP = 44.0
BAND_GAP = 32.0
LINE_STUB = 4.0

SG_PAD = 12
SG_TITLE_H = 20
SG_RX = 8
BOX_RX = 6

ARROW = "#78909C"
ARROW_WIDTH = 1.5

SG_BORDER = "#B0BEC5"
SG_FILL = "#FAFAFA"
SG_TITLE_COLOR = "#556677"

GATE_HALF = 44

COMPASS_BOX_W = 156.0
COMPASS_BOX_H = 46.0
COMPASS_ARM = 52.0
COMPASS_BAND_PAD = 14.0
COMPASS_BELOW_GATE = 28.0

QUADRANT_STYLE = {
    "north": "program",
    "east": "peer",
    "west": "peer",
    "south": "lane",
}

FRAME_W = 1320.0
FRAME_H = 500.0
FRAME_PAD = 16.0
TARGET_SCALE = 1.35
BOX_W_SPREAD = 242.0
BOX_H_SPREAD = 72.0
FONT_SIZE_SPREAD = 13
SPREAD_V_PAD = 52.0
MIN_SPREAD_GAP = 32.0
# Match box pixel size on slide 1 (widest) across all slides.
UNIFIED_SCALE: Optional[float] = None


def _xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_box_label(label: str) -> List[str]:
    if len(label) <= LABEL_MAX_CHARS:
        return [label]
    if " document" in label:
        head, tail = label.split(" document", 1)
        return [head.rstrip(), f"document{tail}"]
    words = label.split()
    lines: List[str] = []
    cur: List[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if len(trial) > LABEL_MAX_CHARS and cur:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines[:2]


def _box_svg(
    x: float,
    y: float,
    label: str,
    style: str,
    *,
    box_w: Optional[float] = None,
    box_h: Optional[float] = None,
    font_size: Optional[int] = None,
) -> str:
    w = box_w if box_w is not None else BOX_W
    h = box_h if box_h is not None else BOX_H
    fs = font_size if font_size is not None else FONT_SIZE
    st = STYLES[style]
    cx = x + w / 2
    lines = _wrap_box_label(label)
    ty0 = y + (h - len(lines) * LINE_H) / 2 + LINE_H - 3
    text_lines = []
    for i, line in enumerate(lines):
        text_lines.append(
            f"<text x='{cx:.1f}' y='{ty0 + i * LINE_H:.1f}' text-anchor='middle' "
            f"font-family='{FONT}' font-size='{fs}' fill='{st['color']}'>"
            f"{_xml(line)}</text>"
        )
    return "\n".join(
        [
            f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{BOX_RX}' "
            f"fill='{st['fill']}' stroke='{st['stroke']}' stroke-width='1.75'/>",
            *text_lines,
        ]
    )


def _connector(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    dashed: bool = False,
    stroke: Optional[str] = None,
    width: Optional[float] = None,
) -> str:
    """Thin line only — no arrowheads (exec-diagram style)."""
    dash = " stroke-dasharray='4,4'" if dashed else ""
    s = stroke or ARROW
    w = width if width is not None else ARROW_WIDTH
    return (
        f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
        f"stroke='{s}' stroke-width='{w}' stroke-linecap='round'{dash}/>"
    )


def _svg_defs() -> str:
    return (
        f"<defs><marker id='{GUIDE_MARKER}' viewBox='0 0 10 10' refX='9' refY='5' "
        f"markerWidth='8' markerHeight='8' orient='auto'>"
        f"<path d='M 0 0 L 10 5 L 0 10 z' fill='{GUIDE_COLOR}'/></marker></defs>"
    )


def _flow_arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return _connector(x1, y1, x2, y2, stroke=FLOW_ARROW, width=FLOW_ARROW_WIDTH)


def _guided_arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
        f"stroke='{GUIDE_COLOR}' stroke-width='{GUIDE_WIDTH}' stroke-linecap='round' "
        f"marker-end='url(#{GUIDE_MARKER})'/>"
    )


def _step_badge(cx: float, cy: float, label: str) -> str:
    r = 12.0
    return (
        f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='#FFFFFF' "
        f"stroke='{GUIDE_COLOR}' stroke-width='2'/>"
        f"<text x='{cx:.1f}' y='{cy + 4.5:.1f}' text-anchor='middle' font-family='{FONT}' "
        f"font-size='12' font-weight='bold' fill='{GUIDE_COLOR}'>{_xml(label)}</text>"
    )


def _lane_outline(band_x: float, y0: float, band_w: float, band_h: float) -> str:
    """Orange bounding box on my-lane column — no duplicate label (band below owns title)."""
    pad = 5.0
    return (
        f"<rect x='{band_x - pad:.1f}' y='{y0 - pad:.1f}' "
        f"width='{band_w + 2 * pad:.1f}' height='{band_h + 2 * pad:.1f}' rx='10' "
        f"fill='none' stroke='#EF6C00' stroke-width='2'/>"
    )


def _h_connector(x_left_end: float, x_right_start: float, y: float) -> str:
    x1 = x_left_end + LINE_STUB
    x2 = x_right_start - LINE_STUB
    if x2 <= x1 + 2:
        return ""
    return _connector(x1, y, x2, y)


def _v_connector(y_top_end: float, y_bottom_start: float, x: float, *, dashed: bool = False) -> str:
    y1 = y_top_end + LINE_STUB
    y2 = y_bottom_start - LINE_STUB
    if y2 <= y1 + 2:
        return ""
    return _connector(x, y1, x, y2, dashed=dashed)


def _sg_band(x: float, y: float, w: float, h: float, title: str) -> str:
    return (
        f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{SG_RX}' "
        f"fill='{SG_FILL}' stroke='{SG_BORDER}' stroke-width='1'/>"
        f"<text x='{x + 12:.1f}' y='{y + 16:.1f}' font-family='{FONT}' font-size='{FONT_SIZE_SG}' "
        f"fill='{SG_TITLE_COLOR}'>{_xml(title)}</text>"
    )


def _wrap_svg(inner: str) -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{FRAME_W:.0f}' height='{FRAME_H:.0f}' "
        f"viewBox='0 0 {FRAME_W:.0f} {FRAME_H:.0f}'>{_svg_defs()}{inner}</svg>"
    )


def _compose(
    arrows: List[str],
    shapes: List[str],
    backgrounds: Optional[List[str]] = None,
    foreground: Optional[List[str]] = None,
) -> str:
    bg = backgrounds or []
    fg = foreground or []
    return "\n".join([*bg, *shapes, *arrows, *fg])


def _slide01_content_size() -> Tuple[float, float]:
    slide = _a3().slide(1)
    groups = slide.stack_groups
    if not groups:
        raise ValueError("Slide 1 needs *group* blocks in manager-arch-vision-a3.md")
    program = groups[0][1]
    dri = groups[1][1] if len(groups) > 1 else []

    def band_size(nodes: Sequence[Tuple[str, str]]) -> Tuple[float, float]:
        inner_w = len(nodes) * BOX_W + max(0, len(nodes) - 1) * H_GAP_SLIDE1
        return inner_w + SG_PAD * 2, SG_TITLE_H + SG_PAD + BOX_H + SG_PAD

    p_w, p_h = band_size(program)
    total_right = MARGIN + p_w
    total_bottom = MARGIN + p_h
    if dri:
        d_w, d_h = band_size(dri)
        total_right = max(total_right, MARGIN + d_w)
        total_bottom = MARGIN + p_h + BAND_GAP + d_h
    return total_right + MARGIN, total_bottom + MARGIN


def _ensure_unified_scale() -> float:
    global UNIFIED_SCALE
    if UNIFIED_SCALE is not None:
        return UNIFIED_SCALE
    cw, ch = _slide01_content_size()
    avail_w = FRAME_W - 2 * FRAME_PAD
    avail_h = FRAME_H - 2 * FRAME_PAD
    UNIFIED_SCALE = min(TARGET_SCALE, avail_w / cw, avail_h / ch)
    return UNIFIED_SCALE


def _resolve_scale(content_w: float, content_h: float, *, fill_height: bool = False) -> float:
    avail_w = FRAME_W - 2 * FRAME_PAD
    avail_h = FRAME_H - 2 * FRAME_PAD
    if fill_height:
        return min(avail_h / max(content_h, 1), avail_w / max(content_w, 1))
    return _ensure_unified_scale()


def _frame(parts: str, content_w: float, content_h: float, *, fill_height: bool = False) -> str:
    """Unified scale keeps box size consistent across slides."""
    s = _resolve_scale(content_w, content_h, fill_height=fill_height)
    sw, sh = content_w * s, content_h * s
    tx = (FRAME_W - sw) / 2
    ty = (FRAME_H - sh) / 2
    inner = f"<g transform='translate({tx:.1f},{ty:.1f}) scale({s:.4f})'>{parts}</g>"
    return _wrap_svg(inner)


def _hrow(
    nodes: Sequence[Tuple[str, str]],
    x0: float,
    y: float,
    arrows: List[str],
    shapes: List[str],
    h_gap: float = H_GAP,
    *,
    box_w: float = BOX_W,
    box_h: float = BOX_H,
    font_size: int = FONT_SIZE,
) -> float:
    x = x0
    prev_right: Optional[float] = None
    cy = y + box_h / 2
    for label, style in nodes:
        shapes.append(
            _box_svg(x, y, label, style, box_w=box_w, box_h=box_h, font_size=font_size)
        )
        if prev_right is not None:
            a = _h_connector(prev_right, x, cy)
            if a:
                arrows.append(a)
        prev_right = x + box_w
        x += box_w + h_gap
    return x - h_gap


def _hband(
    nodes: Sequence[Tuple[str, str]],
    x0: float,
    y: float,
    title: str,
    arrows: List[str],
    shapes: List[str],
    backgrounds: List[str],
    h_gap: float = H_GAP,
) -> Tuple[float, float]:
    inner_w = len(nodes) * BOX_W + max(0, len(nodes) - 1) * h_gap
    band_w = inner_w + SG_PAD * 2
    band_h = SG_TITLE_H + SG_PAD + BOX_H + SG_PAD
    backgrounds.append(_sg_band(x0, y, band_w, band_h, title))
    row_y = y + SG_TITLE_H + SG_PAD
    _hrow(nodes, x0 + SG_PAD, row_y, arrows, shapes, h_gap=h_gap)
    return x0 + band_w, y + band_h


def _column_layout(
    columns: Sequence[Tuple[str, str, str, Sequence[str]]],
    *,
    row_gap: float = ROW_GAP,
    deliverable_ci: Optional[int] = None,
) -> Tuple[List[str], List[str], List[str], float, float, Dict[str, Tuple[float, float, float]]]:
    col_inner_w = BOX_W + SG_PAD * 2
    row_unit = BOX_H + row_gap
    col_heights = [
        SG_TITLE_H + SG_PAD + len(labels) * BOX_H + max(0, len(labels) - 1) * row_gap + SG_PAD
        for _, _, _, labels in columns
    ]
    total_w = len(columns) * col_inner_w + max(0, len(columns) - 1) * COL_GAP
    backgrounds: List[str] = []
    arrows: List[str] = []
    shapes: List[str] = []
    anchors: Dict[str, Tuple[float, float, float]] = {}
    y0 = MARGIN
    col_bottoms: List[float] = []

    for ci, (key, title, style, labels) in enumerate(columns):
        col_h = col_heights[ci]
        cx = MARGIN + ci * (col_inner_w + COL_GAP) + SG_PAD
        band_x = cx - SG_PAD
        backgrounds.append(_sg_band(band_x, y0, col_inner_w, col_h, title))
        node_y = y0 + SG_TITLE_H + SG_PAD
        prev_bottom: Optional[float] = None
        mid_x = cx + BOX_W / 2
        for label in labels:
            shapes.append(_box_svg(cx, node_y, label, style))
            anchors[f"{key}:{label}"] = (mid_x, node_y, node_y + BOX_H)
            if prev_bottom is not None:
                a = _v_connector(prev_bottom, node_y, mid_x)
                if a:
                    arrows.append(a)
            prev_bottom = node_y + BOX_H
            node_y += row_unit
        col_bottoms.append(y0 + col_h)
        if deliverable_ci is not None and ci == deliverable_ci:
            shapes.append(_lane_outline(band_x, y0, col_inner_w, col_h))

    layout_bottom = max(col_bottoms)
    return backgrounds, arrows, shapes, total_w + MARGIN, layout_bottom, anchors


def _diamond_parts(cx: float, cy: float, label: str) -> Tuple[str, List[str]]:
    h = GATE_HALF
    st = STYLES["gate"]
    side = h * math.sqrt(2)
    half = side / 2
    fill = (
        f"<rect x='{cx - half:.1f}' y='{cy - half:.1f}' width='{side:.1f}' height='{side:.1f}' "
        f"transform='rotate(45 {cx:.1f} {cy:.1f})' fill='{st['fill']}' stroke='{st['stroke']}' "
        f"stroke-width='2' stroke-linejoin='round'/>"
        f"<text x='{cx:.1f}' y='{cy + 4:.1f}' text-anchor='middle' font-family='{FONT}' "
        f"font-size='{FONT_SIZE}' fill='{st['color']}'>{_xml(label)}</text>"
    )
    return fill, []


def render_slide01() -> str:
    slide = _a3().slide(1)
    groups = slide.stack_groups
    if not groups:
        raise ValueError("Slide 1 needs *group* blocks in manager-arch-vision-a3.md")
    backgrounds: List[str] = []
    arrows: List[str] = []
    shapes: List[str] = []
    program = groups[0][1]
    dri = groups[1][1] if len(groups) > 1 else []

    p_right, p_bottom = _hband(
        program, MARGIN, MARGIN, groups[0][0], arrows, shapes, backgrounds, h_gap=H_GAP_SLIDE1
    )
    total_right = p_right
    total_bottom = p_bottom
    if dri:
        d_right, d_bottom = _hband(
            dri,
            MARGIN,
            p_bottom + BAND_GAP,
            groups[1][0],
            arrows,
            shapes,
            backgrounds,
            h_gap=H_GAP_SLIDE1,
        )
        total_right = max(p_right, d_right)
        total_bottom = d_bottom

    return _frame(
        _compose(arrows, shapes, backgrounds),
        total_right + MARGIN,
        total_bottom + MARGIN,
    )


def _col_keys(n: int) -> List[str]:
    return (["bar", "lane", "peer", "col4"])[:n]


def _compass_band(
    band_title: str,
    nodes: Sequence[Tuple[str, str]],
    band_x: float,
    band_y: float,
    shapes: List[str],
    backgrounds: List[str],
) -> Tuple[float, float]:
    """Four quadrant boxes inside one band — prefetch org framing (no N/E/W/S labels)."""
    inner_w = COMPASS_BOX_W * 3 + COMPASS_ARM * 2
    inner_h = COMPASS_BOX_H * 3 + COMPASS_ARM * 2
    band_w = inner_w + COMPASS_BAND_PAD * 2
    band_h = inner_h + SG_TITLE_H + COMPASS_BAND_PAD * 2
    backgrounds.append(_sg_band(band_x, band_y, band_w, band_h, band_title))

    cx = band_x + band_w / 2
    cy = band_y + SG_TITLE_H + COMPASS_BAND_PAD + inner_h / 2
    positions = {
        "north": (cx - COMPASS_BOX_W / 2, cy - COMPASS_BOX_H - COMPASS_ARM),
        "south": (cx - COMPASS_BOX_W / 2, cy + COMPASS_ARM),
        "west": (cx - COMPASS_BOX_W - COMPASS_ARM, cy - COMPASS_BOX_H / 2),
        "east": (cx + COMPASS_ARM, cy - COMPASS_BOX_H / 2),
    }
    for label, quadrant in nodes:
        q = quadrant.strip().lower()
        pos = positions.get(q)
        if not pos:
            continue
        style = QUADRANT_STYLE.get(q, "program")
        shapes.append(
            _box_svg(
                pos[0],
                pos[1],
                label,
                style,
                box_w=COMPASS_BOX_W,
                box_h=COMPASS_BOX_H,
                font_size=FONT_SIZE_SG,
            )
        )
        if q == "south":
            pad = 4.0
            shapes.append(
                f"<rect x='{pos[0] - pad:.1f}' y='{pos[1] - pad:.1f}' "
                f"width='{COMPASS_BOX_W + 2 * pad:.1f}' height='{COMPASS_BOX_H + 2 * pad:.1f}' "
                f"rx='8' fill='none' stroke='#EF6C00' stroke-width='2'/>"
            )
    return band_w, band_h


def _slide02_read_guides(
    n_cols: int,
    y0: float,
    col_bottom: float,
    gate_cx: float,
    gate_top: float,
    yes_cx: float,
    split_y: float,
    out_y: float,
    total_w: float,
) -> List[str]:
    """Numbered arrows — columns L→R (1), down to Aligned (2), yes walk (3)."""
    col_inner_w = BOX_W + SG_PAD * 2
    guides: List[str] = []

    guides.append(
        f"<text x='{MARGIN:.1f}' y='{y0 + 11:.1f}' font-family='{FONT}' font-size='{FONT_SIZE_NOTE}' "
        f"fill='{GUIDE_COLOR}' font-weight='bold'>Read order</text>"
    )
    guides.append(
        f"<text x='{total_w - MARGIN - 168:.1f}' y='{y0 + 11:.1f}' font-family='{FONT}' "
        f"font-size='{FONT_SIZE_NOTE}' fill='{GUIDE_COLOR}'>1 columns · 2 aligned · 3 walk</text>"
    )

    flow_y = y0 + SG_TITLE_H + 6
    first_col_right = MARGIN + col_inner_w
    guides.append(_step_badge(MARGIN + col_inner_w / 2, flow_y - 22, "1"))
    for i in range(n_cols - 1):
        x_left = MARGIN + i * (col_inner_w + COL_GAP) + col_inner_w - 10
        x_right = MARGIN + (i + 1) * (col_inner_w + COL_GAP) + 10
        guides.append(_guided_arrow(x_left, flow_y, x_right, flow_y))

    step2_mid = (col_bottom + gate_top) / 2
    guides.append(_step_badge(gate_cx - 24, step2_mid, "2"))
    guides.append(_guided_arrow(gate_cx, col_bottom + 4, gate_cx, gate_top - 4))

    step3_mid_y = (split_y + out_y) / 2
    step3_mid_x = (gate_cx + yes_cx) / 2
    guides.append(_step_badge(step3_mid_x, step3_mid_y - 14, "3"))
    guides.append(_guided_arrow(gate_cx, split_y + 8, yes_cx, out_y - 10))

    return guides


def _gate_tree(
    gate_cx: float,
    gate_cy: float,
    gate_h: float,
    sources: Sequence[Tuple[float, float, bool]],
    yes_cx: float,
    no_cx: float,
    out_y: float,
    arrows: List[str],
    *,
    deemphasize_no: bool = False,
) -> None:
    """Orthogonal connectors — never diagonals across diamond corners."""
    top_y = gate_cy - gate_h
    left_x = gate_cx - gate_h
    right_x = gate_cx + gate_h
    bus_y = top_y - 16
    join_pad = 6.0

    for sx, sy, dashed in sources:
        if abs(sx - gate_cx) < 3:
            arrows.append(_v_connector(sy, top_y - join_pad, gate_cx, dashed=dashed))
        elif sx < gate_cx:
            arrows.append(_v_connector(sy, bus_y, sx, dashed=dashed))
            arrows.append(_connector(sx, bus_y, left_x - join_pad, bus_y, dashed=dashed))
            arrows.append(_connector(left_x - join_pad, bus_y, left_x - join_pad, gate_cy, dashed=dashed))
        else:
            arrows.append(_v_connector(sy, bus_y, sx, dashed=dashed))
            arrows.append(_connector(sx, bus_y, right_x + join_pad, bus_y, dashed=dashed))
            arrows.append(_connector(right_x + join_pad, bus_y, right_x + join_pad, gate_cy, dashed=dashed))

    bot_y = gate_cy + gate_h
    split_y = bot_y + 14
    arrows.append(_v_connector(bot_y, split_y, gate_cx))
    arrows.append(_connector(gate_cx, split_y, yes_cx, split_y))
    arrows.append(_v_connector(split_y, out_y, yes_cx))
    if not deemphasize_no:
        arrows.append(_connector(gate_cx, split_y, no_cx, split_y))
        arrows.append(_v_connector(split_y, out_y, no_cx))
    else:
        arrows.append(_connector(gate_cx, split_y, no_cx, split_y, dashed=True, stroke=FLOW_ARROW))
        arrows.append(_v_connector(split_y, out_y, no_cx, dashed=True))


def render_slide02() -> str:
    slide = _a3().slide(2)
    cols = [
        (_col_keys(len(slide.columns))[i], title, style, labels)
        for i, (title, style, labels) in enumerate(slide.columns)
    ]
    y0 = MARGIN
    backgrounds, arrows, shapes, w, col_bottom, anchors = _column_layout(
        cols, row_gap=ROW_GAP_SLIDE2, deliverable_ci=1
    )

    gate_cx = MARGIN + (BOX_W + SG_PAD * 2) + COL_GAP + SG_PAD + BOX_W / 2
    gate_cy = col_bottom + GATE_HALF + 16
    gate_top = gate_cy - GATE_HALF
    diamond_fill, _ = _diamond_parts(gate_cx, gate_cy, slide.gate or "Aligned")
    foreground: List[str] = [diamond_fill]

    tape_x, _, tape_bot = anchors["bar:Tape-out path"]
    bc_x, _, bc_bot = anchors["lane:Buffer carving"]
    peer_labels = slide.columns[2][2] if len(slide.columns) > 2 else []
    peer_key = peer_labels[-1] if peer_labels else "ECMP"
    ec_x, _, ec_bot = anchors[f"peer:{peer_key}"]

    out_y = gate_cy + GATE_HALF + 40
    yes_cx = gate_cx - 118
    no_cx = gate_cx + 98
    split_y = gate_cy + GATE_HALF + 14
    read_guides = _slide02_read_guides(
        len(cols), y0, col_bottom, gate_cx, gate_top, yes_cx, split_y, out_y, w
    )

    foreground.append(
        _box_svg(
            yes_cx - YES_BOX_W / 2,
            out_y,
            slide.branch_yes or "QoS buffer carving arch",
            "act",
            box_w=YES_BOX_W,
            box_h=YES_BOX_H,
            font_size=FONT_SIZE,
        )
    )
    foreground.append(
        _box_svg(
            no_cx - BOX_W / 2,
            out_y,
            slide.branch_no or "Reframe task",
            "muted",
        )
    )
    foreground.append(
        f"<text x='{yes_cx - 36:.0f}' y='{out_y - 6:.0f}' font-family='{FONT}' "
        f"font-size='{FONT_SIZE_NOTE}' fill='#556677'>yes</text>"
    )

    _gate_tree(
        gate_cx,
        gate_cy,
        GATE_HALF,
        [(tape_x, tape_bot, False), (bc_x, bc_bot, False), (ec_x, ec_bot, True)],
        yes_cx,
        no_cx,
        out_y,
        arrows,
        deemphasize_no=True,
    )

    total_h = out_y + YES_BOX_H + MARGIN
    total_w = w
    if slide.compass and slide.deliverable_band:
        inner_w = COMPASS_BOX_W * 3 + COMPASS_ARM * 2
        band_w = inner_w + COMPASS_BAND_PAD * 2
        band_h = inner_w + SG_TITLE_H + COMPASS_BAND_PAD * 2
        band_x = max(MARGIN, (max(w, band_w + 2 * MARGIN) - band_w) / 2)
        band_y = out_y + YES_BOX_H + COMPASS_BELOW_GATE
        _compass_band(slide.deliverable_band, slide.compass, band_x, band_y, shapes, backgrounds)
        total_h = band_y + band_h + MARGIN
        total_w = max(w, band_w + 2 * MARGIN)

    return _frame(
        _compose(arrows, shapes, backgrounds, [*foreground, *read_guides]),
        total_w,
        total_h,
        fill_height=True,
    )


def _spread_gap(n: int, box_w: float) -> Tuple[float, float]:
    """Size boxes and gap to span the diagram frame width."""
    pad = FRAME_PAD
    avail_w = FRAME_W - 2 * pad
    if n <= 1:
        return box_w, 0.0
    gap = (avail_w - n * box_w) / (n - 1)
    if gap >= MIN_SPREAD_GAP:
        return box_w, gap
    box_w = (avail_w - (n - 1) * MIN_SPREAD_GAP) / n
    return box_w, MIN_SPREAD_GAP


def _hstack_spread(nodes: Sequence[Tuple[str, str]]) -> str:
    """Slides 3–4: larger boxes, gaps computed to fill width and vertical band."""
    n = len(nodes)
    box_w, gap = _spread_gap(n, BOX_W_SPREAD)
    box_h = BOX_H_SPREAD
    content_h = box_h + 2 * SPREAD_V_PAD
    y = SPREAD_V_PAD
    arrows: List[str] = []
    shapes: List[str] = []
    _hrow(
        nodes,
        FRAME_PAD,
        y,
        arrows,
        shapes,
        gap,
        box_w=box_w,
        box_h=box_h,
        font_size=FONT_SIZE_SPREAD,
    )
    return _frame(_compose(arrows, shapes), FRAME_W, content_h, fill_height=True)


def render_slide03() -> str:
    return _hstack_spread(_a3().slide(3).stack)


def render_slide04() -> str:
    return _hstack_spread(_a3().slide(4).stack)


_SLIDE_RENDERERS = {
    1: render_slide01,
    2: render_slide02,
    3: render_slide03,
    4: render_slide04,
}


def diagram_stems_for_doc(doc=None) -> List[str]:
    doc = doc or _a3()
    return [s.diagram for s in doc.ordered_slides() if s.diagram]


def _render_for_stem(stem: str, doc=None) -> str:
    doc = doc or _a3()
    for s in doc.ordered_slides():
        if s.diagram == stem:
            fn = _SLIDE_RENDERERS.get(s.number)
            if not fn:
                raise ValueError(f"No renderer for slide {s.number} (diagram {stem!r})")
            return fn()
    raise ValueError(f"Diagram {stem!r} not declared in {A3_MD.name}")


def _svg_to_png(svg: str, png: Path, scale: float = 2.5) -> None:
    import fitz

    png.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
    try:
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        pix.save(str(png))
    finally:
        doc.close()


def render_all_diagrams(png_dir: Path, doc=None) -> None:
    """Render in slide order so slide 1 sets UNIFIED_SCALE for every diagram."""
    global UNIFIED_SCALE
    UNIFIED_SCALE = None
    doc = doc or _a3()
    for stem in diagram_stems_for_doc(doc):
        render_diagram(stem, png_dir / f"{stem}.png", doc=doc, _skip_scale_reset=True)


def render_diagram(stem: str, png: Path, doc=None, *, _skip_scale_reset: bool = False) -> None:
    if not _skip_scale_reset:
        global UNIFIED_SCALE
        UNIFIED_SCALE = None
    svg = _render_for_stem(stem, doc=doc)
    _svg_to_png(svg, png)
    if not png.is_file() or png.stat().st_size < 100:
        raise RuntimeError(f"Diagram render produced no output: {png}")
