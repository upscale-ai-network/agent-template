# CCC walk (B6) — source of truth

**B6** = shorthand for this deck · share as **`bugatti-qos-ccc.pptx`** (ccc doc) — no `draft-` prefix unless back on draft-board.

**Single file for this deck:** slide titles, bullets, on-slide walk cues → `bugatti-qos-ccc.pptx` via `./scripts/run-deck-build.sh`.

**Presenter script (not in PPTX):** [bugatti-qos-ccc-presenter-notes.md](bugatti-qos-ccc-presenter-notes.md)

**Companion:** [bugatti-qos-architecture.md](bugatti-qos-architecture.md) (slides 1–2, then 3–4 after this walk). **Depth / walk map:** [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).

---

## Cover

**Title:** QoS buffer carving arch  
**Subtitle (navy):** Walk: vision → draft plan → owners → pipeline  
**Meta:** Open after qos-architecture slides 1–2 — role-play, not a handoff  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** Define task — after qos-architecture slides 1–2  
**Subtitle:** Beat 1 · ~1 min  
**Lead:** Transition — alignment deck framed situation + task; this walk defines how.

**Bullets:**
- Assumption: **qos-architecture** aligned on tape-out program bar + QoS RM wedge at CSB.
- Show validation machine, owners, QoS on logical pipeline — co-evolve plan live.
- Close on qos-architecture slides 3–4 (near-term scope + Friday alignment) — not repeated here.

---

## Slide 2

**Title:** Document discipline  
**Subtitle:** Beat 2 · thin  
**Lead:** Thin walk today; depth only if Gururaj redirects.

**Bullets:**
- Friday meeting: qos-architecture slides 1–2, then this walk (~6 beats).
- Next: expand swimlanes / integrated validation plans — format and depth per your steer.
- Not this walk: 50-page dump, full HW catalog.

---

## Slide 3

**Title:** Validation framework (I draft v0; peers align)  
**Subtitle:** Beat 2 · ~3 min  
**Lead:** Gates are v0 for group review — not unilateral.

**Bullets:**
- Product / program use cases
- Architecture validation ↔ datapath arch
- Management plane — SONiC / FBOSS → SAI
- Tape-out path: C-models → emulation / FPGA → silicon
- SDK + SAI gates before tape-out
- I socialize v0 gates for group review; peers own slice proof.

---

## Slide 4

**Title:** Who owns what (don't read every row)  
**Subtitle:** Beat 3 · ~2 min  
**Lead:** My lane first; peer DRIs in W order — then point at pipeline slide.

**Bullets:**
- Validation program + QoS RM: Diwakar Tundlam · QoSMAP · Queue · buffer carve at CSB
- Peer DRIs: Shafi Mohammad · L2/L3/Mirroring · Tippanna Hongal · ECMP/LAG/Counters · Tilak · L2 · Girish Kale · L3
- HW datapath / OCP ESUN: Rupa Budhia · SDK / SAI: SDK leads — consult, not my R
- Program mesh: Prasun Sinha · Scope / company external: Gururaj

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
**Caption:** Beat 4 · QoSMAP + Queue/buffer carve (me) · Shafi (L2/ACL) · Tippanna (ECMP/LAG/Counters) · Tilak (L2) · Girish (L3) · Rupa (parse/datapath)

---

## Slide 7

**Title:** On the picture — blocks and validation tie-in  
**Subtitle:** Beat 4 · optional detail  
**Lead:** Only if Gururaj asks — each block needs AV + software proof before silicon.

**Bullets:**
- Ingress / Parser — parse correctness with Rupa before OCP/BCM calls
- L2 — Shafi · Tilak · L3 — Girish · Forward: ECMP/LAG/Counters (Tippanna), QoSMAP (me) · Egress Queue/carve (me)
- I draft cross-block tape-out gates; block DRIs own slice proof (C-model → emulation)

---

## Slide 8

**Title:** Explicit deferrals (do not merge)  
**Subtitle:** Beat 5 · ~1 min  
**Lead:** Out of this walk — weekly sync, not merged plans.

**Bullets:**
- Rupa SDK/SAI/datapath layout — related, different plan; weekly sync
- OCP ESUN: coordinate with Rupa before vendor calls; company position through Gururaj
- Prabu execution mesh / bs-2 — round 2 unless you redirect

---

## Slide 9

**Title:** If you want me to drive — next beats  
**Subtitle:** Beat 6 · after mandate  
**Lead:** Offer only if asked — who must be in the room.

**Bullets:**
- Expand QoS buffer carving arch: swimlanes, DRI depth, integrated AV / C-model / datapath / SDK / SAI validation
- QoS RM HWv1 scope with HW datapath DRI (Rupa lane) — gates as we agree
- Cadence: Shafi, Tippanna, Rupa, Prasun — if Gururaj redirects drive to me
- Room list — offer here if you ask (not on qos-architecture slides)

---

## Slide 10

**Title:** What this walk is not  
**Subtitle:** Beat 5–6  
**Lead:** Boundaries — keeps Friday walkable.

**Bullets:**
- Not C40 / full HW digest · Not SDK program ownership day one
- Not AI/token policy · Not sponsor homework-check — walkable backup only
- Whiteboard backup: assets/dt100-whiteboards.md (only if asked)

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations, and boundaries: [bugatti-qos-ccc-reference.md](bugatti-qos-ccc-reference.md).
