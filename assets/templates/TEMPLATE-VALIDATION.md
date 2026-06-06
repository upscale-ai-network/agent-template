# Company template validation (Gluon)

**Canonical build file:** `upscale-ccc-style-reference.pptx` — used by `uv run build-decks`.

**Hand-edit seed:** `upscale-company-template.pptx` — duplicate slides in PowerPoint; do not rebuild for every new deck.

---

## Litmus (before commit)

| Check | How |
|-------|-----|
| Opens without **Repair** dialog | Open in PowerPoint on Lepton |
| **2 slides** (seed template) | Cover + content |
| **Logo + footer** on both | UP upscale ai, © Upscale AI line |
| **Gold text** on navy panel (cover) | Not black on blue |
| **Deck build** | `uv run check-decks` passes after regen |

---

## When to use what

| Task | Use |
|------|-----|
| **DT100 A3 / DT122 B6** | Edit md → `uv run build-decks` |
| **New exec deck (hand)** | `upscale-company-template.pptx` |
| **Theme/masters only** | `upscale-exec-empty.pptx` |
