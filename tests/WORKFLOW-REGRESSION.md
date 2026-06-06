# Workflow pipeline regression

**Task:** DT125 · **Fixture:** `tests/fixtures/workflow-canary.md` (never SharePoint)

## Test catalog

| ID | Tier | What it proves |
|----|------|----------------|
| TC01 | fast | Canary md parses — cover + 3 slides + diagram stems |
| TC02 | fast | Diagram stems extracted correctly |
| TC08 | fast | Missing `.mmd` fails loud (no silent skip) |
| TC03 | workflow | Mermaid → PNG valid (size, PIL open) |
| TC04 | workflow | Full build — slide count, markers on-slide |
| TC05 | workflow | Md-only title change regen without re-touching mmd/png |
| TC06 | workflow | Duplicate slide in md → slide count +1 |
| TC07 | workflow | Mmd color change → PNG bytes change |
| TC10 | workflow | Idempotent rebuild — stable slide count |
| TC09 | workflow | Production `check-decks` still passes |

**Planned (your directed torture):** watermark, arrow style, box resize, slide reorder — add TC11+ as you request changes.

## Run

```bash
uv sync --group dev

# Fast only (~1s)
uv run pytest tests/test_workflow_pipeline.py -m "not workflow" -q

# Full pipeline (needs npx; ~30–60s first mmdc pull)
uv run pytest tests/test_workflow_pipeline.py -m workflow -q

# Everything
uv run pytest tests/ -q
```

## Future git gate (DT119)

Pre-commit / CI blocker target:

```bash
uv run pytest tests/ -m workflow -q
```

Zombie vm1: fast tier + `check-decks` only (PNG committed; no npx required).

## Change recipes

| Change | Edit | Regen |
|--------|------|-------|
| Title / lead / bullets | `*.md` | `uv run build-decks` (B6 diagrams cached) |
| Box color / arrows | `*.mmd` | `uv run build-decks` (re-renders mmd) |
| Pipeline overlay | `render_b6_diagrams.py` coords | `uv run build-decks` |
| New slide | new `## Slide N` in md + diagram | full build |
| Duplicate slide | copy slide section in md | full build |

Kit: `scripts/workflow_testkit.py` · render: `scripts/deck_render.py`
