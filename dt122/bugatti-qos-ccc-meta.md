# Buffer-carving CCC (B6) — metadata · not exported to PPTX

Speaker hints, flow, and build context live here — never in `bugatti-qos-ccc.pptx`.

## Flow

qos architecture slides 1–2 → **B6** → qos architecture slides 3–4 (alignment).

## Slide hints

| PPTX | Hint |
|------|------|
| Cover | Buffer-carving CCC — Capabilities · Capacities · Constraints frame. |
| 2 | Gururaj kickoff image — **verbatim export**; do not redraw. |
| 3 | Orange slice = buffer-carving scope; center = Bugatti ASIC. |
| 6 | CCC tables v0 — invite HW arch feedback on Cap/Cap/Con rows. |
| 8 | Closes loop to qos architecture alignment checkpoints. |

## Build

```bash
uv run build-decks
```

PPTX is speaker-notes-free by policy — scrubbed on every B6 build.
