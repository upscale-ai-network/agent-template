#!/bin/sh
# Unit tests — sample programs under src/py (DT125 wiring smoke).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="${HOME}/.local/bin:${PATH}"
uv sync --group dev
uv run pytest tests/ -q
