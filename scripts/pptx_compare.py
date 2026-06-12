"""Stable PPTX content comparison — ignores volatile docProps timestamps."""

from __future__ import annotations

import hashlib
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

# docProps timestamps change on every save; slide XML + embedded media are stable.
_VOLATILE_PARTS = frozenset({"docProps/core.xml", "docProps/app.xml"})


@dataclass(frozen=True)
class PptxContentFingerprint:
    slide_count: int
    slide_texts: Tuple[Tuple[str, ...], ...]
    media_hashes: Tuple[Tuple[str, str], ...]
    xml_hashes: Tuple[Tuple[str, str], ...]

    def as_tuple(self) -> tuple:
        return (
            self.slide_count,
            self.slide_texts,
            self.media_hashes,
            self.xml_hashes,
        )


def fingerprint_pptx(path: Path) -> PptxContentFingerprint:
    """Content fingerprint — slide text, embedded media, non-volatile XML."""
    if not path.is_file():
        raise FileNotFoundError(path)

    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)
        )
        slide_texts: List[Tuple[str, ...]] = []
        for name in slide_names:
            xml = zf.read(name).decode("utf-8", errors="replace")
            runs = tuple(re.findall(r"<a:t[^>]*>([^<]*)</a:t>", xml))
            slide_texts.append(runs)

        media_hashes: List[Tuple[str, str]] = []
        for name in sorted(n for n in zf.namelist() if n.startswith("ppt/media/")):
            digest = hashlib.sha256(zf.read(name)).hexdigest()
            media_hashes.append((Path(name).name, digest))

        xml_hashes: List[Tuple[str, str]] = []
        for name in sorted(zf.namelist()):
            if not name.endswith(".xml"):
                continue
            if name in _VOLATILE_PARTS or name.startswith("ppt/media/"):
                continue
            xml_hashes.append((name, hashlib.sha256(zf.read(name)).hexdigest()))

    return PptxContentFingerprint(
        slide_count=len(slide_names),
        slide_texts=tuple(slide_texts),
        media_hashes=tuple(media_hashes),
        xml_hashes=tuple(xml_hashes),
    )


def diff_pptx_content(reference: Path, candidate: Path) -> List[str]:
    """Return human-readable diffs; empty list means content matches."""
    ref = fingerprint_pptx(reference)
    cand = fingerprint_pptx(candidate)
    diffs: List[str] = []

    if ref.slide_count != cand.slide_count:
        diffs.append(
            f"slide count: reference {ref.slide_count} vs candidate {cand.slide_count}"
        )

    for i, (rt, ct) in enumerate(zip(ref.slide_texts, cand.slide_texts), start=1):
        if rt != ct:
            diffs.append(f"slide {i} text differs (reference {len(rt)} runs, candidate {len(ct)} runs)")

    if len(ref.slide_texts) != len(cand.slide_texts):
        diffs.append(
            f"slide text blocks: reference {len(ref.slide_texts)} vs candidate {len(cand.slide_texts)}"
        )

    if ref.media_hashes != cand.media_hashes:
        ref_map = dict(ref.media_hashes)
        cand_map = dict(cand.media_hashes)
        for name in sorted(set(ref_map) | set(cand_map)):
            if ref_map.get(name) != cand_map.get(name):
                diffs.append(f"media {name}: content hash mismatch")

    if ref.xml_hashes != cand.xml_hashes:
        ref_map = dict(ref.xml_hashes)
        cand_map = dict(cand.xml_hashes)
        for name in sorted(set(ref_map) | set(cand_map)):
            if ref_map.get(name) != cand_map.get(name):
                diffs.append(f"xml {name}: structure/content mismatch")

    return diffs


def assert_pptx_content_equal(
    reference: Path,
    candidate: Path,
    *,
    label: str = "pptx",
) -> None:
    """Raise AssertionError when regenerated deck drifts from committed copy."""
    diffs = diff_pptx_content(reference, candidate)
    if diffs:
        lines = [f"{label}: regenerated content does not match {reference.name}:"]
        lines.extend(f"  - {d}" for d in diffs)
        lines.append(
            "Hint: run `uv run build-decks` and commit md/png/pptx together, "
            "or fix the build pipeline."
        )
        raise AssertionError("\n".join(lines))
