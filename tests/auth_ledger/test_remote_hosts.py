"""AUTH-LEDGER remote host tests — robust tests; DUT may fail."""

from __future__ import annotations

import time
from datetime import datetime, timezone

import pytest

from auth_ledger.ledger import load_ledger
from auth_ledger.ssh_harness import load_ssh_harness, max_skew_seconds, ssh_run

pytestmark = pytest.mark.auth_ledger


def _host_params():
    ledger = load_ledger()
    harness = load_ssh_harness()
    params = []
    for h in ledger:
        if h.name not in harness:
            pytest.fail(f"AUTH-LEDGER host {h.name!r} missing from tests/fixtures/auth-ledger-ssh.yaml")
        spec = harness[h.name]
        params.append(pytest.param(h.name, spec, id=h.name))
    return params


@pytest.mark.parametrize("name,spec", _host_params())
def test_ledger_has_ssh_harness_entry(name, spec):
    assert spec.name == name


@pytest.mark.parametrize("name,spec", _host_params())
def test_ssh_login(name, spec):
    result = ssh_run(spec.ssh, "echo ok")
    assert result.returncode == 0, (
        f"[{name}] ssh login failed (exit {result.returncode})\n"
        f"stderr: {result.stderr.strip()}\nstdout: {result.stdout.strip()}"
    )
    assert result.stdout.strip() == "ok"


@pytest.mark.parametrize("name,spec", _host_params())
def test_login_id(name, spec):
    result = ssh_run(spec.ssh, "id -un")
    assert result.returncode == 0, f"[{name}] id -un failed: {result.stderr.strip()}"
    remote_user = result.stdout.strip()
    assert remote_user == spec.expect_user, (
        f"[{name}] login id mismatch: got {remote_user!r}, expected {spec.expect_user!r}"
    )


@pytest.mark.parametrize("name,spec", _host_params())
def test_date_command(name, spec):
    result = ssh_run(spec.ssh, "date")
    assert result.returncode == 0, f"[{name}] date failed: {result.stderr.strip()}"
    assert result.stdout.strip(), f"[{name}] date produced empty output"


@pytest.mark.parametrize("name,spec", _host_params())
def test_ntp_date_vs_reference(name, spec):
    """Fail if remote clock skew exceeds tolerance vs test runner UTC."""
    epoch_result = ssh_run(spec.ssh, "date +%s")
    assert epoch_result.returncode == 0, (
        f"[{name}] date +%s failed: {epoch_result.stderr.strip()}"
    )
    remote_epoch = int(epoch_result.stdout.strip())
    reference_epoch = time.time()
    skew = abs(remote_epoch - reference_epoch)
    limit = max_skew_seconds()
    ref_human = datetime.fromtimestamp(reference_epoch, tz=timezone.utc).isoformat()
    remote_human = datetime.fromtimestamp(remote_epoch, tz=timezone.utc).isoformat()
    assert skew <= limit, (
        f"[{name}] ntp-date FAILED: skew {skew:.0f}s > {limit}s limit\n"
        f"  remote (UTC): {remote_human}\n"
        f"  reference (UTC): {ref_human}"
    )
