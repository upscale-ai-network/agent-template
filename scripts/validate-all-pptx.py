#!/usr/bin/env python3
"""Validate every committed PPTX in Gluon — run before check-in."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pptx_util import assert_pptx_valid  # noqa: E402

# Gluon-owned outputs (not gitignored reference)
PATHS = [
    ROOT / "assets/templates/upscale-company-template.pptx",
    ROOT / "assets/templates/upscale-exec-empty.pptx",
    ROOT / "dt100/bugatti-qos-architecture.pptx",
    ROOT / "dt100/manager-arch-vision-b6.pptx",
]


def main() -> int:
    failed = []
    for path in PATHS:
        if not path.exists():
            print(f"SKIP (missing): {path.name}")
            continue
        try:
            assert_pptx_valid(path)
            print(f"OK: {path.relative_to(ROOT)}")
        except ValueError as e:
            print(f"FAIL: {path.relative_to(ROOT)} — {e}")
            failed.append(path)

    if failed:
        print("\nFix: python3 scripts/build-company-template.py (template)")
        print("      python3 scripts/build-dt100-decks.py (A3/B6)")
        return 1
    print("\nAll PPTX valid — safe to open without Repair dialog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
