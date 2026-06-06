import shutil
import subprocess

import pytest


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not on PATH")
def test_check_decks_uv_run():
    subprocess.run(["uv", "run", "check-decks"], check=True, timeout=120)


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not on PATH")
def test_build_decks_a3_uv_run():
    subprocess.run(["uv", "run", "build-decks-a3"], check=True, timeout=180)
