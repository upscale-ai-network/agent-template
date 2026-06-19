# Test layers

Scaled test runs: **full default** → **quickpass** → future **slices**.

SoT for quickpass membership: [`tests/layers.yaml`](../tests/layers.yaml)  
Taxonomy below maps to `uv run pytest -v` (34 collected; 29 selected by default).

---

## Commands

| Run | Command |
|-----|---------|
| **Full default** | `uv run pytest -v` |
| **Quickpass (basic acceptance)** | `uv run pytest-quickpass` or `uv run pytest -m quickpass` or `uv run pytest --basic-acceptance` |
| **Artifact parity (opt-in)** | `uv run pytest -m artifact_parity` |
| **Everything** | `uv run pytest -m ""` |

---

## Layer 0 — quickpass (7 tests)

One probe per **slice**; includes **workflow/npx** so Mermaid/Chrome failures surface (unlike old `breadth`).

| Slice | Test |
|-------|------|
| auth_ledger | `test_ledger_loads_two_hosts` |
| auth_ledger (SSH) | `test_ssh_login[linux-vm]`, `test_ssh_login[sw-hq-runner4]` |
| workflow_fast | `test_tc01_parse_canary_md_structure` |
| workflow | `test_tc03_render_produces_valid_pngs` |
| deck | `test_tc16[...][b6-build_production_b6_isolated]` |
| examples | `test_fib_base_values` |

**Grow rule:** add nodeids to `layers.yaml` + `@pytest.mark.quickpass` on that test (or param). Keep quickpass **small**; move depth to slice/full runs.

---

## Full taxonomy (A1–G5)

Partition of all collected tests. **Not** pytest markers (except where noted).

| Cat | ID | Tests |
|-----|-----|-------|
| **Q** | Q1–Q7 | quickpass layer (subset of rows below) |
| **B** | B1–B9 | auth_ledger — `-m "auth_ledger and not quickpass"` |
| **C** | C1–C2 | workflow fast |
| **D** | D1–D7 | workflow (npx) — `-m workflow` |
| **E** | E1 | deck default |
| **F** | F1–F2 | examples |
| **G** | G1–G5 | artifact_parity — excluded from default |

See session table A1–G5 in chat for nodeid list.

---

## Scaling to 1000s

1. **quickpass** — stay ~5–15 probes; edit `layers.yaml` only.
2. **slice_* ** — add yaml sections per subsystem; `uv run pytest $(yq ...)` or future `pytest-slice auth`.
3. **default** — keep fast; mark slow `@pytest.mark.workflow` / `@pytest.mark.artifact_parity`.
4. **CI** — quickpass on every push; full default nightly; parity on release.

---

## Deprecated

- `@pytest.mark.breadth` — removed; use `quickpass`.
