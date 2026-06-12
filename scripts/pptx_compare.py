"""Stable PPTX content comparison — ignores volatile docProps timestamps."""

from __future__ import annotations

import hashlib
import json
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


def content_sha256(path: Path) -> str:
    """Stable SHA256 over slide text, embedded media, and non-volatile XML."""
    fp = fingerprint_pptx(path)
    payload = json.dumps(fp.as_tuple(), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_md5(path: Path) -> str:
    """Raw file MD5 — informational only; zip timestamps make this unstable across regen."""
    return hashlib.md5(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class PublishedDeckHash:
    deck_key: str
    md_source: str
    content_sha256: str
    bytes_md5: str = ""


def load_published_hashes(path: Path) -> Dict[str, PublishedDeckHash]:
    """Parse tests/fixtures/published-deck-hashes.txt."""
    entries: Dict[str, PublishedDeckHash] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            raise ValueError(f"invalid published hash line: {line!r}")
        deck_key, md_source, digest = parts[:3]
        bytes_md5 = parts[3] if len(parts) > 3 else ""
        entries[deck_key] = PublishedDeckHash(
            deck_key=deck_key,
            md_source=md_source,
            content_sha256=digest,
            bytes_md5=bytes_md5,
        )
    return entries


def write_published_hashes(path: Path, entries: List[PublishedDeckHash]) -> None:
    lines = [
        "# Published deck content regression (stable SHA256 of slide text + media + XML).",
        "# Raw zip MD5 differs on every rebuild; CI compares content_sha256 only.",
        "# Refresh: uv run python scripts/pptx_compare.py --update-published-hashes",
        "",
    ]
    for e in entries:
        row = f"{e.deck_key}\t{e.md_source}\t{e.content_sha256}"
        if e.bytes_md5:
            row += f"\t{e.bytes_md5}"
        lines.append(row)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def published_hash_errors(
    built: Dict[str, Path],
    hashes_file: Path,
) -> List[str]:
    """Return validation errors when built pptx content SHA256 drifts from golden file."""
    if not hashes_file.is_file():
        return [f"Missing published hash fixture: {hashes_file}"]

    golden = load_published_hashes(hashes_file)
    errors: List[str] = []
    for deck_key, path in built.items():
        if deck_key not in golden:
            errors.append(f"No golden content hash for deck {deck_key!r}")
            continue
        if not path.is_file():
            errors.append(f"Built deck missing for hash check: {path}")
            continue
        expected = golden[deck_key]
        actual = content_sha256(path)
        if actual != expected.content_sha256:
            errors.append(
                f"{deck_key} content SHA256 drift ({expected.md_source}): "
                f"expected {expected.content_sha256}, got {actual}. "
                "If intentional publish: "
                "`uv run python scripts/pptx_compare.py --update-published-hashes`"
            )
    return errors


def _main() -> int:
    import argparse

    root = Path(__file__).resolve().parents[1]
    default_hashes = root / "tests" / "fixtures" / "published-deck-hashes.txt"
    parser = argparse.ArgumentParser(description="Compare or fingerprint PPTX decks.")
    parser.add_argument("reference", nargs="?", type=Path, help="Reference pptx")
    parser.add_argument("candidate", nargs="?", type=Path, help="Candidate pptx")
    parser.add_argument(
        "--update-published-hashes",
        action="store_true",
        help="Regen A3/B6 from md and rewrite published-deck-hashes.txt",
    )
    parser.add_argument("--hashes-file", type=Path, default=default_hashes)
    args = parser.parse_args()

    if args.update_published_hashes:
        import sys

        sys.path.insert(0, str(root / "scripts"))
        from workflow_testkit import build_production_a3_isolated, build_production_b6_isolated

        import tempfile

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            specs = [
                ("a3", "dt100/bugatti-qos-architecture.md", build_production_a3_isolated),
                ("b6", "dt122/bugatti-qos-ccc.md", build_production_b6_isolated),
            ]
            entries: List[PublishedDeckHash] = []
            for deck_key, md_source, builder in specs:
                pptx = builder(td_path / deck_key)
                entries.append(
                    PublishedDeckHash(
                        deck_key=deck_key,
                        md_source=md_source,
                        content_sha256=content_sha256(pptx),
                        bytes_md5=file_md5(pptx),
                    )
                )
        write_published_hashes(args.hashes_file, entries)
        for e in entries:
            print(f"{e.deck_key}\t{e.content_sha256}\tbytes_md5={e.bytes_md5}")
        print(f"Wrote {args.hashes_file}")
        return 0

    if not args.reference or not args.candidate:
        parser.error("reference and candidate pptx required unless --update-published-hashes")

    diffs = diff_pptx_content(args.reference, args.candidate)
    if diffs:
        for d in diffs:
            print(d)
        return 1
    print("content match")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
