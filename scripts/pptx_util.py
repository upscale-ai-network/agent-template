"""Safe PPTX helpers — avoid duplicate layout parts; preserve Upscale text colors."""

from copy import deepcopy
from typing import List, Optional

from pptx import Presentation
from pptx.dml.color import RGBColor

# CCC deck colors (from slide XML)
COLOR_GOLD = RGBColor(0xFF, 0xE1, 0x9E)  # navy panel callout
COLOR_NAVY_TITLE = RGBColor(0x05, 0x18, 0x30)  # content slide title
COLOR_BODY = RGBColor(0x00, 0x00, 0x00)  # white panel / body
RIGHT_PANEL_LEFT = 5_000_000  # EMU — shapes on navy background
FOOTER_TOP = 4_800_000


def delete_slide(prs: Presentation, index: int) -> None:
    """Remove slide at index from presentation."""
    slides = prs.slides._sldIdLst
    r_id = slides[index].rId
    prs.part.drop_rel(r_id)
    del slides[index]


def trim_to_slides(prs: Presentation, keep_indices: list) -> None:
    """Delete all slides whose index is not in keep_indices (0-based)."""
    keep = set(keep_indices)
    for i in range(len(prs.slides) - 1, -1, -1):
        if i not in keep:
            delete_slide(prs, i)


def duplicate_slide(prs: Presentation, index: int):
    """
    Duplicate slide within the same presentation (shapes + image rels).
    Reuses existing layout part — does not corrupt the package like repeated add_slide.
    """
    source = prs.slides[index]
    layout = source.slide_layout
    dest = prs.slides.add_slide(layout)

    for shape in source.shapes:
        newel = deepcopy(shape.element)
        dest.shapes._spTree.insert_element_before(newel, "p:extLst")

    return dest


def is_footer(shape) -> bool:
    return shape.top > FOOTER_TOP


def _apply_run_color(paragraph, rgb: RGBColor) -> None:
    for run in paragraph.runs:
        run.font.color.rgb = rgb


def set_shape_single_line(shape, text: str, rgb: Optional[RGBColor] = None) -> None:
    """Replace one line of text without resetting to black on navy."""
    if rgb is None:
        rgb = COLOR_GOLD if shape.left >= RIGHT_PANEL_LEFT else COLOR_BODY
    tf = shape.text_frame
    if tf.paragraphs and tf.paragraphs[0].runs:
        tf.paragraphs[0].runs[0].text = text
        for run in tf.paragraphs[0].runs[1:]:
            run.text = ""
        for para in tf.paragraphs[1:]:
            for run in para.runs:
                run.text = ""
        _apply_run_color(tf.paragraphs[0], rgb)
    else:
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        _apply_run_color(p, rgb)


def fill_text_frame_lines(text_frame, lines: List[str], rgb: RGBColor) -> None:
    text_frame.clear()
    for i, line in enumerate(lines):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = line
        p.level = 0
        _apply_run_color(p, rgb)


def fill_cover_slide(slide, headline: str, subline: str, meta: str, tag: str) -> None:
    for shape in slide.shapes:
        if not shape.has_text_frame or is_footer(shape):
            continue
        raw = shape.text_frame.text
        if "Mirror CCC" in raw:
            set_shape_single_line(shape, headline, COLOR_BODY)
        elif "Bugatti" in raw and "Mirror" not in raw:
            set_shape_single_line(shape, subline, COLOR_GOLD)
        elif raw.strip().startswith("Authors:"):
            set_shape_single_line(shape, meta, COLOR_BODY)
        elif "Hardware/Architecture" in raw:
            set_shape_single_line(shape, tag, COLOR_BODY)


def fill_content_slide(
    slide,
    title: str,
    bullets: List[str],
    subtitle: Optional[str] = None,
) -> None:
    title_shape = None
    body_shape = None
    for shape in slide.shapes:
        if not shape.has_text_frame or is_footer(shape):
            continue
        if shape.top < 700_000:
            title_shape = shape
        else:
            body_shape = shape
    if title_shape:
        set_shape_single_line(title_shape, title, COLOR_NAVY_TITLE)
    if body_shape:
        lines: List[str] = []
        if subtitle:
            lines.extend([subtitle, ""])
        lines.extend(bullets)
        fill_text_frame_lines(body_shape.text_frame, lines, COLOR_BODY)


def check_zip_duplicates(path) -> list:
    """Return duplicate member names in pptx zip (empty = OK)."""
    import zipfile
    from collections import Counter

    with zipfile.ZipFile(path) as z:
        counts = Counter(z.namelist())
        return [n for n, c in counts.items() if c > 1]
