#!/bin/sh
# Zombie sync + hatch + regen — subshell lambda; caller $PWD unchanged.
# Usage: zombie-pull-build.sh   (or set DIWAKAR_WORK)

REPO="${1:-${DIWAKAR_WORK:-$HOME/diwakar-work}}"

(
  set -e
  cd "$REPO"
  git pull origin main
  ./scripts/bootstrap-gluon-zombie.sh --full
  ./scripts/run-deck-build.sh
)
