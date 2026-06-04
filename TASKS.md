# TASKS

**Source of truth** for open work. Edit here; commit to git.
**Rules:** [META.md](META.md) · **Activity log:** [TASKS-LOG.md](TASKS-LOG.md)
**Status:** `open` | `doing` | `next` | `done` | `drop`
**`next`:** one queued follow-on — visible while `doing` is elsewhere; not a second `doing`.
**Labels:** `DT###` — permanent id; do not reuse after close.

**Due:** optional date `YYYY-MM-DD` (not a hard deadline unless noted).

**Sort (litmus):** `P0 → P1 → TRIAGE → P2 → P3`; within each band **`doing` → `next` → `open`** — no higher-attention status below a lower one (e.g. no `doing`/`next` under `open`).

---

## Open tasks

| DT | Priority | Status | Title | Due | Notes |
|----|----------|--------|-------|-----|-------|
| DT100 | P0 | doing | 2–3 slide arch vision for manager | 2026-06-05 | **A3** · **B6** · plan [manager-arch-vision-dt100-plan.md](manager-arch-vision-dt100-plan.md) · Thu EOD |
| DT102 | P1 | open | Cursor/doc use — HR / IT / mgmt OK | | Privacy Mode on; formal OK pending |
| DT103 | P1 | open | Org git remote + push policy | | `origin` → `upscale-ai-network/agent-template` · push blocked until write access |
| DT104 | P1 | open | Corp VPN from home + internal tools | | Browser check; no SSH host yet |
| DT105 | P1 | open | UNIX login + SSH to build servers | | Blocked — IT/team |
| DT106 | P1 | open | SSH jump hosts + `~/.ssh/config` | | Template from team |
| DT107 | P1 | open | GCP + AWS VM access | | Office account · **Proton** later |
| DT108 | P1 | open | `bugatti-model` repo access + clone | | Not in org list yet |
| DT101 | TRIAGE | open | Offboard audit: canvas + chat → git | | Anything lost? Add rows + log entry |
| DT109 | P2 | open | Remote workspace + toolchain on build servers | | After DT105–DT106 |
| DT110 | P2 | open | Cursor remote agents — policy + setup | | After DT102 |
| DT111 | P2 | open | Tech arch digest: OCP ESUN + Ultra Ethernet | | Public specs only until DT102 |
| DT112 | P2 | open | Explore `sonic-ztp` codebase | | `~/Projects/sonic-ztp` |
| DT114 | P2 | open | Evolve `TASKS.md` + `TASKS-LOG.md` format | | After ~1 week use |
| DT115 | P2 | open | Weekly manager report — format + cadence | | |
| DT116 | P2 | open | Plan lightweight MD export for new agents | | Optional |
| DT119 | P2 | open | Git hooks: pre-commit / pre-push / agent commit gate | | Enforce rules in tooling, not trust · see **DT119** |
| DT120 | P2 | open | Pensieve → `origin.md` for Gluon constitution | | No PII / past-employer leak · Pensieve/Gluon separate · see **DT120** |
| DT121 | P3 | open | CLI toolbox — past tools list (loose) | | One task, many tools · see **DT121** |
| DT117 | P3 | open | Monthly review — tune tasks + log | | ~4 weeks |

### DT100 — arch vision (open)

**Plan:** [manager-arch-vision-dt100-plan.md](manager-arch-vision-dt100-plan.md)
**Slides:** [manager-arch-vision-a3.md](manager-arch-vision-a3.md) → export
**Walk:** [manager-arch-vision-b6.md](manager-arch-vision-b6.md)
**Done when:** plan checklist §10 complete — not “perfect arch”

---

### DT120 — Pensieve `origin.md` → Gluon (close origin story)

**Pending closure** for Gluon origin in [CONSTITUTION.md](CONSTITUTION.md) — pattern only, no mixing.

**You (via Pensieve):**

- [ ] Export sanitized **`origin.md`** — how Pensieve hatched Gluon; job-search → work transition
- [ ] **Redact:** past employer names, compensation, interviews detail, PII, anything not safe for Upscale repo
- [ ] Review with human eyes before any commit

**Gluon (after import):**

- [ ] Fold into constitution (or `origin.md` + pointer) — keep **separation** rule visible
- [ ] No Pensieve chat/canvas as authority — file in git only after review

**Done when:** `origin.md` in repo, constitution references it, origin story no longer “pending.”

---

### DT121 — CLI toolbox (loose inventory)

**Model:** One ongoing task; **append** tools you’ve used before — no per-tool DT rows. Status stays `open` until you decide it’s “good enough” or fold into README/brew doc.

**Not done when:** every tool is installed — only when the list feels captured for Lepton (and optional one-liner install notes).

| Tool | Role | Install (macOS) | Notes |
|------|------|-----------------|-------|
| **glow** | Color markdown in terminal | `brew install glow` | `glow TASKS.md` · `-p` pager · themes via `GLOW_STYLE` — **likely** the one you forgot |
| **mdcat** | Markdown → terminal (links, code) | `brew install mdcat` | `mdcat file.md` · alternative to glow |
| **bat** | Syntax-highlighted cat (incl. `.md`) | `brew install bat` | `bat README.md` · not markdown-specific |
| **mdless** | Markdown pager | `brew install mdless` | `mdless file.md` |

**Add rows as you remember** (git, ssh, jq, ripgrep, `gh`, `uv`, etc.) — loose bullets OK in Notes column.

- [ ] Confirm which MD viewer you used before (glow vs mdcat vs other)
- [ ] Install chosen viewer on Lepton if missing
- [ ] Append other “past CLI” tools when they surface (no new DT per tool)

---

### DT119 — git workflow hooks (enforce policy) — **plan only, not started**

**Status:** Task created after Gluon ran `git commit` without waiting for explicit human OK (rule break). User reminder: *been there, done that* — rules need **tools**, not trust. A **2-minute spike was implemented and reverted**; do **not** reuse spike code — rebuild carefully.

**Why:** README rule #6 (human-only commit/push) must be **enforced**, not documented only.

---

**Design goals (when executing):**

- Git-tracked hooks under repo (e.g. `hooks/`) + `core.hooksPath` via documented setup
- **Human one-shot unlock** before commit vs push (separate tokens)
- Agent may `git add` / diff; **cannot** commit/push without human running allow + explicit approval
- Optional belt: Cursor `beforeShellExecution` to block `git commit` / `git push` in agent shell
- Fail closed; no `--no-verify` in agent docs

**Spike notes (reverted — reference only):**

| Idea | Spike behavior | Rebuild consideration |
|------|----------------|----------------------|
| Commit gate | `.allow-commit` file, `pre-commit` check, `post-commit` delete | Gitignore tokens; naming; audit trail? |
| Push gate | `.allow-push`, `pre-push` consume | Separate from commit; confirm remote policy |
| Secrets | Block staged `.env`, `credentials.json`, `.pem` | Expand list; false positives |
| Scripts | `allow-commit.sh`, `allow-push.sh`, `setup-git-hooks.sh` | Review UX; document in README |
| commit-msg | Non-empty message | Optional `DT###` reference lint |

**Execution checklist (all open):**

- [ ] Design review with human (you) — no implementation until OK
- [ ] Implement tracked `hooks/` + `scripts/` + `hooks/README.md`
- [ ] `.gitignore` unlock token files
- [ ] Update README rule #6 with real paths
- [ ] Run `./scripts/setup-git-hooks.sh` on Lepton; test commit blocked / allowed
- [ ] Test agent cannot commit without allow (manual or Cursor hook)
- [ ] Optional: `DT###` in commit-msg; org GitHub rulesets later

**Not in scope (v1):** Org-wide rulesets; teaching agents `--no-verify`.

**Trigger:** After DT100 Thu EOD or when you explicitly schedule DT119 **doing**.

---

### DT101 checklist

- [ ] Canvas `.canvas.data.json` — still under `~/.cursor/projects/.../canvases/`?
- [ ] Copy any missing items into this table
- [ ] Chat-only decisions captured here?
- [ ] Onboarding brew list — repo or external?

---

## Done

| DT | Priority | Status | Title | Due | Notes |
|----|----------|--------|-------|-----|-------|
| DT090 | — | done | Deliberate pace + fresh-agent litmus in README | | commit `baf0058` |
| DT091 | — | done | Hatch closed | | `TASKS.md` + META · revisit via DT101 |
| DT092 | — | done | Hatch files committed locally | | META, README, P0 draft |
| DT093 | — | done | Repo moved to `~/diwakar-work` | | **Lepton** |
| DT094 | — | done | Mac dev setup (brew, uv, gh, zsh, day-2) | | |
| DT095 | — | done | `sonic-ztp` clone verified | | |
| DT118 | P0 | done | Test-run Gluon (fresh boot + litmus) | | Litmus pass · template intent in CONSTITUTION + notes below |
| DT113 | P1 | done | Prune Apple Silicon GPU / demos from repo | | Deleted from tree; recover from git history if needed |

### DT118 (closed — template notes)

First working Gluon instance validated from git (stateless boot, sort litmus, constitution load). **Full bar** (kill agent, erase chat, clone, new model → full recovery): [CONSTITUTION.md](CONSTITUTION.md) *North star* — goal, not required yet.

Pattern for others (optional copy, any agent name, any edits) — like a pre-made `/etc/zshrc` plus task-tracking agent:

| Idea | Analog |
|------|--------|
| Pre-wired agent + task shell | `/etc/profile` or `/etc/zshrc` — sensible defaults, not mandatory |
| Stateless agent + git memory | Agent runs when repo opens; law/state in committed files |
| Personal hatch | Clone/fork; rename agent or skip; amend by owner judgment |

**When publishing a template:** ship minimum (constitution, tasks, log, README); no confidential Upscale content without approval; template export is follow-on work (e.g. DT116), not blocked.
