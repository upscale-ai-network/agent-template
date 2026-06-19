# AUTH-LEDGER — authorized servers (APPROVED PLAN)

**Status:** APPROVED — Phase A complete · Phase B/C tests in `tests/auth_ledger/`  
**Approved:** 2026-06-19  
**Scope:** Server **names only**. Authentication lives in SSH / keys / `authorized_keys` — exercised in separate layers, not in this file.

---

## 1. Purpose

Maintain a single registry of servers the owner operates so Gluon (and future tooling) knows **which hosts exist** in scope. Eliminates ad-hoc “which box?” drift without duplicating SSH configuration or credentials in git.

The NTP troubleshooting episode motivated this plan; it is **not** a requirement or test gate for the registry itself.

---

## 2. Principles

1. **Names only** — no SSH targets, keys, tiers, commands, or reach metadata in the ledger.
2. **Auth elsewhere** — connection and trust remain in `~/.ssh/config`, keys, and per-host `authorized_keys`.
3. **Layers separate** — registry → human SSH exercise → optional agent remote ops → law updates → scale. Do not merge layers in one step.
4. **Law later** — no `GLUON.md` / challenge changes until registry exists and a few operational tests have passed informally.
5. **No secrets in git** — ledger rows are names and optional non-sensitive notes only.
6. **Private repo** — host names may appear; repo stays owner-controlled (DT103).

---

## 3. Artifact

**File:** `AUTH-LEDGER.md` (repo root or `docs/` — set at implement)

**Format:**

```markdown
# AUTH-LEDGER — authorized servers

Authentication: SSH / keys / authorized_keys (not recorded here).

| # | Name | Notes |
|---|------|-------|
| 1 | linux-vm | Local virt on macOS |
| 2 | sw-hq-runner4 | Corp dev runner |
```

**Columns (normative):**

| Column | Required | Purpose |
|--------|----------|---------|
| `#` | yes | Stable reference for owner feedback (“see row 2”) |
| `Name` | yes | Canonical alias; matches how owner thinks about the host |
| `Notes` | no | One line; non-sensitive context only |

**Forbidden in notes:** passwords, keys, IPs (optional — owner may add later in notes if desired; v1 plan keeps notes minimal), internal URLs with tokens.

---

## 4. Initial registry (v1)

| # | Name | Notes |
|---|------|-------|
| 1 | linux-vm | Local virt on macOS |
| 2 | sw-hq-runner4 | Corp dev runner |

No third host until v1 process has been exercised on these two.

---

## 5. Lifecycle

| Action | Procedure |
|--------|-----------|
| **Add host** | New `#` + name + notes → owner commit → one line in `TASKS-LOG.md` |
| **Rename** | Edit name; leave old name in notes once: `was: old-name` |
| **Retire** | Delete row or note `retired YYYY-MM-DD` — owner judgment |
| **Review** | Owner spot-check when adding host or on monthly tune (DT117) |

---

## 6. Rollout phases (sequential)

| Phase | Activity | Exit criterion |
|-------|----------|----------------|
| **A — Registry** | Create `AUTH-LEDGER.md` with §4 rows | File in git; owner OK |
| **B — SSH (human)** | Owner logs into each named host via existing SSH setup | Both names reachable without agent |
| **C — Agent ops (optional)** | Gluon uses ledger as allowlist; SSH from Mac | Separate design; not part of this plan |
| **D — Law** | Update `GLUON.md` / challenge if needed | After Phase C feels reliable |
| **E — Scale** | Add rows for new servers | Repeat B (and C if adopted) per host |

**Deferred (not in v1 plan):** permission tiers, `REMOTE-OPS-LOG`, smoke scripts, NTP as acceptance test, DT133 task row, runner mutate policy.

---

## 7. Corner cases

| Case | Handling |
|------|----------|
| Duplicate name | Reject at add; one canonical name per machine |
| Two names, one machine | Avoid; pick one |
| Host unreachable | SSH layer; ledger unchanged |
| Typo in name | Fix row; no auth change on machine |
| Agent in wrong chat/tab | Existing Gluon fail-closed; ledger does not fix |
| Confidential hostname | Owner judgment on notes column; repo stays private |

---

## 8. References

- `CHECKPOINT.md` — VM context (operational, not duplicated in ledger)
- `GLUON.md` D-06 — points here
- `TASKS-LOG.md` — add/change log entries

---

## 9. Execution checklist (Phase A — when ordered)

- [x] Create `AUTH-LEDGER.md` from §3 template with §4 rows
- [x] `tests/auth_ledger/` — SSH harness fixture + pytest (login · id · date · ntp-date skew)
- [x] `TASKS-LOG.md` entry: AUTH-LEDGER v1 live
- [ ] Owner commit when ready (DT119)

Phases B–E: B/C partial via pytest; D–E await separate orders.

---

*Approved plan. Supersedes draft v1/v2 exploration in this file’s history.*
