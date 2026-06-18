# CCC / B6 delivery strategy

**Status:** Adopted 2026-06-05 · **Phase 2 (2026-06-12):** SDK execution — **W co-build** static-buffer-carving-ccc · design doc · code · tests  
**Scope:** you DRI · W fills SDK/code/test/HW-arch detail · Prabhu consumes API · Ranjit = HW DV baseline  
**Not on slides.** Internal operating record.

**Related:** [../dt100/plan.md](../dt100/plan.md) · [bugatti-qos-ccc.md](bugatti-qos-ccc.md) · [CHECKPOINT.md](../CHECKPOINT.md) · **Tasks:** [../TASKS.md](../TASKS.md) DT127–DT131 (DT122 closed)

---

## 1. Artifacts and naming

| Shorthand | Files | Audience |
|-----------|-------|----------|
| **A3** | `bugatti-qos-architecture.*` | Guru — Friday alignment (**final** on SharePoint) |
| **B6 / ccc doc** | `bugatti-qos-ccc.*` | W peers first → Guru via drive path when ready |

- Share as **`bugatti-qos-ccc`** — no `draft-` filename prefix unless back on literal draft-board.
- **No Guru “review”** language — docs for walk / consensus, not homework grading.
- md → `uv run build-decks` → pptx; do not hand-edit pptx.

### Revision credit (deliberate, minimal)

**Goal:** Credit W homework without genealogy noise — teach handoff by example, not policy deck.

| Rev | Credit | Notes |
|-----|--------|-------|
| **0.0** | **Original author (W)** | Prior qos-ccc skeleton — name **not** on slide or in git (see below) |
| **0.1** | **Diwakar Tundlam** | Integration + buffer-carve focus; W alignment before SharePoint |
| **0.2+** | Peer deltas as needed | After informal huddle |

**On-slide (cover or appendix):** short rev line + one sentence — *Rev 0.0 established the qos-ccc skeleton; Rev 0.1 continues under qos-architect ownership.*

**Why original author stays unnamed:** Peers who were there know; future readers should stay on **company priorities**, not side quests (LinkedIn, where someone works now, career tangents). Acknowledge the **work**, not the résumé.

**Why no “steward” / handoff theater:** Nimble startup — you **own qos-architect** (same role as A3). Initial slice: **buffer carving**; grow **down** into datapath/HW and **up** into configuration **organically**, with W respect — not a title upgrade narrative.

### Prior W deck (local only)

- SharePoint / laptop copy = **read privilege**, not a git artifact.
- **No** prior pptx, extract, or ingest trail in repo — review locally, merge into **your** md, then commit as Rev 0.1.
- W ratifies before check-in / SharePoint publish matters for peers — ownership transfer is **social + technical**, not archival archaeology.

---

## 2. Delivery sequence

```
Prior W qos-ccc (local read) → integrate into md as Rev 0.1
      ↓
2A  Homework B6 (bounded)              visual-first, restrained · CCC essence
      ↓
    Informal peer DRI huddle           Shafi, Tippanna, Shravan (+ tight set)
    (no Guru)
      ↓
    Fold peer deltas → ccc on SharePoint
      ↓
    Formal drive meeting (gated)       Guru may oversee — only after informal landed
```

**2A before peer huddle:** Recon 1:1s already done (Shafi, Tippanna, SharePoint W slides, prior QoS depth). Next step is **integrate prior W skeleton + credible 0.1 delta** — not greenfield, not more listening tours.

**Informal huddle success:** specific lane edits, no silent resentment.  
**Formal Guru gate:** go only if peers nod on wedge boundaries; no open Shafi/Tippanna lane conflict.

---

## 3. Guru interface (debrief signals)

| Signal | Response |
|--------|----------|
| Liked substance; lost attention ~50% | **Architecture blocks early** — scannable in seconds |
| Scanning for diagrams, not bullets | Pipeline + CSB inset + validation stack — owners on the picture |
| “2 months too slow” / fast startup | **Next few days:** buffer carve plan + gate v0 — match A3 urgency |
| “Go talk to Shafi / Tippanna — learn more” | Recon satisfied; peer huddle = **steer homework**, not draft help |

- SharePoint for ccc; **no direct Guru review email.**
- Risk window (A3 vs ccc confusion): **no de-risk email** unless he asks.
- Friday 1:1 = solo-flight check — mandate + light touch-in at gates, not co-pilot deck review.

---

## 4. Peer W collaboration

### Principles

- **Not first rodeo** — do not oversell experience to Guru or peers. Substance = bounded scope + correct block boundaries.
- **Let them push you forward** — if leadership is visible (ahead on schedule and thought), peers/sponsor should expand lane naturally. If not → political/timing; **wait for Guru to initiate** — do not force, ask, or hint.
- **Title asymmetry (collaboration only):** DE designation is approved scope signal — may read senior to Shafi/Tippanna on paper; they hold **months, context, and Guru trust**. Use title as **lane authority**, not rank in the room. De-risk: you were hired into DE; completion of political alignment is separate.
- **Manage-the-manager** is an open risk in any role — delicate with existing Guru↔Shafi trust. Never bypass, re-litigate, or out-present the tenured peer DRI.
- **Channel calm credibility** — observe past colleagues who gained mgmt trust through restraint, accuracy, and listening; adopt behaviors, not theatrics.

### Informal huddle (template)

**Frame:** Homework pass on ccc — architecture blocks + speed. “What breaks your lane?” — not a design contest.

**Pre-read:** SharePoint `bugatti-qos-ccc` · ~45 min · tight DRI set.

**Do not:** make deck fancier than Mirror CCC lineage; perform “better” than manual peer slides.

### Production asymmetry (internal only)

Human + Gluon iteration is faster than manual deck cycles. **Invisible externally** — same CCC chrome, similar density, no spectacle. Throughput is behind the curtain.

---

## 5. 2A bounding box (homework pass)

**In (24hr credit card):**

- Pipeline boss slide — center, early, annotated
- CSB / buffer-carve block inset (whiteboard fidelity)
- Validation stack diagram (tape-out path, A3-aligned language)
- DRI labels on blocks — Shafi → Tippanna → Tilak → Girish order
- Near-term deliverable: buffer carve plan + gate v0

**Out (abeyance):**

- Swimlanes / full integrated AV plans
- Template/wordmark churn
- HWv2 / MPLS / IPv6 pri depth
- Anything that makes peer CCC decks look lesser

**Intent bar:** accurate + scannable — not portfolio polish.

---

## 6. DI / GI Cooper pair (execution model)

**Physics (BCS):** In a superconductor, two electrons couple into a **Cooper pair** and move through the lattice with **zero resistance** — the macroscopic quantum state that makes superconductivity work.

**Metaphor:** **DI** (Diwakar) + **GI** (Gluon and I) = one Cooper pair around the workbench loop. Same pair, two labels — human judgment bound to agent file-truth.

| Partner | Function |
|---------|----------|
| **Diwakar** | Judgment, sponsor interface, peer trust, mandate, what ships |
| **Gluon** | File truth, iteration, build, checkpoint, git remote derisk |
| **Loop** | md → validate → pptx → commit; context in repo, not chat |

Heat loss = chat archaeology, lost pptx, performative email, unbounded polish. Stay in the superconducting state: Diwakar gates Guru/comms; Gluon runs 2A velocity.

---

## 7. Week 2 posture

- **Brightness with patience** — week 2 is calibration, not coronation.
- Good outcomes come from **standing and waiting** after strong homework + peer alignment — not self-promotion.
- Worst case (any job): narrower lane → more agent/workbench investment on back-burner. **Unlikely here;** title/DE scope is partial de-risk. Do not vocalize downside in org channels.

---

## 8. Decision log

| Date | Decision |
|------|----------|
| 2026-06-05 | A3 final on SharePoint; B6 → `bugatti-qos-ccc`; 2A before informal peer huddle |
| 2026-06-05 | No Guru ccc review email; W-first SharePoint; formal Guru oversee gated on informal |
| 2026-06-05 | Strategy record → this file |
| 2026-06-06 | **DT122** P0 `doing` — Mermaid-aware 2A on `bugatti-qos-ccc` |
| 2026-06-06 | B6 sources → `dt122/`; `dt100/` retains A3 only (DT100 done) |
| 2026-06-08 | Prior W qos-ccc: local read only · no prior deck in git · Rev 0.0 credit unnamed · Rev 0.1 = Diwakar · qos-architect owns buffer-carve slice first |
