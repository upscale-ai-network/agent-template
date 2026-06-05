# Arch vision plan (B6) — source of truth

**Single file for this deck:** slide titles, bullets, notes → `manager-arch-vision-b6.pptx` via `./scripts/run-deck-build.sh`.

**Companion:** [manager-arch-vision-a3.md](manager-arch-vision-a3.md) (slides 1–2, then 3–4 after this walk). **Depth / walk map:** [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md).

---

## Cover

**Title:** Arch vision plan (B6)  
**Subtitle (navy):** Walk: machine → owners → pipeline → defer → Cx  
**Meta:** Open after Yes on A3  
**Tag:** Confidential — Upscale AI

---

## Slide 1

**Title:** Define task — after A3 slides 1–2  
**Subtitle:** Beat 1 · ~1 min

**Bullets:**
- Assumption: situation and task on A3 slides 1–2 are aligned.
- This walk: define the task — validation machine, owners, QoS wedge on pipeline — deferrals and Cx.
- After walk: A3 slides 3–4 — result and sponsorship (not repeated here).

---

## Slide 2

**Title:** Document discipline  
**Subtitle:** Beat 2 · thin

**Bullets:**
- Thu: A3 slides 1–2, then this deck (~6 beats).
- Next: Cx 2-pager — decisions, gates, open issues (~2 weeks).
- Not Thu: 50-page dump, full HW catalog.

---

## Slide 3

**Title:** Validation framework (I draft v0; peers align)  
**Subtitle:** Beat 2 · ~3 min

**Bullets:**
- Product / customer use cases
- Arch validation (AV) ↔ datapath arch
- Mgmt plane — SONiC / FBOSS lands
- SW validation: C-models → emulation / FPGA → silicon
- SDK + SAI done with explicit gates before tape-out
- I socialize v0 of done per gate for group review — not unilateral mandate.

---

## Slide 4

**Title:** Who owns what (don't read every row)  
**Subtitle:** Beat 3 · ~2 min

**Bullets:**
- Sponsor (Gururaj): exec alignment — external narrative
- Validation program + QoS RM: Diwakar Tundlam
- L2/L3 / ACL: Shafi Mohammad · ECMP / AV: Tippanna Hongal
- SDK / SAI: SDK leads — consult, not my R
- Program mesh: Prasun Sinha · HW datapath / OCP: Rupa Budhia

---

## Slide 5

**Title:** My wedge — QoS / RM (HWv1)  
**Subtitle:** Beat 4 · before pipeline

**Bullets:**
- VLAN-PRI, TOS/DSCP → queues → schedulers
- Buffer management and carving (resource manager)
- Port speed + queue/port policy coherence
- ESUN — align buffer/TM with standardization (OCP)
- HWv1 now: no MPLS EXP, no IPv6 priority mapping yet · HWv2: EXP + IPv6 pri

---

## Slide 6

**Title:** Your pipeline slide — my wedge (center of walk)  
**Image:** logical-pipeline-boss-slide.png  
**Caption:** Beat 4 · QoSMAP + Queue/buffer carve (me) · Shafi (L2/ACL) · Tippanna (ECMP) · Rupa (parse/datapath)

---

## Slide 7

**Title:** On the picture — blocks and validation tie-in  
**Subtitle:** Beat 4 · optional detail

**Bullets:**
- Ingress / Parser — align parse correctness with Rupa before OCP/BCM calls
- L2 — Shafi · Forward: ECMP (Tippanna), QoSMAP (me) · Egress Queue/carve (me)
- Each block: AV done + SW proof (C-model → emulation) before silicon — I draft cross-block gates

---

## Slide 8

**Title:** Defer on Thu (do not merge)  
**Subtitle:** Beat 5 · ~1 min

**Bullets:**
- Rupa SDK/SAI/datapath layout — related, different plan; weekly sync, not on Thu
- OCP ESUN: coordinate with Rupa before vendor calls; company position through Sponsor
- Prabu execution mesh / bs-2 — round 2 unless you redirect

---

## Slide 9

**Title:** ~2 weeks — Cx 2-pager  
**Subtitle:** Beat 6

**Bullets:**
- Decision: validation gate definitions (C-model / emu / pre-tapeout) v0
- Decision: QoS RM HWv1 scope sign-off with HW datapath DRI
- Open: access to models, lab, repos · Actions: cadence with Shafi, Tippanna, Rupa, Prasun
- If asked who must be in the room — offer here (not on A3)

---

## Slide 10

**Title:** What Thu is not  
**Subtitle:** Beat 5–6

**Bullets:**
- Not C40 / full HW digest · Not SDK program ownership day one
- Not AI/token policy · Not a second 50-pager — walkable backup only
- Whiteboard backup: assets/dt100-whiteboards.md (only if asked)

---

## Reference (not in deck)

Full walk map, DRI tables, whiteboard annotations, and boundaries: [manager-arch-vision-b6-reference.md](manager-arch-vision-b6-reference.md).
