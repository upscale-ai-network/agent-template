# Arch vision plan (B6) — Gururaj review

**DT100 · P0 · Thu package**  
**Reader:** Gururaj (Sponsor) — cross-functional names where needed; not a company-wide deck.  
**Confidential — Upscale AI, Inc.**

**Companion:** [manager-arch-vision-a3.md](manager-arch-vision-a3.md) (abstract / hook — open first, ~10 s).  
**This file:** Full plan if you say **Yes** to the hook, or if you ask *“where’s the homework?”*

---

## 1. The question you need answered

**How do we ensure SW is done and validated** — aligned with product/customer intent, mgmt-plane deployment (SONiC/FBOSS-class), datapath architecture, and **ASIC/SDK/SAI schedule** — so SDK/SAI are tested against **C-models**, then **emulation/FPGA**, with clear “done” criteria **before HW tape-out**?

**My answer:** I will **drive** a repeatable **2-pager + validation-gate** machine; I am **DRI** on arch-vision framing and **QoS/resource-management (RM)** wedge; peer architects are **DRIs** on their slices.

---

## 2. Document discipline (AWS-style)

| Deliverable | Format | When |
|-------------|--------|------|
| Thu discussion | **A3** (2–3 slides) + this **B6** (≤6 sections, walkable) | Now |
| Next artifact | **Cx 2-pager** (decisions, gates, open issues) | ~2 weeks |
| Not Thu / not 2 weeks | 50-page arch dump, full HW catalog digest | After access + your steer |

Same lesson as peer L2/L3 work: full truth can exist; **exec read = 2-pager**. I will not ask you to read 50 pages.

---

## 3. End-to-end validation framework (I drive draft; peers align)

```text
  Product / customer use cases
           ↓
  Arch validation (AV) ↔ datapath arch
           ↓
  Mgmt plane — deployment-shaped (SONiC / FBOSS lands)
           ↓
  SW validation ↔ C-models → emulation / FPGA → silicon
           ↓
  SDK + SAI “done” with explicit gates before tape-out
```

**I will** socialize a **v0** of “done” per gate for **group review** — not unilateral mandate.  
**Prior discipline (my background):** pre-tapeout C-model and emulation validation in prior roles — adapted to Upscale assets **when** models and access land.

---

## 4. DRI map (B6 level)

| Area | DRI | I will |
|------|-----|--------|
| **Exec alignment / scope** | **Gururaj** (Sponsor) | Bring 2-pagers; you own external/exec narrative |
| **Arch vision + validation program** | **Diwakar Tundlam** | Draft framework; facilitate consensus |
| **QoS / buffer / queue / scheduler / RM carve** | **Diwakar Tundlam** | Author Cx slice + implementation path |
| **L2/L3 / ACL pipeline** | **Shafi Mohammad** | Align on shared validation story — his DRI |
| **Arch validation / use-case framing** | **Tippanna Hongal** | Align on AV methodology — his DRI |
| **SDK / SAI implementation** | SDK leads (e.g. Girish Kale, Shravan CS) | Consult on schema/path; not my R |
| **Program / sprint mesh** | Prasun Sinha (and team) | Align cadence — sneak peek below |
| **HW datapath / OCP ESUN** | **Rupa Budhia** | Weekly align before Thu OCP calls; SW-arch lane |

**Round 2:** Flesh RACI-like cadence and forums — not required for Thu Yes/No on premise.

---

## 5. My wedge — QoS resource management (RM)

**Scope I own (DRI):**

- Classification: **VLAN-PRI, TOS/DSCP** → queues → schedulers  
- **Buffer management and carving** (traffic / resource manager — MPLS-era analog)  
- **Port speed** and queue/port policy coherence  
- **ESUN** — align buffer/TM design with standardization direction (OCP context)

**HWv1 (now):** Above mapping; **no** MPLS EXP, **no** IPv6 priority mapping yet.  
**HWv2:** EXP + IPv6 pri — planned extension.

**Relation to your buffer-mgr ask:** I treat carving/RM as **my** technical DRI; arch-vision plan shows how it plugs into validation pyramid above.

---

## 6. Logical pipeline (boss slide — buffer mgr / carving context)

**Source:** Gururaj kickoff slide (SharePoint **PPTX**) with Rupa, Girish, and team — buffer manager + carving module.  
**Git copy (walk/export):** [assets/logical-pipeline-boss-slide.png](assets/logical-pipeline-boss-slide.png) — export one slide from PPTX if you need pixel parity in PDF backup.  
**Do not commit** SharePoint PPTX to `agent-template` unless IT/policy OK — link or export is enough for Thu.

**Ingress → lookup → forward → QoS → egress (logical blocks):**

| Stage | Blocks | DRI / align |
|-------|--------|-------------|
| **Ingress** | **Port** → **Parser** → **MyMAC** · **VLAN Membership** | Parse correctness with **Rupa** (per-packet unambiguous parse vs NOS header build) |
| **L2** | **L2-FBD** · **UFH** | **Shafi Mohammad** |
| **L3 / overlay** | **VRF** · **Intf** · **L3-FIB** · **ESUN FDB** | L3/ESUN peers + **Rupa** datapath |
| **Forward + QoS** | **ECMP** · **QoSMAP** | **ECMP:** Tippanna Hongal · **QoSMAP:** **me (QoS RM DRI)** |
| **Egress path** | **NH** · **LAG** · **IACL** · **Queue** · **Egress Port** · **EgrNH** · **EACL** | **Queue / buffer / carve:** **me** · **ACL:** **Shafi** |

**My wedge on this picture (not the whole pipe):**

- **QoSMAP** — VLAN-PRI / TOS-DSCP → queues/schedulers (HWv1); ESUN-aligned policy evolution  
- **Queue + buffer carving / RM** — resource manager behavior at egress (your charter)  
- **Port speed** coherence with queue/port policy  

**Validation tie-in:** Each block needs **AV “done”** against product use cases and **SW proof** (C-model → emulation) before silicon — I **draft** cross-block gates; block **DRIs** own slice proof.

**Correctness lens (Rupa thread):** If **Parser** / HW pipeline cannot classify a packet unambiguously, downstream QoSMAP/Queue policy is built on sand — I will align weekly with **Rupa** before OCP/BCM-facing calls.

### 6a. Gururaj whiteboards (annotated)

**Full annotations:** [manager-arch-vision-whiteboards.md](manager-arch-vision-whiteboards.md)  
**Images:** [assets/pics/arch-vision.jpeg](assets/pics/arch-vision.jpeg) · [assets/pics/first-1-1.jpeg](assets/pics/first-1-1.jpeg)

| Source | Adds to §6 |
|--------|------------|
| **arch-vision** | **Buffer carving** (200G/400G/800G→SDK); **lossy/lossless→PFC→Queues**; **WRED/ECN/PFC/Pause** APIs; **TC→queues**, **IPv4-TOS**, **ESUN-QoS**; HW path **IFP/ISB/CSB/EFP** (context) |
| **first-1-1** | **SONiC/FBOSS→SAI→SAI Adapter→USDK→ASIC**; **sai-router-crm**; ties validation pyramid to SDK delivery (see §7) |

**Delta vs PPTX alone:** Whiteboards make **RM/carve + congestion APIs** explicit — PPTX names blocks; boards name **behaviors and rates**.

---

## 7. Parallel track (explicitly **out of Thu scope**)

**Rupa Budhia** datapath/SDK/SAI validation layout (how to build SDK and validate against SAI) is **related but different** from this plan:

| This B6 (Thu) | Rupa / SDK thread |
|---------------|-------------------|
| How **I** run **DE** role + QoS RM + validation **framework** | How **SDK/SAI** binds to datapath variants |
| 2-pager arch vision for **Gururaj** | Engineering execution with HW/SDK leads |

**I will** stay aligned with Rupa (weekly sync) without merging the two plans on Thu.

---

## 8. External / OCP ESUN (coordinated, not solo)

- Attend OCP ESUN as you directed; **coordinate** with **Rupa Budhia** before Thu 8AM BCM/vendor-facing calls  
- **SW architect** on QoS/TM/ESUN — not full network-arch owner  
- **Company position:** through **you** (Sponsor) until you redirect

---

## 9. ~2 weeks → **Cx 2-pager** (draft outline)

1. **Decision:** Validation gate definitions (C-model / emu / pre-tapeout) v0  
2. **Decision:** QoS RM HWv1 scope sign-off with HW datapath DRI  
3. **Open issues:** Access to models, lab, repos  
4. **Actions:** Cadence with Shafi, Tippanna, Rupa, Prasun  
5. **Non-goals:** Full C40-class HW digest in Cx

---

## 10. Execution mesh (hook only — detail round 2)

- Align task intake with **SDK/ASIC milestones** and **SONiC/FBOSS** release cadence (~15-day lands)  
- **Prasun Sinha** — program touchpoint for sprint planning integration  
- **Prabu Dev** brainstorm (not Thu center): **qos mgr → qos api**; **HW DR/DV** ↔ **SW UR/AV** lockstep → **[chip SW SDK]**; **PM → data plan** — see [assets/pics/bs-1.jpeg](assets/pics/bs-1.jpeg) + [whiteboards](manager-arch-vision-whiteboards.md) §3  
- **Not Thu:** Full PM design or AI-scale GPU diagrams ([bs-2](assets/pics/bs-2.jpeg)) unless you redirect

---

## 11. Asks for Gururaj (Sponsor)

1. **Confirm** this framing answers your question — or redirect A3 premise if not.  
2. **Confirm** DRI split: me on arch-vision + QoS RM; **Shafi** / **Tippanna** on their slices.  
3. **Confirm** OCP/external: Rupa + me aligned; **you** approve company messaging.  
4. **Confirm** Thu deliverable: **A3** + walk **B6**; **Cx 2-pager** ~2 weeks.  
5. **Confirm** format: async PDF vs 15 min live vs Fri continuation (expected).  
6. **Step in** if peer alignment on validation gates stalls.

---

## 12. Boundaries (what Thu is not)

- Not a finished C40 or full HW-doc digest  
- Not claiming SDK/SAI program ownership day one  
- Not AI tooling / token policy (separate thread with Santosh)  
- Not 50-page substitute — **B6 is walkable backup**, not a second 50-pager

---

## Materials to merge (your action — unblocks polish)

- [x] Boss **Logical Pipeline** slide → §6 + `assets/logical-pipeline-boss-slide.png`  
- [x] Guru whiteboards → §6a + `assets/pics/` + [manager-arch-vision-whiteboards.md](manager-arch-vision-whiteboards.md)  
- [x] Prabu **bs-1/bs-2** → whiteboards §3–4 (bs-2 optional)  
- [ ] **Your correction pass** on whiteboards doc (checkboxes at bottom)  
- [ ] Export **A3** (+ optional B6 PDF) for Thu send
