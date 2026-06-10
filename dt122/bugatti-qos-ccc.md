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
| 0.1 | Diwakar Tundlam | Buffer-carving CCC |

---

## Cover

**Title:** Buffer-carving CCC  
**Subtitle (navy):** Dynamic Switch-Buffer Management · logical pipeline  
**Meta:** Diwakar Tundlam · 5 Jun 2026  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Image:** logical-pipeline-boss-slide.png

---

## Slide 2

**Title:** QoS CCC scope  
**Lead:** QoSMAP → CSB buffer-carving → QoS-CCC  
**Diagram:** b6-slide02-pipeline-scope-pie

---

## Slide 3

**Title:** Capabilities · QoS classify and remark  
**Lead:** VLAN · DSCP · ESUN · UFH → TC on egress.  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- ACL can override remark policy.

---

## Slide 4

**Title:** Capacities · Buffer-carving at CSB  
**Lead:** Pool modes, carve sizes, admission, PFC — HW arch limits.  
**Diagram:** b6-slide04-csb-inset

---

## Slide 5

**Title:** Constraints · CSB buffer-carving  
**Diagram:** b6-slide05-csb-ccc-tables

---

## Slide 6

**Title:** Scope  
**Diagram:** b6-slide06-boundaries

---

## Slide 7

**Title:** Closing  
**Diagram:** b6-slide07-next-steps

---

## Reference (not in deck)

Full map, DRI tables, whiteboard annotations: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
