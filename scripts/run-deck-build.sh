#!/usr/bin/env bash
# DT100 deck build — md → validated PNGs (PyMuPDF) → validated pptx.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
uv run python scripts/build-dt100-decks.py
