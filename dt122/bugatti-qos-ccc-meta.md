# Buffer-carving CCC (B6) — metadata · not exported to PPTX

Speaker hints, flow, and build context — never in `bugatti-qos-ccc.pptx`.

## Flow

qos architecture slides 1–2 → **B6** → qos architecture slides 3–4.

## Verbal hooks (not on slides)

| Slide | Say |
|-------|-----|
| 2 · Scope pie | **Star slide** — pause for W; **CSB buffer-carving** bold on QoS wedge. |
| 3 · Logical pipeline | Guru kickoff image — shared program context (W yes; not for N). Rework deferred. |
| 6 · Constraints tables | SAMPLE — align rows with HW arch; pull credible numbers from prior QoS depth / vault drafts with W guidance. |
| 7 · Scope · deliverable | Top = bugatti-qos-ccc wedge; bottom = **qos-arch-ccc** artifact; **full Datapath** band = program context — speak live. |

## Review notes (Prabhu · Hongal · 2026-06)

| Slide | Note |
|-------|------|
| 2 | Pie is the star — vision first; peers on slice labels are context only. |
| 3 | Guru kickoff image — no duplicate title; pipeline rework deferred. |
| 6 | CCC tables — pause; SAMPLE watermark; Friday feedback → refine rows. |
| 7 | Closing diagram only — you speak detail live. |

## Build

```bash
uv run build-decks
```

B6 PPTX: no speaker notes (scrubbed every build).
