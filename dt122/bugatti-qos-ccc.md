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
**Meta:** Diwakar Tundlam · 10 Jun 2026  
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

**Title:** Capabilities · classify and remark  
**Layout:** split  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- VLAN · DSCP · ESUN · UFH → TC
- Remark on egress
- ACL override
- Policer · ECN
- Queue · QoSMAP → CSB

---

## Slide 4

**Title:** Capacities · buffer-carving at CSB  
**Layout:** split  
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- Lossy / lossless pools
- Port tiers: 200G · 400G · 800G
- Carve sizes · admission
- PFC · pause · headroom
- Per-TC · egress queues

---

## Slide 5

**Title:** Constraints · CSB tables  
**Diagram:** b6-slide05-csb-ccc-tables

---

## Slide 6

**Title:** Scope · deliverable  
**Diagram:** b6-slide06-scope-deliverable

---

## Reference (not in deck)

Full map, DRI tables, whiteboard annotations: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
