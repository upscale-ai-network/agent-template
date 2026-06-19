"""Load test layer definitions from tests/layers.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

_LAYERS = Path(__file__).resolve().parent / "layers.yaml"


def load_layers(path: Path | None = None) -> dict:
    return yaml.safe_load((path or _LAYERS).read_text(encoding="utf-8"))


def breadth_nodeids(path: Path | None = None) -> list[str]:
    data = load_layers(path)
    raw = data["layers"]["breadth"]["tests"]
    return [f"tests/{node}" if not node.startswith("tests/") else node for node in raw]
