# TASKS

**Source of truth** for open work. Edit here; commit to git.  
**Rules:** [META.md](META.md) (Px order, triage, hatch vs run).  
**Not** chat history or Cursor canvas.

Update `status`: `open` | `doing` | `done` | `drop`

---

## TRIAGE (process — short bursts)

| id | task | status | notes |
|----|------|--------|-------|
| triage-offboard | Offboard audit: canvas + chat → git — anything tangible lost? | open | If yes: add rows to P1/P2 here; see checklist below |

**Offboard checklist (verify once):**
- [ ] Canvas click-state (`.canvas.data.json`) — still on disk under `~/.cursor/projects/.../canvases/`?
- [ ] `brew-dev-setup.canvas.tsx` / `work-progress-tracker.canvas.tsx` — copy any missing items into `TASKS.md`
- [ ] Decisions only in chat (VPN partial, privacy, paths) — captured in `TASKS.md`?
- [ ] Onboarding brew list — needed in repo or stay external?

---

## P0

| id | task | status | notes |
|----|------|--------|-------|
| p0-slides | 2–3 slide arch vision for manager | doing | `manager-arch-vision-draft.md` · Thu EOD |

---

## P1

| id | task | status | notes |
|----|------|--------|-------|
| p1-privacy | Cursor/doc use — HR / IT / mgmt OK for confidential | doing | Privacy Mode on; formal OK pending |
| p1-remote | Org git remote `upscale-ai-network/diwakar-work` + push policy | open | personal `origin` only today |
| p1-vpn | Corp VPN from home + internal tools (browser) | open | no SSH host yet |
| p1-unix | UNIX login + SSH (build servers, workstations) | open | IT/team |
| p1-ssh | `~/.ssh/config` jump hosts — template from team | open | |
| p1-cloud | GCP + AWS VM access (office account) | open | |
| p1-bugatti | `bugatti-model` repo access + clone | open | |

---

## P2

| id | task | status | notes |
|----|------|--------|-------|
| p2-toolchain | Remote workspace + toolchain on build servers | open | after SSH |
| p2-agents | Cursor remote agents — policy + setup | open | after IT |
| p2-specs | Tech arch digest: OCP ESUN + Ultra Ethernet | open | public specs only until policy OK |
| p2-sonic | Explore `sonic-ztp` | open | cloned under `~/Projects` |
| p2-prune | Prune Apple Silicon GPU / demos from repo | open | move to `archive/` or branch |
| p2-tracker | Evolve task format / `TASKS.md` (was canvas Week 2) | open | after a week of use |
| p2-report | Weekly manager report — format + cadence | open | |
| p2-export | Plan lightweight MD export for new agents | open | optional |

---

## P3

| id | task | status | notes |
|----|------|--------|-------|
| p3-meta-monthly | Monthly review — tune `TASKS.md`, archive stale | open | ~4 weeks |

---

## Done

| id | task | notes |
|----|------|-------|
| done-hatch | Hatch closed — `TASKS.md` + META/README pointers | 2026-05-30 |
| done-hatch-git | `META.md`, README, P0 draft committed locally | |
| done-move | Repo at `~/diwakar-work` | |
| done-day1-2 | Mac setup, brew, uv, gh SSH, zsh/p10k, day-2 tools | see onboarding thread |
| done-clone | `sonic-ztp` clone verified | |
