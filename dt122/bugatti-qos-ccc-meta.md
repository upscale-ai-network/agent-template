# Buffer-carving CCC (B6) — metadata · not exported to PPTX

Speaker hints, flow, and build context — never in `bugatti-qos-ccc.pptx`.

## Flow

qos architecture slides 1–2 → **B6** → qos architecture slides 3–4.

## Verbal hooks (not on slides)

| Slide | Say |
|-------|-----|
| 2 · Logical pipeline | One-slider from Gururaj's kickoff vision — shared program context (W yes; not for N). |
| 6 · Constraints tables | SAMPLE — align rows with HW arch; pull credible numbers from prior QoS depth / vault drafts with W guidance. |
| 8 · Closing | Tables converge HW arch + peer QoS depth — doc follows when W-aligned (Architecture Documentation). |

## Review notes (Prabhu · 2026-06)

| Slide | Note |
|-------|------|
| 2 | Guru kickoff image — no duplicate title; W may ask origin (not N). |
| 3 | Pie — pause for W discussion; **CSB buffer-carving** bold on QoS slice. |
| 6 | CCC tables — pause; SAMPLE watermark; Friday feedback → refine rows. |
| 8 | Closing diagram only — you speak detail live. |

## Build

```bash
uv run build-decks
```

B6 PPTX: no speaker notes (scrubbed every build).
