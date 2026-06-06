# Arch vision (A3) — source of truth

**Single file for this deck:** on-slide copy + presenter notes → `qos-architecture.pptx` via `./scripts/run-deck-build.sh`.

**Terms:** [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) · **Meeting playbook:** [plan.md](plan.md)

**Frame (not on slides):** **DT100 deliverable** = these slide decks (A3 + B6) — files you build and bring. **Friday meeting input** = walk them. **Friday outcome** = mandate + marching orders (not another document; Cx/two-pager was a wrong fork). Decks sell **trust in the role** — vision, draft plan, how I drive with light steer.

---

## Cover

**Left title:** qos architecture  
**Left subtitle:** End-to-end datapath hardware–software validation  
**Meta:** Diwakar Tundlam - qos architect  
**Right (navy, 3 lines):** Dynamic / Switch-Buffer / Management  
**Tag:** Architecture review · Confidential — Upscale AI

```notes
This deck sells me in the role — vision, draft plan, how I drive — not a document handoff.

Left = program bar (done and validated to tape-out). Right = Diwakar DRI wedge (DBM). Close = mandate + **concrete draft in next few days** (steer post-meeting).
```

---

## Before slide 1

```notes
Sponsor is you — your name is not on this deck.

I am Diwakar. You need someone you can trust to drive with little supervision — not get lost or stuck — while you guide at critical junctures. These slides show what I will do in that role: vision, plans, draft execution path.

Two alignments: (1) your done-and-validated bar — product, mgmt plane, architecture validation, SDK/SAI, C-model → emulation → silicon; (2) my wedge — Dynamic Switch-Buffer Management (DBM) at CSB (QoSMAP, Queue, buffer carving).

DBM (say once): ESUN-world pair to DLB — buffers/CSB layer, not ECMP/fabric. **Datapath Architecture** (E-level lane; implicit owner — no name, no OCP on slide). W peers: Shafi (L2/L3/Mirroring), Tippanna (ECMP/Stats), Tilak (L2), SDK leads.

Flow: slides 1–2 (situation + task) → QoS buffer carving arch walk → slides 3–4 (mandate + alignment).
```

---

## Slide 1

**Title:** Dynamic Switch-Buffer Management  
**Subtitle:** Buffer carving at Central Scheduler Block (CSB)  
**Diagram:** slide01-scope

**On-slide (stack):**

*Validation path to tape-out*
- Product | program
- Management plane (FBOSS / SONiC) | program
- Architecture validation | program
- SDK / SAI | program
- C-model → emulation → silicon | program

*Diwakar Tundlam - qos architect*
- CSB | lane
- QoSMAP | lane
- Queue | lane
- Buffer carving | lane
- Friday meeting · scope align | act

```notes
What I will drive in your program bar — not owning product, mgmt, full AV, or SDK programs, but contributing with a clear wedge.

Bottom band = function lane (not role title): QoSMAP, Queue, buffer carving at CSB. Bounded scope under steer.

Selling: I have a bounded wedge and understand how it sits in the full tape-out path.
```

---

## Slide 2

**Title:** Validated to tape-out  
**Diagram:** slide02-validated

**Deliverable band:** Diwakar Tundlam - qos architect · deliverable

**On-slide (deliverable row):**
- Shafi · L2/L3/Mirroring | peer
- Tippanna · ECMP/Stats | peer
- Tilak · L2 | peer
- Datapath Architecture | peer
- Diwakar · buffer carve plan | lane

**On-slide (columns):**

**Column:** Tape-out validation · program
- Product
- Management plane
- Architecture validation
- SDK / SAI
- Tape-out path

**Column:** Diwakar Tundlam — qos architect · lane
- QoSMAP
- Queue
- Buffer carving

**Column:** Peer DRIs · peer
- Shafi · L2/L3/Mirroring
- Tippanna · ECMP/Stats
- Tilak · L2
- Counters

**Outcome:** QoS buffer carving arch
**Read guide:** 1 columns left→right · 2 walk

```notes
Walk order: three columns **left → right**, then **down** to QoS buffer carving arch walk. **Read order** on-slide: 1 → 2.

Col 1 = tape-out validation (program). Col 2 = Diwakar lane (orange). Col 3 = peer DRIs. **Bottom row** = W intersects + buffer carve plan.

**No gate diamond** — stand-alone / forward-safe (Thippanna Sr.W + Prabhu A). Alignment / reframe with sponsor — spoken at Friday meeting, not on-wall.

*(Thippanna stacked layout → B6 backlog.)*
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
- Next few days · buffer carve plan | highlight
- Software ↔ hardware · validated | step
- SDK / SAI / mgmt → tape-out | step
- AV · C-model / co-dev | step

```notes
SharePoint timeline: 2–3 month window was too slow — concrete output in the **next few days** (yellow highlight on slide).

Say: **buffer carve plan** + validation gates v0 (format per steer) — not another 50-pager. North star unchanged: tape-out with SDK, SAI, mgmt on silicon.

Sponsor touch-in at gates; Diwakar drives day-to-day technical work.
```

---

## After pipeline walk

```notes
Slide 4: four engineering checkpoints before Friday meeting close. Mandate = permission to drive the sprint. Pipeline plan co-evolved on the walk — alignment, not a doc handoff.
```

---

## Slide 4

**Title:** Alignment · Friday meeting  
**Diagram:** slide04-sponsor

**On-slide (stack):**
- Scope · situation + task | ask
- Diwakar Tundlam - qos architect scope | ask
- QoS buffer carving arch | act
- Datapath Architecture | ask

```notes
Four checkpoints — technical, not a sign-off deck.

Scope: slides 1–2 — program bar + DBM at CSB framed correctly? Lane: QoSMAP, Queue, buffer carving vs peer DRIs. Pipeline walk: logical pipeline and draft validation path. **Datapath Architecture** checkpoint — her lane; OCP implicit, not on slide.

If aligned: mandate to ship **buffer carve plan in next few days** → iterate toward tape-out (AV/C-model, SDK/SAI/mgmt).
```
