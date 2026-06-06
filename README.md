# diwakar-work

**Private workbench** for Upscale AI — learning, drafts, and personal scripts.
**Confidential — Upscale AI, Inc. Do not distribute.**

**Not** a team/product repo: promote code *out* to org repos when something should be shared.

---

## How this repo is run (read this first)

| File | Role |
|------|------|
| **[CONSTITUTION.md](CONSTITUTION.md)** | Initial v0 — runtime model, layers, boot order, invariants; amend by your judgment only |
| **[GLUON.md](GLUON.md)** | Gluon identity, challenge, fail-closed ([GLUON-REQUIREMENTS-SPEC.md](GLUON-REQUIREMENTS-SPEC.md) imported) |
| **[README.md](README.md)** | Operating discipline + fresh-agent litmus test (this file) |
| **[TASKS.md](TASKS.md)** | Open work — **source of truth**; labels `DT###`; optional due |
| **[TASKS-LOG.md](TASKS-LOG.md)** | Task activity log (append-only, loose format) |
| **[META.md](META.md)** | Px priorities, triage, hatch vs run — do not re-derive unless asked |

**Offboarded:** Cursor canvas and chat history are **not** authoritative. Git files are.

---

## Deliberate pace — big steps need human intent

Until org remote + PR/review workflow exists, **go slowly**. The human owns merge-worthy decisions.

### What counts as a big step

- Closing or reopening **hatch**
- Declaring a phase “done” (onboarding, offboard, access)
- Renaming/moving the repo root
- Changing **source-of-truth** files (`TASKS.md`, `META.md`, this README)
- Bulk deletes or large refactors
- Pushing to any remote with confidential content

### Rules (local git only, for now)

1. **Double-check** with the human before a big step — state what will change and wait for explicit OK.
2. **One concern per commit** — big steps get their **own** commit message; do not bundle with drive-by edits.
3. **Small steps** — prefer several small commits over one “cleanup” commit.
4. **No silent policy changes** — if behavior changes, update `README.md` or `META.md` in the same commit.
5. **Tasks follow work** — update [TASKS.md](TASKS.md) when status changes (same session or immediate follow-up commit).
6. **Git commit/push** — **human explicit only** (*commit*, *push*, or pasted command). Agent may `git add` / show diff when asked; **do not run `git commit` or `git push`** without clear approval. Enforce via [DT119](TASKS.md) when built (not rushed).

### Later (when org remote + PRs exist)

- PR + human review required for big steps
- Until then: local `main` only; **no push** of confidential material without explicit approval ([TASKS.md](TASKS.md) `p1-remote`, `p1-privacy`)

---

## Fresh checkout — agent litmus test (human-run)

**North star (full bar):** kill agent, erase chat, clone repo, new model/host — Gluon recovers **fully** from git. See [CONSTITUTION.md](CONSTITUTION.md) *North star — full Gluon recovery*. **Not there yet; that’s ok** — this section is the test we run today.

**Only you run this test** — in a new machine or new agent chat, no prior context.

1. `git clone` (or copy) `~/diwakar-work` and `cd` into it.
2. Open **CONSTITUTION.md** → confirm stateless boot, single-writer, three layers.
3. Open **GLUON.md** → confirm challenge template and fail-closed rules.
4. Open **README.md** (this file) → confirm deliberate-pace rules are visible.
5. Open **TASKS.md** → list open tasks; confirm **Priority** and **Title** columns; find P0 row.
6. Open **META.md** → confirm Px order; confirm hatch status matches your expectation.
7. Ask the agent: *“What is open in P0? Where are rules? Was hatch closed?”*
8. **Pass:** answers cite only these files, no canvas/chat; agent asks before proposing a big step.
9. **Pass:** `TASKS.md` open table sorted `P0 → P1 → TRIAGE → P2 → P3`; within each band `doing` → `next` → `open`.
10. **Pass:** without challenge, agent refuses `git commit` / file writes (see **GLUON.md**).
11. **Fail:** agent invents tasks, merges big changes without asking, or re-derives Px/WFQ unprompted → fix docs, not the agent.
12. **Fail:** any `doing` or `next` row appears below an `open` row in the same band → sort order broken.

---

## Machines (names)

| Name | Role |
|------|------|
| **Lepton** | This MacBook Pro — local dev, clone, commit (`~/diwakar-work`) |
| **Proton** | Future cloud workstation (GCP/AWS workhorse) — not provisioned yet |
| **Gluon** | Agent that lives in this repo; context = committed files only |

---

## Git remote (pipe-clean)

| What | Where |
|------|--------|
| **Working copy (Gluon)** | `~/diwakar-work` on **Lepton** — this is the repo |
| **`origin`** | `git@github.com:upscale-ai-network/agent-template.git` — empty org home for Gluon/template |
| **Ignore** | `~/work/agent-template` — colleague’s dummy clone only; **not** a second checkout to use |

**Push:** `git push -u origin main` once you have **write** on `agent-template` ([TASKS.md](TASKS.md) DT103). Until then, work local; no `dtundlam/diwakar-work` remote configured.

---

## Repo map

| Path | Purpose |
|------|---------|
| `CONSTITUTION.md` | Gluon runtime contract |
| `TASKS.md` / `TASKS-LOG.md` | Work queue + log |
| `META.md` | Px / triage |
| `dt100/` | **DT100** done — A3 md + pptx ([`dt100/README.md`](dt100/README.md)) |
| `dt122/` | **DT122** doing — ccc / B6 md + pptx ([`dt122/README.md`](dt122/README.md)) |
| `scratch/` | Chat scratch / mini tasks (not task-scoped) |
| `archive/` | Portable snapshots (e.g. [zsh dotfiles](archive/zsh/)) |
| `src/py/` | Sample programs (pytest wiring smoke) |
| `src/gluon_cli/` | `uv run build-decks` / `check-decks` entry points |
| `scripts/` | **PPTX pipeline** Python — see [scripts/PPTX-PIPELINE.md](scripts/PPTX-PIPELINE.md) |
| `tests/` | `uv sync --group dev && uv run pytest tests/ -q` |
| `assets/` | Shared pipeline slide, whiteboard photos, templates |

**Removed (2026-06-04):** Apple Silicon MLX brief, demos, PDFs/HTML — history in git; future copy from archive repo if needed.

---

## Clone

```bash
git clone https://github.com/upscale-ai-network/agent-template.git diwakar-work
cd diwakar-work
```

**Primary (Mac):** write Gluon · after `uv sync`:

```bash
uv run build-decks          # A3 + B6
uv run build-decks-a3       # A3 only
uv run check-decks          # litmus (md, PNGs, pptx)
uv sync --group dev && uv run pytest tests/ -q
```

Entry points live in `src/gluon_cli/` (`[project.scripts]` in `pyproject.toml`). Legacy `scripts/*.sh` wrappers only `exec uv run …`.

**Zombie standby (Linux vm):** read-only · hatch once:

```bash
./scripts/bootstrap-gluon-zombie.sh --full
```

**From any directory (subshell lambda — caller `$PWD` unchanged):**

```sh
(
  set -e
  cd "${DIWAKAR_WORK:-$HOME/diwakar-work}"
  git fetch origin main
  git reset --hard origin/main
  export PATH="$HOME/.local/bin:$PATH"
  uv sync --group dev
  uv run pytest tests/ -q
  uv run build-decks
  uv run check-decks
)
```

Wrapper: `~/diwakar-work/scripts/zombie-pull-build.sh`

Installs **uv**, `uv sync`, zsh dotfiles, pytest, then regen + litmus. No parallel writes — see [CHECKPOINT.md](CHECKPOINT.md).

---

## File layout

```
.
├── CONSTITUTION.md
├── TASKS.md
├── TASKS-LOG.md
├── META.md
├── README.md
├── dt100/                         # DT100 done — A3
├── dt122/                         # DT122 — ccc / B6
├── scratch/                       # non-task scratch notes
└── assets/
    ├── logical-pipeline-boss-slide.png
    └── pics/
```
