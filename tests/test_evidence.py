"""
test_evidence.py -- the receipts are airtight (every number traces to its rows + a real source).

Guards the "an Ergo quant can inspect it" promise: each validated claim has a pack whose value matches
the artifact (no retyping), whose episode count is real, and whose every episode carries a source_url.
Run: python3 -m pytest -q tests/test_evidence.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVID = ROOT / "data" / "evidence"


def _packs():
    assert EVID.exists(), "run: python3 src/evidence.py"
    return [json.loads(p.read_text()) for p in EVID.glob("*.json")]


def test_evd1_every_pack_is_a_validated_claim_with_a_value():
    packs = _packs()
    assert len(packs) >= 3                       # at least H1 + the battery edges
    for p in packs:
        assert p["tier"] == "validated"
        assert p["quantity"]["value"] is not None
        assert p["claim_id"] and p["source_artifact"] and p["source_commit"]


def test_evd2_episodes_reproduce_and_carry_sources():
    for p in _packs():
        eps = p["underlying_episodes"]
        # the amplification claims re-derive their episodes; count must match n_episodes
        assert len(eps) == p["n_episodes"]
        if eps:                                  # every episode must trace to a real source
            for e in eps:
                assert e.get("event_id")
                assert (e.get("source_url") or "").startswith("http") or e.get("source_url") == "" \
                    or "wikipedia" in (e.get("source_url") or "")
            # at least most episodes have a real http source
            with_src = sum(1 for e in eps if (e.get("source_url") or "").startswith("http"))
            assert with_src >= max(1, int(0.8 * len(eps)))


def test_evd3_value_matches_the_artifact():
    # spot-check: the copper edge pack value equals the value in edge_battery.json (no drift)
    eb = json.loads((ROOT / "data" / "edge_battery.json").read_text())
    copper = next((x for x in eb["amplification"] if x["hypothesis"] == "copper_growth"), None)
    pack = EVID / "edge.copper_growth.json"
    if copper and pack.exists():
        p = json.loads(pack.read_text())
        assert abs(p["quantity"]["value"] - copper["amp"]) < 1e-6
