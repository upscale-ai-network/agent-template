# Slide templates (Gluon)

**In git for reuse:** `upscale-exec-empty.pptx` + `template-spec.md`

| Artifact | Use |
|----------|-----|
| **`upscale-exec-empty.pptx`** | Blank exec deck — theme/masters from company CCC deck; **0 slides**. Start here in PowerPoint for ad-hoc decks. |
| **`template-spec.md`** | Colors, fonts, slide size (from theme XML). |
| **`upscale-ccc-style-reference.pptx`** | Local only (gitignored) — full 32-slide CCC source for `build-dt100-decks.py`. |

## Regenerate empty template

```bash
python3 scripts/extract-empty-template.py ~/Downloads/Mirror-Sflow-Bugatti-ASIC-CCC.pptx
```

Source: SharePoint `Mirror-Sflow-Bugatti-ASIC-CCC.pptx` — do **not** commit that file unless IT OK.

## Styled DT100 decks (company chrome)

```bash
python3 scripts/build-dt100-decks.py
```

Clones **slide 0 (cover)** and **slide 2 (content)** from the local reference copy — logo, footer, navy/gold layout. Not from the empty template file.
