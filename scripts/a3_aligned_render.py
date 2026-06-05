"""Aligned A3 diagram renderer — reads labels from manager-arch-vision-a3.md."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from deck_from_md import A3_MD, load_deck_md


def _a3():
    return load_deck_md(A3_MD, a3_cover_fields=True)

# Upscale palette (match assets/diagrams/a3/_classes.mmd)
STYLES: Dict[str, Dict[str, str]] = {
    "program": {"fill": "#E3F2FD", "stroke": "#1565C0", "color": "#051830"},
    "lane": {"fill": "#FFF3E0", "stroke": "#EF6C00", "color": "#051830"},
    "peer": {"fill": "#ECEFF1", "stroke": "#455A64", "color": "#051830"},
    "gate": {"fill": "#F3E5F5", "stroke": "#7B1FA2", "color": "#051830"},
    "step": {"fill": "#E8F5E9", "stroke": "#2E7D32", "color": "#051830"},
    "doc": {"fill": "#E3F2FD", "stroke": "#1565C0", "color": "#051830"},
    "ask": {"fill": "#FFF3E0", "stroke": "#EF6C00", "color": "#051830"},
    "act": {"fill": "#F3E5F5", "stroke": "#7B1FA2", "color": "#051830"},
}

BOX_W = 200
BOX_H = 46
ROW_GAP = 30
COL_GAP = 52
SG_PAD = 14
SG_TITLE_H = 22
FONT = "Arial, Helvetica, sans-serif"
FONT_SIZE = 13
ARROW = "#455A64"
SG_BORDER = "#B0BEC5"
SG_FILL = "#FAFAFA"
SG_TITLE_COLOR = "#556677"


def _xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _box_svg(x: float, y: float, label: str, style: str) -> str:
    st = STYLES[style]
    parts = [
        f"<rect x='{x:.1f}' y='{y:.1f}' width='{BOX_W}' height='{BOX_H}' rx='6' "
        f"fill='{st['fill']}' stroke='{st['stroke']}' stroke-width='2'/>",
        f"<text x='{x + BOX_W / 2:.1f}' y='{y + BOX_H / 2 + 5:.1f}' text-anchor='middle' "
        f"font-family='{FONT}' font-size='{FONT_SIZE}' fill='{st['color']}'>"
        f"{_xml(label)}</text>",
    ]
    return "\n".join(parts)


def _arrow_v(x: float, y1: float, y2: float, dashed: bool = False) -> str:
    dash = " stroke-dasharray='6,4'" if dashed else ""
    return (
        f"<line x1='{x:.1f}' y1='{y1:.1f}' x2='{x:.1f}' y2='{y2:.1f}' "
        f"stroke='{ARROW}' stroke-width='2' marker-end='url(#arrow)'{dash}/>"
    )


def _arrow_diag(x1: float, y1: float, x2: float, y2: float, dashed: bool = False) -> str:
    dash = " stroke-dasharray='6,4'" if dashed else ""
    return (
        f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
        f"stroke='{ARROW}' stroke-width='2' marker-end='url(#arrow)'{dash}/>"
    )


def _diamond(cx: float, cy: float, label: str, half: float = 52) -> Tuple[str, float, float, float, float]:
    pts = f"{cx},{cy - half} {cx + half},{cy} {cx},{cy + half} {cx - half},{cy}"
    st = STYLES["gate"]
    svg = (
        f"<polygon points='{pts}' fill='{st['fill']}' stroke='{st['stroke']}' stroke-width='2'/>"
        f"<text x='{cx:.1f}' y='{cy + 5:.1f}' text-anchor='middle' font-family='{FONT}' "
        f"font-size='{FONT_SIZE}' fill='{st['color']}'>{_xml(label)}</text>"
    )
    return svg, cx - half, cy - half, half * 2, half * 2


def _sg_band(x: float, y: float, w: float, h: float, title: str) -> str:
    return (
        f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='8' "
        f"fill='{SG_FILL}' stroke='{SG_BORDER}' stroke-width='1'/>"
        f"<text x='{x + 12:.1f}' y='{y + 18:.1f}' font-family='{FONT}' font-size='12' "
        f"fill='{SG_TITLE_COLOR}'>{_xml(title)}</text>"
    )


def _wrap_svg(inner: str, w: float, h: float) -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w:.0f}' height='{h:.0f}' "
        f"viewBox='0 0 {w:.0f} {h:.0f}'>"
        "<defs><marker id='arrow' markerWidth='10' markerHeight='8' refX='9' refY='4' "
        "orient='auto'><path d='M0,0 L10,4 L0,8 z' fill='#455A64'/></marker></defs>"
        f"{inner}</svg>"
    )


def _column_layout(
    columns: Sequence[Tuple[str, str, str, Sequence[str]]],
) -> Tuple[str, float, float, Dict[str, Tuple[float, float]]]:
    """Top-aligned columns; returns svg, width, height, node centers."""
    col_inner_w = BOX_W + SG_PAD * 2
    max_rows = max(len(nodes) for _, _, _, nodes in columns)
    col_h = SG_TITLE_H + SG_PAD + max_rows * BOX_H + (max_rows - 1) * ROW_GAP + SG_PAD
    total_w = len(columns) * col_inner_w + (len(columns) - 1) * COL_GAP
    parts: List[str] = []
    centers: Dict[str, Tuple[float, float]] = {}
    y0 = 8.0

    for ci, (key, title, style, labels) in enumerate(columns):
        cx = 8 + ci * (col_inner_w + COL_GAP) + SG_PAD
        band_x = cx - SG_PAD
        parts.append(_sg_band(band_x, y0, col_inner_w, col_h, title))
        node_y = y0 + SG_TITLE_H + SG_PAD
        prev_bottom = None
        for label in labels:
            parts.append(_box_svg(cx, node_y, label, style))
            centers[f"{key}:{label}"] = (cx + BOX_W / 2, node_y + BOX_H / 2)
            if prev_bottom is not None:
                parts.append(_arrow_v(cx + BOX_W / 2, prev_bottom, node_y))
            prev_bottom = node_y + BOX_H
            node_y += BOX_H + ROW_GAP

    return "\n".join(parts), total_w + 16, col_h + y0 + 16, centers


def render_slide01() -> str:
    slide = _a3().slide(1)
    groups = slide.stack_groups
    if not groups:
        raise ValueError("Slide 1 needs *group* blocks in manager-arch-vision-a3.md")
    w = BOX_W + 48
    x = 24.0
    y = 16.0
    parts: List[str] = []
    sg_h = lambda n: SG_TITLE_H + SG_PAD + n * BOX_H + (n - 1) * ROW_GAP + SG_PAD
    h1 = sg_h(len(groups[0][1]))
    h2 = sg_h(len(groups[1][1])) if len(groups) > 1 else 0
    parts.append(_sg_band(x - SG_PAD, y, BOX_W + SG_PAD * 2, h1, groups[0][0]))
    if len(groups) > 1:
        parts.append(_sg_band(x - SG_PAD, y + h1 + 24, BOX_W + SG_PAD * 2, h2, groups[1][0]))
    program = groups[0][1]
    dri = groups[1][1] if len(groups) > 1 else []
    cy = y + SG_TITLE_H + SG_PAD
    prev = None
    for label, style in program:
        parts.append(_box_svg(x, cy, label, style))
        if prev is not None:
            parts.append(_arrow_v(x + BOX_W / 2, prev, cy))
        prev = cy + BOX_H
        cy += BOX_H + ROW_GAP
    cy2 = y + h1 + 24 + SG_TITLE_H + SG_PAD
    parts.append(_arrow_v(x + BOX_W / 2, prev, cy2))
    prev2 = None
    for label, style in dri:
        parts.append(_box_svg(x, cy2, label, style))
        if prev2 is not None:
            parts.append(_arrow_v(x + BOX_W / 2, prev2, cy2))
        prev2 = cy2 + BOX_H
        cy2 += BOX_H + ROW_GAP
    total_h = y + h1 + 24 + h2 + 24
    return _wrap_svg("\n".join(parts), w, total_h)


def _col_keys(n: int) -> List[str]:
    defaults = ["bar", "lane", "peer", "col4"]
    return defaults[:n]


def render_slide02() -> str:
    slide = _a3().slide(2)
    cols = [
        (_col_keys(len(slide.columns))[i], title, style, labels)
        for i, (title, style, labels) in enumerate(slide.columns)
    ]
    inner, w, h_top, centers = _column_layout(cols)
    parts = [inner]
    gate_y = h_top + 20
    gate_cx = 8 + (BOX_W + SG_PAD * 2) + COL_GAP + SG_PAD + BOX_W / 2  # center column
    dia, _, _, _, _ = _diamond(gate_cx, gate_y + 52, slide.gate or "Aligned?")
    parts.append(dia)

    def bottom(key: str, label: str) -> Tuple[float, float]:
        cx, cy = centers[f"{key}:{label}"]
        return cx, cy + BOX_H / 2

    tape_x, tape_y = bottom("bar", "Tape-out path")
    bc_x, bc_y = bottom("lane", "Buffer carving")
    ec_x, ec_y = bottom("peer", "ECMP")
    gate_top = gate_y
    parts.append(_arrow_diag(tape_x, tape_y, gate_cx - 20, gate_top))
    parts.append(_arrow_v(bc_x, bc_y, gate_top))
    parts.append(_arrow_diag(ec_x, ec_y, gate_cx + 20, gate_top, dashed=True))

    out_y = gate_y + 110
    yes_x, no_x = gate_cx - 150, gate_cx + 70
    parts.append(_box_svg(yes_x - BOX_W / 2, out_y, slide.branch_yes or "Pipeline walk", "gate"))
    parts.append(_box_svg(no_x - BOX_W / 2, out_y, slide.branch_no or "Fix slides 1–2", "gate"))
    parts.append(
        f"<text x='{gate_cx - 70:.0f}' y='{out_y - 8:.0f}' font-family='{FONT}' font-size='11' "
        f"fill='#556677'>yes</text>"
    )
    parts.append(
        f"<text x='{gate_cx + 55:.0f}' y='{out_y - 8:.0f}' font-family='{FONT}' font-size='11' "
        f"fill='#556677'>no</text>"
    )
    gate_bot = gate_y + 104
    parts.append(_arrow_diag(gate_cx - 15, gate_bot, yes_x, out_y))
    parts.append(_arrow_diag(gate_cx + 15, gate_bot, no_x, out_y))

    total_h = out_y + BOX_H + 24
    total_w = w + 80
    return _wrap_svg("\n".join(parts), total_w, total_h)


def render_slide03() -> str:
    return _stack(_a3().slide(3).stack, 24)


def render_slide04() -> str:
    return _stack(_a3().slide(4).stack, 24)


def _stack(nodes: Sequence[Tuple[str, str]], margin: float) -> str:
    x = margin
    y = margin
    parts: List[str] = []
    prev = None
    for label, style in nodes:
        parts.append(_box_svg(x, y, label, style))
        if prev is not None:
            parts.append(_arrow_v(x + BOX_W / 2, prev, y))
        prev = y + BOX_H
        y += BOX_H + ROW_GAP
    return _wrap_svg("\n".join(parts), BOX_W + margin * 2, y + margin)


RENDERERS = {
    "slide01-scope": render_slide01,
    "slide02-validated": render_slide02,
    "slide03-outcomes": render_slide03,
    "slide04-sponsor": render_slide04,
}


def _svg_to_png(svg: str, png: Path, scale: float = 2.5) -> None:
    """Rasterize SVG via PyMuPDF (repo dep) or cairosvg when available."""
    png.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fitz

        doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        pix.save(str(png))
        doc.close()
        return
    except Exception:
        pass
    import cairosvg

    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png), output_width=2400)


def render_aligned_png(stem: str, png: Path) -> bool:
    fn = RENDERERS.get(stem)
    if not fn:
        return False
    _svg_to_png(fn(), png)
    return True
