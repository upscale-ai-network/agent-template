# DT100 plan

**Task:** DT100 · P0 · **`done`** · due **2026-06-05** · SharePoint → Gururaj · git `445afec` pushed
**Deliverables:** [qos-architecture-diwakar-tundlam.md](qos-architecture-diwakar-tundlam.md) · [manager-arch-vision-b6.md](manager-arch-vision-b6.md) · slide export for Gururaj

**This file:** Decisions and meeting playbook only — **save the plan, not how we arrived at it.** Update here when the plan changes.

---

## 1. DT100 — input vs outcome (do not conflate)

| | What | Type |
|---|------|------|
| **DT100 deliverable (your work)** | **A3 + B6** slide decks — built, exported, ready | **Files / artifacts** (INPUT) |
| **Friday 11am meeting outcome** | **Mandate + marching orders** for 2–3 month sprint | **Not a document** — lived alignment |
| **Wrong fork (nix)** | Cx, two-pager reference doc, post-meeting PDF as “deliverable” | Misread of thin-read *discipline* |

**Decks sell:** trust in you in the role — vision, draft plan, drive with light steer to tape-out (SDK/SAI/mgmt, AV/co-dev).

**Meeting flow:**

| Step | Deck |
|------|------|
| Situation + task | A3 slides 1–2 |
| Vision + draft plan walk | B6 (if gate yes) |
| Mandate + sponsor alignment | A3 slides 3–4 |

**Not the meeting:** Finished architecture sign-off, C40 digest, 50-page doc, AI/token deck.

---

## 2. Artifacts (roles)

| Artifact | Role | Audience |
|----------|------|----------|
| **A3** (.pptx / PDF) | **INPUT** — bookend: situation → task → mandate ask → sponsor (4 slides) | Gururaj · Fri 11am |
| **B6** (.pptx) | **INPUT** — walk: vision, owners, pipeline, draft execution | After A3 1–2 if aligned |
| **Mandate** (Fri close) | **OUTCOME** — permission to drive 2–3 month sprint | Gururaj → you |
| **whiteboards.md** + **`../assets/pics/`** | Drill-down backup | If asked |
| **Logical pipeline PNG** | B6 §6 — boss slide | B6 walk |

**DT100 done when:** A3 + B6 reviewed, exported, presented (or sent) — see §10. **Mandate is not DT100** — it is what Fri produces if trust lands.

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
| **Gururaj** | Scope steer, company/OCP external, escalation |
| **DRI (you)** | Arch-vision framework + **QoS RM** (QoSMAP, Queue/carve, ESUN align) |
| **DRI (peers)** | **Shafi Mohammad** — L2/L3/ACL · **Tippanna Hongal** — ECMP/LAG/Counters/AV |
| **Contributors** | **Rupa** (datapath/OCP), **Prasun** (program mesh), SDK leads |

**Drop:** RACI, “mental model,” tribe metaphors on slides.

---

## 5. Names — slides vs B6 only

**On A3 slides:** Gururaj by name only where external/OCP voice applies. **B6** owner slide names Gururaj once + peer DRIs.

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
- **~2 weeks:** **Two-pager reference document** — decisions + gates + QoS HWv1 scope.
- Deep truth can exist later; **exec read stays thin**.

---

## 9. Two-core execution (you + Gluon)

| Core | DT100 `done` — Fri meeting + mandate out of band |
|------|-----------------------------------------------------|
| **Human** | Walk A3/B6; Fri edits if Guru redirects |
| **Gluon** | On request only — not default P0 |

When Gluon is active, you’re **fused** — don’t pretend parallel P1 work counts.

**Updates:** Edit this file when decisions change; do not append process notes or chat transcripts.

---

## 10. DT100 done checklist

- [ ] Whiteboard corrections — [../assets/dt100-whiteboards.md](../assets/dt100-whiteboards.md) checkboxes
- [x] A3 / B6 reviewed; messaging aligned (md ↔ pptx via regen)
- [ ] A3 exported → PDF (optional B6 PDF)
- [x] **Gururaj** — pptx on SharePoint, link shared
- [x] `TASKS.md`: DT100 → `done` + `TASKS-LOG` entry

**Not required for done:** Two-pager reference document, org hooks, peer sign-off on validation v0.

---

## 11. Layout

See [README.md](README.md) in this directory.

---

## 12. Directive feedback → active / passive (W review)

Peer feedback (e.g. Thippanna) often arrives **directive** — layout, owners, publish-ready close. **Refine before acting:**

| Class | Meaning | Example (Thippanna 2026-06) |
|-------|---------|------------------------------|
| **Active · A3** | Ships on **Guru tactical** deck now | Peer labels (Shafi/Tippanna/Tilak), Datapath wording, buffer carve timeline |
| **Passive · B6** | Spirit / structure for **pipeline walk** deck | Wedge layout, Girish L3, publish-ready close |
| **Active · A3 (post-A)** | Stand-alone / forward-safe | Drop **Reframe** + **Aligned** diamond; **Friday meeting** not **Fri** |
| **Abeyance** | Right idea; wrong time or too “made-up” | Full wedge redraw of slide 2 |

**Rule:** A3 = short N-line reply (situation → gate → mandate). B6 = how/who/W publish path. When feedback mixes both, **split the list** — do not let B6 polish block A3 send.

**Process:** capture verbatim → tag A3 / B6 / abeyance → active tasks in `TASKS.md` only for **A3 now**; B6 items in [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md) backlog.
