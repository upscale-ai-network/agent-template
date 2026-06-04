#!/usr/bin/env bash
# DT100 deck build — uv Python + local mermaid-cli (npm).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="$ROOT/node_modules/.bin:${PATH:-}"
uv run python scripts/render-a3-diagrams.py
uv run python scripts/build-dt100-decks.py
