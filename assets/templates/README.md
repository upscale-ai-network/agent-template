# Slide templates (Gluon)

## Use this for new decks (validated)

**`upscale-company-template.pptx`** — 2 seed slides (cover + content). **Committed. Do not rebuild for routine work.**

1. Open in PowerPoint.
2. Duplicate slide 1 or 2.
3. Replace `[...]` placeholders.
4. Logo, footer, navy/gold layout stay.

Validation: [TEMPLATE-VALIDATION.md](TEMPLATE-VALIDATION.md)

```bash
python3 scripts/validate-company-template.py
python3 scripts/validate-all-pptx.py   # before any git check-in
```

Builds use atomic save + zip integrity checks — **Repair dialog should not appear** if validation passed.

---

## Scripts (DT100 / rare regen only)

| Script | When |
|--------|------|
| `validate-company-template.py` | Before every template commit |
| `build-company-template.py` | Only if CCC source or placeholders change |
| `build-dt100-decks.py` | Regenerate A3/B6 from markdown |
| `extract-empty-template.py` | Masters-only extract (not litmus) |

**Local only (gitignored):** `upscale-ccc-style-reference.pptx` (full CCC download)

---

## Files

| File | In git? | Purpose |
|------|---------|---------|
| `upscale-company-template.pptx` | **Yes** | Standard company deck — **your default** |
| `upscale-exec-empty.pptx` | Yes | 0-slide theme shell — not for new exec decks |
| `template-spec.md` | Yes | Hex/fonts from theme XML |
| `TEMPLATE-VALIDATION.md` | Yes | Litmus + validation log |
