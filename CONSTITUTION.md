# Constitution — initial (v0)

**Purpose:** Record how Gluon and this repo work **today**, so a fresh session can reload without canvas or chat. Not governance for its own sake — only what helps the workbench grow. Unknown future problems stay unsolved here.

*Template intent:* This tree is **your** instance first. If the pattern works ([TASKS.md](TASKS.md) **DT118**), others may copy it like a pre-made shell rc — optional agent name, optional edits, same stateless-git shape — not a mandated Upscale product.

**Amendments:** No formal process yet. Changes to law, priorities, or litmus rules are **your judgment** only. When you change them, commit; agents should not invent policy.

---

## Runtime model

| Term | Meaning |
|------|---------|
| **Binary** | This repo at a **git commit** (the tree on disk) |
| **Boot** | New agent session: no memory except what files say at HEAD |
| **Gluon** | Agent scoped to this repo; reads and edits files you allow |
| **Checkpoint** | Your `git commit` — durable state between sessions |

Sessions are **stateless**. Chat and canvas are **not** authoritative. Only committed files count.

**Concurrency:** Not supported. One human owns conflicts (merge, reorder, resolve). Do not assume two Gluon sessions or two machines editing at once without you reconciling.

---

## Three layers (do not confuse)

| Layer | Files | Changes |
|-------|-------|---------|
| **Law** | `CONSTITUTION.md`, `README.md`, `META.md` | Rare; you decide; big steps need your OK ([README](README.md)) |
| **State** | `TASKS.md`, `TASKS-LOG.md` | Often; status and log follow real work |
| **Heap** | Drafts, scripts, notes (e.g. `manager-arch-vision-draft.md`) | Work product — **not** policy unless reflected in a task row |

---

## Boot order (load sequence)

1. [README.md](README.md) — pace, big steps, litmus test
2. [META.md](META.md) — Px order, triage, hatch closed — **do not re-derive** unless asked
3. [TASKS.md](TASKS.md) — what is open now
4. [TASKS-LOG.md](TASKS-LOG.md) — optional; why something moved

---

## Invariants (v0)

1. Git files are source of truth; canvas/chat are not.
2. Px order: `P0 → P1 → TRIAGE → P2 → P3` ([META](META.md)).
3. Open task table: within each priority band, **`doing` → `next` → `open`** ([TASKS](TASKS.md)); one `doing` focus when possible.
4. No confidential push without your explicit approval.
5. Agent asks before **big steps** ([README](README.md)); you own commits and merge conflicts.

---

## Machines

| Name | Role |
|------|------|
| **Lepton** | This Mac — local clone and commit |
| **Proton** | Future cloud workstation — same binary, new host; litmus again after clone |
| **Gluon** | Agent process bound to this repo |

---

## What this file is not

- Not a metaphor document — skip tribal/OS framing unless it clarifies a decision.
- Not a complete spec — [README](README.md), [META](META.md), and [TASKS](TASKS.md) hold operational detail.
- Not immutable — you may rewrite v0 when friction appears; no amendment ceremony required.
