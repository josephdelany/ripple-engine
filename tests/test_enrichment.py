"""
test_enrichment.py -- tests for the enrichment adapters (prediction markets, ...).

Pure-function tests over the parsing/scoring logic so they need no network.
Run:  python3 -m pytest tests/test_enrichment.py -q
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


# e1 -- a live binary market parses to a clean record; the probability is P(first
# outcome) and the series is tagged to Polymarket.
def test_e1_parse_live_market():
    import fetch_predmkt
    m = {"id": "123", "slug": "hormuz-normal-dec31",
         "question": "Strait of Hormuz traffic returns to normal by December 31?",
         "outcomes": '["Yes", "No"]', "outcomePrices": '["0.555", "0.445"]',
         "volume": 6133622, "liquidity": 50000,
         "endDate": "2026-12-31T00:00:00Z", "active": True, "closed": False}
    r = fetch_predmkt.parse_market(m, query="hormuz")
    assert r["series_id"] == "predmkt.polymarket.hormuz-normal-dec31"
    assert r["prob"] == 0.555 and r["outcome"] == "Yes"
    assert r["volume"] == 6133622 and r["end_date"] == "2026-12-31"
    assert "polymarket.com" in r["url"]


# e1b -- closed / inactive / price-less markets are rejected (None), so dead or
# malformed markets never pollute the signal.
def test_e1b_parse_rejects_dead_markets():
    import fetch_predmkt
    base = {"slug": "x", "question": "q", "outcomes": '["Yes","No"]',
            "outcomePrices": '["0.5","0.5"]', "active": True, "closed": False}
    assert fetch_predmkt.parse_market({**base, "closed": True}) is None
    assert fetch_predmkt.parse_market({**base, "active": False}) is None
    assert fetch_predmkt.parse_market({**base, "outcomePrices": "[]"}) is None
    assert fetch_predmkt.parse_market(None) is None
    assert fetch_predmkt.parse_market({**base}) is not None      # the good one
