#!/usr/bin/env bash
# Zombie hatch audit — standby readiness probe (failover not declared).
#
# Live Gluon (Mac) moves the line; Linux zombie runs this after git sync.
# Proves: toolchain hatch + committed-artifact litmus. No npx, no regen, no pytest.
#
# Usage (from any directory; caller $PWD unchanged):
#   ~/diwakar-work/scripts/zombie-hatch-audit.sh
#   DIWAKAR_WORK=/path/to/clone ./scripts/zombie-hatch-audit.sh
#
# Expected clean output (tail):
#   HEAD after: <sha>
#   ==> Zombie bootstrap OK
#   All deck checks passed (md, PNGs, pptx)
#   ==> hatch audit OK
#
# Out of scope: node/npx, workflow pytest, build-decks (cross-OS .pptx drift).
# See CHECKPOINT.md § Multi-host Gluon.

REPO="${1:-${DIWAKAR_WORK:-$HOME/diwakar-work}}"

(
  set -euo pipefail
  cd "$REPO"

  echo "=== zombie hatch audit ==="
  echo "host: $(hostname) · arch: $(uname -m)"
  echo "repo: $REPO"
  echo "HEAD before: $(git rev-parse --short HEAD)"

  echo ""
  echo "=== required toolchain ==="
  for cmd in git curl python3; do
    command -v "$cmd" >/dev/null || {
      echo "FAIL: missing $cmd (install OS package)" >&2
      exit 1
    }
    echo "ok: $cmd"
  done

  echo ""
  echo "=== git sync (read-only zombie) ==="
  git fetch origin main
  git reset --hard origin/main
  echo "HEAD after: $(git rev-parse --short HEAD)"

  echo ""
  echo "=== bootstrap ==="
  export PATH="$HOME/.local/bin:$PATH"
  ./scripts/bootstrap-gluon-zombie.sh --skip-check

  echo ""
  echo "=== dev sync ==="
  uv sync --group dev

  echo ""
  echo "=== litmus (committed md / PNG / pptx; no regen) ==="
  uv run check-decks

  echo ""
  echo "=== hatch audit OK ==="
)
