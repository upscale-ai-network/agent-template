#!/bin/sh
# Zombie sync + hatch + pytest + regen — subshell lambda; caller $PWD unchanged.
# Usage: zombie-pull-build.sh   (or set DIWAKAR_WORK)

REPO="${1:-${DIWAKAR_WORK:-$HOME/diwakar-work}}"

(
  set -e
  cd "$REPO"
  git fetch origin main
  git reset --hard origin/main
  export PATH="$HOME/.local/bin:$PATH"
  ./scripts/bootstrap-gluon-zombie.sh --full --skip-check
  uv sync --group dev
  uv run pytest tests/ -q
  uv run build-decks
  uv run check-decks
)
