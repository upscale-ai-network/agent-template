"""Shared diagram render — Mermaid via npx mmdc."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]
MMDC_PKG = "@mermaid-js/mermaid-cli@11.15.0"
DEFAULT_CONFIG = ROOT / "assets" / "diagrams" / "b6" / "mermaid-config.json"


def require_npx() -> str:
    npx = shutil.which("npx")
    if not npx:
        raise RuntimeError("npx not on PATH")
    return npx


def render_mermaid_diagram(
    diagram_dir: Path,
    stem: str,
    *,
    mmd_name: Optional[str] = None,
    config_path: Optional[Path] = None,
    width: int = 1800,
    height: int = 900,
) -> Path:
    """Render one .mmd file to {stem}.png under diagram_dir."""
    mmd_name = mmd_name or f"{stem}.mmd"
    mmd = diagram_dir / mmd_name
    out = diagram_dir / f"{stem}.png"
    if not mmd.is_file():
        raise FileNotFoundError(f"Missing mermaid source: {mmd}")
    diagram_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_path if config_path is not None else DEFAULT_CONFIG
    cmd = [
        require_npx(),
        "--yes",
        MMDC_PKG,
        "-i",
        str(mmd),
        "-o",
        str(out),
        "-b",
        "white",
        "-w",
        str(width),
        "-H",
        str(height),
    ]
    if config_path.is_file():
        cmd.extend(["-c", str(config_path)])
    subprocess.run(cmd, check=True, cwd=ROOT)
    return out


def render_stems_from_dir(
    diagram_dir: Path,
    stems: List[str],
    *,
    config_path: Optional[Path] = None,
) -> List[Path]:
    """Render each stem using {stem}.mmd in diagram_dir."""
    paths: List[Path] = []
    for stem in stems:
        paths.append(
            render_mermaid_diagram(diagram_dir, stem, config_path=config_path)
        )
    return paths
