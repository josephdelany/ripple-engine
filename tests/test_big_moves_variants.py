"""BIG_MOVES_REGISTRATION.md Amendment 4: the registered rule vs the rule the code actually ran.

§3 registers clustering within 60 TRADING days of an episode's start, with no merge step.
`src/big_moves.py` has, since its first commit, clustered at 90 CALENDAR days and then merged
same-sign episodes within 60 — and both the registration and the code first appear in the same
commit, so registered-before-computed cannot be shown from history.

Joe ruled on 2026-09-03: re-run under the registered rule as the primary result, publish the
as-computed one beside it, amend with the honest history. These tests hold both, so neither can
drift and neither can quietly become the other.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import big_moves as BM                                                 # noqa: E402
import materiality as M                                                # noqa: E402

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "big_moves"


@pytest.fixture(scope="module")
def brent():
    if not DB.exists():
        pytest.skip("needs the built oil.db")
    conn = sqlite3.connect(DB)
    s = BM.series(conn, "fred.DCOILBRENTEU")
    conn.close()
    if s.empty:
        pytest.skip("no Brent series")
    return s


def _pos(s):
    return {d: i for i, d in enumerate(s.index)}


# --------------------------------------------------------------- the two variants are pinned

def test_A4_as_computed_reproduces_the_published_history(brent):
    """The old numbers must still be reproducible, or 'published beside it' means nothing."""
    eps = BM.episodes_for(brent, "price", variant="as_computed")
    assert len(eps) == 43, f"the as-computed rule no longer gives the 43 episodes it published: {len(eps)}"


def test_A4_registered_rule_gives_its_own_count(brent):
    eps = BM.episodes_for(brent, "price", variant="registered")
    assert len(eps) == 44


def test_A4_an_unknown_variant_is_refused(brent):
    with pytest.raises(ValueError):
        BM.episodes_for(brent, "price", variant="whatever_is_convenient")


# --------------------------------------------------------------- §3 as written

def test_A4_registered_clusters_in_trading_days_not_calendar_days(brent):
    """The constraint §3 actually states. An episode's qualifying dates span at most 60 TRADING
    days; under the as-computed rule the span is bounded in calendar days instead, so this is the
    test that tells the two apart."""
    pos = _pos(brent)
    eps = BM.episodes_for(brent, "price", variant="registered")
    spans = [pos[pd.Timestamp(e["end"])] - pos[pd.Timestamp(e["onset"])] for e in eps]
    assert max(spans) <= 60, f"an episode spans {max(spans)} trading days, more than §3 allows"


def test_A4_trading_gap_counts_observations_not_days():
    """A weekend or a holiday must not consume the budget: the gap is positions in the asset's own
    observation index."""
    idx = list(pd.bdate_range("2020-01-01", periods=10))
    pos = {d: i for i, d in enumerate(idx)}
    assert BM._trading_gap(pos, idx[0], idx[5]) == 5
    assert (idx[5] - idx[0]).days == 7, "fixture no longer spans a weekend; the test proves nothing"


def test_A4_registered_performs_no_merge_step(brent):
    """§3 has no merge. The proof is direct: the registered output CONTAINS adjacent same-sign
    episodes whose onsets are within the merge window, which the as-computed rule collapses. If a
    merge ever crept back in, this count would fall to zero."""
    def adjacent_same_sign(eps):
        return sum(1 for a, b in zip(eps, eps[1:])
                   if a["sign"] == b["sign"]
                   and (pd.Timestamp(b["onset"]) - pd.Timestamp(a["onset"])).days <= BM.MERGE_DAYS)
    reg = BM.episodes_for(brent, "price", variant="registered")
    ac = BM.episodes_for(brent, "price", variant="as_computed")
    assert adjacent_same_sign(reg) == 3, "the registered rule is merging (or the data moved)"
    assert adjacent_same_sign(ac) == 0, "the as-computed rule is no longer merging"


# --------------------------------------------------------------- the monthly tier is not in dispute

def test_A4_monthly_tier_is_identical_under_both_variants():
    """Amendment 3 registers cluster 365 days + same-sign merge within 180 for the monthly tier,
    which is exactly what the code does. Only the DAILY tier deviates, and only it is re-run."""
    if not DB.exists():
        pytest.skip("needs the built oil.db")
    conn = sqlite3.connect(DB)
    s = BM.series(conn, "fred.WTISPLC")
    conn.close()
    if s.empty:
        pytest.skip("no monthly series")
    a = BM.episodes_for(s, "price", "monthly", variant="registered")
    b = BM.episodes_for(s, "price", "monthly", variant="as_computed")
    assert a == b


# --------------------------------------------------------------- nothing else moved

def test_A4_no_threshold_or_attribution_window_changed():
    """Amendment 4 changes how qualifying dates are GROUPED and nothing else."""
    assert BM.TOP_Q == 0.95
    assert BM.TIERS["daily"]["attr_before_days"] == 7 and BM.TIERS["daily"]["anticipated_lag"] == 20
    assert BM.TIERS["monthly"] == dict(windows=(3, 12), cluster_days=365, merge_days=180,
                                       attr_before_days=31, anticipated_lag=60, unit="months")


def test_A4_the_default_variant_stays_as_computed(brent):
    """src/walk.py (session B) calls episodes_for without a variant. Its numbers must not move
    unless B chooses it; the re-run is published through data/big_moves/*.json, not by changing
    what every caller silently gets."""
    assert BM.episodes_for(brent, "price") == BM.episodes_for(brent, "price", variant="as_computed")


# --------------------------------------------------------------- what is published

def test_A4_published_file_leads_with_registered_and_carries_as_computed():
    p = OUT / "brent.json"
    if not p.exists():
        pytest.skip("run python3 src/big_moves.py")
    j = json.loads(p.read_text())
    assert j["variant"] == "registered"
    assert j["n_episodes"] == 44 and j["no_identified_event"] == 14
    assert j["as_computed"]["n_episodes"] == 43 and j["as_computed"]["no_identified_event"] == 15
    assert "60 TRADING days" in j["registration"] and "no merge" in j["registration"]
    assert len(j["episodes"]) == j["n_episodes"]
    assert len(j["as_computed"]["episodes"]) == j["as_computed"]["n_episodes"]


def test_A4_the_materiality_verdicts_are_unchanged_by_the_re_run():
    """A robustness result worth pinning: the gate's INPUTS move but not one of its VERDICTS.
    If a future change to the clustering does flip a class, this test is where it surfaces."""
    p = OUT / "summary.json"
    if not p.exists():
        pytest.skip("run python3 src/big_moves.py")
    j = json.loads(p.read_text())
    reg = {a: j[a] for a in ("brent", "diesel_crack") if a in j}
    alt = {a: {**j[a], **j[a]["as_computed"]} for a in reg}
    classes = sorted(reg["brent"]["p_big_given_class"])
    flips = [c for c in classes if M.gate(c, reg)["significance"] != M.gate(c, alt)["significance"]]
    assert flips == [], f"the re-run flipped a materiality verdict: {flips}"
