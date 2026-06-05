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

Left = your program bar (done and validated to tape-out). Right = my DRI wedge (DBM). Fri 11am close = mandate and marching orders for a 2–3 month sprint, if trust is there.
```

---

## Before slide 1

```notes
Sponsor is you — your name is not on this deck.

I am Diwakar. You need someone you can trust to drive with little supervision — not get lost or stuck — while you guide at critical junctures. These slides show what I will do in that role: vision, plans, draft execution path.

Two alignments: (1) your done-and-validated bar — product, mgmt plane, architecture validation, SDK/SAI, C-model → emulation → silicon; (2) my wedge — Dynamic Switch-Buffer Management (DBM) at CSB (QoSMAP, Queue, buffer carving).

DBM (say once): ESUN-world pair to DLB — buffers/CSB layer, not ECMP/fabric. Rupa owns datapath architecture; I drive by understanding the pipe. Peers on B6: Shafi (L2/ACL), Tippanna (ECMP/AV), SDK leads, Rupa (datapath/OCP).

Flow: slides 1–2 (situation + task) → B6 (vision + draft plan walk) → slides 3–4 (mandate + sponsor alignment).
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

**Title:** SW done and validated before tape-out  
**Diagram:** slide02-validated

**On-slide (columns):**

**Column:** SW done and validated · program
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

**Gate:** Task aligned?
**Branch yes:** B6 pipeline walk
**Branch no:** Reframe task

```notes
Can you trust this split? Column 1 = your org-level question. Column 2 = what I own and drive. Column 3 = peers I align with, not compete with.

Yes → B6 shows my vision and draft plan on the pipeline. No → we fix framing before any mandate.

This slide is the trust checkpoint before you invest guidance in a 2–3 month sprint.
```

---

## Into B6

```notes
B6 is not a deliverable — it is how I show vision, draft plans, and execution instinct. Walk it; steer me at junctures. Role-play the arch execution plan.
```

---

## Slide 3

**Title:** Sprint scope · Fri close  
**Diagram:** slide03-outcomes

**On-slide (stack):**
- 2–3 month window | step
- SW ↔ HW · validated | step
- AV · C-model / co-dev | step
- SDK / SAI / mgmt → tape-out | step

```notes
Fri 11am — if aligned, mandate for this sprint scope (not another deck).

Window: 2–3 months on the tape-out path. SW ↔ HW: validation gates before silicon. AV · C-model / co-dev: architecture validation and HW–SW co-development cadence. Exit: SDK, SAI, mgmt plane working on silicon.

Gururaj touch-in at gates; I drive day-to-day technical work. Depth follows redirect after mandate.
```

---

## After B6

```notes
Slide 4: four engineering checkpoints before Fri close. Mandate = permission to drive the sprint. Pipeline plan co-evolved on B6 — alignment, not a doc handoff.
```

---

## Slide 4

**Title:** Alignment · Fri close  
**Diagram:** slide04-sponsor

**On-slide (stack):**
- Scope · slides 1–2 | ask
- QoS RM · lane boundary | ask
- Pipeline · B6 walk-through | act
- OCP · Rupa datapath | ask

```notes
Four checkpoints — technical, not a sign-off deck.

Scope: slides 1–2 — program bar + DBM at CSB framed correctly? Lane: QoSMAP, Queue, buffer carving vs peer DRIs. B6: logical pipeline and draft validation path. OCP: I align with Rupa on datapath standards; Gururaj carries company position externally (standards body, customer-facing).

If aligned: Fri mandate for the 2–3 month sprint — AV/C-model, SDK/SAI/mgmt integration to tape-out.
```
