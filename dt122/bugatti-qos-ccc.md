# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`**.

**Single file for this deck:** slide titles → `bugatti-qos-ccc.pptx` via `uv run build-decks`.

**Flow:** [../dt100/bugatti-qos-architecture.md](../dt100/bugatti-qos-architecture.md) slides 1–2 → **B6** → A3 slides 3–4 (alignment).

**Metadata (not in PPTX):** [bugatti-qos-ccc-meta.md](bugatti-qos-ccc-meta.md)

**Depth / reference:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

**Revision (not exported — git / meta only):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author | Prior qos-ccc skeleton — unnamed ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | Buffer-carving CCC · A3-aligned |

---

## Cover

**Title:** Buffer-carving CCC  
**Subtitle (navy):** Dynamic Switch-Buffer Management · logical pipeline  
**Meta:** Follows qos architecture · Revision 0.1  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** Logical pipeline  
**Subtitle:** Program kickoff slide — unchanged  
**Image:** logical-pipeline-boss-slide.png

---

## Slide 2

**Title:** Datapath · CCC scope  
**Subtitle:** Orange slice = buffer-carving scope  
**Lead:** QoSMAP · CSB buffer-carving · QoS-CCC — aligned with qos architecture.  
**Diagram:** b6-slide02-pipeline-scope-pie

**Bullets:**
- Schematic only — equal slices, not sizing metrics.
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
- Use-case-driven datapath may revise rows.

---

## Slide 6

**Title:** Scope and open items  
**Subtitle:** In scope versus deferred  
**Lead:** What this CCC covers versus peer decks.  
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

Full map, DRI tables, whiteboard annotations: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
