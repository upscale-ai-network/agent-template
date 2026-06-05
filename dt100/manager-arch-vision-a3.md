# Arch vision (A3) — source of truth

**Single file for this deck:** on-slide copy + presenter notes → `manager-arch-vision-a3.pptx` via `./scripts/run-deck-build.sh`.

**Terms:** [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) · **Meeting playbook:** [plan.md](plan.md)

**Frame (not on slides):** **DT100 deliverable** = these slide decks (A3 + B6) — files you build and bring. **Friday meeting input** = walk them. **Friday outcome** = mandate + marching orders (not another document; Cx/two-pager was a wrong fork). Decks sell **trust in the role** — vision, draft plan, how I drive with light steer.

---

## Cover

**Left title:** Architecture Vision  
**Left subtitle:** End-to-end datapath hardware–software validation  
**Right (navy, 3 lines):** Dynamic / Switch-Buffer / Management  
**Tag:** Architecture review · Confidential — Upscale AI

```notes
This deck sells me in the role — vision, draft plan, how I drive — not a document handoff.

Left = your program bar (done and validated to tape-out). Right = my DRI wedge (DBM). Close = mandate + **concrete draft in next few days** (Guru steer post-meeting).
```

---

## Before slide 1

```notes
Sponsor is you — your name is not on this deck.

I am Diwakar. You need someone you can trust to drive with little supervision — not get lost or stuck — while you guide at critical junctures. These slides show what I will do in that role: vision, plans, draft execution path.

Two alignments: (1) your done-and-validated bar — product, mgmt plane, architecture validation, SDK/SAI, C-model → emulation → silicon; (2) my wedge — Dynamic Switch-Buffer Management (DBM) at CSB (QoSMAP, Queue, buffer carving).

DBM (say once): ESUN-world pair to DLB — buffers/CSB layer, not ECMP/fabric. Rupa owns datapath architecture; I drive by understanding the pipe. Peer intersects: Shafi (L2/ACL), Tippanna (ECMP/AV), SDK leads, Rupa (datapath/OCP).

Flow: slides 1–2 (situation + task) → QoS buffer carving arch walk → slides 3–4 (mandate + alignment).
```

---

## Slide 1

**Title:** Dynamic Switch-Buffer Management  
**Subtitle:** Buffer carving at Central Scheduler Block (CSB)  
**Diagram:** slide01-scope

**On-slide (stack):**

*Program — done and validated*
- Product | program
- Management plane (FBOSS / SONiC) | program
- Architecture validation | program
- SDK / SAI | program
- C-model → emulation → silicon | program

*DRI — QoS RM at CSB*
- CSB | lane
- QoSMAP | lane
- Queue | lane
- Buffer carving | lane
- Scope align · Fri | act

```notes
What I will drive in your program bar — not owning product, mgmt, full AV, or SDK programs, but contributing with a clear wedge.

Bottom band = my lane: QoS RM on QoSMAP, Queue, buffer carving at CSB. This is the draft scope I execute under your steer.

Selling: I have a bounded wedge and understand how it sits in the full tape-out path.
```

---

## Slide 2

**Title:** Done and validated before tape-out  
**Diagram:** slide02-validated

**Deliverable band:** My deliverable

**On-slide (compass):**
- Gururaj · scope | north
- Shafi · Tippanna | east
- Rupa · datapath | west
- QoS carve · pipeline walk | south

**On-slide (columns):**

**Column:** Done and validated · program
- Product
- Management plane
- Architecture validation
- SDK / SAI
- Tape-out path

**Column:** My lane (QoS RM) · lane
- QoSMAP
- Queue
- Buffer carving

**Column:** Peer DRIs · peer
- Layer 2 / 3
- ECMP / LAG
- Port-Mirroring
- Counters

**Gate:** Aligned
**Branch yes:** QoS buffer carving arch
**Branch no:** Reframe task
**Read guide:** 1 columns left→right · 2 down to aligned · 3 yes walk

```notes
Walk order: three columns **left → right**, then **down** to Aligned → QoS buffer carving arch. **Read order** on-slide: numbered arrows 1 → 2 → 3 (Guru: visual learner — how to read).

**Aligned · Wed 1:1** — not a re-ask. Middle column = my lane (QoS buffer carve). Bottom band = **My deliverable** — compass prefetch for org framing (no N-E-W-S label on wall).

Yes → QoS buffer carving arch walk. No path grayed — closed at 1:1.
```

---

## Into pipeline walk

```notes
Pipeline walk is not a deliverable — it is how I show vision, draft plans, and execution instinct. Walk it; steer me at junctures. Role-play the arch execution plan.
```

---

## Slide 3

**Title:** Near-term scope  
**Diagram:** slide03-outcomes

**On-slide (stack):**
- Next few days · draft plan | step
- Software ↔ hardware · validated | step
- AV · C-model / co-dev | step
- SDK / SAI / mgmt → tape-out | step

```notes
Guru redirect: 2–3 month window was too slow — he wants something concrete in the **next few days**.

Say: draft plan / validation gates v0 (format per his steer) — not another 50-pager. North star unchanged: tape-out with SDK, SAI, mgmt on silicon.

Gururaj touch-in at gates; I drive day-to-day technical work.
```

---

## After pipeline walk

```notes
Slide 4: four engineering checkpoints before Fri close. Mandate = permission to drive the sprint. Pipeline plan co-evolved on the walk — alignment, not a doc handoff.
```

---

## Slide 4

**Title:** Alignment · Fri close  
**Diagram:** slide04-sponsor

**On-slide (stack):**
- Scope · draft QoS slides | ask
- QoS RM · lane boundary | ask
- QoS buffer carving arch | act
- OCP · Rupa datapath | ask

```notes
Four checkpoints — technical, not a sign-off deck.

Scope: slides 1–2 — program bar + DBM at CSB framed correctly? Lane: QoSMAP, Queue, buffer carving vs peer DRIs. Pipeline walk: logical pipeline and draft validation path. OCP: I align with Rupa on datapath standards; Gururaj carries company position externally (standards body, customer-facing).

If aligned: mandate to ship **draft plan in next few days** — then iterate toward tape-out (AV/C-model, SDK/SAI/mgmt).
```
