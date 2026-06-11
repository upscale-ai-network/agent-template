# Buffer-carving CCC (B6) — metadata · not exported to PPTX

Speaker hints, flow, and build context — never in `bugatti-qos-ccc.pptx`.

## Flow

A3 slides 1–2 → **B6** (this deck) → A3 slides 3–4.

## Verbal hooks (not on slides)

| Slide | Say |
|-------|-----|
| 1 · Scope pie | **Star slide** — pause for W; **CSB buffer-carving** bold on QoS wedge. |
| 2 · Logical pipeline | Guru kickoff image — shared program context (W yes; not for N). Annotations deferred. |
| 3 · Capabilities | Split: bullets left · diagram right — HW arch feature list (Rupa/E lane). |
| 4 · Capacities | CSB inset — lossy/lossless · tiers · carve · PFC/headroom. |
| 5 · Constraints tables | **SAMPLE** — align rows with HW arch; credible numbers with W guidance; Fri → refine. |
| 6 · Scope · deliverable | Top = bugatti-qos-ccc wedge; bottom = **qos-arch-ccc** artifact; **Datapath** band = program context — speak live. |

## Review notes (Prabhu · Hongal · 2026-06)

| Slide | Note |
|-------|------|
| 1 | Pie is the star — vision first; peers on slice labels are context only. |
| 2 | Guru kickoff — no duplicate title on image; pipeline annotation rework after W. |
| 3–4 | Split layout — expand bullets for HW arch; diagram carries blocks. |
| 5 | CCC tables — pause; SAMPLE watermark; Fri feedback → refine rows. |
| 6 | Closing diagram — you speak detail live; Datapath label on lower band. |

## Build

```bash
uv run build-decks
```

B6 PPTX: no speaker notes (scrubbed every build).

## Launch

Playbook: [friday-launch.md](friday-launch.md) · W ask: [w-review-brief.md](w-review-brief.md)
