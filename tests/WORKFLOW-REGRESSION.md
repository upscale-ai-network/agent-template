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

---

## What the run does (and why ~25s is expected)

A full `uv run pytest tests/ -q` is intentionally **heavy** — it is a end-to-end regression suite, not a unit-test sniff. Wall time (~15–26s on Lepton after `mmdc` is cached) comes from **subprocesses**, **headless diagram rendering**, and **deliberate duplication** of production paths. `time` reporting ~10s user / ~4s system / ~26s total is normal: much of the cost is child processes (uv, npx, node/puppeteer) plus pptx I/O, not Python CPU in the pytest process itself.

### Layer 1 — Fast tests (~1s)

Six tests stay in-process: `hello` / `fib` (uv wiring smoke), **TC01** / **TC02** / **TC08** (parse canary md, extract diagram stems, assert missing `.mmd` raises). These prove the **md contract** without touching disk-heavy artifacts beyond a tmp dir.

Three more “fast” tests are **not** cheap — they shell out to production entry points:

- **`test_check_decks_uv_run`** — spawns `uv run check-decks`, which loads both production decks’ md, validates every committed A3/B6 diagram PNG, opens both pptx files, and checks slide counts. This is the same litmus you run before delivery.
- **`test_build_decks_a3_uv_run`** — spawns `uv run build-decks-a3`, which runs **PyMuPDF** to rasterize four A3 diagrams from `dt100/bugatti-qos-architecture.md`, copies the company template, fills five slides, and writes `dt100/bugatti-qos-architecture.pptx`. That alone is several seconds of render + pptx zip work.

So the “fast” tier is misnamed if you include `test_uv_commands` — only the workflow parse tests are truly sub-second.

### Layer 2 — Workflow tests (~14s, needs `npx`)

Seven tests marked `@workflow` exercise the **canary fixture** in isolated tmp dirs (no pollution of `dt122/`). Each test that renders calls **`npx @mermaid-js/mermaid-cli`** — a Node subprocess that launches headless Chromium, loads the `.mmd`, and writes PNG. First run after boot may pull npm packages (~45s once); cached runs are ~1–2s **per diagram**.

Rough work per test:

| Test | Work |
|------|------|
| TC03 | 2× mmdc (canary slide01 + slide02) |
| TC04 | 2× mmdc + full canary pptx build (template copy, 4 slides, embed PNGs) |
| TC05 | 1× full build with render + 1× build **without** re-render (md-only path) |
| TC06 | 2× mmdc (duplicate reuses slide01 stem) + build with 4 content slides |
| TC07 | 2× mmdc on same stem (before/after color change) — proves png bytes change |
| TC10 | 2× full canary builds back-to-back (idempotency) |
| TC09 | **`check-decks` again** — duplicates production litmus from `test_uv_commands` |

Across the workflow tier you get **roughly 10–14 mmdc invocations** and **4–5 canary pptx builds**, plus **one extra `check-decks`**. That is by design: each test is a **falsifiable stage** (render, build, md-only, duplicate slide, idempotent) rather than one mega-integration test that would be faster but harder to debug.

### Layer 3 — Full suite duplication

Running **everything** (`pytest tests/` without `-m`) executes fast + workflow sequentially. Overlap you pay for:

- **`check-decks` runs twice** (`test_uv_commands` + TC09)
- **`build-decks-a3` runs once** in fast tier (touches production A3 pptx bytes)
- **Canary builds never touch production B6** — tmp paths only

Production B6 (`dt122/bugatti-qos-ccc.pptx`) is validated by `check-decks` but **not rebuilt** on every full pytest unless you also run `uv run build-decks` separately.

### What we are not doing (yet)

- No line-coverage collection (`pytest-cov` not wired)
- No parallel pytest workers (`-n auto`) — would speed wall time but scramble subprocess logs
- No shared session fixture for mmdc — each test gets clean tmp dirs for isolation
- No git gate yet (DT119) — tests are advisory until pre-commit enforces `-m workflow`

### Lighter runs (daily driver)

| Command | ~Time | Use when |
|---------|-------|----------|
| `pytest tests/ -m "not workflow" -q` | ~1s* | After md-only edits (*still runs check-decks + build-a3 if uv_commands included) |
| `uv run check-decks` | ~1s | Quick production litmus |
| `pytest tests/test_workflow_pipeline.py -m workflow -q` | ~14s | After mmd / render / build changes |
| `pytest tests/ -q` | ~15–26s | Pre-push / weekly full regression |

To avoid A3 regen during quick checks, run only workflow + litmus:

```bash
uv run check-decks && uv run pytest tests/test_workflow_pipeline.py -m workflow -q
```

### Future slim-down (DT125 backlog)

- Deduplicate `check-decks` (keep one canonical production litmus test)
- Optional `--stem` render in workflow tests to share PNGs within a session
- Session-scoped mmdc warm-up fixture (one diagram boot, then tests)
- Split `test_uv_commands` into “litmus only” vs “full a3 build” markers
