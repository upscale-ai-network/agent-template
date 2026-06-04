# Company template validation (Gluon)

**Canonical file:** `upscale-company-template.pptx` — **committed, hand-off ready.**

**You should not rebuild this for every new deck.** Open it in PowerPoint → duplicate slide 1 (cover) or slide 2 (content) → replace `[...]` text. Colors and chrome stay.

---

## Litmus (must pass before commit)

| Check | How |
|-------|-----|
| Opens without **Repair** dialog | Open in PowerPoint on Lepton |
| **2 slides** | Cover + content |
| **Logo + footer** on both | UP upscale ai, © Upscale AI line |
| **Gold text** on navy panel (cover slide, `[Subtitle line 1]` box) | Not black on blue |
| **Black/navy text** on white areas | Title, meta, content title `#051830` |
| **Duplicate slide** → new slide still has chrome | Manual spot-check |

**Automated (internal — no Repair dialog before you open):**

```bash
python3 scripts/build-company-template.py   # atomic save + zip assert
python3 scripts/validate-company-template.py
python3 scripts/validate-all-pptx.py        # all Gluon pptx before check-in
```

Build uses **copy-and-trim only** (never clone-into-empty-deck). Saves go to `.pptx.tmp` then replace after `assert_pptx_valid`.

---

## When to use what

| Task | Use |
|------|-----|
| **New exec deck (you)** | `upscale-company-template.pptx` only |
| **DT100 A3/B6** | `python3 scripts/build-dt100-decks.py` → `dt100/manager-arch-vision-*.pptx` |
| **Regenerate template** (rare) | `build-company-template.py` → **must** run `validate-company-template.py` → commit |
| **Theme/masters only** | `upscale-exec-empty.pptx` — not for litmus |

---

## Optional: `.potx`

In PowerPoint: **File → Save as Template** → `upscale-company-template.potx` (local; add to git only if IT OK).

---

## Validation log

| Date | Validator | Result | Commit |
|------|-----------|--------|--------|
| 2026-06-04 | Gluon script + color fix | `validate-company-template.py` pass | pending |
