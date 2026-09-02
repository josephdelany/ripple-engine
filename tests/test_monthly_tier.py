"""Brief 3 B-12 — monthly-tier readiness.

Power says n ~ 1,200 scored reads to detect +0.05 skill (`summary.json.power`), against 150 today, so the
pre-1987 admissions (`data/candidates/pre1987_candidates.csv`, PATH Step 5) are the only route to a decisive
answer. These tests keep the scoring path ready for the moment Joe admits a batch:

1. `test_b12_monthly_machinery_scores_a_filled_tier` — PASSES TODAY on a synthetic 1946-1990 corpus: the walk
   reads, seals, scores and summarizes a monthly tier with n >= 30, with all four G baselines and the +3-month
   P horizon. This is the proof that no code change is needed when the corpus grows.
2. `test_b12_real_monthly_tier_smoke` — the smoke on the REAL corpus. It XFAILS today, for the stated reason:
   the corpus holds 14 monthly-tier events, burn-in is 8 per class and `min_tier_n` is 30, so the tier scores
   0 reads and cannot validate. The xfail condition is computed from the database, so when the tier fills the
   marker stops applying and the test must genuinely PASS -- it is not a note that can rot.

Then a full publication run is one command: `python3 src/walk.py` (Amendment I's digest and the filtration
audit run with it). Nothing here writes to `data/walk_forward`.
"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import pytest

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
import engine.read as R
import engine.similarity as S
import walk as W
from test_walk import MENU, FAST

DB = os.path.join(ROOT, "data", "oil.db")
MIN_TIER_N = W.REGISTERED["min_tier_n"]


def _real_monthly_corpus():
    """The real corpus restricted to its monthly-tier events (cheap: the tier is small by construction)."""
    from _db import connect
    c = R.Corpus.from_db(connect(read_only=True))
    monthly = [e for e in c.events if e["tier"] == "monthly"]
    sub = R.Corpus(monthly, c.info, c.prices, edges=c.edges, big_moves=c.big_moves,
                   panel={e["event_id"]: c.panel.get(e["event_id"], []) for e in monthly},
                   schema_extra=c.schema_extra,
                   ies90={e["event_id"]: c.ies90[e["event_id"]] for e in monthly if e["event_id"] in c.ies90},
                   persistence={e["event_id"]: c.persistence[e["event_id"]] for e in monthly if e["event_id"] in c.persistence})
    return sub, len(monthly)


def _n_monthly():
    if not os.path.exists(DB):
        return 0
    try:
        return _real_monthly_corpus()[1]
    except Exception:
        return 0


N_MONTHLY = _n_monthly()


def _synthetic_monthly(n=40, seed=5):
    """A 1946-1990 monthly corpus: WTI-shaped spine, IES-90 labels following the actor, knowable situation rows."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("1946-01-01", "1990-12-01", freq="MS")
    wti = pd.Series(20 * np.exp(np.cumsum(rng.normal(0, 0.05, len(idx)))), index=idx)
    vix = pd.Series(rng.normal(50, 10, len(idx)), index=idx)
    events, ies90, panel = [], {}, {}
    for i, d in enumerate(pd.date_range("1950-01-15", "1985-12-15", periods=n)):
        eid, ds = f"m{i:02d}", str(d.date())
        events.append({"event_id": eid, "event_date": ds, "type": "conflict_escalation", "title": eid,
                       "sr_actor": "country.a" if i % 2 else "country.c", "sr_target": "country.b",
                       "sr_conflict_scope": "isolated", "sr_tempo": "nth", "sr_prior_dyad": "none",
                       "sr_asset_role": "unknown", "sr_actor_propensity": None})
        ies90[eid] = {"level": ["0", "3", "0", "1"][i % 4], "deal": 0}
        panel[eid] = [{"field": "sr_actor", "value": events[-1]["sr_actor"], "vintage": ds},
                      {"field": "sr_target", "value": "country.b", "vintage": ds}]
    big = {"monthly": {"windows": [("1973-10-01", "1974-03-01")], "base_pct": 18.3}}
    return R.Corpus(events, S.InfoSet({"vix_pct": vix}), {"monthly": wti}, edges={}, big_moves=big,
                    ies90=ies90, panel=panel)


def _run(corpus):
    w = W.Walk(corpus, MENU, out_dir=tempfile.mkdtemp(prefix="monthly_smoke_"), params=FAST, quiet=True).run_reads()
    tier = W.summarize_tier(w.reads, w.scores, dict(W.REGISTERED) | FAST, "monthly", n_boot=100, n_spa=50)
    return w, tier


def test_b12_monthly_machinery_scores_a_filled_tier():
    """No code change is needed when the tier fills: n = 40 monthly events score, summarize and permit validation."""
    c = _synthetic_monthly(n=40)
    assert all(c.tier_of(e["event_date"]) == "monthly" for e in c.events)
    w, tier = _run(c)
    assert len([r for r in w.reads if r["tier"] == "monthly"]) == 40
    assert tier["n_scored_burn_in"] >= MIN_TIER_N and tier["permits_validation"] is True
    assert tier["horizon"] == 3 and tier["unit"] == "months"                       # the registered monthly P horizon
    assert set(tier["G"]["engine_vs"]) == {"climatology", "frozen", "random_analogs", "persistence"}
    assert tier["G"]["engine_vs"]["climatology"]["n"] >= MIN_TIER_N
    assert tier["P"]["engine_vs"]["climatology"]["n"] >= MIN_TIER_N
    assert tier["G"]["rps"]["engine_vs"]["climatology"]["skill"] is not None       # RPS block computed on this tier
    assert W.verify_file(os.path.join(str(w.out), "reads.jsonl"))[0]               # the tier's reads seal and re-hash
    audit = W.filtration_audit(c, w.reads)                                          # Amendment F.1 runs on monthly reads
    assert audit["clean"] and audit["checks"]["analog_date"] > 0


@pytest.mark.skipif(not os.path.exists(DB), reason="needs the built data/oil.db")
@pytest.mark.xfail(N_MONTHLY < MIN_TIER_N, strict=False,
                   reason=(f"the monthly tier holds {N_MONTHLY} corpus events (< min_tier_n {MIN_TIER_N}); with "
                           "burn-in 8 per class it scores 0 reads and cannot validate (protocol §9: it describes, "
                           "it does not validate). Fills when Joe admits a batch from "
                           "data/candidates/pre1987_candidates.csv (PATH Step 5); this test then passes on its own."))
def test_b12_real_monthly_tier_smoke():
    """The real monthly tier, end to end: reads sealed, scored past burn-in, and validation permitted."""
    c, n_monthly = _real_monthly_corpus()
    w, tier = _run(c)
    assert n_monthly >= MIN_TIER_N, f"monthly tier has {n_monthly} events"
    assert tier["n_scored_burn_in"] >= MIN_TIER_N, f"{tier['n_scored_burn_in']} scored of {n_monthly} monthly reads"
    assert tier["permits_validation"] is True
    assert tier["G"]["engine_vs"]["persistence"]["n"] is not None
    assert W.filtration_audit(c, w.reads)["clean"]
