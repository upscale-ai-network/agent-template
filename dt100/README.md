# DT100 — arch vision for manager

**Task:** [TASKS.md](../TASKS.md) · **Playbook:** [plan.md](plan.md)

## Source of truth (decks)

| File | → PPTX |
|------|--------|
| [bugatti-qos-architecture.md](bugatti-qos-architecture.md) | `bugatti-qos-architecture.pptx` — **DT100 input** · Fri meeting |
| [manager-arch-vision-b6.md](manager-arch-vision-b6.md) | `manager-arch-vision-b6.pptx` — **DT100 input** · walk deck |

**DT100 = the decks (files). Fri outcome = mandate (not a doc).** See [plan.md](plan.md) §1.

**Status:** `done` — SharePoint → Gururaj · git `445afec` on `origin/main` (2026-06-05).

**Build:** `./scripts/run-deck-build.sh` (reads only the two `.md` files above; do not hand-edit pptx)

**Check only (no writes):** `./scripts/check-decks.sh` — fails on any missing field, PNG, or corrupt pptx

**Setup (once):** `uv sync` (PyMuPDF + python-pptx; no npm/Chrome)

**Diagrams (A3):** labels from `bugatti-qos-architecture.md` → `scripts/a3_aligned_render.py` → PNG → pptx (no Mermaid; build validates every step)

**Preview (gitignored):** `scripts/preview-a3-deck.sh` → `assets/previews/a3/`

## Reference (not in decks)

| File | Role |
|------|------|
| [manager-arch-vision-b6-presenter-notes.md](manager-arch-vision-b6-presenter-notes.md) | B6 rehearse script — not in pptx (on-slide Subtitle + Lead cues only) |
| [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md) | B6 walk map, DRI tables, whiteboards — not parsed into pptx |
| [../assets/dt100-whiteboards.md](../assets/dt100-whiteboards.md) | Photo annotations |
| [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) | Guru vocabulary |
| [plan.md](plan.md) | Meeting order + done checklist |
| **README.md (below)** | Private prep only — never slide copy |

## You vs Gluon

| You | Gluon |
|-----|--------|
| Edit `bugatti-qos-architecture.md` or `manager-arch-vision-b6.md` | `./scripts/run-deck-build.sh` |

---

## Private prep

**Not on slides. Not in PowerPoint Notes.** Curate verbally; read the room.

### The hook (internal — do not read aloud as a paragraph)

End-to-end **SW–HW combined validation** — closed loop:

```text
  Use-case (product / management)
       ↓
  Arch models · C-models · emulation · silicon
       ↓
  AV + validation gates — aligned to SW program milestones
       ↓
  Complete before HW tape-out
```

Hold this vision while your **named DRI** is **Dynamic Switch-Buffer Management (DBM)** at **CSB** — **DLB** is the existing ESUN-world acronym you mirror, not a competing scope.

### Instill without saying

| He should feel | On-wall / walk support |
|----------------|------------------------|
| Product + management in the bar | A3 slide 1 diagram |
| Tape-out discipline | A3 slides 1–2 |
| Not another 50-pager | A3 slide 3; B6 slide 2 |
| Gates, not narrative | A3 slide 3; B6 slide 3 |
| Wedge is real, bounded | A3 slide 1; B6 slides 5–6 |
| Reuse upward | A3 cover |

**Do not merge on Thu unless he pulls:** Rupa SDK layout (B6 slide 8), Prabu execution mesh, AI/token thread.

### Title and terms

- **On slide:** **Dynamic Switch-Buffer Management** · sub **Buffer carving at CSB**
- **DBM** — ESUN pair to **DLB**, not competition
- **Switch-Buffer** — one compound term (hyphenated)
- **at CSB** — location in block; not **for** whole datapath (**Rupa**)
- **Not your brand:** Logical Pipeline (his/Rupa seed slide in B6)
