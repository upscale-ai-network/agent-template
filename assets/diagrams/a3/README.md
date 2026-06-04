# A3 diagrams

| Source | PNG | Slide |
|--------|-----|-------|
| `slide00-cover.mmd` | `.png` | Cover — Thu flow |
| `slide01-scope.mmd` | `.png` | 1 — DSBM + program bar |
| `slide02-validated.mmd` | `.png` | 2 — done and validated |
| `slide03-outcomes.mmd` | `.png` | 3 — What you get |
| `slide04-sponsor.mmd` | `.png` | 4 — Sponsor asks |

**Render:** `uv run python scripts/render-a3-diagrams.py` (also runs at start of `build-dt100-decks.py`).

**Tooling:** `./node_modules/.bin/mmdc` (after `npm install`) → best quality; else Pillow parser fallback.

Edit `.mmd` → regen PNG → regen pptx.
