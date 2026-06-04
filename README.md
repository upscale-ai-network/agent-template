# diwakar-work

**Private workbench** for Upscale AI — learning, drafts, and personal scripts.  
**Confidential — Upscale AI, Inc. Do not distribute.**

**Not** a team/product repo: promote code *out* to org repos when something should be shared.

---

## How this repo is run (read this first)

| File | Role |
|------|------|
| **[CONSTITUTION.md](CONSTITUTION.md)** | Initial v0 — runtime model, layers, boot order, invariants; amend by your judgment only |
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
- Bulk deletes (e.g. Apple Silicon prune) or large refactors
- Pushing to any remote with confidential content

### Rules (local git only, for now)

1. **Double-check** with the human before a big step — state what will change and wait for explicit OK.
2. **One concern per commit** — big steps get their **own** commit message; do not bundle with drive-by edits.
3. **Small steps** — prefer several small commits over one “cleanup” commit.
4. **No silent policy changes** — if behavior changes, update `README.md` or `META.md` in the same commit.
5. **Tasks follow work** — update [TASKS.md](TASKS.md) when status changes (same session or immediate follow-up commit).

### Later (when org remote + PRs exist)

- PR + human review required for big steps
- Until then: local `main` only; **no push** of confidential material without explicit approval ([TASKS.md](TASKS.md) `p1-remote`, `p1-privacy`)

---

## Fresh checkout — agent litmus test (human-run)

**Only you run this test** — in a new machine or new agent chat, no prior context.

1. `git clone` (or copy) `~/diwakar-work` and `cd` into it.
2. Open **CONSTITUTION.md** → confirm stateless boot, single-writer, three layers.
3. Open **README.md** (this file) → confirm deliberate-pace rules are visible.
4. Open **TASKS.md** → list open tasks; confirm **Priority** and **Title** columns; find P0 and P2 prune row.
5. Open **META.md** → confirm Px order; confirm hatch status matches your expectation.
6. Ask the agent: *“What is open in P0? Where are rules? Was hatch closed?”*
7. **Pass:** answers cite only these files, no canvas/chat; agent asks before proposing a big step.  
8. **Pass:** `TASKS.md` open table sorted `P0 → P1 → TRIAGE → P2 → P3`; within each band `doing` → `next` → `open`.  
9. **Fail:** agent invents tasks, merges big changes without asking, or re-derives Px/WFQ unprompted → fix docs, not the agent.  
10. **Fail:** any `doing` or `next` row appears below an `open` row in the same band → sort order broken.

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

```
TASKS.md                      # open work (DT | Priority | Status | Title | Due | Notes)
TASKS-LOG.md                  # DT activity log
META.md                       # Px, triage, hatch/run
README.md                     # this file — operating discipline
manager-arch-vision-draft.md  # P0 draft
…                             # workbench content below (Apple Silicon — prune planned P2)
```

---

## Workbench contents (Apple Silicon ML brief — P2 prune planned)

See [TASKS.md](TASKS.md) `p2-prune`. Content below is legacy/workbench until archived.

---

## Contents (Apple Silicon ML brief)

| Path | Purpose |
|------|---------|
| `Apple-Silicon-ML-Slides.pdf` / `slides.html` | 7-slide internal brief (~5 min) |
| `Apple-Silicon-ML-Study-Guide.pdf` / `study-guide.html` | Full phased study plan |
| `PRESENTER-NOTES.md` | Spoken script + demo timing |
| `demo.py` / `demo.sh` | Paced MLX demo (Activity Monitor + 4 acts) |
| `generate-pdfs.sh` | Rebuild PDFs from HTML (macOS + Chrome) |
| `assets/upscale-logo.webp` | Logo for slides |

---

## Clone parity (Mac or ARM Linux VM)

After `git clone`, every machine should run the same setup:

```bash
cd diwakar-work    # or your clone path

# 1) Install uv if missing (see below)
# 2) Create/sync the virtualenv from the lockfile
uv sync

# 3) Smoke test (Mac Apple Silicon only for full MLX demo)
./demo.sh --quick
```

| Step | Mac (Apple Silicon) | ARM Linux VM |
|------|---------------------|--------------|
| `git clone` | Yes | Yes |
| `uv sync` | Yes | Yes (venv + deps install) |
| `./demo.sh` (MLX GPU) | **Yes** | **No** — MLX targets Apple Silicon only |
| Slides / PDFs / HTML | Yes | Yes |
| `./generate-pdfs.sh` | Yes (needs Chrome) | Optional / regenerate on Mac |

**Takeaway:** Use this README + `uv.lock` to restore Python tooling anywhere; run the **MLX live demo on a Mac with Apple silicon**, not on a Linux VM.

---

## Python & tooling versions (pinned in repo)

| Tool | Version / constraint | Where defined |
|------|----------------------|---------------|
| **Python** | **3.12** (recommended) | `.python-version`, `requires-python >=3.10` in `pyproject.toml` |
| **uv** | **0.11.x** or newer | Install separately per machine |
| **mlx** | **0.31.2** | `uv.lock` |
| **mlx-metal** | **0.31.2** (transitive) | `uv.lock` — Apple GPU backend |

Check what a machine resolved after sync:

```bash
uv --version
uv run python --version
uv run python -c "import mlx.core as mx; print('mlx ok', mx.default_device())"
```

---

## uv setup (venv on each machine)

This project uses **uv** for env management (not `pip install` into system Python).

### Install uv

**macOS (Homebrew):**

```bash
brew install uv
```

**macOS / Linux (install script):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify:**

```bash
uv --version
```

### Create / refresh the virtualenv

From the repo root:

```bash
uv sync
```

- Creates **`.venv/`** in the repo (gitignored).
- Installs exact versions from **`uv.lock`**.
- `uv` will download **Python 3.12** if needed (via `.python-version`).

**After pulling new commits** (if `uv.lock` or `pyproject.toml` changed):

```bash
uv sync
```

### Run commands inside the venv

Prefer **`uv run`** (no manual `source .venv/bin/activate` required):

```bash
uv run python demo.py
uv run python demo.py --quick
./demo.sh              # wraps uv run
```

Optional — classic activate:

```bash
source .venv/bin/activate
python demo.py
deactivate
```

### Add a dependency later

```bash
uv add <package>
# commits: pyproject.toml + uv.lock — push both for parity on other machines
```

### If sync fails on a new machine

```bash
# Ensure Python 3.12 is available to uv
uv python install 3.12

# Clean recreate venv
rm -rf .venv
uv sync
```

---

## Demo

**Full paced demo (~2–3 min)** — open Activity Monitor → Window → GPU History first:

```bash
./demo.sh
```

**Quick test (no pauses):**

```bash
./demo.sh --quick
```

See `PRESENTER-NOTES.md` for what to watch (flat GPU graph → spike on `mx.eval`).

---

## Regenerate slide PDFs (macOS)

Requires Google Chrome:

```bash
./generate-pdfs.sh
# → Apple-Silicon-ML-Slides.pdf, Apple-Silicon-ML-Study-Guide.pdf
```

Or open `slides.html` / `study-guide.html` in a browser → Print → Save as PDF.

---

## Git remote (reference)

```bash
git remote -v
# origin  git@github.com:dtundlam/diwakar-work.git
```

Clone elsewhere:

```bash
git clone git@github.com:dtundlam/diwakar-work.git
cd diwakar-work
uv sync
```

Branching / merging: your workflow; this repo is a personal workbench.

---

## File layout

```
.
├── .python-version      # uv: use Python 3.12
├── .gitignore           # ignores .venv/
├── pyproject.toml       # project deps (mlx)
├── uv.lock              # lockfile — commit with pyproject.toml
├── TASKS.md               # open work — source of truth
├── META.md                # Px rules, hatch vs run
├── README.md
├── manager-arch-vision-draft.md   # P0 manager slides (draft)
├── PRESENTER-NOTES.md
├── demo.py
├── demo.sh
├── generate-pdfs.sh
├── slides.html
├── study-guide.html
├── assets/
└── *.pdf
```
