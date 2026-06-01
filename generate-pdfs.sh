#!/usr/bin/env bash
# Generate PDFs from HTML using headless Chrome (macOS)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [[ ! -x "$CHROME" ]]; then
  echo "Chrome not found. Open slides.html and study-guide.html in a browser → Print → Save as PDF."
  exit 1
fi

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$DIR/Apple-Silicon-ML-Slides.pdf" \
  "file://$DIR/slides.html"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$DIR/Apple-Silicon-ML-Study-Guide.pdf" \
  "file://$DIR/study-guide.html"

echo "Created:"
echo "  $DIR/Apple-Silicon-ML-Slides.pdf"
echo "  $DIR/Apple-Silicon-ML-Study-Guide.pdf"
