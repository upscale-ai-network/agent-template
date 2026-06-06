# CCC walk presenter notes (B6) — not exported to PPTX

**Use:** Rehearse from this file; on-slide **Subtitle** + **Lead** lines are the walk cues in the deck.

**Flow:** A3 slides 1–2 → B6 (this deck) → A3 slides 3–4.

---

## Cover

Open only after qos-architecture slides 1–2 land. One line: *“I’ll define how — validation machine, owners, my QoS wedge on your pipeline slide.”*

---

## Slide 1 — Define task (~1 min)

A3 already framed **program bar** + **QoS RM at CSB**. This deck is **how** — not another PDF.

Co-evolve live: steer at gates; I drive technical detail day-to-day.

Do **not** re-close mandate here — that is A3 slides 3–4.

---

## Slide 2 — Document discipline

Friday walk stays thin by design. Peer L2/L3 already showed cost of 50-page dumps — you won’t get that from me.

If you want swimlanes or integrated validation depth, say format — I expand in ~1–2 weeks after mandate.

---

## Slide 3 — Validation framework (~3 min)

Walk top-to-bottom once. Emphasize: **v0 gates for group review** — Shafi, Tippanna, Rupa, SDK leads align on “done” per gate.

Mgmt plane: SONiC / FBOSS lands on SAI — adjacent to my lane, not my program ownership.

Prior roles: C-model + emulation before tape-out — adapt when Upscale models and access land.

---

## Slide 4 — Who owns what (~2 min)

**Don’t read every row.** Wedge first, peers in W order, Gururaj scope last — then pipeline slide.

- **Me:** validation program draft + QoS RM (QoSMAP, Queue, buffer carve at CSB).
- **Shafi → Tippanna → Tilak → Girish:** L2/L3/Mirroring · ECMP/LAG/Counters · L2 · L3.
- **Rupa:** datapath / OCP ESUN — weekly before vendor calls · **Prasun:** program mesh if asked.
- **Gururaj:** scope + company/OCP external — context band, not row-by-row read.

---

## Slide 5 — My wedge (~2 min)

HWv1 scope is explicit — no MPLS EXP, no IPv6 pri mapping yet.

ESUN: align buffer/TM direction with OCP context — coordinate with Rupa, not solo vendor calls.

QoSMAP = DSCP/TOS (and ESUN-QoS where applicable) → internal TC; Queue = egress scheduling attachment; carve at **CSB**.

---

## Slide 6 — Pipeline slide (center of walk)

**Spend most time here.** Use Gururaj’s logical pipeline PNG.

Point: **QoSMAP + Queue/carve** = my wedge; everything else = peer DRIs.

Caption names: Shafi L2/ACL, Tippanna ECMP/LAG/Counters, Tilak L2, Girish L3, Rupa parse/datapath.

---

## Slide 7 — Block detail (optional)

Only if he asks. Parser correctness with Rupa — if parse is ambiguous, QoS policy is built on sand.

Cross-block gates: I draft; block DRIs own C-model → emulation proof.

---

## Slide 8 — Defer (~1 min)

Rupa SDK layout is **related, different plan** — weekly sync, no Friday merge.

OCP: SW-arch voice on QoS/TM/ESUN — **Gururaj** carries company position externally.

Prabu bs-1/bs-2 — round 2 unless redirected.

---

## Slide 9 — Next beats (if asked)

Not committed until mandate. Offer: expanded swimlanes, QoS HWv1 gates with Rupa, cadence forum with named DRIs.

Room list: Shafi, Tippanna, Rupa, SDK lead, Prasun — only if he asks who must be in the room.

---

## Slide 10 — What this walk is not

Short boundary slide — use if conversation drifts to C40, AI policy, or full HW catalog.

Whiteboards: `assets/dt100-whiteboards.md` + `assets/pics/` — backup only.

---

## Close

Return to **A3 slides 3–4**: near-term scope + alignment checkpoints. Guru expects **concrete draft in next few days** — tape-out remains north star.
