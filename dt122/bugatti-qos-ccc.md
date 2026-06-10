# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`** (ccc doc) — no `draft-` prefix unless back on draft-board.

**Single file for this deck:** slide titles, walk cues → `bugatti-qos-ccc.pptx` via `uv run build-decks`.

**Presenter script (not in PPTX):** [bugatti-qos-ccc-presenter-notes.md](bugatti-qos-ccc-presenter-notes.md)

**Companion:** [../dt100/bugatti-qos-architecture.md](../dt100/bugatti-qos-architecture.md) (slides 1–2, then 3–4 after this walk). **Depth / walk map:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

**Revision (cover or appendix):**

| Rev | Credit | Summary |
|-----|--------|---------|
| 0.0 | Original author (W) | Prior qos-ccc skeleton — unnamed ([ccc-strategy.md](ccc-strategy.md)) |
| 0.1 | Diwakar Tundlam | qos-architect · buffer carving wedge · W CCC hooks · Rev 0.1 draft |

**Role:** qos-architect — **buffer carving** wedge on the pipeline log; classify/remark = Shrawan lane; Cap/Cap/Con numbers for HW pools = **TODO** with Rupa + E.

---

## Cover

**Title:** QoS buffer carving arch  
**Subtitle (navy):** CCC walk — Capabilities · Capacities · Constraints  
**Meta:** Open after qos-architecture slides 1–2 · Rev 0.1 draft  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** CCC — datapath vocabulary  
**Subtitle:** Act I · one framework  
**Lead:** **Capability** = what · **Capacity** = how many · **Constraint** = how used — maps to header fields → TC → resources.  
**Diagram:** b6-slide01-ccc-framework

**Bullets:**
- Same framework as peer W CCC decks (ACL, ECMP, L2/L3, Mirror, QoS classify).
- Wedge deck — not a 50-pager; essence for qos-arch, starting at buffer carve.

---

## Slide 2

**Title:** Logical pipeline — W hooks on the log  
**Subtitle:** Act I · stitch story  
**Lead:** Packet path picks which CCC applies — peer DRIs on their blocks; I own QoSMAP · Queue · CSB carve.  
**Diagram:** b6-slide03-pipeline-annotated

**Caption:** L2 Tilak · L3/ESUN Girish · ACL Shrawan · ECMP Hongal · QoS classify Shrawan · carve Diwakar · Mirror Shafi.

---

## Slide 3

**Title:** QoS classify & remark — W lane (interface)  
**Subtitle:** Act II · upstream of carve  
**Lead:** TC from VLAN .1p · DSCP · ESUN CoS · UFH DSCP — remark on egress; ACL can override. Detail in peer QoS Classification CCC.  
**Diagram:** b6-slide04-qos-stitch

**Bullets:**
- Shrawan DRI — full Cap/Cap/Con in QoS-Pkt-Classification & Remarking CCC.
- ECN · policer · WRED — same deck; not re-litigated here.
- Handoff to my wedge: **TC → queues → buffer @ CSB**.

---

## Slide 4

**Title:** Buffer carve @ CSB — my wedge  
**Subtitle:** Act II · qos-arch focus  
**Lead:** **Capability:** pool modes · sharing · lossy/lossless · **Capacity:** carve sizes · port tiers · **Constraint:** admission · PFC · speed coherence — v0 draft.  
**Diagram:** b6-slide04-csb-inset

**Bullets:**
- Near-term: buffer carve plan + gate v0 for W review.
- HW pool / RTL numbers — slide 5 TODO; sync Rupa + E.

---

## Slide 5

**Title:** Scope · HW TODO · peer CCC refs  
**Subtitle:** Act III · boundaries  
**Lead:** In this walk vs deferred; cross-decks by reference (ECMP capacity in ECMP CCC, etc.).  
**Diagram:** b6-slide06-boundaries

**Bullets:**
- **TODO:** Cap/Cap/Con cells for IFP/ISB/CSB/EFP pools — owner HW arch / RTL · sync **Rupa** + E.
- Not merged: full SDK swimlanes · 50-page digest · peer CCC bodies (on SharePoint Arch–CCC).

---

## Slide 6

**Title:** Rev 0.1 · next steps  
**Subtitle:** Act III · forward  
**Lead:** Draft for steer — peer lane edits welcome; Friday walk if aligned.  
**Diagram:** b6-slide07-next-steps

**Bullets:**
- Rev 0.0 original author (W) · Rev 0.1 Diwakar Tundlam — qos-architect.
- Return to A3 slides 3–4 after this walk for mandate · alignment.

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
