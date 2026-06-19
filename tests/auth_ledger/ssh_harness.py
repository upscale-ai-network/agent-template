"""SSH test harness — not part of AUTH-LEDGER (auth lives in SSH)."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "auth-ledger-ssh.yaml"
DEFAULT_MAX_SKEW_SEC = 120


@dataclass(frozen=True)
class SshHostSpec:
    name: str
    ssh: str
    expect_user: str


def load_ssh_harness(path: Path | None = None) -> dict[str, SshHostSpec]:
    raw = yaml.safe_load((path or _FIXTURE).read_text(encoding="utf-8"))
    out: dict[str, SshHostSpec] = {}
    for name, cfg in raw["hosts"].items():
        out[name] = SshHostSpec(name=name, ssh=cfg["ssh"], expect_user=cfg["expect_user"])
    return out


def max_skew_seconds() -> int:
    return int(os.environ.get("AUTH_LEDGER_MAX_SKEW_SEC", DEFAULT_MAX_SKEW_SEC))


def ssh_run(ssh_target: str, remote_cmd: str, *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=10",
            "-o",
            "StrictHostKeyChecking=accept-new",
            ssh_target,
            remote_cmd,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
