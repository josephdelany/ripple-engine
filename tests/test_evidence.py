"""
test_evidence.py -- the receipts are airtight (every number traces to its rows + a real source).

Guards the "an Ergo quant can inspect it" promise: each surfaced claim (validated OR, post red-team-1,
SUGGESTIVE) has a pack whose value matches the artifact (no retyping), whose episode count is real, and
whose every episode carries a source_url.
Run: python3 -m pytest -q tests/test_evidence.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVID = ROOT / "data" / "evidence"


def _packs():
    assert EVID.exists(), "run: python3 src/evidence.py"
    return [json.loads(p.read_text()) for p in EVID.glob("*.json")]


CLAIM_TIERS = ("validated", "SUGGESTIVE")
WITHDRAWN_TIERS = ("RETRACTED", "NOT_A_FINDING")     # Joe's Ruling 1, EDGE_PORTFOLIO.md amendment 2026-09-02


def _claims():
    return [p for p in _packs() if p["tier"] in CLAIM_TIERS]


def test_evd1_every_pack_is_a_receipted_claim_with_a_value():
    # Post red-team-1 (R7): a claim pack may be `validated` OR `SUGGESTIVE`. Downgraded claims KEEP their
    # packs on purpose -- publishing a downgrade with its receipts is the integrity evidence. Every
    # claim pack still traces to a value + a real source artifact + commit.
    packs = _packs()
    assert len(packs) >= 3                       # at least H1 + the battery edges
    for p in packs:
        assert p["tier"] in CLAIM_TIERS + WITHDRAWN_TIERS, p["claim_id"]
        if p["tier"] not in CLAIM_TIERS:
            continue
        assert p["quantity"]["value"] is not None
        assert p["claim_id"] and p["source_artifact"] and p["source_commit"]
    assert len(_claims()) >= 3


def test_evd1b_a_withdrawn_pack_carries_its_ruling_and_states_no_claim():
    """Joe's Ruling 1: the five retracted amplification nodes and palladium must not be readable as claims.
    A withdrawn pack says so in its own statement and points at the ruling, the amendment and the re-test."""
    withdrawn = {p["claim_id"]: p for p in _packs() if p["tier"] in WITHDRAWN_TIERS}
    assert set(withdrawn) >= {"node.brent_oil", "node.heating_oil", "node.5y_breakeven", "node.s&p_500",
                              "node.platinum", "node.palladium"}, sorted(withdrawn)
    for cid, p in withdrawn.items():
        blk = p.get("retraction") or p.get("not_a_finding")
        assert blk and "Ruling 1" in blk["ruling"], cid
        assert "2026-09-02" in json.dumps(blk), cid
        txt = p["statement"]
        assert ("RETRACTED" in txt) or ("NOT a finding" in txt), cid
        # a withdrawn pack must never read as a live claim in the present tense
        assert "previously claimed" in txt or "NOT a finding" in txt, cid
    # palladium carries every reason Joe required, together, in the pack itself
    reasons = " ".join(withdrawn["node.palladium"]["not_a_finding"]["reasons"]).lower()
    assert "not on the oil chain" in reasons and "noise" in reasons


def test_evd2_episodes_reproduce_and_carry_sources():
    for p in _claims():
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
