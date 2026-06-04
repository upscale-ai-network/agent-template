#!/usr/bin/env python3
"""
Render assets/diagrams/a3/*.mmd → PNG for A3 pptx build.

Tries mmdc if installed; otherwise parses simple flowchart LR Mermaid and emits SVG → PNG (cairosvg).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
MMD_DIR = ROOT / "assets" / "diagrams" / "a3"
NODE = Path("/Applications/Cursor.app/Contents/Resources/app/resources/helpers/node")

# Upscale-adjacent palette (readable on white slides)
DEFAULT_FILL = "#F5F7FA"
DEFAULT_STROKE = "#051830"
DEFAULT_TEXT = "#051830"


@dataclass
class Node:
    nid: str
    label: str
    subgraph: Optional[str] = None


@dataclass
class Edge:
    src: str
    dst: str
    label: Optional[str] = None
    dashed: bool = False


@dataclass
class Diagram:
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    classes: Dict[str, Dict[str, str]] = field(default_factory=dict)
    node_class: Dict[str, str] = field(default_factory=dict)
    subgraph_titles: Dict[str, str] = field(default_factory=dict)
    node_order: List[str] = field(default_factory=list)


def _parse_classdef(line: str, diagram: Diagram) -> None:
    m = re.match(
        r"classDef\s+(\w+)\s+fill:(#[0-9A-Fa-f]+),stroke:(#[0-9A-Fa-f]+)(?:,color:(#[0-9A-Fa-f]+))?",
        line,
    )
    if m:
        name, fill, stroke, color = m.group(1), m.group(2), m.group(3), m.group(4)
        diagram.classes[name] = {
            "fill": fill,
            "stroke": stroke,
            "color": color or DEFAULT_TEXT,
        }


def _parse_class(line: str, diagram: Diagram) -> None:
    m = re.match(r"class\s+([\w,\s]+)\s+(\w+)", line)
    if m:
        for nid in re.split(r"[\s,]+", m.group(1).strip()):
            if nid:
                diagram.node_class[nid] = m.group(2)


def _parse_node_id(token: str) -> Tuple[str, str]:
    token = token.strip()
    m = re.match(r"(\w+)(?:\{([^}]+)\}|\[([^\]]+)\])", token)
    if not m:
        return token, token
    nid = m.group(1)
    label = (m.group(2) or m.group(3) or nid).replace("\\n", "\n")
    return nid, label


def _parse_edge(line: str, diagram: Diagram) -> None:
    dashed = "-.->" in line or "-.-" in line
    arrow = "-->" if "-->" in line else "-.->"
    parts = re.split(r"\|([^|]+)\|\s*" + re.escape(arrow), line)
    label = None
    if len(parts) >= 3:
        label = parts[1].strip()
        left, right = parts[0].strip(), parts[-1].strip()
    else:
        left, _, right = line.partition(arrow)
        left, right = left.strip(), right.strip()
    src_tok = left.split()[-1] if left.startswith("subgraph") else left
    dst_tok = right.split()[0]
    src, slabel = _parse_node_id(src_tok)
    dst, dlabel = _parse_node_id(dst_tok)
    _ensure_node(diagram, src, slabel)
    _ensure_node(diagram, dst, dlabel)
    diagram.edges.append(Edge(src, dst, label, dashed))


def _ensure_node(diagram: Diagram, nid: str, label: str) -> None:
    if nid not in diagram.nodes:
        diagram.nodes[nid] = Node(nid, label, diagram.nodes.get(nid, Node(nid, label)).subgraph)
        diagram.node_order.append(nid)
    else:
        diagram.nodes[nid].label = label


def parse_mermaid(text: str) -> Diagram:
    diagram = Diagram()
    current_subgraph: Optional[str] = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        if line.startswith("flowchart"):
            continue
        if line == "direction LR":
            continue
        if line.startswith("classDef"):
            _parse_classdef(line, diagram)
            continue
        if line.startswith("class "):
            _parse_class(line, diagram)
            continue
        if line.startswith("subgraph"):
            m = re.match(r'subgraph\s+(\w+)(?:\["([^"]+)"\]|\[([^\]]+)\])?', line)
            if m:
                current_subgraph = m.group(1)
                title = m.group(2) or m.group(3) or current_subgraph
                diagram.subgraph_titles[current_subgraph] = title
            continue
        if line == "end":
            current_subgraph = None
            continue
        if "-->" in line or "-.->" in line or "-.-" in line:
            _parse_edge(line, diagram)
            continue
        m = re.match(r"(\w+)(?:\{([^}]+)\}|\[([^\]]+)\])", line)
        if m:
            nid, label = _parse_node_id(line.split()[0] if " " not in line else line)
            _ensure_node(diagram, nid, label)
            if current_subgraph:
                diagram.nodes[nid].subgraph = current_subgraph
    return diagram


def _node_style(diagram: Diagram, nid: str) -> Dict[str, str]:
    cname = diagram.node_class.get(nid)
    if cname and cname in diagram.classes:
        return diagram.classes[cname]
    return {"fill": DEFAULT_FILL, "stroke": DEFAULT_STROKE, "color": DEFAULT_TEXT}


def _wrap_label(label: str, max_chars: int = 18) -> List[str]:
    lines: List[str] = []
    for part in label.split("\n"):
        words = part.split()
        cur: List[str] = []
        for w in words:
            trial = " ".join(cur + [w])
            if len(trial) > max_chars and cur:
                lines.append(" ".join(cur))
                cur = [w]
            else:
                cur.append(w)
        if cur:
            lines.append(" ".join(cur))
    return lines or [label]


def layout(diagram: Diagram) -> Dict[str, Tuple[float, float, float, float]]:
    """Return node id -> x, y, w, h."""
    subgraph_ids = list(dict.fromkeys(n.subgraph for n in diagram.nodes.values() if n.subgraph))
    loose = [n.nid for n in diagram.nodes.values() if not n.subgraph]
    positions: Dict[str, Tuple[float, float, float, float]] = {}
    row_y = 40.0
    box_w, box_h, gap_x, gap_y = 200.0, 72.0, 36.0, 120.0

    def place_row(nids: List[str], y: float, x0: float = 40.0) -> float:
        x = x0
        max_h = box_h
        for nid in nids:
            lines = _wrap_label(diagram.nodes[nid].label)
            h = max(box_h, 22 + 16 * len(lines))
            positions[nid] = (x, y, box_w, h)
            max_h = max(max_h, h)
            x += box_w + gap_x
        return y + max_h + gap_y

    ordered_sub = subgraph_ids or []
    for sg in ordered_sub:
        nids = [n.nid for n in diagram.nodes.values() if n.subgraph == sg]
        if not nids:
            continue
        row_y = place_row(nids, row_y + 28)
    if loose:
        row_y = place_row(loose, row_y)
    # nodes only on edges
    for e in diagram.edges:
        for nid in (e.src, e.dst):
            if nid not in positions:
                row_y = place_row([nid], row_y)
    return positions


def render_svg(diagram: Diagram) -> str:
    pos = layout(diagram)
    max_x = max((p[0] + p[2] for p in pos.values()), default=800)
    max_y = max((p[1] + p[3] for p in pos.values()), default=400)
    w, h = max_x + 60, max_y + 60
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">',
        "<defs><marker id='arrow' markerWidth='10' markerHeight='8' refX='9' refY='4' "
        "orient='auto'><path d='M0,0 L10,4 L0,8 z' fill='#455A64'/></marker></defs>",
    ]
    # subgraph bands
    by_sg: Dict[str, List[str]] = {}
    for nid, node in diagram.nodes.items():
        if node.subgraph:
            by_sg.setdefault(node.subgraph, []).append(nid)
    for sg, nids in by_sg.items():
        xs = [pos[n][0] for n in nids if n in pos]
        ys = [pos[n][1] for n in nids if n in pos]
        ws = [pos[n][0] + pos[n][2] for n in nids if n in pos]
        hs = [pos[n][1] + pos[n][3] for n in nids if n in pos]
        if not xs:
            continue
        x0, y0, x1, y1 = min(xs) - 16, min(ys) - 32, max(ws) + 16, max(hs) + 12
        title = diagram.subgraph_titles.get(sg, sg)
        parts.append(
            f"<rect x='{x0}' y='{y0}' width='{x1-x0}' height='{y1-y0}' rx='8' "
            f"fill='#FAFAFA' stroke='#B0BEC5' stroke-width='1'/>"
        )
        parts.append(
            f"<text x='{x0+12}' y='{y0+18}' font-family='Arial,sans-serif' font-size='13' "
            f"fill='#556677'>{_xml(title)}</text>"
        )
    for e in diagram.edges:
        if e.src not in pos or e.dst not in pos:
            continue
        x1, y1, w1, h1 = pos[e.src]
        x2, y2, w2, h2 = pos[e.dst]
        sx, sy = x1 + w1, y1 + h1 / 2
        ex, ey = x2, y2 + h2 / 2
        dash = "stroke-dasharray='6,4'" if e.dashed else ""
        parts.append(
            f"<line x1='{sx}' y1='{sy}' x2='{ex}' y2='{ey}' stroke='#455A64' "
            f"stroke-width='2' marker-end='url(#arrow)' {dash}/>"
        )
    for nid, (x, y, bw, bh) in pos.items():
        st = _node_style(diagram, nid)
        parts.append(
            f"<rect x='{x}' y='{y}' width='{bw}' height='{bh}' rx='6' "
            f"fill='{st['fill']}' stroke='{st['stroke']}' stroke-width='2'/>"
        )
        lines = _wrap_label(diagram.nodes[nid].label)
        ty = y + 20
        for line in lines:
            parts.append(
                f"<text x='{x + bw/2}' y='{ty}' text-anchor='middle' "
                f"font-family='Arial,sans-serif' font-size='12' fill='{st['color']}'>"
                f"{_xml(line)}</text>"
            )
            ty += 16
    parts.append("</svg>")
    return "\n".join(parts)


def _xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _mmdc_candidates() -> List[Path]:
    root = Path(__file__).resolve().parents[1]
    local = root / "node_modules" / ".bin" / "mmdc"
    out: List[Path] = []
    if local.is_file():
        out.append(local)
    found = shutil.which("mmdc")
    if found:
        out.append(Path(found))
    return out


def try_mmdc(mmd: Path, png: Path) -> bool:
    for mmdc in _mmdc_candidates():
        try:
            subprocess.run(
                [str(mmdc), "-i", str(mmd), "-o", str(png), "-b", "white", "-w", "2400"],
                check=True,
                timeout=120,
            )
            if png.is_file():
                return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def render_png_pillow(diagram: Diagram, png: Path, scale: float = 3.0) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pos = layout(diagram)
    max_x = max((p[0] + p[2] for p in pos.values()), default=800)
    max_y = max((p[1] + p[3] for p in pos.values()), default=400)
    w, h = int((max_x + 60) * scale), int((max_y + 60) * scale)
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", int(12 * scale))
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", int(11 * scale))
        font_sg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", int(13 * scale))
    except OSError:
        font = font_sm = font_sg = ImageFont.load_default()

    def rect(nid, fill, stroke, width=2):
        x, y, bw, bh = pos[nid]
        x, y, bw, bh = x * scale, y * scale, bw * scale, bh * scale
        draw.rounded_rectangle([x, y, x + bw, y + bh], radius=int(6 * scale), fill=fill, outline=stroke, width=width)

    for e in diagram.edges:
        if e.src not in pos or e.dst not in pos:
            continue
        x1, y1, w1, h1 = pos[e.src]
        x2, y2, w2, h2 = pos[e.dst]
        sx, sy = (x1 + w1) * scale, (y1 + h1 / 2) * scale
        ex, ey = x2 * scale, (y2 + h2 / 2) * scale
        draw.line([sx, sy, ex, ey], fill="#455A64", width=int(2 * scale))
        draw.polygon(
            [(ex, ey), (ex - 10 * scale, ey - 4 * scale), (ex - 10 * scale, ey + 4 * scale)],
            fill="#455A64",
        )

    for nid, (x, y, bw, bh) in pos.items():
        st = _node_style(diagram, nid)
        rect(nid, st["fill"], st["stroke"])
        lines = _wrap_label(diagram.nodes[nid].label)
        ty = y * scale + 18 * scale
        for line in lines:
            draw.text((x * scale + bw * scale / 2, ty), line, fill=st["color"], font=font, anchor="mm")
            ty += 16 * scale

    png.parent.mkdir(parents=True, exist_ok=True)
    img.save(png, "PNG")


def render_png(mmd: Path, png: Path) -> None:
    if try_mmdc(mmd, png):
        return
    text = mmd.read_text(encoding="utf-8")
    diagram = parse_mermaid(text)
    try:
        import cairosvg

        svg = render_svg(diagram)
        png.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png), output_width=2400)
    except (ImportError, OSError):
        render_png_pillow(diagram, png)


def main() -> int:
    if not MMD_DIR.is_dir():
        print(f"Missing {MMD_DIR}", file=sys.stderr)
        return 1
    mmds = sorted(MMD_DIR.glob("*.mmd"))
    if not mmds:
        print("No .mmd files", file=sys.stderr)
        return 1
    for mmd in mmds:
        png = mmd.with_suffix(".png")
        render_png(mmd, png)
        print(f"OK: {png.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
