#!/usr/bin/env bash
# Export dt100 A3 pptx → PDF (PowerPoint) → PNGs (PyMuPDF). Run from repo root.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PPTX="$ROOT/dt100/qos-architecture.pptx"
PDF="$ROOT/assets/previews/a3-deck.pdf"
OUT="$ROOT/assets/previews/a3"
mkdir -p "$OUT"

osascript <<EOF
tell application "Microsoft PowerPoint"
    set pptPath to POSIX file "$PPTX"
    set pdfPath to POSIX file "$PDF"
    open pptPath
    delay 2
    save active presentation in pdfPath as save as PDF
    close active presentation saving no
end tell
EOF

python3 - "$PDF" "$OUT" <<'PY'
import fitz
import sys
from pathlib import Path
pdf = Path(sys.argv[1])
out = Path(sys.argv[2])
doc = fitz.open(pdf)
n = len(doc)
for i in range(n):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    pix.save(out / f"slide-{i:02d}.png")
doc.close()
print(f"Wrote {n} slides to {out}")
PY

open -g "$OUT"
