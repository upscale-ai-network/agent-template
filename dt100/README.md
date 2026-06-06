# DT100 — arch vision for manager (A3)

**Task:** [TASKS.md](../TASKS.md) DT100 · **`done`** · **Playbook:** [plan.md](plan.md)  
**CCC walk (B6):** moved to [../dt122/](../dt122/) — task **DT122**

## Source of truth (A3)

| File | → PPTX |
|------|--------|
| [bugatti-qos-architecture.md](bugatti-qos-architecture.md) | `bugatti-qos-architecture.pptx` — **final** · Guru SharePoint 2026-06-05 |

**Regen anytime:** edit md → `./scripts/run-deck-build.sh` (do not hand-edit pptx)

**Check:** `./scripts/check-decks.sh`

**Diagrams:** `bugatti-qos-architecture.md` → `scripts/a3_aligned_render.py` → PNG → pptx (PyMuPDF; no Mermaid)

**Preview (gitignored):** `scripts/preview-a3-deck.sh` → `assets/previews/a3/`

## Reference

| File | Role |
|------|------|
| [bugatti-qos-architecture-speaker-notes.md](bugatti-qos-architecture-speaker-notes.md) | Legacy pointer — notes in md ` ```notes ` blocks |
| [plan.md](plan.md) | DT100 meeting playbook + done checklist |
| [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) | Guru vocabulary |

## You vs Gluon

| You | Gluon |
|-----|--------|
| Edit `bugatti-qos-architecture.md` | `./scripts/run-deck-build.sh` |

---

## Private prep (A3)

**Not on slides.** Curate verbally; read the room.

### The hook (internal)

End-to-end **SW–HW combined validation** — closed loop. Hold **DBM at CSB** while program bar runs to tape-out.

| He should feel | On-wall support |
|----------------|-----------------|
| Product + management in the bar | A3 slide 1 |
| Tape-out discipline | A3 slides 1–2 |
| Not another 50-pager | A3 slide 3 |
| Wedge is real, bounded | A3 slide 1 |
| Concrete near-term output | A3 slide 3 · buffer carve plan |

**CCC walk detail:** [../dt122/](../dt122/) — not repeated here.
