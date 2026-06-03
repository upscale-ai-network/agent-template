# META — hatching context (P(-1))

**Status:** Fixed for a long period (e.g. through year-end). Refine only as a **P2** item if real friction appears.

This file is the **shell** that hatches before P0/P1 work makes sense. It connects:

- **`diwakar-work`** — personal workbench (scripts, learning, drafts; copy *out* to product repos)
- **Onboarding / dev setup** — brew, `uv`, SSH, corp access, [work-progress-tracker](file:///Users/dtundlam/.cursor/projects/empty-window/canvases/work-progress-tracker.canvas.tsx)
- **Task handling** — Px priorities + triage + calendar bandwidth (WFQ analogy)

---

## Hatching metaphor (execution order)

```
  EGG                    HATCH (P-1)              RUN (P0+)
  ───                    ───────────              ────────
  diwakar-work           META.md + Px rules        Real tasks
  local / light          (this file)               manager slides,
  pipe-clean             define once               arch digest,
  infra: uv, git         lightly                   engineering repos
```

| Phase | Name | What happens |
|-------|------|----------------|
| **Egg** | Workbench exists | Folder + git; optional `dtundlam/diwakar-work`; **no confidential** on remote until org repo approved |
| **Hatch** | **P(-1)** | Agree how work is classified and scheduled — **not** doing the big tasks yet |
| **Run** | P0 → P1 → … | Execute inside the hatched shell |

**P(-1) is the hatching process itself** — figuratively: cracking the egg and establishing the operating system for everything else.

---

## Px stack (priority — strict order)

Highest → lowest:

1. **P0** — deadline / new boss / business-now (e.g. arch vision slides, Thu EOD)
2. **P1** — important, soon; after P0 blocks
3. **TRIAGE** — *process*, not a peer priority (15–20 min bursts; feeds the Px list)
4. **P2** — scheduled real work (already classified)
5. **P3** — backlog / idle
6. **P(-1)** — meta only: define or change this system (done for now)

**One line:** `P0 → P1 → [triage burst] → P2 → P3`

---

## Bandwidth (WFQ analogy) — calendar, not priority

Separate axis from Px **rank**:

| Scheduler | Task system |
|-----------|-------------|
| Strict q0, q1 | **P0, P1** — eat the morning first |
| WFQ flows | Each **P2 task** = one flow (equal weight by default) |
| One thin flow | **TRIAGE** = **one** aggregate queue (~one P2 slot); quantum = burst |

- Triage **classifies** incoming work → becomes P0–P3.
- Fairness among **P2 projects** is WFQ among flows.
- Triage does **not** get one full P2 flow per Slack thread.

Refine weights later as **P2** if needed — arbitrary is fine at hatch time.

---

## Workstreams (where threads belong)

| Stream | Home | Examples |
|--------|------|----------|
| **A. Onboarding / infra** | Dev-setup chat + tracker canvas | brew, `uv`, VPN, SSH, IT access, Cursor privacy |
| **B. Workbench** | `diwakar-work` (local → org when approved) | Apple Silicon brief, demos, personal scripts |
| **C. Job / product** | Org repos (`bugatti-*`, `sonic-*`, `usdk`, …) | Real engineering; clone when IT grants access |
| **D. Alignment** | Manager / arch | 2–3 slide vision draft; digest specs over 2–3 weeks |

**Px applies across A–D.** P0 is whatever your **new boss timeline** says — not “whatever inbox is loudest.”

---

## diwakar-work in the META picture

| Layer | Role |
|-------|------|
| **Git remote** | Approved company home when `upscale-ai-network/diwakar-work` exists; until then local or `dtundlam/*` for non-confidential pipe-clean only |
| **`uv` + `uv.lock`** | Clone parity across Mac / Linux VM ([README](README.md)) |
| **Content** | Experiments and drafts — **promote out** to org product repos when ready |

Workbench = **egg container**. META + Px = **how you decide what to put in the container and when.**

---

## Eisenhower (quick map)

| | Urgent | Not urgent |
|--|--------|------------|
| **Important** | P0, P1 | P2, org repo approval, engineering access |
| **Less important** | Most triage | P3, backup brew tools, WFQ tuning |

---

## Exit criteria for P(-1) — **met**

- [x] Px order agreed (P0 beats triage)
- [x] Triage ≠ P2; one aggregate triage flow (WFQ)
- [x] diwakar-work role vs org product repos
- [x] Remote policy: no confidential until IT/org repo
- [x] This file written — **stop tuning the system**

## Hatch status — **open**

- [x] `META.md` + `README.md` committed on local `main`
- [x] Repo at `~/diwakar-work`
- [x] P0 draft in repo: `manager-arch-vision-draft.md`
- [ ] **`TASKS.md`** — git source of truth for open work (see [TASKS.md](TASKS.md))
- [ ] Hatch closed in `TASKS.md` when task list + META pointer are stable
- [ ] Org remote `upscale-ai-network/diwakar-work` — **P1**, not a hatch gate

**Run phase (after hatch closes):** P0 arch vision (Thu EOD) → P1 access → P2 digest/repos.

**Do not re-tune Px/WFQ** — treat friction as **P2** tweak only.

---

## Agent / chat hygiene

- **Open tasks:** [TASKS.md](TASKS.md) only — not chat history, not canvas.
- **Rules / Px:** this `META.md` — do not re-derive P(-1) unless asked.
- **Onboarding infra** — separate chat ok; mirror status into `TASKS.md` when it changes.
