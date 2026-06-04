# DT100 plan

**Task:** DT100 · P0 · `doing` · due **2026-06-05**
**Deliverables:** [manager-arch-vision-a3.md](manager-arch-vision-a3.md) · [manager-arch-vision-b6.md](manager-arch-vision-b6.md) · slide export for Gururaj

**This file:** Decisions and meeting playbook only — **save the plan, not how we arrived at it.** Update here when the plan changes.

---

## 1. What Thu is for (meta — both edges in one sitting)

| Step | What you lead with |
|------|-------------------|
| **Situation** | Clean slate — tape-out SW path, 2-pager constraint (A3 slide 1) |
| **Task** | Clarify the job — definition of done, DRI charter (A3 slide 2) |
| **Define** | Walk **B6** — how, who, wedge (only if task framing holds) |
| **Close** | **Result** + **sponsorship** (A3 slides 3–4) |

**Not Thu:** Finished architecture, C40, full HW digest, 50-page doc, AI/token policy deck.

**True goal:** Gururaj trusts you can **build vision under ambiguity** — **2-pager machine**, not arch sign-off.

---

## 2. Artifacts (roles)

| Artifact | Role | Audience |
|----------|------|----------|
| **A3** | **Bookend** — situation + task → (B6) → result + sponsorship (4 slides) | Gururaj only |
| **B6** | **Define task** — walkable plan (not a bag of diamonds) | After A3 slides 1–2 |
| **Cx** (~2 weeks) | First **Amazon-style 2-pager** (decisions, gates, issues) | Gururaj |
| **whiteboards.md** + **`../assets/pics/`** | Evidence / drill-down | B6 backup |
| **Logical pipeline PNG** | Aligns with boss SharePoint PPTX | B6 §6 |

**A3 is not complete without:** export 4 slides/PDF (present 1–2 → B6 → 3–4). **B6 is not complete without:** whiteboard pass in [../assets/dt100-whiteboards.md](../assets/dt100-whiteboards.md).

---

## 3. Meeting playbook (Thu → Fri)

```text
  A3 slides 1–2   Situation → clarify task
       ↓
  Task OK? ──→ B6 define task (15–20 min)
       ↓
  No?      ──→ Fix slides 1–2 only · B6 closed unless he asks
       ↓
  A3 slides 3–4   Result → sponsorship
       ↓
  Fri          Expected iteration
```

| Do | Don’t |
|----|--------|
| Expect **his edits** on A3/B6 — welcome them | Defend draft as final |
| **No** on task (slide 2) → listen, redo framing | Open B6 if task wrong |
| B6 **defines** task after A3 **clarifies** it | RACI grid, SWOT, EM on slides |

**Fri:** Expected iteration — not failure.

---

## 4. Language (AWS / Apple habit — not on slides)

| Term | Who |
|------|-----|
| **Sponsor** | Gururaj — scope, exec/OCP voice, escalation |
| **DRI (you)** | Arch-vision framework + **QoS RM** (QoSMAP, Queue/carve, ESUN align) |
| **DRI (peers)** | **Shafi Mohammad** — L2/L3/ACL · **Tippanna Hongal** — ECMP/AV |
| **Contributors** | **Rupa** (datapath/OCP), **Prasun** (program mesh), SDK leads |

**Drop:** RACI, “mental model,” tribe metaphors on slides.

---

## 5. Names — slides vs B6 only

**On A3 slides:** **Sponsor** only (no name — you say “Sponsor is you” at open). **B6** owner slide names Sponsor (Gururaj) once + peer DRIs.

**B6 only (deeper):** Srihari, Girish/Shravan, coalition cadence, Prabu brainstorm (§10), OCP Thu 8AM.

**Off slides / off Thu:** CEO/CTO/Chairman, Madhu channeling, 25yr friendship wording, Santosh AI economics, CEO spambot story, full org chart.

---

## 6. Technical spine (what to say)

**Boss question:** SW **done and validated** with product, mgmt plane, datapath/AV, **SDK/SAI before tape-out** (C-model → emulation → silicon).

**Your wedge:** **CSB** + **buffer carving** (his words — complex, under-owned); deliver via datapath *understanding*, not **owning** datapath arch (**Rupa**). On the pipe: **QoSMAP** + **Queue** / Switch-Buffer · resource mgmt; **ESUN** direction; **HWv1** (no MPLS EXP / IPv6 pri yet → HWv2).

**Pipeline:** Port → Parser → … → **QoSMAP** → … → **Queue** / egress (see B6 §6 + `../assets/logical-pipeline-boss-slide.png`).

**Parallel track (do not merge on Thu):** Rupa’s SDK/SAI/datapath-variant layout — related, different plan (B6 §7).

**Rupa thread:** Per-packet **parse correctness** vs NOS header confusion; weekly align before OCP/BCM calls.

**Shafi:** 50-pager issue — you aligned offline (Apple: attention vs importance with execs); **do not re-litigate** on Thu; peer DRI on L2/L3; Gururaj escalates if stress.

---

## 7. Explicitly back-burner

| Topic | Where |
|-------|--------|
| AI tokens / Santosh / Byzantine refs | Separate deck/thread — not A3/B6 |
| Prabu **bs-1/bs-2** brainstorm | B6 §10 hook only if asked |
| **bs-2** GPU/scale AI diagram | Omit unless Gururaj pulls AI-scale |
| Program management detail | Sneak peek → Prasun; round 2 |
| DT113 prune | **Done** — tree is Gluon-only now |

---

## 8. Document discipline (his AWS habit)

- He **will not read 50 pages** — same as Shafi’s pain point.
- **Thu:** A3 + walkable B6 (≤~6 sections).
- **~2 weeks:** **Cx 2-pager** — decisions + gates + QoS HWv1 scope.
- Deep truth can exist later; **exec read stays thin**.

---

## 9. Two-core execution (you + Gluon)

| Core | While DT100 `doing` |
|------|---------------------|
| **Human** | Notes, photos, slide export, meeting, Fri edits |
| **Gluon** | One hat per session: DT100 merge/polish **or** nothing else |

When Gluon is active, you’re **fused** — don’t pretend parallel P1 work counts.

**Updates:** Edit this file when decisions change; do not append process notes or chat transcripts.

---

## 10. DT100 done checklist

- [ ] Whiteboard corrections — [../assets/dt100-whiteboards.md](../assets/dt100-whiteboards.md) checkboxes
- [ ] A3 / B6 reviewed; messaging aligned (md ↔ pptx via regen)
- [ ] A3 exported → PDF (optional B6 PDF)
- [ ] Sent or presented to **Gururaj**; Fri follow-up if needed
- [ ] `TASKS.md`: DT100 → `done` + `TASKS-LOG` entry

**Not required for done:** Cx 2-pager, org hooks, peer sign-off on validation v0.

---

## 11. Layout

See [README.md](README.md) in this directory.
