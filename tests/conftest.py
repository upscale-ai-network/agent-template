import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
CANARY_MD = FIXTURES / "workflow-canary.md"
CANARY_DIAGRAMS = FIXTURES / "diagrams" / "canary"
CANARY_OUT_DIR = ROOT / "tests" / "output"


def has_npx() -> bool:
    return shutil.which("npx") is not None


def has_uv() -> bool:
    return shutil.which("uv") is not None


workflow = pytest.mark.workflow
artifact_parity = pytest.mark.artifact_parity
requires_npx = pytest.mark.skipif(not has_npx(), reason="npx required for mermaid render")
requires_uv = pytest.mark.skipif(not has_uv(), reason="uv required")


@pytest.fixture
def canary_paths(tmp_path):
    """Isolated diagram dir + output pptx per test (avoids cross-test pollution)."""
    diagram_dir = tmp_path / "diagrams"
    diagram_dir.mkdir()
    for mmd in CANARY_DIAGRAMS.glob("*.mmd"):
        (diagram_dir / mmd.name).write_text(mmd.read_text(encoding="utf-8"), encoding="utf-8")
    config = CANARY_DIAGRAMS / "mermaid-config.json"
    if config.is_file():
        (diagram_dir / "mermaid-config.json").write_text(
            config.read_text(encoding="utf-8"), encoding="utf-8"
        )
    md_path = tmp_path / "canary.md"
    md_path.write_text(CANARY_MD.read_text(encoding="utf-8"), encoding="utf-8")
    out_pptx = tmp_path / "canary.pptx"
    return md_path, diagram_dir, out_pptx
