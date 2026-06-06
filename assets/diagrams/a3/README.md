# A3 diagrams

Diagrams are **not** built from Mermaid. Labels and layout come from `dt100/qos-architecture-diwakar-tundlam.md`; PNGs are rendered by `scripts/a3_aligned_render.py` (PyMuPDF).

| PNG | Slide | Md section |
|-----|-------|------------|
| `slide01-scope.png` | 1 | DSBM + program bar |
| `slide02-validated.png` | 2 | done and validated |
| `slide03-outcomes.png` | 3 | What you get |
| `slide04-sponsor.png` | 4 | Sponsor asks |

**Build:** `./scripts/run-deck-build.sh` — validates md, renders PNGs, builds pptx, validates output. Fails on any missing field, renderer, or corrupt file.

**Diagram-only render:** `uv run python scripts/render_a3_diagrams.py`

**Legacy:** `legacy-mermaid/` holds old `.mmd` sources — not used by the build.

Edit `qos-architecture-diwakar-tundlam.md` → rebuild.
