# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`csb-buffer-carving-ccc.pptx`**.

**Single file for this deck:** slide titles → `csb-buffer-carving-ccc.pptx` via `uv run build-decks`.

**Flow:** [../dt100/csb-buffer-carving-architecture.md](../dt100/csb-buffer-carving-architecture.md) slides 1–2 → **B6** → A3 slides 3–4.

**Metadata (not in PPTX):** [csb-buffer-carving-ccc-meta.md](csb-buffer-carving-ccc-meta.md)

**Depth / reference:** [csb-buffer-carving-ccc-reference.md](csb-buffer-carving-ccc-reference.md).

**Revision (not exported — git / meta only):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author | Prior qos-ccc skeleton — unnamed ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | csb-buffer-carving-ccc |

---

## Cover

**Title:** csb-buffer-carving-ccc
**Subtitle (navy):** Static and dynamic buffer carving at Central Scheduler Block (CSB)
**Meta:** Diwakar Tundlam · 11 Jun 2026  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** csb-buffer-carving-ccc scope  
**Lead:** QoSMAP → buffer carving at CSB → csb-buffer-carving-ccc  
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
- (draft in progress ... RFC)
- Buffer-carving (CSB)
  - Port-speed bifurcation → static carve → scheduler configuration
  - TC → QoSMAP · queues · egress scheduler · per-port queue
- Classify · enqueue · remark
  - ESUN-UFH → TC (4 or 3-bit=8) — different MAC layer
  - AFH → (BCM: SUE) → vTC → VLAN · L3/DSCP → TC
  - EFH → VLAN · PRI → L3/DSCP → TC
- L2/L3 datapath · ACL · police · ECN · PFC · global pause (802.3x) control
- Other peer contexts
  - Dual-die Sky-Hammer · UCIe D2D · logical port mapping and X-connect verification
  - ECMP · Mirroring · Counters/Stats · sFlow · CPU punt · Control / Management plane handling
  - UA-Link (**descoped) — same PHY/PMD, different PCS/PMA

---

## Slide 4

**Title:** Capacities · CSB Resource Management
**Layout:** split
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- (draft in progress ... RFC)
- Port tiers · bifurcation table setup
  - 200G · 400G · 800G modes and rate mapping
  - Validating line-rate matching serdes and standard, optics tuning, etc.
- Buffer pools at CSB
  - Lossless pools — pause / PFC · with headroom / guarantees
  - Lossy pools — ECN · WRED controlled with qos-mapping
- Carve control
  - Static and dynamic pool sizing
  - Traffic-aware congestion management (WRED? Tail-drop, packet-id retire/drops)
- Egress bandwidth scheduling (EBS)
  - Per-TC queues · WFQ/SPQ · Total port bandwidth
  - ECMP DLB · entropy / dynamic readjust / re-write / encap size adjusting
- Other considerations (ideas..)
  - AI/XPU workload rebalance · SDN/controller alignment

---

## Slide 5

**Title:** Constraints · CSB table sizes, limits, combinations
**Title:** (samples only - review with HW arch and publish)
**Diagram:** b6-slide05-csb-ccc-tables

---

## Slide 6

**Title:** Scope · deliverable
**Diagram:** b6-slide06-scope-deliverable

---

## References (not in deck)

Whiteboard pictures, review comments, full map, DRI tables: [csb-buffer-carving-ccc-reference.md](csb-buffer-carving-ccc-reference.md - not completely captured).
All changes committed in git for traceabilty and restore previous state and forensics
