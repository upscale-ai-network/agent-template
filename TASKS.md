# TASKS

**Source of truth** for open work. Edit here; commit to git.  
**Rules:** [META.md](META.md) · **Activity log:** [TASKS-LOG.md](TASKS-LOG.md)  
**Status:** `open` | `doing` | `done` | `drop`  
**Labels:** `DT###` — permanent id; do not reuse after close.

**Due:** optional date `YYYY-MM-DD` (not a hard deadline unless noted).

**Sort (litmus):** `P0 → P1 → TRIAGE → P2 → P3`; within each band **`doing` before `open`** — no `doing` row below any `open` row.

---

## Open tasks

| DT | Priority | Status | Title | Due | Notes |
|----|----------|--------|-------|-----|-------|
| DT100 | P0 | doing | 2–3 slide arch vision for manager | 2026-06-05 | `manager-arch-vision-draft.md` · Thu EOD · was `p0-slides` |
| DT102 | P1 | doing | Cursor/doc use — HR / IT / mgmt OK | | Privacy Mode on; formal OK pending |
| DT103 | P1 | open | Org git remote + push policy | | Local-only for now · `upscale-ai-network/diwakar-work` |
| DT104 | P1 | open | Corp VPN from home + internal tools | | Browser check; no SSH host yet |
| DT105 | P1 | open | UNIX login + SSH to build servers | | Blocked — IT/team |
| DT106 | P1 | open | SSH jump hosts + `~/.ssh/config` | | Template from team |
| DT107 | P1 | open | GCP + AWS VM access | | Office account · **Proton** later |
| DT108 | P1 | open | `bugatti-model` repo access + clone | | Not in org list yet |
| DT113 | P1 | open | Prune Apple Silicon GPU / demos from repo | | `archive/` or branch · elevated from P2 |
| DT101 | TRIAGE | open | Offboard audit: canvas + chat → git | | Anything lost? Add rows + log entry |
| DT109 | P2 | open | Remote workspace + toolchain on build servers | | After DT105–DT106 |
| DT110 | P2 | open | Cursor remote agents — policy + setup | | After DT102 |
| DT111 | P2 | open | Tech arch digest: OCP ESUN + Ultra Ethernet | | Public specs only until DT102 |
| DT112 | P2 | open | Explore `sonic-ztp` codebase | | `~/Projects/sonic-ztp` |
| DT114 | P2 | open | Evolve `TASKS.md` + `TASKS-LOG.md` format | | After ~1 week use |
| DT115 | P2 | open | Weekly manager report — format + cadence | | |
| DT116 | P2 | open | Plan lightweight MD export for new agents | | Optional |
| DT117 | P3 | open | Monthly review — tune tasks + log | | ~4 weeks |

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
