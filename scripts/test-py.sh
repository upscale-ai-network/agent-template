#!/bin/sh
# Deprecated — use: uv sync --group dev && uv run pytest tests/ -q
set -e
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"
uv sync --group dev
exec uv run pytest tests/ "$@"
