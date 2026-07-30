"""
test_lens.py -- the domain-lens views (Step 4).

Each domain is a view over the ONE validated core: it returns that domain's validated nodes (only),
honest nulls, and coverage. Run: python3 -m pytest -q tests/test_lens.py
"""

import research


def test_l1_lens_filters_to_domain_and_only_claims_validated():
    r = research.lens_data("commodities")
    assert r["ok"]
    # commodities lens returns only commodity-domain nodes, and validated ones have CI excluding 0
    for n in r["validated_nodes"]:
        lo, hi = n["ci"]
        assert lo is not None and (lo > 0 or hi < 0)
    # a macro-only node (breakeven) must NOT appear in the commodities lens
    all_nodes = {n["node"] for n in r["validated_nodes"] + r["null_nodes"]}
    assert "5Y breakeven" not in all_nodes and "S&P 500" not in all_nodes


def test_l2_domains_partition_sensibly():
    macro = research.lens_data("macro")
    macro_nodes = {n["node"] for n in macro["validated_nodes"] + macro["null_nodes"]}
    assert "5Y breakeven" in macro_nodes           # breakevens live in macro
    assert "Gold" not in macro_nodes               # gold is a commodity, not macro
    # me-risk carries ME situations and conflict/infra event coverage
    me = research.lens_data("me-risk")
    assert "conflict_escalation" in me["event_coverage"]


def test_l3_unknown_domain_is_handled():
    r = research.lens_data("not-a-domain")
    assert r["ok"] is False and "domains" in r
