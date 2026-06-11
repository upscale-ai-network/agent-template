# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`**.

**Single file for this deck:** slide titles → `bugatti-qos-ccc.pptx` via `uv run build-decks`.

**Flow:** [../dt100/bugatti-qos-architecture.md](../dt100/bugatti-qos-architecture.md) slides 1–2 → **B6** → A3 slides 3–4.

**Metadata (not in PPTX):** [bugatti-qos-ccc-meta.md](bugatti-qos-ccc-meta.md)

**Depth / reference:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

**Revision (not exported — git / meta only):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author | Prior qos-ccc skeleton — unnamed ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | bugatti-qos-ccc |

---

## Cover

**Title:** bugatti-qos-ccc
**Subtitle (navy):** Dynamic Switch-Buffer Management · logical pipeline  
**Meta:** Diwakar Tundlam · 11 Jun 2026  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** bugatti-qos-ccc scope  
**Lead:** QoSMAP → CSB buffer-carving → bugatti-qos-ccc  
**Diagram:** b6-slide02-pipeline-scope-pie

---

## Slide 2

**Image:** logical-pipeline-boss-slide.png

---

## Slide 3

**Title:** Capabilities · Classify and Remark
**Layout:** split  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- ... incomplete+review: Bugatti datapath features
- Port-Speed Bifurcation -> Static Buffer Carving in CSB
- Dual-Die Sky-Hammer Support - 2x115Tbps - w/UCIE D2D
- UA-Link (descoped..) - (same PHY/PMD, different PCS/PMA)
- ESUN-UFH -> TC (4 _or_ [3-bit=8]) - different MAC layer
-   AFH -> (BCM: SUE) -> vTC -> VLAN · L3/DSCP -> QoS
-   EFH -> VLAN · PRI -> L3/DSCP -> QoS
- L2 /L3 L3 Datapath and ACL, Policer · ECN, PFC, Pause (.3x), flow-control?
- Queues · QoSMAP · Egress Scheduler · Per-Port Queue, Egress remap (egress ACL?)
- ECMP / Mirroring / Fine-grain stats / SFlow? / CPU punt-path / slow-path (DPI?)

---

## Slide 4

**Title:** Capacities · buffer-carving at CSB  
**Layout:** split
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- ... incomplete+review: Bugatti capacifies
- Port tiers: 200G · 400G · 800G Bifurcation modes / speeds rate mapping
- Lossless buffer pools (Pause / PFC)
- Lossy buffer pools (ECN)
- Carve sizes · Static and Dynamic control of buffer-pools.
- PFC · pause · headroom
- Traffic aware congestion management and control
- ECMP based DLB(?), Entropy seed logic, dynamic re-adjust?
- Per-TC · Egress Queues, Egress QoS, Scheduler, WFQ/SPQ, Port-BW configuration, etc.
- AI / XPU workload based dynamic rebalacing?
- SDN / Controller / Orchestrator / Operator alignment (in scope?)

---

## Slide 5

**Title:** Constraints · CSB table sizes, limits, combinations (samples only - review with HW arch and publish)
**Diagram:** b6-slide05-csb-ccc-tables

---

## Slide 6

**Title:** Scope · deliverable
**Diagram:** b6-slide06-scope-deliverable

---

## References (not in deck)

Whiteboard pictures, review comments, full map, DRI tables: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md - not completely captured).
All changes committed in git for traceabilty and restore previous state and forensics
