"""
test_status.py -- the one-glance verdict + the acceptance gate behave.

status.run() must produce a valid GREEN/AMBER/RED with reasons; acceptance.run(fast) must aggregate the
soundness checks into COMMISSIONED/DEGRADED. Run: python3 -m pytest -q tests/test_status.py
"""

import status as S
import acceptance as A


def test_st1_status_verdict_is_valid():
    r = S.run()
    assert r["verdict"] in ("GREEN", "AMBER", "RED")
    assert isinstance(r["reasons"], list) and r["reasons"]
    assert "framework_sound" in r["evaluation"]
    assert r["backups"]["restore_tested"] is True        # WS-B tested the restore path


def test_st2_acceptance_aggregates_checks():
    r = A.run(fast=True)                                  # skip the nested pytest
    assert r["verdict"] in ("COMMISSIONED", "DEGRADED")
    labels = " ".join(m for _, m in r["checks"])
    assert "framework_sound" in labels and "evidence packs" in labels and "cage" in labels
    # with a sound framework + receipts + non-RED status, it should commission
    assert r["commissioned"] is True
