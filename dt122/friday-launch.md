# Friday launch — W + N alignment

**Not in PPTX.** Tactical playbook · **DT122 + DT126**  
**Abeyance:** git worktree / test detangle — after launch.

---

## Eisenhower (this week)

| Quadrant | Item | Status |
|----------|------|--------|
| **Do now** | Schedule Fri hold on NW calendar | **You** — N OOTO today |
| **Do now** | W scan of B6 (blocks, not bullets) | Send [w-review-brief.md](w-review-brief.md) |
| **Do now** | Dry run A3 1–2 → B6 → A3 3–4 | Thu EOD |
| **Schedule** | Regen pptx + SharePoint | After W OK on md |
| **Drop / later** | Worktree submit · route-#2 test split | Post-launch |

---

## Calendar (NW) — paste / send

**Subject:** Bugatti QoS — architecture walk + mandate alignment (A3 + B6)

| Field | Value |
|-------|--------|
| **When** | Friday **11:00–12:00** (local) |
| **Required** | **N** (Gururaj) — confirm when off OOTO |
| **Optional** | **W** peers (Shafi, Tippanna) — async pre-read if not attending |
| **Location** | NW calendar / Teams (your default) |

**Body (short):**

> Walk for Friday alignment: **A3** slides 1–2 (situation + task) → **B6** qos-ccc walk (vision, CSB buffer carve, scope·deliverable) → **A3** slides 3–4 (mandate + sponsorship).  
> Decks on SharePoint before the meeting. Expect iteration — not final sign-off.  
> *(Sent while N OOTO — please confirm slot.)*

---

## Run of show (~45–60 min)

```text
0:00   A3 cover + slides 1–2     Situation · task clarity
       ↓ gate: task framed OK?
0:10   B6 (bugatti-qos-ccc)      Slide 1 pie (pause) · Guru pipeline · Cap/Cap · tables · close
0:35   A3 slides 3–4             Mandate · sponsor alignment
0:50   Close                     Marching orders · buffer carve plan timing
```

| Do | Don't |
|----|--------|
| Welcome **his edits** | Defend draft as final |
| **Pause on pie** (slide 1) | Read bullets on B6 |
| **SAMPLE** on tables — verbal align | RACI / 50-page depth |

**Artifacts:** `dt100/bugatti-qos-architecture.pptx` · `dt122/bugatti-qos-ccc.pptx`

---

## W pre-read (before Friday)

Send peers [w-review-brief.md](w-review-brief.md) — 30 min scan:

1. **Slide 1** — pie / scope wedge (star)
2. **Slides 3–4** — split Cap/Cap bullets (HW arch ask)
3. **Slide 5** — CSB tables (SAMPLE)
4. **Slide 6** — scope · deliverable close

**Not asking:** line edits, Guru copy, filename churn.

---

## Open from Hongal pass (defer if W churn)

| Item | When |
|------|------|
| Pipeline annotations (slide 2 image) | After W; optional Fri rework |
| Pie wedge layout (orange detach, adj labels) | Post top-level W |
| Closing slide polish | After slides 3–6 stable |

Source: [hongal-review-2026-06-06.md](hongal-review-2026-06-06.md)

---

## Build before SharePoint

```bash
uv run build-decks
uv run build-decks-a3
uv run check-decks    # opt-in · md may lead pptx
```

Cold read both pptx — peer CCC bar — then upload.

---

## Done when (launch)

- [ ] Fri hold on NW calendar (N confirmed)
- [ ] W brief sent · at least one peer ack
- [ ] pptx regen · SharePoint · links in invite
- [ ] Dry run once · meta hooks in head
- [ ] Fri meeting held · mandate captured (notes, not deck)
