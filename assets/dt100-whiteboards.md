# Whiteboard annotations — DT100 source material

**Confidential — Upscale AI, Inc.**
**Use:** Feed [dt122/bugatti-qos-ccc.md](../dt122/bugatti-qos-ccc.md); not on **A3** slides.

| File | Source | Thu use |
|------|--------|---------|
| [pics/first-1-1.jpeg](pics/first-1-1.jpeg) | **Gururaj** — first 1:1 | SDK/SAI stack context → B6 §7 |
| [pics/arch-vision.jpeg](pics/arch-vision.jpeg) | **Gururaj** — vision blocks | **Core** — QoS RM, buffer carve, ESUN |
| [pics/bs-1.jpeg](pics/bs-1.jpeg) | **Prabu Dev** brainstorm | Execution mesh → B6 §10 |
| [pics/bs-2.jpeg](pics/bs-2.jpeg) | **Prabu** brainstorm (cont.) | AI scale — **optional** |

---

## 1. `first-1-1.jpeg` — Gururaj 1:1 (mgmt / SDK stack)

**What I read on the board:**

| Block / label | Interpretation | B6 tie-in |
|---------------|----------------|-----------|
| **SONiC** + **PB** (FBOSS-class) | Mgmt/NOS lands on **SAI** | §3 mgmt plane |
| **SAI** → **SAI ADAPTER** → **USDK API** → **ASIC** | Vertical “SW done” stack | §7 Rupa thread (SDK validate SAI) — **adjacent**, not Thu merge |
| **L3** → **PKT** | Packet path from L3 | Logical pipeline §6 |
| **sai-router-crm** (circled) | Router CRM / resource model in SAI | QoS RM ↔ SAI objects (reference-document topic) |
| **ESUN4**, row/row_ok notes | ESUN + table/row semantics | §5 ESUN align |
| **CRM / L3** (right circle) | Control/resource plane with L3 | Cross-check **Tippanna** AV |

**Thu line:** *“I will align validation gates on the SAI→SDK→ASIC stack with SDK leads and Rupa; my DRI remains QoS RM on the logical pipeline.”*

**You correct:** [ ] PB = FBOSS? [ ] USDK naming [ ] sai-router-crm scope

---

## 2. `arch-vision.jpeg` — Gururaj vision blocks (your wedge)

**Top — strategy**

| Label | Note |
|-------|------|
| **Scale up** | Company scale-up networking context |
| **UAL / Pensando?, Eth → ESUN, AFH, UFH** | Ethernet branches; **ESUN** is your standards lane |
| **Meta, Msft, Arista, Bcm, Upscale** | Customer/vendor ecosystem |

**Left — buffer / QoS (your DRI)**

| Label | Note |
|-------|------|
| **Buffer carving** | **200G / 400G / 800G** → **SDK** → carving | Port-speed tiers |
| **lossy / lossless → PFC → Queues** | Buffer behavior + PFC |
| **Modified APIs: WRED, ECN, PFC, Pause** | Congestion feature set for HWv1 discussion |
| **Queues QoS, TC → Queue-4, ESUN-QoS, IPv4-TOS** | Maps to **QoSMAP** on logical pipeline slide |

**Left — silicon**

| Label | Note |
|-------|------|
| **D0 — UCIE D2D — D1**, **PCIe** | Multi-die; align **Rupa** |
| **Shaping / Policer** | Adjacent to QoS; scope boundary for reference document |

**Right — HW datapath (context, not full ownership)**

| Label | Note |
|-------|------|
| **CPUSS → PCIe** | Host path |
| **800G → MAC / NIG / IFP / ISB → CSB → EFP** | Ingress/egress fabric blocks |
| **MSN, 2×50G, LPO** | Port optics / speeds |

**Thu:** Walk **buffer carving + Queues QoS + ESUN**; show you see CSB/IFP context; **do not** present as full HW arch sign-off.

**You correct:** [ ] Pensando vs Pensad spelling [ ] ESUN-QoS vs ESUN4 from 1:1 board

---

## 3. `bs-1.jpeg` — Prabu brainstorm (SW alignment / PM) — **appendix**

**Not Thu center** — supports §10 “execution mesh” if Gururaj asks.

| Element | Interpretation |
|---------|----------------|
| **qos mgr** (hub) | Central QoS management — aligns with your charter |
| **qos api** (3 blocks) | API surface under mgr |
| **CLI → SLX** | Operator/config path |
| **HW: DR, DV** | Design + design verification |
| **SW: UR, AV** | Unit review + arch validation — **red dashed box** = HW/SW lockstep |
| **PM → Data plan** | Program drives data-plane plan — **Prasun** mesh |
| **[chip SW SDK]** | End state of validated SW |
| **$** near SDK | Cost/schedule pressure on SDK delivery |

**Thu one-liner (if asked):** *“Prabu and I mapped qos-mgr to HW DV and SW AV gates feeding SDK — I’ll align cadence with Prasun; details in round 2.”*

---

## 4. `bs-2.jpeg` — Prabu brainstorm (scale / AI context) — **optional**

**Appears to be:** PCIe switch → **TPB/HBM**, **GPU** pools, **RDMA/TCP/IP/Eth** stack, **BW vs delay** — AI scale-up networking bottleneck framing.

**Thu:** Omit unless Gururaj ties vision to AI cluster networking.
**Use:** Background for why scale-up networking matters; **not** DT100 proof.

**You correct:** [ ] Confirm this was same session as bs-1 [ ] Any Gururaj-owned content on this board

---

## Crosswalk: three Guru sources

| Concept | Logical pipeline PPTX | arch-vision WB | first-1-1 WB |
|---------|----------------------|----------------|--------------|
| QoS / queues | **QoSMAP**, **Queue** | Queues QoS, TC, PFC, WRED/ECN | qos via SAI/SDK |
| Buffer carve | egress **Queue** | Buffer carving 200–800G | sai-router-crm? |
| ESUN | **ESUN FDB** | ESUN branch + ESUN-QoS | ESUN4 |
| SDK/SAI | (via Girish/Shravan) | SDK arrow to carving | SAI → USDK → ASIC |
| AV/DV | (Tippanna / HW) | CSB datapath | HW/SW box in bs-1 |

---

## Your correction pass

Add inline fixes above, then tell Gluon “apply corrections to B6 §6–7, §10.”
