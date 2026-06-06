# Arch vision plan (B6) — source of truth

**Single file for this deck:** slide titles, bullets, on-slide walk cues → `manager-arch-vision-b6.pptx` via `./scripts/run-deck-build.sh`.

**Presenter script (not in PPTX):** [manager-arch-vision-b6-presenter-notes.md](manager-arch-vision-b6-presenter-notes.md)

**Companion:** [qos-architecture-diwakar-tundlam.md](qos-architecture-diwakar-tundlam.md) (slides 1–2, then 3–4 after this walk). **Depth / walk map:** [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md).

---

## Cover

**Title:** QoS buffer carving arch  
**Subtitle (navy):** Walk: vision → draft plan → owners → pipeline  
**Meta:** Open after aligned on draft QoS slides — role-play, not a handoff  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** Define task — after draft QoS slides  
**Subtitle:** Beat 1 · ~1 min  
**Lead:** Transition — draft QoS slides framed situation + task; this walk defines how.

**Bullets:**
- Assumption: draft QoS slides aligned on program bar + QoS RM wedge.
- Show validation machine, owners, QoS on logical pipeline — co-evolve plan live.
- Close on draft QoS slides (near-term scope + alignment) — not repeated here.

---

## Slide 2

**Title:** Document discipline  
**Subtitle:** Beat 2 · thin  
**Lead:** Thin walk today; depth only if Gururaj redirects.

**Bullets:**
- Thu: draft QoS slides, then this deck (~6 beats).
- Next: expand swimlanes / integrated validation plans — format and depth per your steer.
- Not Thu: 50-page dump, full HW catalog.

---

## Slide 3

**Title:** Validation framework (I draft v0; peers align)  
**Subtitle:** Beat 2 · ~3 min  
**Lead:** Gates are v0 for group review — not unilateral.

**Bullets:**
- Product / customer use cases
- AV ↔ datapath arch
- Mgmt plane — SONiC / FBOSS lands
- Software validation: C-models → emulation / FPGA → silicon
- SDK + SAI done with explicit gates before tape-out
- I socialize v0 “done” per gate; peers own slice proof.

---

## Slide 4

**Title:** Who owns what (don't read every row)  
**Subtitle:** Beat 3 · ~2 min  
**Lead:** Name DRIs once; point at pipeline slide next.

**Bullets:**
- Gururaj: scope · company / OCP external
- Validation program + QoS RM: Diwakar Tundlam
- L2/L3 / ACL: Shafi Mohammad · ECMP / LAG / Counters · AV: Tippanna Hongal
- SDK / SAI: SDK leads — consult, not my R
- Program mesh: Prasun Sinha · HW datapath / OCP: Rupa Budhia

---

## Slide 5

**Title:** My wedge — QoS / RM (HWv1)  
**Subtitle:** Beat 4 · reference only (historical)  
**Lead:** Kept for reference — validation scope lives on slide 3 framework.

**Bullets:**
- VLAN-PRI, TOS/DSCP → queues → schedulers
- Buffer management and carving (resource manager)
- Port speed + queue/port policy coherence
- ESUN — align buffer/TM with standardization (OCP)
- HWv1: no MPLS EXP, no IPv6 priority mapping · HWv2: EXP + IPv6 pri

---

## Slide 6

**Title:** Your pipeline slide — my wedge (center of walk)  
**Image:** logical-pipeline-boss-slide.png  
**Caption:** Beat 4 · QoSMAP + Queue/buffer carve (me) · Shafi (L2/ACL) · Tippanna (ECMP / LAG / Counters) · Rupa (parse/datapath)

---

## Slide 7

**Title:** On the picture — blocks and validation tie-in  
**Subtitle:** Beat 4 · optional detail  
**Lead:** Only if Gururaj asks — each block needs AV + software proof before silicon.

**Bullets:**
- Ingress / Parser — parse correctness with Rupa before OCP/BCM calls
- L2 — Shafi · Forward: ECMP / LAG / Counters (Tippanna), QoSMAP (me) · Egress Queue/carve (me)
- I draft cross-block gates; block DRIs own slice proof (C-model → emulation)

---

## Slide 8

**Title:** Defer on Thu (do not merge)  
**Subtitle:** Beat 5 · ~1 min  
**Lead:** Explicitly out of Thu — weekly sync, not merged plans.

**Bullets:**
- Rupa SDK/SAI/datapath layout — related, different plan; weekly sync
- OCP ESUN: coordinate with Rupa before vendor calls; company position through Gururaj
- Prabu execution mesh / bs-2 — round 2 unless you redirect

---

## Slide 9

**Title:** If you want me to drive — next beats  
**Subtitle:** Beat 6 · not committed Thu  
**Lead:** Offer only if asked — who must be in the room.

**Bullets:**
- Expand QoS buffer carving arch: swimlanes, DRI depth, integrated AV / C-model / datapath / SDK / SAI validation
- QoS RM HWv1 scope with HW datapath DRI (Rupa lane) — gates as we agree
- Cadence: Shafi, Tippanna, Rupa, Prasun — if Gururaj redirects drive to me
- Room list — offer here if you ask (not on draft QoS slides)

---

## Slide 10

**Title:** What Thu is not  
**Subtitle:** Beat 5–6  
**Lead:** Boundaries — keeps Thu walkable.

**Bullets:**
- Not C40 / full HW digest · Not SDK program ownership day one
- Not AI/token policy · Not a second 50-pager — walkable backup only
- Whiteboard backup: assets/dt100-whiteboards.md (only if asked)

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations, and boundaries: [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md).
