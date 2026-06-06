# Slide templates (Gluon)

## Deck build (DT100 / DT122)

**`upscale-ccc-style-reference.pptx`** — full CCC company chrome. **Committed.** Used by `uv run build-decks` (`scripts/build-dt100-decks.py`).

Do not hand-edit built decks in `dt100/` or `dt122/` — edit md and regen.

```bash
uv run build-decks       # A3 + B6
uv run build-decks-a3    # A3 only
uv run check-decks       # litmus
```

---

## Hand-edit template (optional)

**`upscale-company-template.pptx`** — 2 seed slides (cover + content). Duplicate slide 1 or 2 in PowerPoint; replace `[...]` placeholders.

**`upscale-exec-empty.pptx`** — theme/masters shell only — not for routine exec decks.

Manual checks before commit: open without Repair dialog; logo + footer on both slides; gold on navy cover panel.

Spec: [template-spec.md](template-spec.md) · [COMPANY-COLORS.md](COMPANY-COLORS.md)

---

## Files

| File | In git? | Purpose |
|------|---------|---------|
| `upscale-ccc-style-reference.pptx` | **Yes** | **Deck build source** |
| `upscale-company-template.pptx` | Yes | 2-slide seed — hand duplicate |
| `upscale-exec-empty.pptx` | Yes | Masters-only shell |
