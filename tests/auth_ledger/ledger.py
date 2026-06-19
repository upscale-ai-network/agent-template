"""Parse AUTH-LEDGER.md (names only)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = _REPO_ROOT / "AUTH-LEDGER.md"


@dataclass(frozen=True)
class LedgerHost:
    number: int
    name: str
    notes: str


_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$")


def load_ledger(path: Path | None = None) -> list[LedgerHost]:
    text = (path or LEDGER_PATH).read_text(encoding="utf-8")
    hosts: list[LedgerHost] = []
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if not m:
            continue
        num, name, notes = m.group(1), m.group(2).strip(), m.group(3).strip()
        if name.lower() == "name":
            continue
        hosts.append(LedgerHost(int(num), name, notes))
    if not hosts:
        raise ValueError(f"No hosts parsed from {path or LEDGER_PATH}")
    return hosts
