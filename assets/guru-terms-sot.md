# Guru terms — source of truth (do not invent on slides)

**Sources (in repo):**

| Source | File |
|--------|------|
| Logical pipeline slide (Gururaj kickoff PPTX export) | [logical-pipeline-boss-slide.png](logical-pipeline-boss-slide.png) |
| Whiteboard — vision / QoS | [pics/arch-vision.jpeg](pics/arch-vision.jpeg) → [dt100-whiteboards.md](dt100-whiteboards.md) §2 |
| Whiteboard — mgmt / SDK stack | [pics/first-1-1.jpeg](pics/first-1-1.jpeg) → §1 |
| Plan — his question (paraphrase approved) | [../dt100/plan.md](../dt100/plan.md) §6 |

**Not Guru Thu center:** [pics/bs-1.jpeg](pics/bs-1.jpeg), [pics/bs-2.jpeg](pics/bs-2.jpeg) (Prabu) — AV/DV/UR labels only if he asks.

---

## His question (program — story A)

Use this spine, not “validation bar”:

> SW **done and validated** with product, mgmt plane, datapath/**AV**, **SDK/SAI before tape-out** — **C-model → emulation → silicon**.

Kickoff slide also names: **buffer manager + carving module** (logical pipeline context).

---

## Your DRI wedge (story B) — exact labels

| Use on slides | Guru / pipeline source | Avoid |
|---------------|------------------------|--------|
| **QoS RM** | arch-vision WB; plan §6 | “QoS carve” alone |
| **Buffer carving** | arch-vision WB (**Buffer carving**) | Generic “carve (CCC)” on slide |
| **QoSMAP** | logical pipeline slide | “QoS mapping” |
| **Queue** | logical pipeline (egress); WB **Queues QoS** | “buffer carve” without Queue |
| **ESUN** / **ESUN-QoS** / **ESUN FDB** | WB + pipeline **ESUN FDB** | Invented “ESUN align” only |

**Congestion (B6 / if asked):** lossy/lossless, **PFC**, **WRED**, **ECN**, **Pause** — arch-vision WB.

**Rates (if asked):** **200G / 400G / 800G** → SDK — arch-vision WB.

---

## Logical pipeline blocks (boss slide — exact spelling)

**Title on slide:** Logical Pipeline

Port → Parser → MyMAC · VLAN Membership → VRF · Intf · L3-FIB · L2-FBD · UFH · ESUN FDB → ECMP · QoSMAP → NH · LAG · IACL → Queue · Egress Port · EgrNH · EACL

**Your DRI on picture:** **QoSMAP** + **Queue** (buffer manager / carving at egress).

---

## Mgmt / SDK stack (first-1-1 WB — story A detail, B6 §7)

SONiC · PB (FBOSS-class) → **SAI** → **SAI ADAPTER** → **USDK API** → **ASIC** · **sai-router-crm** · **ESUN4**

---

## AV / validation words he uses

| Term | Where |
|------|--------|
| **AV** | **Architecture validation** (plan, bs-1) — spell out on A3 slides; say “AV” in notes after first use |
| **done and validated** | plan §6 boss question |
| **validation gates** | whiteboards §1 Thu line (spoken program) |

Avoid on slides: “validation bar”, “end-to-end HW-SW co-design” (not on Guru artifacts).

---

## A3 recommended on-slide vocabulary

| Slide | Title / lines |
|-------|----------------|
| **1** | **Dynamic Switch-Buffer Management** · sub: **Buffer carving at CSB** (internal **DBM**; **at** = location, not **for** datapath ownership) |
| **1** bullets | **done and validated** · product · mgmt · **Architecture validation** · **SDK/SAI** · **C-model → emulation → silicon** · **QoSMAP** · **Queue** · carve at **CSB** — **Rupa** owns datapath arch (notes) |
| **2** | **SW done and validated** before tape-out |
| **2** bullets | **My lane (QoS RM)** · **QoSMAP** · **Queue** · buffer carving · peers · **B6 pipeline walk** (Rupa seed — don’t rebrand as your title) |
| **3** | **Sprint scope · Fri close** — **2–3 month window** · SW↔HW validated · **AV · C-model / co-dev** · **SDK/SAI/mgmt → tape-out** |
| **4** | **Alignment · Fri close** — scope · slides 1–2 · **QoS RM lane boundary** · **Pipeline B6 walk-through** · **OCP · Rupa datapath** (Gururaj: company/OCP external — notes only) |

**Cover tagline:** **Dynamic Switch-Buffer Management** — not **Logical Pipeline** as DRI label. **Switch-Buffer** is one compound term (hyphenated). On-wall: full words; deliberate acronyms only (**CSB**, **SDK/SAI**, **QoSMAP**, **ECMP**, **OCP**). **AV** = architecture validation — spell out on slides.
