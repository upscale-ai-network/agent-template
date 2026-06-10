# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`**.

**Single file for this deck:** slide titles, walk cues → `bugatti-qos-ccc.pptx` via `uv run build-decks`.

**Flow:** [../dt100/bugatti-qos-architecture.md](../dt100/bugatti-qos-architecture.md) slides 1–2 → **B6** → A3 slides 3–4 (mandate / alignment).

**Optional presenter hints (not in PPTX):** [bugatti-qos-ccc-presenter-notes.md](bugatti-qos-ccc-presenter-notes.md)

**Depth / walk map:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

**Revision (not exported — git / presenter only):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author | Prior qos-ccc skeleton — unnamed ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | Buffer-carving walk · A3-aligned |

---

## Cover

**Title:** Quality of Service (QoS) buffer-carving architecture  
**Subtitle (navy):** Dynamic Switch-Buffer Management · logical pipeline  
**Meta:** Follows qos architecture · Revision 0.1  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** Logical pipeline  
**Subtitle:** Validated to tape-out · datapath context  
**Lead:** QoSMAP, Queue, and buffer-carving at Central Scheduler Block (CSB) — aligned with qos architecture.  
**Image:** logical-pipeline-boss-slide.png

---

## Slide 2

**Title:** Pipeline scope  
**Subtitle:** Orange slice = Dynamic Switch-Buffer Management scope  
**Lead:** QoSMAP · CSB buffer-carving · QoS-CCC — aligned with qos architecture.  
**Diagram:** b6-slide02-pipeline-scope-pie

**Bullets:**
- Center hub: Bugatti — Rupa · N · E org alignment (not slice owners).
- Peers acknowledged in parentheses — schematic only.
- Other pipeline blocks covered on peer architecture decks (SharePoint).

---

## Slide 3

**Title:** QoS classify and remark  
**Subtitle:** Upstream of buffer-carving  
**Lead:** VLAN priority, Differentiated Services Code Point (DSCP), ESUN class of service, and Unified Forwarding Header (UFH) → Traffic Class (TC) on egress.  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- Access Control List (ACL) can override remark policy.
- Handoff: classify → remark → Queue → buffer-carving at CSB.

---

## Slide 4

**Title:** Buffer-carving at Central Scheduler Block (CSB)  
**Subtitle:** Egress buffer policy · version 0  
**Lead:** Pool modes, buffer-carving sizes, admission, Priority Flow Control (PFC), port-speed coherence.  
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- Near-term deliverable: buffer-carving plan and gate version 0 · next few days.
- Hardware pool and register-transfer-level (RTL) sizing — in progress with architecture.

---

## Slide 5

**Title:** CSB buffer-carving · CCC  
**Subtitle:** Capabilities · Capacities · Constraints  
**Lead:** Version 0 placeholders — refine from HW architecture, RTL, and c-models.  
**Diagram:** b6-slide05-csb-ccc-tables

**Bullets:**
- Orange rows: CSB buffer-carving and fabric pool context — values TBD.
- Use-case-driven datapath may revise rows after qos-aware walk.

---

## Slide 6

**Title:** Scope and open items  
**Subtitle:** In this walk versus deferred  
**Lead:** What we cover today versus what stays on peer decks.  
**Diagram:** b6-slide06-boundaries

**Bullets:**
- Open: Ingress Fabric Port (IFP), Ingress Switch Buffer (ISB), CSB, and Egress Fabric Port (EFP) pool sizing.
- Deferred: software development kit (SDK) swimlanes and duplicating full peer deck bodies.

---

## Slide 7

**Title:** Next steps  
**Subtitle:** Back to alignment · checkpoints  
**Lead:** Lock version 0 gates — continue qos architecture close.  
**Diagram:** b6-slide07-next-steps

**Bullets:**
- Revision 0.1.
- Publish to SharePoint after group review.

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
