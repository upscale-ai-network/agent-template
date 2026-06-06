# Deck acceptance tests — spec (not implemented)

**Task:** [TASKS.md](../TASKS.md) **DT124** · **After:** DT122 ccc ship

## Gap today

| Layer | Script | Proves |
|-------|--------|--------|
| **Build litmus** | `check-decks.sh` | md valid · PNGs exist · pptx opens · slide **count** |
| **Zombie regen** | `zombie-pull-build.sh` | Toolchain works cross-host |
| **Acceptance** | *missing* | pptx is **stakeholder-deliverable** |

Build success ≠ correct on-slide copy, layout, or delivery readiness.

## Acceptance framework (target)

1. **Extract** — pull visible text + alt text from built `.pptx` (python-pptx).
2. **Assert md ↔ pptx** — every on-slide title/bullet from md appears in deck; no orphan placeholders (`[...]`, `TODO`, `draft`, known nits).
3. **Deck-specific gates** — A3: cover labels, 4 diagrams embedded; B6: pipeline image, owner order strings, no banned terms ([guru-terms-sot.md](../assets/guru-terms-sot.md)).
4. **Report** — `scripts/accept-decks.sh` → pass/fail + diff of missing/extra strings; exit non-zero blocks delivery tag.
5. **Human optional** — checklist row in [dt122/ccc-strategy.md](../dt122/ccc-strategy.md) §2A cold-read; automation does not replace sponsor judgment.

## Done when (DT124)

- `accept-decks.py` runs after `run-deck-build.sh`
- Documented in `dt100/README.md` / `dt122/README.md` as delivery gate
- Zombie may run acceptance read-only; only **primary** marks deliverable
