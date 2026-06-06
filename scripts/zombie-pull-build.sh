#!/usr/bin/env bash
# Zombie sync + hatch + regen — subshell preserves caller $PWD.
# Usage: ./scripts/zombie-pull-build.sh [repo-path]
set -euo pipefail

REPO="${1:-${DIWAKAR_WORK:-$HOME/diwakar-work}}"

(
  cd "$REPO"
  echo "==> zombie-pull-build (subshell) repo=$PWD"
  git pull origin main
  ./scripts/bootstrap-gluon-zombie.sh --full
  ./scripts/run-deck-build.sh
)

echo "==> done (caller PWD unchanged: $(pwd -P))"
