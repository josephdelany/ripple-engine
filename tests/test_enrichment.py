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


# ---- E3: corroboration (cluster + weight-of-evidence) ----------------------

# e3 -- near-duplicate headlines cluster together; a distinct one stays separate.
def test_e3_cluster_collapses_duplicates():
    import corroborate
    atoms = [
        {"headline": "Houthis strike Saudi oil facility in Red Sea", "source_url": "http://a.com/1"},
        {"headline": "Saudi oil facility struck by Houthis in Red Sea", "source_url": "http://b.com/2"},
        {"headline": "Fed holds interest rates steady", "source_url": "http://c.com/3"},
    ]
    clusters = corroborate.cluster_atoms(atoms, threshold=72)
    sizes = sorted(len(c) for c in clusters)
    assert sizes == [1, 2]                     # the two Houthi items merge; Fed alone


# e3b -- weight-of-evidence: more INDEPENDENT sources -> higher confidence, and it
# never reaches certainty (correlated evidence can't manufacture 100%).
def test_e3b_score_monotonic_and_capped():
    import corroborate
    p1 = corroborate.score(1)[1]
    p2 = corroborate.score(2)[1]
    p4 = corroborate.score(4)[1]
    assert p1 < p2 < p4                          # more independent sources -> more confident
    assert corroborate.score(50)[1] <= corroborate.CAP_PROB   # never certain
    assert corroborate.score(1)[2] in ("unverified", "possible")   # one source is weak
    assert corroborate.score(4)[2] in ("likely", "corroborated")   # four is strong


# e3c -- the independence key is the domain: reprints of one wire (same domain)
# count ONCE, not many times (the correlated-source fix).
def test_e3c_domain_independence():
    import corroborate
    assert corroborate._domain("https://www.reuters.com/world/x") == "reuters.com"
    # two atoms, same domain -> one independent source -> 'possible', not inflated.
    atoms = [{"headline": "X happened", "source_url": "https://reuters.com/a"},
             {"headline": "X happened", "source_url": "https://reuters.com/b"}]
    c = corroborate.cluster_atoms(atoms)[0]
    domains = {corroborate._domain(a["source_url"]) for a in c}
    assert len(domains) == 1


# ---- E4: IMF PortWatch physical-flow anomaly ------------------------------

# e4 -- assess flags a sharp drop in tanker transits as 'reduced' (a physical
# disruption), a surge as 'elevated', and steady flow as 'normal'.
def test_e4_portwatch_assess_flags():
    import fetch_portwatch as fp
    # newest-first; latest far below the trailing median -> reduced.
    assert fp.assess([2, 10, 11, 9, 12])["flag"] == "reduced"
    assert fp.assess([25, 10, 11, 9, 12])["flag"] == "elevated"
    assert fp.assess([10, 10, 11, 9, 12])["flag"] == "normal"
    assert fp.assess([])  is None
    r = fp.assess([6, 12, 12])            # 6 vs median 12 -> 0.5x -> reduced
    assert r["pct_of_median"] == 0.5 and r["flag"] == "reduced"


# e4b -- cross-modal boost: a physical disruption at a chokepoint named in a news
# cluster adds an independent vote (news + ships stopping > either alone).
def test_e4b_physical_corroboration():
    import corroborate
    cluster = [{"headline": "Tankers avoid Strait of Hormuz amid tension",
                "source_url": "http://x/1"}]
    assert corroborate._physical_hit(cluster, {"hormuz"}) == "hormuz"
    assert corroborate._physical_hit(cluster, set()) is None         # not disrupted
    assert corroborate._physical_hit(
        [{"headline": "Fed holds rates", "source_url": "x"}], {"hormuz"}) is None
    # one physical vote on top of one news source is strictly more confident.
    assert corroborate.score(2)[1] > corroborate.score(1)[1]


# ---- E6: Wikipedia attention anomaly --------------------------------------

# e6 -- assess (oldest-first) flags a pageview surge as 'spike', a collapse as
# 'quiet', steady as 'normal'.
def test_e6_wiki_assess_flags():
    import fetch_wiki_attention as w
    assert w.assess([100, 100, 100, 100, 500])["flag"] == "spike"      # 5x
    assert w.assess([100, 100, 100, 100, 145])["flag"] == "elevated"   # 1.45x
    assert w.assess([100, 100, 100, 100, 40])["flag"] == "quiet"       # 0.4x
    assert w.assess([100, 100, 100, 100, 110])["flag"] == "normal"
    assert w.assess([]) is None
