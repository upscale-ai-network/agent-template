# Arch vision draft — manager review (P0)

**Superseded for Thu DT100** — use:

- **[../dt100/manager-arch-vision-a3.md](../dt100/manager-arch-vision-a3.md)** — hook (2–3 slides)
- **[../dt100/bugatti-qos-ccc.md](../dt100/bugatti-qos-ccc.md)** — plan (walkable backup)

**Below:** early hatch draft (week-1 table, 30–60d arc) — mine for facts; do not send as-is.

**Target:** 2–3 slides, Thu EOD
**Status:** Legacy v0
**Confidential — Upscale AI, Inc.**

---

## Slide 1 — Where I am (week 1)

**Title:** Onboarding posture — ready to execute once access lands

| Done | In flight | Blocked on access |
|------|-----------|-------------------|
| Dev environment (Mac, brew, uv, git/gh SSH) | Corp VPN from home verified | UNIX / SSH to build servers & lab |
| GitHub org access (`sonic-ztp` cloned) | Cursor / doc policy check with IT | `bugatti-model` and product repos |
| Task system + priorities hatched ([META.md](META.md)) | | GCP / AWS VM credentials |

**Message:** Infrastructure on my side is in place; **engineering velocity** is gated on **accounts, hosts, and repo access** — not tooling.

---

## Slide 2 — Technical focus (first 30–60 days)

**Title:** Proposed learning and contribution arc

**Near term (weeks 1–2)**
- Map team stack: SONiC / ZTP path (`sonic-ztp`), deployment and lab workflow
- Digest public scale-up networking context (OCP ESUN, Ultra Ethernet) — **no confidential paste into AI** until IT clears
- Align on what “good” looks like for my first code contribution (size, review bar, test expectations)

**Medium term (weeks 3–8)**
- First meaningful commits in an **approved org repo** (target TBD with you)
- Build fluency in Linux networking software workflow: build, test, SSH-based debug
- Close the loop: design doc → implementation → review → lab validation

**Explicitly not this week:** Deep product architecture commitments — need codebase + lab access first.

---

## Slide 3 — Ask + how we’ll track progress

**Title:** Alignment asks and cadence

**Asks (please confirm or redirect)**
1. **Priority repo** after access: `bugatti-model` vs `sonic-ztp` vs other?
2. **Lab / build host** path: jump host, hostname template, who provisions UNIX account?
3. **First deliverable shape:** bugfix, small feature, doc, or lab script?
4. **Arch vision depth:** is this deck the right granularity, or do you want a follow-on deep-dive in 2–3 weeks?

**How I’ll run the work**
- **P0** = your timeline (this alignment)
- **Tracker:** onboarding + access items in [work-progress-tracker canvas](file:///Users/dtundlam/.cursor/projects/empty-window/canvases/work-progress-tracker.canvas.tsx)
- **Weekly:** short status (done / in progress / blocked) — format per your preference

**Success at 60 days (draft — edit together)**
- [ ] SSH + build + test loop on team-standard host
- [ ] Merged PR(s) in agreed repo with review feedback incorporated
- [ ] Can explain one end-to-end path in the product stack (ZTP / networking — scope TBD)

---

## Conversion notes (for slides)

- Slide 1 → one table or 3 checkmarks (done / flight / blocked)
- Slide 2 → timeline or 2-column near/medium term
- Slide 3 → bullet asks + one “60-day success” line

---

## Open questions for you before Thu

- [ ] Manager name / team name for slide footer?
- [ ] Any product names safe to name on slides vs “TBD”?
- [ ] Thu EOD = send PDF, live 15 min, or async read?
