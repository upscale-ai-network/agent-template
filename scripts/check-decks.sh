#!/usr/bin/env bash
# Validate DT100 deck sources and outputs — no writes, no silent fixes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
uv run python scripts/check_decks.py
