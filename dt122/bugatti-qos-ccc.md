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

**Title:** Capabilities · Classify, Enqueue and Remark
**Layout:** split  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- (draft in progress ... )
- Buffer-carving path (CSB)
  - Port-speed bifurcation → static carve in CSB
  - QoSMAP · queues · egress scheduler · per-port queue
- Classify · enqueue · remark
  - ESUN-UFH → TC (4 or 3-bit=8) — different MAC layer
  - AFH → (BCM: SUE) → vTC → VLAN · L3/DSCP → TC
  - EFH → VLAN · PRI → L3/DSCP → TC
- L2/L3 datapath · ACL · policer · ECN · PFC · pause (802.3x)
- Peer context (not this wedge)
  - Dual-die Sky-Hammer · UCIe D2D
  - UA-Link (descoped) — same PHY/PMD, different PCS/PMA
  - ECMP · mirror · stats · sFlow · CPU punt

---

## Slide 4

**Title:** Capacities · buffer-carving at CSB  
**Layout:** split
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- (draft in progress ...)
- Port tiers · bifurcation
  - 200G · 400G · 800G modes and rate mapping
- Buffer pools at CSB
  - Lossless pools — pause / PFC · headroom
  - Lossy pools — ECN · WRED
- Carve control
  - Static and dynamic pool sizing
  - Traffic-aware congestion management
- Egress scheduling (context)
  - Per-TC queues · WFQ/SPQ · port bandwidth
- Out of wedge (peer / defer)
  - ECMP DLB · entropy / dynamic readjust
  - AI/XPU workload rebalance · SDN/controller alignment

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
