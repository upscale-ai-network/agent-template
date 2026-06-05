# Arch vision (A3) — source of truth

**Single file for this deck:** on-slide copy + presenter notes → `manager-arch-vision-a3.pptx` via `./scripts/run-deck-build.sh`.

**Terms:** [../assets/guru-terms-sot.md](../assets/guru-terms-sot.md) · **Meeting playbook:** [plan.md](plan.md)

---

## Cover

**Left title:** Architecture Vision  
**Left subtitle:** End-to-end datapath hardware–software validation  
**Right (navy, 3 lines):** Dynamic / Switch-Buffer / Management  
**Tag:** For Executive Review · Confidential — Upscale AI

```notes
Arch vision review. Upscale confidential. Main deck is four slides plus B6 backup.
```

---

## Before slide 1

```notes
Sponsor is you — your name is not on this deck.

I am Diwakar. I am here to align on two things: your done and validated bar before tape-out (product, mgmt, datapath AV, SDK/SAI), and my scope: Dynamic Switch-Buffer Management (DBM — same ESUN-world idea as DLB, but at Switch-Buffer / CSB, not fabric load balancing). Buffer carving at CSB; queues, PFC, WRED/ECN/Pause via SDK/SAI — Rupa owns datapath architecture.

If slide one or two is off, tell me now; we fix that before B6, not after.

Flow: slides 1–2 → B6 (his pipeline slide — you point carve, don’t reframe Rupa’s map) → slides 3–4.
```

---

## Slide 1

**Title:** Dynamic Switch-Buffer Management  
**Subtitle:** Buffer carving at CSB  
**Diagram:** slide01-scope

**On-slide (stack):**

*Program — done and validated*
- Product | program
- Management plane | program
- Arch validation | program
- SDK / SAI | program
- C-model → silicon | program

*Your DRI — switch-buffer at CSB*
- CSB | lane
- Buffer carving | lane
- Align today | act

```notes
Point at slide: Title is DBM; subtitle is his ink — buffer carving at CSB (at = in that block, not owning full datapath).

DBM (spoken once): Pairs with DLB in ESUN scale-up vocabulary — equivalent branding, different layer (buffers/CSB, not ECMP/fabric).

His words: no one has looked at CSB and buffer carving. You have confidence I can deliver by understanding datapath; Rupa owns datapath architecture. Her pipeline slide in B6 is a seed for her work — you walk it; you don’t own pkt-format / L2-L3 path framing.

Story A on the slide: done and validated · product · mgmt · AV · SDK/SAI · C-model → emulation → silicon. I contribute; I do not own the full bar.

Today: align on scope, not full HW sign-off or fifty-page packs.
```

---

## Slide 2

**Title:** SW done and validated before tape-out  
**Diagram:** slide02-validated

**On-slide (columns):**

**Column:** SW done and validated · program
- Product
- Arch validation
- SDK / SAI
- Tape-out path

**Column:** Your lane · lane
- QoSMAP
- Queue
- Buffer carving

**Column:** Peer DRIs · peer
- Layer 2 / 3
- ECMP

**Gate:** Aligned?
**Branch yes:** Pipeline walk
**Branch no:** Fix slides 1–2

```notes
Program (his language): SW done and validated before tape-out — product, mgmt plane, datapath AV, SDK/SAI, milestones on the path to silicon.

My lane: QoS RM — QoSMAP, Queue, buffer carving. Not L2/L3, ECMP, or SDK programs.

Peers: Shafi on L2-FBD / ACL, Tippanna on ECMP / AV, SDK leads, Rupa on datapath / ESUN — names on B6.

If this matches your expectation, we open B6 — his pipeline slide; you anchor CSB, QoSMAP, Queue, carve.
```

---

## Into B6

```notes
B6 is the how — whole pipe, owners, my wedge on QoSMAP and Queue. I will not read every row unless you want detail.
```

---

## Slide 3

**Title:** What you get  
**Diagram:** slide03-outcomes

**On-slide (stack):**
- Cx 2-pager | doc
- Validation gates | doc
- AV decisions | doc
- Friday edits | step

```notes
Outcome: You get a 2-pager machine — Cx in ~two weeks: decisions, validation gates, open issues — not a fifty-page arch dump.

For him: done and validated clarity at milestones; AV at gates; thin read he can use upward (Executive review on cover is intentional).

~two weeks: First Cx drop — gates v0 + CSB / carve HWv1 scope inside the 2-pager, not as a separate QoS-only promise.

This week: 1–2, B6, Friday on his edits.
```

---

## After B6

```notes
Last two slides — outcomes and what I need from you as Sponsor.
```

---

## Slide 4

**Title:** What I need from you  
**Diagram:** slide04-sponsor

**On-slide (stack):**
- Scope OK on 1–2? | ask
- Program chair? | ask
- Owners · B6 | ask
- OCP voice | ask

```notes
Are slides 1–2 right? If not, we fix before treating B6 as agreed.

Confirm who owns which slice — B6 owner slide has names.

Program chair (spoken, optional): Are you comfortable with me driving the done and validated program with you as Sponsor, or do you want to chair that yourself?

OCP / vendors: I coordinate with datapath; you own company position externally.

Format: PDF async, live, or Friday follow-up — your call.

Escalation: Step in if architects stall on validation gates.
```
