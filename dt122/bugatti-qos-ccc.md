# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`** (ccc doc) — no `draft-` prefix unless back on draft-board.

**Single file for this deck:** slide titles, walk cues → `bugatti-qos-ccc.pptx` via `uv run build-decks`.

**Presenter script (not in PPTX):** [bugatti-qos-ccc-presenter-notes.md](bugatti-qos-ccc-presenter-notes.md)

**Companion:** [../dt100/bugatti-qos-architecture.md](../dt100/bugatti-qos-architecture.md) (slides 1–2, then 3–4 after this walk). **Depth / walk map:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

**Revision (export to cover or appendix when integrated):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author (W) | Prior qos-ccc skeleton — unnamed on purpose ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | qos-architect · buffer carving focus · W review TBD |

**Role:** qos-architect — initial **buffer carving** slice; expand into datapath/HW and configuration layers over time.

---

## Cover

**Title:** QoS buffer carving arch  
**Subtitle (navy):** Walk: process → pipeline → alignment  
**Meta:** Open after qos-architecture slides 1–2 — role-play, not a handoff  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** The walk — five beats (process)  
**Subtitle:** Act I · broad strokes  
**Lead:** A3 framed situation + task — this deck shows how we execute.  
**Diagram:** b6-slide01-process-ribbon

**Bullets:**
- Not a 50-pager — scannable blocks, owners on the picture.
- Co-evolve gates live; I drive technical detail day-to-day.

---

## Slide 2

**Title:** Validation machine — how we prove tape-out  
**Subtitle:** Act II · focus  
**Lead:** v0 gates for group review — not unilateral.  
**Diagram:** b6-slide02-validation-stack

**Bullets:**
- I draft “done” per gate; Shafi, Tippanna, Rupa, SDK leads align on slices.

---

## Slide 3

**Title:** Logical pipeline — my wedge on your slide  
**Subtitle:** Act II · center of walk  
**Lead:** QoSMAP + Queue = my lane; peers on their blocks.  
**Diagram:** b6-slide03-pipeline-annotated

**Caption:** Shafi · Tippanna · Tilak · Girish · Rupa — W order on the picture.

---

## Slide 4

**Title:** Buffer carve @ CSB  
**Subtitle:** Act II · egress wedge  
**Lead:** Process outcome — carve plan + gate v0 in the next few days.  
**Diagram:** b6-slide04-csb-inset

---

## Slide 5

**Title:** Who aligns on which gate  
**Subtitle:** Act III · review  
**Lead:** Don’t read every row — point at the matrix.  
**Diagram:** b6-slide05-gate-alignment

**Bullets:**
- My lane: validation framework draft + QoS / buffer @ CSB.
- Peer DRIs own slice proof (C-model → emulation).

---

## Slide 6

**Title:** Boundaries — in this walk vs not merged  
**Subtitle:** Act III · defer  
**Lead:** Weekly sync on adjacent threads — no scope merge this walk.  
**Diagram:** b6-slide06-boundaries

---

## Slide 7

**Title:** Next steps — if you want me to drive  
**Subtitle:** Act III · forward  
**Lead:** Offer only if asked — peer huddle follows homework.  
**Diagram:** b6-slide07-next-steps

**Bullets:**
- Return to A3 slides 3–4 for mandate + alignment — not repeated here.

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations, and boundaries: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
