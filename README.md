# Apple Silicon ML — Upscale AI Internal Brief

**Confidential — Upscale AI, Inc. Do not distribute.**

## Share with team

| File | Purpose |
|------|---------|
| **Apple-Silicon-ML-Slides.pdf** | 7-slide deck (~5 min): hook story, context, stack, **live demo** close |
| **Apple-Silicon-ML-Study-Guide.pdf** | Detailed companion: phases, labs, exit criteria |
| **PRESENTER-NOTES.md** | Spoken anecdote, timing, demo script |
| **demo.sh** / **demo.py** | Paced 4-act demo (~2–3 min); `./demo.sh --quick` to test |

## Presenting (~5 min)

1. **Lead with slide 2** (standup story) — don’t skip; fixes “no context” at open.
2. Run **slide 7 demo**: `uv sync` once, then Activity Monitor GPU History + `./demo.sh`.
3. See `PRESENTER-NOTES.md` for word-for-word cues.

## Edit & regenerate

- `slides.html` + `assets/upscale-logo.webp`
- `./generate-pdfs.sh` — rebuild PDFs (Chrome headless)
