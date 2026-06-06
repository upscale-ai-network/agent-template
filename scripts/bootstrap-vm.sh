#!/usr/bin/env bash
# One-shot vm litmus: uv + project deps. Idempotent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "==> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> uv: $(uv --version)"
uv sync
echo "==> Ready. Try: ./scripts/check-decks.sh  or  ./scripts/run-deck-build.sh"
