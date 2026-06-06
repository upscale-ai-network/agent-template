"""Parse dt100 manager-arch-vision-*.md deck files (shared slide / notes format)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CoverSlide:
    title: str = ""
    subtitle: str = ""
    meta: str = ""
    tag: str = ""
    # A3-specific cover fields
    left_title: str = ""
    left_subtitle: str = ""
    right_lines: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class DeckSlide:
    number: int
    title: str = ""
    subtitle: str = ""
    lead: str = ""
    bullets: List[str] = field(default_factory=list)
    notes: str = ""
    diagram: str = ""
    image: str = ""
    caption: str = ""
    # A3 diagram layout (optional)
    stack: List[Tuple[str, str]] = field(default_factory=list)
    stack_groups: List[Tuple[str, List[Tuple[str, str]]]] = field(default_factory=list)
    columns: List[Tuple[str, str, List[str]]] = field(default_factory=list)
    gate: str = ""
    branch_yes: str = ""
    branch_no: str = ""
    deliverable_band: str = ""
    compass: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class DeckDocument:
    path: Path
    cover: CoverSlide = field(default_factory=CoverSlide)
    slides: Dict[int, DeckSlide] = field(default_factory=dict)
    extra_notes: Dict[str, str] = field(default_factory=dict)

    def slide(self, n: int) -> DeckSlide:
        if n not in self.slides:
            raise KeyError(f"Slide {n} missing in {self.path.name}")
        return self.slides[n]

    def ordered_slides(self) -> List[DeckSlide]:
        return [self.slides[k] for k in sorted(self.slides)]


def _parse_field(line: str) -> Optional[Tuple[str, str]]:
    m = re.match(r"\*\*([^*]+):\*\*\s*(.*)", line.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None


def _section_kind(title: str) -> Optional[str | int]:
    t = title.strip().lower()
    if t == "cover":
        return "cover"
    m = re.match(r"slide\s*(\d+)", t, re.I)
    if m:
        return int(m.group(1))
    m = re.match(r"before\s+slide\s*(\d+)", t, re.I)
    if m:
        return f"before-{m.group(1)}"
    if "into" in t and ("pipeline" in t or "walk" in t):
        return "into-pipeline"
    if "after" in t and ("pipeline" in t or "walk" in t):
        return "after-pipeline"
    return None


def _parse_node(line: str) -> Optional[Tuple[str, str]]:
    line = line.strip()
    if not line.startswith("- "):
        return None
    body = line[2:].strip()
    if "|" in body:
        label, style = [p.strip() for p in body.split("|", 1)]
        return label, style
    return body, "program"


def load_deck_md(
    path: Path,
    *,
    stop_at_reference: bool = True,
    a3_cover_fields: bool = False,
) -> DeckDocument:
    text = path.read_text(encoding="utf-8")
    doc = DeckDocument(path=path)
    current: Optional[DeckSlide] = None
    section_key: Optional[str | int] = None
    mode: Optional[str] = None
    notes_buf: List[str] = []
    in_notes_fence = False
    group_title: Optional[str] = None
    group_nodes: List[Tuple[str, str]] = []
    col_title: Optional[str] = None
    col_style: Optional[str] = None
    col_labels: List[str] = []

    def flush_notes(target: Optional[DeckSlide] = None, extra_key: Optional[str] = None) -> None:
        nonlocal notes_buf, in_notes_fence
        if not notes_buf:
            return
        body = "\n".join(notes_buf).strip()
        notes_buf = []
        in_notes_fence = False
        if section_key == "cover":
            doc.cover.notes = body
        elif extra_key:
            doc.extra_notes[extra_key] = body
        elif target is not None:
            target.notes = body

    def flush_group() -> None:
        nonlocal group_title, group_nodes
        if current and group_title and group_nodes:
            current.stack_groups.append((group_title, list(group_nodes)))
        group_title = None
        group_nodes = []

    def flush_column() -> None:
        nonlocal col_title, col_style, col_labels
        if current and col_title and col_style is not None:
            current.columns.append((col_title, col_style, list(col_labels)))
        col_title = None
        col_style = None
        col_labels = []

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if stop_at_reference and stripped.lower().startswith("## reference"):
            break

        if stripped.startswith("```notes"):
            flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)
            in_notes_fence = True
            continue
        if stripped == "```" and in_notes_fence:
            flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)
            continue
        if in_notes_fence:
            notes_buf.append(line)
            continue

        if stripped.startswith("## "):
            flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)
            flush_group()
            flush_column()
            mode = None
            new_section = _section_kind(stripped[3:].strip())
            section_key = new_section
            current = None
            if section_key == "cover":
                pass
            elif isinstance(section_key, int):
                current = DeckSlide(number=section_key)
                doc.slides[section_key] = current
            continue

        if not stripped or stripped == "---":
            continue

        field = _parse_field(line)
        if field:
            key, val = field
            if key == "Notes":
                flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)
                in_notes_fence = True
                if val:
                    notes_buf.append(val)
                continue

            flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)

            if section_key == "cover" or (section_key is None and key.startswith("Left")):
                cov = doc.cover
                if a3_cover_fields:
                    if key == "Left title":
                        cov.left_title = val
                    elif key == "Left subtitle":
                        cov.left_subtitle = val
                    elif key == "Right (navy, 3 lines)":
                        cov.right_lines = [p.strip() for p in re.split(r"\s*/\s*", val)]
                    elif key == "Meta":
                        cov.meta = val
                    elif key == "Tag":
                        cov.tag = val
                else:
                    if key == "Title":
                        cov.title = val
                    elif key in ("Subtitle (navy)", "Subtitle"):
                        cov.subtitle = val
                    elif key == "Meta":
                        cov.meta = val
                    elif key == "Tag":
                        cov.tag = val
                continue

            if not isinstance(section_key, int) or not current:
                continue

            if key == "Title":
                current.title = val
            elif key == "Subtitle":
                current.subtitle = val
            elif key == "Lead":
                current.lead = val
            elif key == "Diagram":
                m = re.search(r"slide\d{2}-[\w-]+", val)
                current.diagram = m.group(0) if m else val.split()[0]
            elif key == "Image":
                current.image = val.split("/")[-1].strip()
            elif key == "Caption":
                current.caption = val
            elif key == "Gate":
                current.gate = val
            elif key in ("Branch yes", "Outcome"):
                current.branch_yes = val
            elif key == "Branch no":
                current.branch_no = val
            elif key == "Deliverable band":
                current.deliverable_band = val
            elif key == "On-slide (stack)":
                mode = "stack"
                flush_group()
                flush_column()
            elif key == "On-slide (columns)":
                mode = "columns"
                flush_group()
                flush_column()
            elif key in ("On-slide (compass)", "On-slide (deliverable row)"):
                mode = "compass"
                flush_group()
                flush_column()
            elif key == "Bullets":
                mode = "bullets"
            elif key == "Column":
                flush_column()
                flush_group()
                mode = "columns"
                title_part, _, style_part = val.partition("·")
                col_title = title_part.strip()
                col_style = style_part.strip() if style_part else "program"
                col_labels = []
            continue

        if stripped.startswith("*") and stripped.endswith("*") and current:
            flush_group()
            group_title = stripped.strip("*").strip()
            group_nodes = []
            mode = "stack_groups"
            continue

        node = _parse_node(line)
        if node and current:
            if mode == "stack":
                current.stack.append(node)
            elif mode == "stack_groups":
                group_nodes.append(node)
            elif mode == "columns" and col_title:
                col_labels.append(node[0])
            elif mode == "bullets":
                current.bullets.append(node[0])
            elif mode == "compass":
                current.compass.append(node)
            continue

    flush_notes(current if isinstance(section_key, int) else None, section_key if isinstance(section_key, str) else None)
    flush_group()
    flush_column()
    return doc


A3_MD = ROOT / "dt100" / "manager-arch-vision-a3.md"
B6_MD = ROOT / "dt100" / "manager-arch-vision-b6.md"


def load_b6_md(path: Path = B6_MD) -> DeckDocument:
    return load_deck_md(path, stop_at_reference=True, a3_cover_fields=False)
