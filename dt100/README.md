# DT100 — arch vision for manager

**Task:** [TASKS.md](../TASKS.md) · **Playbook:** [plan.md](plan.md)

## Files in this dir

| File | Role |
|------|------|
| `manager-arch-vision-a3.md` / `.pptx` | **Deliverable** — A3 on-slide fragments → Guru-facing deck |
| `manager-arch-vision-a3-speaker-notes.md` | **Deliverable** — presenter script → ppt **Notes** on regen |
| `manager-arch-vision-b6.md` / `.pptx` | **Deliverable** — B6 walk (after A3 slides 1–2) |
| `plan.md` | Meeting playbook + done checklist (not slides) |
| `README.md` | **This file** — dir map + private prep (below); not sent to Sponsor |

**Convention:** `manager-arch-vision-*` = task outputs. `README.md` = how the dir works and what stays off the deck.

## Supporting (not in this dir)

| Path | Role |
|------|------|
| [../assets/dt100-whiteboards.md](../assets/dt100-whiteboards.md) | Photo annotations → B6 §6a |
| [../assets/pics/](../assets/pics/) | Whiteboard JPEGs |
| [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) | Guru vocabulary — whiteboards + pipeline |
| [../assets/logical-pipeline-boss-slide.png](../assets/logical-pipeline-boss-slide.png) | Pipeline slide for B6 |
| [../scratch/archive-manager-arch-vision-draft.md](../scratch/archive-manager-arch-vision-draft.md) | Superseded draft (git history) |

**Build:** `scripts/build-dt100-decks.py` · preview (local, gitignored): `scripts/preview-a3-deck.sh` → `assets/previews/a3/`

## You vs Gluon

| You | Gluon |
|-----|--------|
| Edit `manager-arch-vision-a3.md` + speaker-notes | Mirror → `build-dt100-decks.py`, regen `.pptx` |
| Rehearse from ppt **Notes** or speaker-notes md | `python3 scripts/build-dt100-decks.py` |

**Which file to read?**

- **On-wall copy** → `manager-arch-vision-a3.md` · **on screen** → `manager-arch-vision-a3.pptx`
- **1:1 words** → `manager-arch-vision-a3-speaker-notes.md`
- **Meeting order / done** → `plan.md`
- **Strategy, DBM/DLB, instill** → [Private prep](#private-prep) (this README)

Do not hand-edit pptx bullets if md is truth — regen after copy changes.

---

## Private prep

**Not on slides. Not in PowerPoint Notes.** Curate verbally; read the room.

**Published script:** [manager-arch-vision-a3-speaker-notes.md](manager-arch-vision-a3-speaker-notes.md)

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
| Product + management in the bar | Slide 1: done and validated · product · management plane · AV |
| Tape-out discipline | Slide 1–2: SDK/SAI · C-model → emulation → silicon |
| Not another 50-pager | Slide 3: Cx two-pager; B6 §2 discipline |
| Gates, not narrative | Slide 3: validation gates; B6 §3 machine |
| Wedge is real, bounded | Slide 1: CSB buffer carving — not datapath architecture; B6 §6 |
| Reuse upward | Cover: Executive review — his deck |

**Tactical drops (if the room opens):**

- “Use-case in, proof out — same milestone plan as SDK delivery.”
- “I draft gates so every block, including CSB carve, has AV before tape-out.”
- “Closed loop is the program; CSB carve is where I start proving I can run it.”

**Do not merge on Thu unless he pulls:** Rupa SDK layout (B6 §7), Prabu execution mesh, AI/token thread.

### Title and terms

- **On slide:** **Dynamic Switch-Buffer Management** · sub **Buffer carving at CSB**
- **DBM** — ESUN pair to **DLB**, not competition
- **Switch-Buffer** — one compound term (hyphenated)
- **at CSB** — location in block; not **for** whole datapath (**Rupa**)
- **Not your brand:** Logical Pipeline (his/Rupa seed slide in B6)

### After B6 — slide 3 close

Land **outcome**: Cx two-pager, validation gates (~two weeks), **Friday** edits. Carve HWv1 scope lives **inside** Cx, not as a separate on-wall promise.
