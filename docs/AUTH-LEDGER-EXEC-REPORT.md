# AUTH-LEDGER — execution report (2026-06-19)

**Process note:** Inline fixes during execution are **forbidden** unless plan-scoped and reviewed. Findings flagged here; owner decides fixes.

---

## Run summary (first execution)

| Result | Count |
|--------|-------|
| Passed | 4 (ledger/harness metadata only, with buggy SSH flag) |
| Failed | 8 (all SSH integration tests — see bugs below) |

Re-run after bug fixes: 8 passed / 4 failed (linux-vm unreachable from agent env; runner4 passed when SSH flag was corrected **outside this report — reverted for review**).

---

## BUG-E1 — SSH harness invalid flag (execution bug)

| Field | Value |
|-------|-------|
| **Class** | **Execution bug** — test harness implementation error |
| **Not** | Plan / use-case bug — approved plan does not specify SSH invocation |
| **File** | `tests/auth_ledger/ssh_harness.py` |
| **Symptom** | `getifaddrs: atchMode=yes: no suitable addresses` |
| **Cause** | Used `-BatchMode=yes` as a single argv token; OpenSSH interprets `-B` separately; correct form is `-o BatchMode=yes` |
| **Owner note** | SSH login works from iTerm2; failure was harness, not host auth |
| **Status** | **Open** — flagged; inline fix reverted pending review |

---

## BUG-E2 — linux-vm unreachable from agent run (environment)

| Field | Value |
|-------|-------|
| **Class** | **Environment** — not plan defect, not host SSH misconfig |
| **Symptom** | `ssh: connect to host 192.168.64.3 port 22: No route to host` (after E1 corrected) |
| **Likely cause** | Local virt stopped and/or Cursor agent sandbox cannot reach LAN |
| **Owner note** | `ssh diwakar@192.168.64.3` works from Mac when VM is up |
| **Status** | **Open** — re-run `uv run pytest tests/auth_ledger -v` from Mac with VM up |

---

## Plan scope assessment

| Question | Answer |
|----------|--------|
| Is `-BatchMode` issue from the plan? | **No** — execution bug in pytest harness |
| Is ledger design wrong? | **No** — metadata tests passed |
| Should tests auto-fix during exec? | **No** — flag and report only |

---

## Awaiting owner

1. Approve/reject BUG-E1 fix (`-o BatchMode=yes`)
2. Re-run suite from Mac (linux-vm up)
3. Commit when ready (DT119)
