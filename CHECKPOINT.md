# CHECKPOINT — session handoff

**When:** 2026-06-06 (eve) · active/standby ratified (failover not declared)  
**Authority:** git HEAD + this file · chat/canvas not authoritative

---

## Mandate (Satish huddle · 2026-06-06)

- **Guru tracking XLS:** Diwakar = **Datapath arch DRI** (program row — wider than qos wedge alone).
- **Confirmed on Satish laptop:** name replaces **“New Hire — Starting soon”** → **N delivered his piece.**
- **Pending:** Satish sends copy of **your row** (scope · peers · green) → add to Gluon when received · yap then.
- **Execution unchanged:** B6 = first scoped walk; buffer-carving plan + Cap/Cap/Con tables + W alignment + reflect in XLS when copy lands.

---

## Today → tonight

**Ratified (2026-06-06):** `bugatti-qos-ccc.pptx` **locked for Hongal 3pm** — draft approved by human; incorporate feedback only after review.

| When | What |
|------|------|
| **3pm** | **Hongal** — visual review `bugatti-qos-ccc.pptx` (local); incorporate feedback · regen |
| **Tonight (optional)** | SharePoint `bugatti-qos-ccc` after Hongal OK — W-first · no Guru review email |
| **Friday (TODO schedule)** | **N + W optional** — draft pending after final pptx + 3pm review |

Deck flow **as planned:** A3 bookends · B6 walk · Architecture Documentation after W-aligned.

---

## Multi-host Gluon

| Host | Path | Role |
|------|------|------|
| **Mac Lepton** | `/Users/dtundlam/diwakar-work` | **Live Gluon** — forward line; read/write; commit/push when human says |
| **Linux vm1** | `/home/diwakar/diwakar-work` | **Zombie Gluon** — standby; `git fetch` + `reset --hard origin/main` only · **no** commit/push/edits |

**Discipline:** **ONE live global Gluon** at a time (Mac today). Two writers → divergent commits and checkpoint drift.

Zombie hatch audit (standby readiness):

```bash
git fetch origin main && git reset --hard origin/main
uv sync --group dev
uv run check-decks
```

Optional: `./scripts/zombie-hatch-audit.sh` · **DT124** acceptance before stakeholder delivery.

---

## Guru (closed loop)

- **SharePoint:** `bugatti-qos-architecture` = **final** A3
- **Language:** no Guru “review” — walk / consensus; Friday = mandate touch-in at gates
- **ccc:** SharePoint `bugatti-qos-ccc` → **W first** after Hongal + regen

## B6 / DT122

| Shorthand | Files | Status |
|-----------|-------|--------|
| **B6** | `dt122/bugatti-qos-ccc.md` → `.pptx` | **Hongal-ready** · sharp Pillow flow PNGs (1800×720) · Cap/Cap/Con walk |
| Share name | `bugatti-qos-ccc` | Local until 3pm review · SharePoint tonight if OK |
| Meta | `bugatti-qos-ccc-meta.md` | Verbal hooks (Guru pipeline · vault QoS · Architecture Documentation) |

**Build:** `uv run build-decks` · edit md only  
**Strategy:** [dt122/ccc-strategy.md](dt122/ccc-strategy.md)

## Layout

- **`dt100/`** — DT100 **done** · A3
- **`dt122/`** — DT122 **doing** · B6 / ccc

## Human — do not ask Gluon to

- Commit/push without explicit OK (DT119 policy)
- Email Guru performatively
- SharePoint before Hongal feedback incorporated (unless human overrides)

## Next queue (Gluon)

1. Incorporate **Hongal 3pm** deltas → regen → cold read
2. **SharePoint** `bugatti-qos-ccc` if human OK tonight
3. **Schedule Friday** N + W optional ([DT126](TASKS.md))
4. Ingest **Satish XLS row** when received → checkpoint + execution map
