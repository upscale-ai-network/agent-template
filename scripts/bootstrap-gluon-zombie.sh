#!/usr/bin/env bash
# Fresh Gluon zombie hatch — run once after git clone on standby host (vm1).
# Read-only role: bootstraps toolchain only; ONE live global Gluon writes on primary.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WITH_ZSH=0
WITH_ZSH_HISTORY=0
SKIP_CHECK=0

usage() {
  echo "Usage: $0 [--full] [--zsh-history] [--skip-check]"
  echo "  default   uv + uv sync"
  echo "  --full    + zsh dotfiles (archive/zsh/restore-linux.sh)"
  echo "  --zsh-history  merge archived zsh_history (only with --full)"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full) WITH_ZSH=1 ;;
    --zsh-history) WITH_ZSH_HISTORY=1; WITH_ZSH=1 ;;
    --skip-check) SKIP_CHECK=1 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
  shift
done

echo "==> Gluon zombie bootstrap"
echo "    root: $ROOT"
echo "    role: read-only standby — do not commit/push in parallel with primary"

for cmd in git curl; do
  command -v "$cmd" >/dev/null || { echo "Missing required command: $cmd" >&2; exit 1; }
done

if ! command -v uv >/dev/null 2>&1; then
  echo "==> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
echo "==> uv: $(uv --version)"

echo "==> uv sync"
uv sync

if [[ "$WITH_ZSH" -eq 1 ]]; then
  echo "==> zsh restore (non-interactive)"
  export GLUON_ZOMBIE_BOOTSTRAP=1
  if [[ "$WITH_ZSH_HISTORY" -eq 1 ]]; then
    export GLUON_ZOMBIE_ZSH_HISTORY=1
  fi
  "$ROOT/archive/zsh/restore-linux.sh"
fi

if [[ "$SKIP_CHECK" -eq 0 ]]; then
  echo "==> deck litmus (read-only)"
  uv run check-decks
fi

echo "==> Zombie bootstrap OK"
echo "    regen (optional litmus): uv run build-decks"
echo "    primary Gluon: Mac Lepton — ONE live writer"
