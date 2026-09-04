"""
test_status.py -- the one-glance verdict + the acceptance gate behave.

status.run() must produce a valid GREEN/AMBER/RED with reasons; acceptance.run(fast) must aggregate the
soundness checks into COMMISSIONED/DEGRADED. Run: python3 -m pytest -q tests/test_status.py
"""

import status as S
import acceptance as A


def test_st1_status_verdict_is_valid(tmp_path, monkeypatch):
    monkeypatch.setattr(S, "OUT", tmp_path / "engine_status.json")
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
    # Until 2026-09-03 this asserted commissioned is True. It no longer is, and that is the
    # gate working: evaluate.py's framework_sound now comes from the REGISTERED gates (protocol
    # §6 placebo null_holds is false; H1 is DOWNGRADE (SUGGESTIVE) under the R7 bar) instead of
    # from its own placebo shuffle, and engine_status is RED. Commissioning while the registered
    # placebo fails is exactly what SESSION_CHARTER §2.4 forbids. The assertion is therefore on
    # the RELATION, which holds whichever way the checks fall.
    assert r["commissioned"] is all(ok for ok, _ in r["checks"]), \
        "commissioned must be true if and only if every check passes"
    if not r["commissioned"]:
        assert r["verdict"] == "DEGRADED"
        assert [m for ok, m in r["checks"] if not ok], "DEGRADED with no failing check named"
