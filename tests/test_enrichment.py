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


# ---- E2: NASA FIRMS satellite-fire modality --------------------------------

# e2 -- the FIRMS CSV parser extracts detections with FRP; malformed rows drop.
def test_e2_firms_parser():
    import fetch_firms
    csv = ("latitude,longitude,bright_ti4,acq_date,confidence,frp\n"
           "25.93,49.67,340.1,2026-07-28,h,55.4\n"
           "bad,row,,,,\n"
           "25.94,49.66,330.0,2026-07-28,n,12.1\n")
    d = fetch_firms.parse_firms_csv(csv)
    assert len(d) == 2 and round(sum(x["frp"] for x in d), 1) == 67.5
    b = fetch_firms.bbox(25.93, 49.67)
    assert b.count(",") == 3        # west,south,east,north


# e2b -- a thermal anomaly at a NAMED facility corroborates a news cluster
# (cross-modal), and only when that facility is actually flagged elevated.
def test_e2b_thermal_corroboration():
    import corroborate
    cluster = [{"headline": "Drone strike hits Abqaiq oil facility", "source_url": "x"}]
    assert corroborate._thermal_hit(cluster, {"abqaiq"}) == "abqaiq"
    assert corroborate._thermal_hit(cluster, set()) is None      # not flagged
    assert corroborate._thermal_hit(
        [{"headline": "Fed holds rates", "source_url": "x"}], {"abqaiq"}) is None


# ---- E7: GDELT DOC coverage tone ------------------------------------------

# e7 -- latest_tone parses the DOC TimelineTone JSON to the most recent value.
def test_e7_gdelt_latest_tone():
    import fetch_gdelt_tone as g
    js = ('{"timeline":[{"series":"Average Tone","data":['
          '{"date":"20260720T000000Z","value":-1.2},'
          '{"date":"20260728T000000Z","value":-3.5}]}]}')
    assert g.latest_tone(js) == -3.5
    assert g.latest_tone('{"timeline":[]}') is None
    assert g.latest_tone("not json") is None


# ---- Calibration: corroboration weights vs resolved outcomes ---------------

# c1 -- Brier is a proper score: perfect confident predictions ~0, confident-wrong ~1.
def test_c1_brier():
    import calibrate_corroboration as cal
    assert cal.brier([1.0, 0.0], [1, 0]) == 0.0
    assert cal.brier([0.9, 0.9, 0.1, 0.1], [1, 1, 0, 0]) == 0.01
    assert cal.brier([0.9, 0.9], [0, 0]) == 0.81
    assert cal.brier([], []) is None


# c2 -- reliability diagram: each band reports mean predicted vs observed real-rate.
def test_c2_reliability_and_refit():
    import calibrate_corroboration as cal
    rb = cal.reliability_buckets([0.8, 0.85, 0.2, 0.15], [1, 1, 0, 0])
    hi = [b for b in rb if b["band"].startswith("0.75")][0]
    assert hi["observed_rate"] == 1.0 and hi["n"] == 2
    # refit only fires on a sufficient, balanced labeled set.
    small = {str(i): {"confidence": "0.8", "label": "1", "n_independent": "3"}
             for i in range(5)}
    assert cal.calibrate(small)["refit"] is None            # too few + one class
    balanced = {str(i): {"confidence": "0.8", "label": str(i % 2),
                         "n_independent": "3"} for i in range(40)}
    assert cal.calibrate(balanced)["refit"]["prior_prob"] == 0.5   # base rate


# c3 -- gate auto-confirm labels a logged event 1 when its source_url is now a
# coded event; positive-only (never auto-negative).
def test_c3_gate_auto_confirm():
    import calibrate_corroboration as cal
    rows = {"k1": {"label": "", "source_urls": "http://a/1|http://b/2",
                   "resolved_at": ""},
            "k2": {"label": "", "source_urls": "http://c/3", "resolved_at": ""}}
    n = cal.auto_confirm(rows, {"http://a/1"}, "2026-07-28T00:00:00")
    assert n == 1 and rows["k1"]["label"] == "1"
    assert rows["k2"]["label"] == ""                        # unmatched stays unlabeled


# ---- Autonomous analyst: deterministic divergence detection ---------------

# a1 -- a spiking-attention chokepoint with a cheap priced disruption is flagged;
# a quiet one is not. 'normal'-framed markets are inverted to a disruption prob.
def test_a1_attention_vs_priced():
    import divergence
    wiki = [{"page": "Bab el-Mandeb", "pct_of_median": 4.7, "flag": "spike"},
            {"page": "Strait of Hormuz", "pct_of_median": 0.71, "flag": "normal"},
            {"page": "Suez Canal", "pct_of_median": 1.3, "flag": "elevated"}]
    mk = [{"question": "Bab el-Mandeb Strait effectively closed by Sep 30?",
           "prob": 0.16, "volume": 1_393_951, "url": "x"},
          {"question": "Strait of Hormuz traffic returns to normal by Dec 31?",
           "prob": 0.56, "volume": 6_000_000, "url": "y"},
          {"question": "Suez Canal effectively closed?", "prob": 0.05,
           "volume": 100, "url": "z"}]
    g = divergence.attention_vs_priced(wiki, mk)
    subjects = [d["subject"] for d in g]
    assert "Bab el-Mandeb" in subjects            # spike + cheap -> flagged
    assert "Strait of Hormuz" not in subjects     # attention normal -> not flagged
    bab = [d for d in g if d["subject"] == "Bab el-Mandeb"][0]
    assert bab["priced_disruption"] == "16%"      # 'closed' framing = direct
    suez = [d for d in g if d["subject"] == "Suez Canal"][0]
    assert suez["priced_disruption"] == "5%"      # 'closed' 5% stays 5% (direct)


# ---- Strategic-commodity criticality ---------------------------------------

# cr1 -- at_risk flags a commodity iff a critical producer is in an active situation,
# with the correct at-risk share, sorted by share.
def test_cr1_criticality_at_risk():
    import criticality
    commodities = {
        "uranium": {"top": {"kazakhstan": 39, "russia": 5}, "stage": "mine"},
        "chips": {"top": {"taiwan": 92}, "stage": "fab"},
        "palm": {"top": {"indonesia": 58}, "stage": "prod"}}
    r = criticality.at_risk(commodities, {"russia", "taiwan"})
    names = [x["commodity"] for x in r]
    assert names == ["chips", "uranium"]          # sorted by share; palm excluded
    assert r[0]["at_risk_share"] == 92
    assert r[1]["at_risk_share"] == 5             # only russia's 5%, not kazakhstan's


# cr2 -- watch_list maps each critical country to what it's critical for.
def test_cr2_watch_list():
    import criticality
    commodities = {"uranium": {"top": {"kazakhstan": 39}, "stage": "mine"},
                   "copper": {"top": {"chile": 23, "kazakhstan": 2}, "stage": "mine"}}
    wl = criticality.watch_list(commodities)
    assert set(c[0] for c in wl["kazakhstan"]) == {"uranium", "copper"}
    assert wl["kazakhstan"][0][0] == "uranium"    # sorted by share (39 > 2)


# ---- Oil/energy propagation graph ------------------------------------------

# pr1 -- a chain is LIVE iff one of its trigger countries is in an active situation;
# chokepoint chains sort before bulk ones.
def test_pr1_propagation_live_chains():
    import propagation
    chains = {
        "palladium": {"geometry": "chokepoint", "countries": ["russia"],
                      "downstream": "autocatalysts"},
        "gas_food": {"geometry": "bulk", "countries": ["russia", "ukraine"],
                     "downstream": "food"},
        "rare_earths": {"geometry": "chokepoint", "countries": ["china"],
                        "downstream": "magnets"}}
    live = propagation.live_chains(chains, {"russia"})            # china NOT active
    names = [d["chain"] for d in live]
    assert names == ["palladium", "gas_food"]     # rare_earths excluded; choke before bulk
    assert live[0]["triggered_by"] == ["russia"]
    assert live[1]["triggered_by"] == ["russia"]  # only russia, not ukraine


# pr2 -- downstream_markets flattens the live chains to distinct 'so what' markets.
def test_pr2_downstream_markets():
    import propagation
    live = [{"downstream": "food"}, {"downstream": "autocatalysts"}, {"downstream": "food"}]
    assert propagation.downstream_markets(live) == ["autocatalysts", "food"]


# pr3 -- active-situation reader ignores closed situations (matches criticality's rule).
def test_pr3_active_situation_reader(tmp_path):
    import propagation
    y = tmp_path / "situations.yaml"
    y.write_text(
        "situations:\n"
        "  - status: active\n    member_entities: [country.russia, chokepoint.hormuz]\n"
        "  - status: closed\n    member_entities: [country.france]\n")
    assert propagation.active_situation_countries(y) == {"russia"}


# ---- GPR risk-vs-priced divergence read ------------------------------------

# gp1 -- pct_rank is the share of history at-or-below the value; band buckets it.
def test_gp1_pct_rank_and_band():
    import gpr_signal
    assert gpr_signal.pct_rank([1, 2, 3, 4], 3) == 75.0
    assert gpr_signal.pct_rank([1, 2, 3, 4], 4) == 100.0     # highest ever
    assert gpr_signal.pct_rank([], 5) is None
    assert gpr_signal.band(10) == "calm"
    assert gpr_signal.band(30) == "normal"
    assert gpr_signal.band(60) == "elevated"
    assert gpr_signal.band(90) == "high"
    assert gpr_signal.band(97) == "extreme"


# gp2 -- divergence: small gap = aligned; risk running hotter than priced is flagged.
def test_gp2_divergence():
    import gpr_signal
    gap, b, d = gpr_signal.divergence(95, 90)
    assert b == "aligned" and gap == 5
    gap, b, d = gpr_signal.divergence(90, 40)          # risk hot, market calm
    assert b == "wide gap" and gap == 50 and "HOTTER" in d
    gap, b, d = gpr_signal.divergence(30, 60)          # market more nervous
    assert b == "mild gap" and gap == -30 and "nervous" in d


# ---- Analogue probability function (Stage 1: predictive engine) -------------

_LIB = [
    {"event_id": "a", "event_type": "geo", "archetype": "geopolitical_shock",
     "event_date": "1990-08-02",
     "gap_patterns": [{"asset_token": "wti", "pattern": "overshoot"},
                      {"asset_token": "sp500", "pattern": "clean_absorption"}]},
    {"event_id": "b", "event_type": "geo", "archetype": "war_geopolitical",
     "event_date": "2022-02-24",
     "gap_patterns": [{"asset_token": "wti", "pattern": "overshoot"}]},
    {"event_id": "c", "event_type": "cpi", "archetype": "economic_release",
     "event_date": "2021-01-01",
     "gap_patterns": [{"asset_token": "sp500", "pattern": "directional_error"}]},
]


# an1 -- scoring: exact event_type=40 + archetype=15; a non-matching type scores 0.
def test_an1_score():
    import analogue
    q = {"event_type": "geo", "archetype": "geopolitical_shock"}
    assert analogue.score(q, _LIB[0])[0] == 55        # type + archetype
    assert analogue.score(q, _LIB[1])[0] == 40        # type only (archetype differs)
    assert analogue.score(q, _LIB[2])[0] == 0         # cpi: no overlap


# an2 -- search_multi pools across queries and keeps each event once at its BEST score.
def test_an2_search_multi_dedup():
    import analogue
    lib = [_LIB[0]]                                    # single geo/geopolitical_shock event
    m = analogue.search_multi([{"event_type": "geo"},               # scores 40
                               {"archetype": "geopolitical_shock"}], # scores 15
                              lib)
    assert len(m) == 1 and m[0][0] == 40               # deduped, kept the higher score


# an3 -- outcome_distribution tallies the dominant pattern + share per asset.
def test_an3_outcome_distribution():
    import analogue
    matches = [(55, _LIB[0]), (40, _LIB[1])]           # two geo analogues
    dist, overall = analogue.outcome_distribution(matches)
    assert dist["wti"]["dominant"] == "overshoot" and dist["wti"]["share"] == 1.0
    assert dist["wti"]["n"] == 2
    assert overall["overshoot"] == 2


# an4 -- thin support returns the honest 'no good analogue' band (never manufactured).
def test_an4_confidence_thin():
    import analogue
    matches = [(55, _LIB[0]), (40, _LIB[1])]           # only 2 < MIN_ANALOGUES
    _, overall = analogue.outcome_distribution(matches)
    assert "no good analogue" in analogue.confidence(matches, overall)["band"]


# ---- Calibration loop: engine forecasts + point-in-time backtest -----------

# fc1 -- re-specced target: P(turbulence) = non-clean share; realised vol + Brier.
def test_fc1_auto_forecast_helpers():
    import auto_forecast as af
    fc = {"key_assets": {"wti": {"n": 4, "patterns": {"overshoot": 3, "clean_absorption": 1}}}}
    assert af.p_turbulence(fc) == 0.75                       # (4-1)/4 non-clean
    assert af.p_turbulence({"key_assets": {}}) is None
    assert af.realized_vol([100, 100, 100, 100]) == 0.0      # flat -> zero vol
    assert af.realized_vol([100, 110, 100, 110]) > 0
    assert af.vol_rose([100, 100, 100], [100, 110, 100]) is True   # calm -> turbulent
    assert af.vol_rose([100, 110, 100], [100, 100, 100]) is False
    assert af.brier(0.7, 1) == 0.09 and af.brier(0.2, 0) == 0.04


# fc2 -- backtest resolution (vol rose, point-in-time) + reliability bins.
def test_fc2_backtest():
    import backtest_analogue as bt
    dates = [f"2020-{1+(d//28):02d}-{1+(d%28):02d}" for d in range(60)]   # 60 daily points
    vals = [100.0] * 60
    for k in range(30, 45):                                  # inject post-event turbulence
        vals[k] = 100.0 + (5 if k % 2 else -5)
    # anchor at index 25 (>=20 both sides): pre calm, post turbulent -> vol rose -> 1
    assert bt.resolve_turbulence(dates, vals, dates[25]) == 1
    assert bt.resolve_turbulence(dates, [100.0] * 60, dates[25]) == 0   # flat both sides
    assert bt.resolve_turbulence(dates, vals, dates[2]) is None         # not enough pre-data
    rel = bt.reliability([{"p": 0.1, "outcome": 1}, {"p": 0.1, "outcome": 0},
                          {"p": 0.9, "outcome": 1}])
    assert rel[0]["n"] == 2 and rel[0]["mean_outcome"] == 0.5
    assert rel[-1]["n"] == 1 and rel[-1]["mean_pred"] == 0.9


# ---- Oil map status --------------------------------------------------------

# om1 -- chokepoint status: PortWatch anomaly wins; else active theatre; else normal.
def test_om1_oil_map_status():
    import backend
    assert backend.oil_map_status("reduced", False) == "disrupted"
    assert backend.oil_map_status("elevated", False) == "elevated"
    assert backend.oil_map_status(None, True) == "watch"      # theatre active
    assert backend.oil_map_status(None, False) == "normal"


# ---- Conflict media intensity (GDELT per-situation) ------------------------

# ci1 -- timeline parsing + volume-ratio banding.
def test_ci1_conflict_intensity():
    import fetch_conflict_intensity as ci
    js = '{"timeline":[{"data":[{"value":1.0},{"value":2.0},{"value":3.0}]}]}'
    assert ci.timeline_values(js) == [1.0, 2.0, 3.0]
    assert ci.timeline_values("garbage") == []
    assert ci.intensity_band(2.0) == "surge"
    assert ci.intensity_band(1.4) == "elevated"
    assert ci.intensity_band(0.9) == "normal"
    assert ci.intensity_band(0.4) == "quiet"
    assert ci.intensity_band(None) == "n/a"


# ---- Source-aware transmission (the 'stop lying' fix) -----------------------

# sa1 -- channel classification: an oil-producer theatre = supply channel; else demand.
def test_sa1_channel_of():
    import gpr_signal as g
    assert g.channel_of(["iran"]) == "supply"
    assert g.channel_of([]) == "demand"


# sa2 -- the verdict compares EXPECTED direction (from source) to the REAL oil move.
def test_sa2_source_aware_verdict():
    import gpr_signal as g
    # supply theatre + oil FALLING = the divergence the old engine missed
    d = g.source_aware_verdict("supply", -7.9, ["iran"])
    assert d["flag"] == "divergence" and d["expected"] == "up" and d["actual"] == "down"
    # supply theatre + oil rising = premium confirming
    assert g.source_aware_verdict("supply", 5.0, ["iran"])["flag"] == "confirmed"
    # diffuse risk + oil falling = the demand channel, consistent
    assert g.source_aware_verdict("demand", -3.0, [])["flag"] == "consistent"
    # diffuse risk + oil rising = watch (a supply factor may be emerging)
    assert g.source_aware_verdict("demand", 4.0, [])["flag"] == "watch"
    # flat / missing
    assert g.source_aware_verdict("supply", 0.4, ["iran"])["flag"] == "flat"
    assert g.source_aware_verdict("supply", None, ["iran"])["flag"] == "unknown"


# ---- Stories layer (thin first version) ------------------------------------

# st1 -- band severity: stress detection + change detection + nearest watch date.
def test_st1_story_logic():
    import story
    assert story.worsened("comfortable", "stress") is True
    assert story.worsened("stress", "comfortable") is False
    assert story.worsened("stress", "stress") is False
    prev = [{"country": "saudi", "band": "balanced", "gap": 5.0}]
    new = [{"country": "saudi", "band": "stress", "gap": -7.0}]
    ch = story.detect_changes(prev, new)
    assert len(ch) == 2                                    # worsened + crossed breakeven
    assert any("worsened" in c for c in ch) and any("below" in c for c in ch)
    assert story.detect_changes(prev, prev) == []         # no change -> nothing pings
    w = story.nearest_watch([{"date": "2026-08-02", "event": "OPEC+"}], "2026-07-28")
    assert w["days_away"] == 5 and w["event"] == "OPEC+"
    assert story.nearest_watch([{"date": "2020-01-01", "event": "past"}], "2026-07-28") is None


# ---- Calibration (honest OOS validation of the analogue math) --------------

# cal1 -- isotonic (PAV) is monotone non-decreasing; predict clamps to [0,1].
def test_cal1_isotonic():
    import calibrate
    sx, fit = calibrate.isotonic([1, 2, 3], [0.0, 1.0, 0.0])
    assert fit == sorted(fit)                       # monotone non-decreasing (PAV)
    assert abs(fit[1] - 0.5) < 1e-9                 # the 1,0 violators pool to 0.5
    assert 0.0 <= calibrate.predict(sx, fit, 2.5) <= 1.0
    assert abs(calibrate.brier(0.7, 1) - 0.09) < 1e-9
