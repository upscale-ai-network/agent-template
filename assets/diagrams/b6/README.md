# B6 diagrams (DT122)

Sources for `dt122/bugatti-qos-ccc.md` → `bugatti-qos-ccc.pptx`.

| PNG stem | Source |
|----------|--------|
| `b6-slide01-process-ribbon` | Mermaid |
| `b6-slide02-validation-stack` | Mermaid |
| `b6-slide03-pipeline-annotated` | Pillow overlay on `logical-pipeline-boss-slide.png` |
| `b6-slide04-csb-inset` | Mermaid |
| `b6-slide05-gate-alignment` | Mermaid |
| `b6-slide06-boundaries` | Mermaid |
| `b6-slide07-next-steps` | Mermaid |

**Render:** `uv run python scripts/render_b6_diagrams.py` (or `uv run build-decks`)

**Requires:** `npx` + network on primary (Mac); committed PNGs let zombie litmus skip render.

Palette matches A3 (`#E3F2FD` program · `#EF6C00` lane).
