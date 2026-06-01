# Presenter notes — ~5 minutes

**Audience:** Small internal group · Upscale AI  
**Tone:** Motivation, not training. Use the story before any acronyms.

---

## Slide 1 — Title (~20 sec)

- “Quick internal brief — not datacenter networking, but the MacBook side of ML.”
- Point at confidentiality badge: “Please don’t forward outside the company.”
- One line public hook: “We build scale-up/scale-out AI networking; this is literacy for when you touch models on Apple silicon.”

---

## Slide 2 — Story hook (~90 sec) **MOST IMPORTANT**

Read the quote slowly, then walk the three steps:

1. **Cluster world** — “At Upscale we live in milliseconds between GPUs. That’s the bottleneck we know.”
2. **Laptop world** — “On a Mac, CPU, GPU, and Neural Engine share one memory pool. There is no PCIe hop.”
3. **Insight** — “The bug is mental: we still write code like we’re copying to a discrete GPU.”

**Room engagement:** Pause and ask: “Who’s run PyTorch or MLX on a Mac and wasn’t sure where the work actually ran?” Wait for hands/nods.

If attention was lost in the first deck, this slide is the fix — **don’t skip it**.

---

## Slide 3 — Why us (~45 sec)

- Tie to public mission only (no insider product details): SkyHammer scale-up, open Ethernet scale-out, open standards.
- “This talk is for prototyping, demos, edge experiments, and reading Apple performance reports — not replacing your day job in networking.”
- Analogy: scale-out fabric (us) vs scale-up on one die (Apple) — same discipline, different layer.

---

## Slide 4 — Silicon (~45 sec)

- Three engines + UMA in plain language.
- One sentence takeaway: routing + measurement.

---

## Slide 5 — Software (~60 sec)

- Point at diagram left-to-right.
- ANE line: “It doesn’t make GPU cores faster; it absorbs compatible inference work.”

---

## Slide 6 — Path (~45 sec)

- “PDF has labs — we’re not doing them today.”
- Assign: buddy pair runs demo this week.

---

## Slide 7 — Live demo (~2–3 min)

### What you (and the room) are watching

| When | GPU History | Meaning |
|------|-------------|---------|
| Act 1 — build `a`, `b` | **Flat** | Lazy graph — MLX scheduled work, didn’t run it |
| Act 2 — `mx.eval(a @ b)` | **Spike** | Materialize — this is the “GPU turned on” moment |
| Act 3 — CPU matmul | GPU quiet, clock slow | Same API, different **engine** — routing, not memcpy |

**Contrast with CUDA habit:** no `.cuda()`, no “copy to device” line — unified memory + `mx.eval()`.

**Value for Upscale folks:** same instinct as picking scale-out vs scale-up — find where work actually runs, instrument, don’t assume the wrong bottleneck.

### Prep (before meeting)

```bash
cd /Users/dtundlam/Documents/apple-silicon-ml-study
uv sync
./demo.sh --quick   # optional dry run (~15s)
```

Open **Activity Monitor → Window → GPU History** on the projector *before* act 1.

### Script (demo prints cues — read them aloud)

```bash
./demo.sh
```

1. **Banner** — explain CUDA vs Apple in one sentence.
2. **Act 1** — “Graph should stay flat” (5s pause baked in).
3. **Act 2** — “Spike now” — largest matmul (~12k² on GPU).
4. **Act 3** — CPU contrast — wall clock proves engine choice matters.
5. **Act 4** — printed takeaways + ANE teaser discussion.

### Fallback

```bash
system_profiler SPHardwareDataType | head -12
```

---

## Timing cheat sheet

| Slide | Target |
|-------|--------|
| 1 Title | 0:20 |
| 2 Story | 1:30 |
| 3 Why us | 2:15 |
| 4 Silicon | 3:00 |
| 5 Software | 4:00 |
| 6 Path | 4:45 |
| 7 Demo | 7:30 (2–3 min demo + discussion) |

**Total:** ~6–8 min with demo.

---

## Regenerate PDFs

```bash
./generate-pdfs.sh
```
