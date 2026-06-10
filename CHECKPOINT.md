# CHECKPOINT — session handoff

**When:** 2026-06-06 · active/standby ratified (failover not declared)  
**Authority:** git HEAD + this file · chat/canvas not authoritative

---

## Multi-host Gluon

| Host | Path | Role |
|------|------|------|
| **Mac Lepton** | `/Users/dtundlam/diwakar-work` | **Live Gluon** — forward line; read/write; commit/push when human says |
| **Linux vm1** | `/home/diwakar/diwakar-work` | **Zombie Gluon** — standby; `git fetch` + `reset --hard origin/main` only · **no** commit/push/edits |

**Ratified (2026-06-06):** Active/standby sync is **good enough for now**. Standby exists; **failover is not declared and not ready** — readiness probes only. Live Mac moves the repo; Linux runs **`./scripts/zombie-hatch-audit.sh`** after sync (bootstrap → `uv sync --group dev` → `check-decks`). Goal = **Linux vs Mac tool gaps**, not pytest green on standby. Out of scope: `node`/`npx`, workflow pytest, `build-decks` regen on Linux (cross-OS `.pptx` drift), fresh-clone DR drill. Human declares takeover if primary is lost.

**Discipline:** **ONE live global Gluon** at a time (Mac today). Two writers → divergent commits and checkpoint drift.

Zombie hatch audit (standby readiness) — **lambda** (shell already at repo clone; you own PWD):

```bash
git fetch origin main && git reset --hard origin/main
uv sync --group dev
uv run check-decks
```

Optional wrapper (any cwd): `./scripts/zombie-hatch-audit.sh`  
Zombie sync+regen (optional, heavier): `./scripts/zombie-pull-build.sh` · `git restore dt100/*.pptx dt122/*.pptx` before leave · **DT124** acceptance before stakeholder delivery · hermetic builds / multi-host automation → later.

---

## Guru (closed loop)

- **SharePoint:** `bugatti-qos-architecture` = **final** A3 (1pm draft review → evening minimal-diff share)
- **Risk window:** open until Friday; **no de-risk email** unless he asks
- **Language:** no Guru “review” — solo DE flight; Friday 1:1 = mandate / light touch-in at gates
- **ccc delivery plan:** announce thin (if needed) → SharePoint `bugatti-qos-ccc` → **W team first** — no direct Guru review email

## B6 (in progress)

| Shorthand | Files | Status |
|-----------|-------|--------|
| **B6 / DT122** | `dt122/bugatti-qos-ccc.md` → `.pptx` | **DT122** `doing` — **integrate** prior W qos-ccc (local read) → Rev 0.1 |
| Share name | `bugatti-qos-ccc` | No `draft-` prefix · W alignment before publish |
| Prior deck | SharePoint / laptop only | **Not in git** · Rev 0.0 credit unnamed |

**Build:** `uv run build-decks` · edit md only · after local ingest + human OK  
**Strategy:** [dt122/ccc-strategy.md](dt122/ccc-strategy.md) — integrate → 2A → informal peer → gated formal

## Layout

- **`dt100/`** — DT100 **done** · A3 sources + regen
- **`dt122/`** — DT122 **doing** · B6 / ccc sources

## Git

- **A3:** `dt100/` on `origin/main`
- **B6:** `dt122/` — task-scoped dir (git tracks moves)

## Human — do not ask Gluon to

- Commit/push without explicit OK (DT119 policy) — *exception: chief-of-staff may propose; human approves push to main*
- Email Guru performatively
- Open TASKS rows for tonight (credit-card debt accepted)

## Next autonomous queue (Gluon)

1. **DT122** — local ingest (human path + **ingest now**) → merge into md as Rev 0.1 · no prior pptx in git
2. Regen + cold read → informal W huddle → SharePoint when W-aligned
3. Rev line on cover/appendix: 0.0 original author (W) · 0.1 Diwakar Tundlam
