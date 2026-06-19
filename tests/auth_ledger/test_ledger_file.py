"""AUTH-LEDGER file integrity."""

from __future__ import annotations

import pytest

from auth_ledger.ledger import load_ledger
from auth_ledger.ssh_harness import load_ssh_harness

pytestmark = pytest.mark.auth_ledger


@pytest.mark.breadth
def test_ledger_loads_two_hosts():
    hosts = load_ledger()
    names = [h.name for h in hosts]
    assert names == ["linux-vm", "sw-hq-runner4"]


def test_harness_covers_all_ledger_names():
    ledger_names = {h.name for h in load_ledger()}
    harness_names = set(load_ssh_harness())
    assert ledger_names == harness_names
