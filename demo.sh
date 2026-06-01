#!/usr/bin/env bash
# Educational MLX demo (~2–3 min paced) — uses uv
# Fast test: ./demo.sh --quick
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Install: https://docs.astral.sh/uv/"
  exit 1
fi

echo "Syncing mlx via uv..."
uv sync --quiet

exec uv run python demo.py "$@"
