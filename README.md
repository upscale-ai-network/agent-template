# diwakar-work

**Private workbench** — internal learning materials, demos, and scripts for Upscale AI work.

**Task system (P(-1) hatch):** see **[META.md](META.md)** — Px priorities, triage vs P2, WFQ bandwidth model, and how this repo fits onboarding + P0 work.  
**Not** a team/product repo: copy code *out* into project repos when something should be shared and maintained.

**Confidential — Upscale AI, Inc. Do not distribute.**

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
├── META.md                # P(-1) hatch — Px, triage, WFQ (closed; see Hatch status)
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
