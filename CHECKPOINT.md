# CHECKPOINT — session handoff

**When:** 2026-06-06 · Linux vm1 hatched  
**Authority:** git HEAD + this file · chat/canvas not authoritative

---

## Multi-host Gluon

| Host | Path | Role |
|------|------|------|
| **Mac Lepton** | `/Users/dtundlam/diwakar-work` | **Primary** — read/write Gluon |
| **Linux vm1** | `/home/diwakar/diwakar-work` | **Read-only zombie** — `git pull` · boot/read · **no** commit/push/edits |

No multi-agent sync protocol yet. vm1 is warm standby; human declares takeover if primary is lost. Multi-host sync → fix later (not tasked).

---

## Guru (closed loop)

- **SharePoint:** `bugatti-qos-architecture` = **final** A3 (1pm draft review → evening minimal-diff share)
- **Risk window:** open until Friday; **no de-risk email** unless he asks
- **Language:** no Guru “review” — solo DE flight; Friday 1:1 = mandate / light touch-in at gates
- **ccc delivery plan:** announce thin (if needed) → SharePoint `bugatti-qos-ccc` → **W team first** — no direct Guru review email

## B6 (in progress)

| Shorthand | Files | Status |
|-----------|-------|--------|
| **B6 / DT122** | `dt122/bugatti-qos-ccc.md` → `.pptx` | **DT122** `doing` — Mermaid 2A next |
| Share name | `bugatti-qos-ccc` | No `draft-` prefix — doc for review when complete |

**Build:** `./scripts/run-deck-build.sh` · edit md only  
**Strategy:** [dt122/ccc-strategy.md](dt122/ccc-strategy.md) — 2A → informal peer → gated formal

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

1. **DT122** — 2A Mermaid-aware slide upgrade · `dt122/bugatti-qos-ccc.md` → regen ([ccc-strategy.md](dt122/ccc-strategy.md) §5)
2. Human cold read → informal peer DRI huddle → SharePoint when ready
3. Friday: A3 1–2 → B6 walk → A3 3–4
