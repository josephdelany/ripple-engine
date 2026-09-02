"""
read.py -- PATH Step 7 / BUILD_V3 S5: the read.

Stand at date t on a development and say what history's nearest states did next -- as frequencies
with their n, never as an invented probability:
  G  the IES-90 escalation level reached in (d, d+90] (0 none / 1 threat or display / 2 use of force / 3 war;
     OUTCOME_MAPPING.md Amendment 1+1.1, from independent dated sources, event_outcomes source='ies90') and the
     DEAL flag, geopolitical classes only: counts / n over the analogs. sr_outcome_90 is retired (never used).
  P  the price outcome at the tier's horizon (+20 trading days on Brent; +3 months on WTI monthly):
     the EMPIRICAL distribution of the analogs' realized % changes (every value kept, so CRPS/PIT/
     pinball can be scored on it), with quantiles and n
  F  realized flow disruption: the share of analogs whose move was a large sustained one-way supply
     signal (|chg| >= 10%) -- a PRICE PROXY until flow history exists (2026->), labelled so
  M  materiality: MATERIAL when the analogs sat inside a Big Moves window at >= 1.2x the everyday rate
     (the registered gate ratio in CLAIM_LEDGER_REGISTRATION §1 / materiality.py), else NOT_MATERIAL
  propagation per branch through the measured `edges` (event x asset CAR20), every hop with its n
  differencing table: field-by-field then-vs-now for each analog, each difference tagged with its
     evidence status ("unmeasured" until the walk records a measured shift in summary.json)

THE FILTRATION (protocol §1), enforced here and tested:
  - a candidate is a precedent only if its event_date < t (knowable) AND its outcome window had
    closed by t: +90 calendar days for the branch label, +H observations for the price path. An
    event whose outcome was still unfolding at t is not evidence at t.
  - the pool is the target's class (same `type`); the tiers are never pooled on the price side
    (a monthly-tier analog carries no Brent path); for the branch model a cross-tier analog is
    admitted (protocol §2: "for the geopolitical branch model only, jointly").
  - standardization is the target's information set at t (similarity.InfoSet).
  - break_filtration=True is the deliberate leak used ONLY by the walk's leakage test (§1).
"""
from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))     # src/ on the path when run as a script
from engine import similarity as S                               # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
WF = DATA / "walk_forward"
FAR_FUTURE = "2200-01-01"     # inside numpy's datetime64[ns] range (2262); 2999 overflowed to index 0

GEO_TYPES = S.GEO_TYPES
LEVELS = S.LEVELS
LEVEL_MEANING = S.LEVEL_MEANING
G_HORIZON_DAYS = 90
TIERS = {
    "daily": {"series": "fred.DCOILBRENTEU", "horizon": 20, "unit": "trading days", "big_moves": "brent",
              "horizons": (15, 20, 25), "before_days": 7},
    "monthly": {"series": "fred.WTISPLC", "horizon": 3, "unit": "months", "big_moves": "wti_monthly",
                "horizons": (3, 12), "before_days": 31},
}
LOG_FLOOR = 0.01           # registered: the floor applied to a zero frequency FOR THE LOG SCORE ONLY
DISRUPTION_MIN = 10.0      # propagate.py: |chg| >= this = a real, sustained supply move
MATERIAL_RATIO = 1.2       # materiality.py MATERIAL_RATIO
CHAIN = [                  # propagate.CHAIN, kept identical so the desk's hops line up
    ("crude", "fred.DCOILBRENTEU", "Brent crude"), ("crude", "fred.DCOILWTICO", "WTI crude"),
    ("refined", "fred.DHOILNYH", "Heating oil / diesel"), ("refined", "fred.DGASUSGULF", "Gulf gasoline"),
    ("margin", "derived.gasoline_crack", "Gasoline crack"), ("margin", "derived.diesel_crack", "Diesel crack"),
    ("gas_lng", "fred.DHHNGSP", "Henry Hub gas"), ("gas_lng", "yf.ttf", "TTF gas (EU)"), ("gas_lng", "yf.jkm", "JKM LNG (Asia)"),
    ("ngl", "fred.DPROPANEMBTX", "Propane"), ("fertilizer", "fred.PCU325311325311", "Nitrogen fertilizer PPI"),
    ("cross", "yf.sp500", "S&P 500"), ("cross", "fred.BAMLH0A0HYM2", "US HY credit"),
]


# ============================================================================ the corpus, loaded once

class Corpus:
    """Everything the read needs, loaded once; every question is asked 'as of t'.

    events: list of event dicts (events table rows) sorted by date.
    info:   similarity.InfoSet for the continuous fields.
    prices: {tier: pd.Series} the tier's spine series.
    edges:  {(event_id, series_id): car20_pct}.
    big_moves: {tier: {"windows": [(start, end)], "base_pct": everyday base rate %}}.
    panel:  optional {event_id: [situation_state rows]} (the Step 3 seam); schema_extra from the codebook.
    ies90:  {event_id: {"level": "0".."3", "deal": 0/1/None}} -- the G target (Amendment 1); an event absent
            here has no independent outcome and is neither scored on G nor used as G evidence."""

    def __init__(self, events, info, prices, edges=None, big_moves=None, panel=None, schema_extra=None, ies90=None):
        self.events = sorted(events, key=lambda e: (e["event_date"], e["event_id"]))
        self.by_id = {e["event_id"]: e for e in self.events}
        self.info = info
        self.prices = {k: v for k, v in prices.items() if v is not None and len(v)}
        self.edges = edges or {}
        self.big_moves = big_moves or {}
        self.panel = panel or {}
        self.schema_extra = schema_extra or {}
        self.ies90 = ies90 or {}
        self.daily_start = self.prices["daily"].index[0] if "daily" in self.prices else pd.Timestamp(FAR_FUTURE)
        self._vec = {}
        self._out = {}
        for e in self.events:
            e["tier"] = self.tier_of(e["event_date"])

    def tier_of(self, date):
        return "daily" if pd.Timestamp(date) >= self.daily_start else "monthly"

    def vector(self, event_id):
        """The state of the world at that event's own date (cached)."""
        if event_id not in self._vec:
            e = self.by_id[event_id]
            v = S.state_vector(e, info=self.info, panel_rows=self.panel.get(event_id), schema_extra=self.schema_extra)
            lab = self.ies90.get(event_id)
            v["outcome"] = lab["level"] if lab else None          # the IES-90 level: label only, never a similarity field
            v["deal"] = lab["deal"] if lab else None
            self._vec[event_id] = v
        return self._vec[event_id]

    # ---- outcomes (looked up by the walk only AFTER sealing; the read never calls these on the target)
    def path(self, event_id, tier=None, hmax=None):
        """% path from the first observation on/after the event date: [0, +1, ..., +hmax]; None if no data."""
        e = self.by_id[event_id]
        tier = tier or e["tier"]
        s = self.prices.get(tier)
        if s is None:
            return None
        hmax = hmax or max(TIERS[tier]["horizons"])
        d = pd.Timestamp(e["event_date"])
        if d < s.index[0]:
            return None
        pos = int(s.index.searchsorted(d))
        if pos >= len(s):
            return None
        seg = s.iloc[pos:pos + hmax + 1].to_numpy(float)
        return {"dates": [str(x.date()) for x in s.index[pos:pos + hmax + 1]],
                "pct": ((seg / seg[0] - 1.0) * 100.0).tolist()}

    def outcome(self, event_id, horizon=None, tier=None):
        """Realized % change at +horizon (default: the tier's registered horizon), or None if the window
        has not closed in the data."""
        e = self.by_id[event_id]
        tier = tier or e["tier"]
        h = horizon or TIERS[tier]["horizon"]
        key = (event_id, tier, h)
        if key not in self._out:
            p = self.path(event_id, tier, hmax=h)
            self._out[key] = None if (p is None or len(p["pct"]) < h + 1) else \
                {"chg_pct": float(p["pct"][h]), "closed_on": p["dates"][h]}
        return self._out[key]

    def closed_by(self, event_id, as_of, horizon=None):
        """True when the price window of event_id had closed (its +H observation is dated <= as_of)."""
        o = self.outcome(event_id, horizon)
        return o is not None and pd.Timestamp(o["closed_on"]) <= pd.Timestamp(as_of)

    def g_closed_by(self, event_id, as_of):
        e = self.by_id[event_id]
        return pd.Timestamp(e["event_date"]) + pd.Timedelta(days=G_HORIZON_DAYS) <= pd.Timestamp(as_of)

    def in_big_move(self, event_id):
        e = self.by_id[event_id]
        bm = self.big_moves.get(e["tier"])
        if not bm:
            return None
        d = pd.Timestamp(e["event_date"])
        return any(pd.Timestamp(a) <= d <= pd.Timestamp(b) for a, b in bm["windows"])

    def big_move_base(self, tier):
        bm = self.big_moves.get(tier)
        return None if not bm else bm.get("base_pct")

    # ---- the pool at t (the filtration)
    def pool(self, target, as_of, break_filtration=False, horizon=None):
        """Candidates for a target: same class; event_date < as_of; outcome window closed by as_of
        (G for geo classes; P for same-tier candidates). With break_filtration=True every class event
        is admitted regardless of date -- the deliberate leak for the leakage test only."""
        out = []
        ttier = target.get("tier") or self.tier_of(target["date"])
        for e in self.events:
            if e["type"] != target["type"] or e["event_id"] == target.get("event_id"):
                continue
            if break_filtration:
                out.append(self.vector(e["event_id"]) | {"tier": e["tier"],
                                                          "p_closed": e["tier"] == ttier and self.outcome(e["event_id"], horizon) is not None,
                                                          "g_closed": e["type"] in GEO_TYPES and e["event_id"] in self.ies90})
                continue
            if not (e["event_date"] < str(pd.Timestamp(as_of).date())):
                continue
            g_ok = e["type"] in GEO_TYPES and self.g_closed_by(e["event_id"], as_of) and e["event_id"] in self.ies90
            p_ok = e["tier"] == ttier and self.closed_by(e["event_id"], as_of, horizon)
            if not (g_ok or p_ok):
                continue
            out.append(self.vector(e["event_id"]) | {"tier": e["tier"], "p_closed": p_ok, "g_closed": g_ok})
        return out


def _series(conn, sid):
    return S._series(conn, sid)


def _big_moves(tier):
    p = DATA / "big_moves" / f"{TIERS[tier]['big_moves']}.json"
    if not p.exists():
        return None
    j = json.load(open(p))
    before = TIERS[tier]["before_days"]
    win = [(str((pd.Timestamp(m["onset"]) - pd.Timedelta(days=before)).date()), m["end"]) for m in j["episodes"]]
    return {"windows": win, "base_pct": j.get("everyday_base_rate_pct"), "n_episodes": j.get("n_episodes")}


def _panel_rows(conn):
    """The Step 3 seam: if session A's situation_state table exists, load it per event (all vintages;
    apply_panel enforces vintage <= t at read time). Absent table -> {} (inert)."""
    try:
        has = conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name='situation_state'").fetchone()
        if not has:
            return {}
        rows = {}
        for eid, f, v, vin, src in conn.execute("SELECT event_id, field, value, vintage, source FROM situation_state"):
            rows.setdefault(eid, []).append({"field": f, "value": v, "vintage": vin, "source": src})
        return rows
    except Exception:
        return {}


def _ies90(conn):
    """OUTCOME_MAPPING.md Amendment 1: the IES-90 level (0-3) and DEAL flag per geopolitical event, from
    event_outcomes rows with source='ies90' (written by src/state/ies90.py; session A). An event with
    no_independent_outcome has no level and is absent here -- never guessed. Absent table -> {}."""
    try:
        if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='event_outcomes'").fetchone():
            return {}
        out = {}
        for eid, f, v in conn.execute("SELECT event_id, field, value FROM event_outcomes WHERE source='ies90' AND field IN ('level', 'deal')"):
            d = out.setdefault(eid, {"level": None, "deal": None})
            if v is not None:
                d[f] = str(int(v)) if f == "level" else int(v)
        return {e: d for e, d in out.items() if d["level"] in LEVELS}
    except Exception:
        return {}


def corpus_from_db(conn):
    events = S.load_events(conn)
    extra = {}
    prop = pd.Series({pd.Timestamp(e["event_date"]): e["sr_actor_propensity"] for e in events
                      if not S.is_unknown(e.get("sr_actor_propensity"))})
    if len(prop):
        extra["propensity"] = prop.sort_index()
    info = S.InfoSet.from_db(conn, extra=extra)
    prices = {t: _series(conn, cfg["series"]) for t, cfg in TIERS.items()}
    edges = {(r[0], r[1]): float(r[2]) for r in conn.execute(
        "SELECT event_id, target_series, car20 FROM edges WHERE units='%' AND car20 IS NOT NULL")}
    return Corpus(events, info, prices, edges=edges, big_moves={t: _big_moves(t) for t in TIERS},
                  panel=_panel_rows(conn), schema_extra=S.codebook_schema(), ies90=_ies90(conn))


Corpus.from_db = staticmethod(corpus_from_db)


# ============================================================================ the read

def _quantiles(vals):
    a = np.asarray(vals, float)
    return {"p10": round(float(np.percentile(a, 10)), 2), "p50": round(float(np.percentile(a, 50)), 2),
            "p90": round(float(np.percentile(a, 90)), 2), "mean": round(float(a.mean()), 2),
            "min": round(float(a.min()), 2), "max": round(float(a.max()), 2)}


def g_distribution(analogs):
    """Frequencies over the analogs' IES-90 levels (ordinal 0-3) and, separately, the DEAL rate over the analogs
    whose DEAL flag is known (null when neither ICB nor MID covered the analog's window)."""
    closed = [a for a in analogs if a.get("g_closed") and a.get("outcome") in LEVELS]
    outs = [a["outcome"] for a in closed]
    deals = [a["deal"] for a in closed if a.get("deal") in (0, 1)]
    n = len(outs)
    counts = {b: outs.count(b) for b in LEVELS}
    deal = {"n": len(deals), "rate": (round(sum(deals) / len(deals), 4) if deals else None)}
    if n == 0:
        return {"n": 0, "counts": counts, "rates": None, "probs_for_log_score": None, "deal": deal, "levels": LEVEL_MEANING}
    rates = {b: counts[b] / n for b in LEVELS}
    floored = {b: max(rates[b], LOG_FLOOR) for b in LEVELS}
    z = sum(floored.values())
    return {"n": n, "counts": counts, "rates": {b: round(rates[b], 4) for b in LEVELS},
            "probs_for_log_score": {b: round(floored[b] / z, 4) for b in LEVELS}, "deal": deal, "levels": LEVEL_MEANING,
            "log_floor": LOG_FLOOR,
            "basis": "frequency over the analogs' IES-90 levels in (d, d+90] (OUTCOME_MAPPING.md Amendment 1+1.1: independent dated sources; 30-event audit pending)"}


def p_distribution(corpus, analogs, tier, horizon=None):
    h = horizon or TIERS[tier]["horizon"]
    vals, ids = [], []
    for a in analogs:
        if not a.get("p_closed") or a.get("tier") != tier:
            continue
        o = corpus.outcome(a["event_id"], h, tier)
        if o is not None:
            vals.append(round(o["chg_pct"], 3)); ids.append(a["event_id"])
    if not vals:
        return {"n": 0, "values": [], "horizon": h, "unit": TIERS[tier]["unit"], "series": TIERS[tier]["series"]}
    return {"n": len(vals), "values": vals, "analog_ids": ids, "horizon": h, "unit": TIERS[tier]["unit"],
            "series": TIERS[tier]["series"], **_quantiles(vals),
            "share_up": round(sum(1 for v in vals if v > 0) / len(vals), 3),
            "share_abs_ge_10": round(sum(1 for v in vals if abs(v) >= DISRUPTION_MIN) / len(vals), 3)}


def f_read(p):
    if not p.get("n"):
        return {"n": 0, "realized_disruption_share": None}
    return {"n": p["n"], "realized_disruption_share": p["share_abs_ge_10"],
            "basis": f"share of analogs with |{TIERS['daily']['series'] if p['series'].endswith('BRENTEU') else p['series']}| move >= {DISRUPTION_MIN:.0f}%",
            "caveat": "price proxy: flow history (PortWatch) begins 2026; the flow side of P is a price proxy until then (protocol §9)"}


def m_read(corpus, analogs, tier):
    flags = [corpus.in_big_move(a["event_id"]) for a in analogs if a.get("tier") == tier]
    flags = [f for f in flags if f is not None]
    base = corpus.big_move_base(tier)
    if not flags or not base:
        return {"n": len(flags), "call": None, "rate_pct": None, "base_pct": base, "ratio": None}
    rate = 100.0 * sum(flags) / len(flags)
    ratio = rate / base
    return {"n": len(flags), "k": int(sum(flags)), "rate_pct": round(rate, 1), "base_pct": base, "ratio": round(ratio, 2),
            "call": "MATERIAL" if ratio >= MATERIAL_RATIO else "NOT_MATERIAL", "rule": f"MATERIAL if rate/base >= {MATERIAL_RATIO}"}


def propagation(corpus, subset, tier):
    """Per IES-90 level (geo; keyed by the level string, meaning in LEVEL_MEANING) or ALL: at each hop of the
    value chain, the measured CAR20 of the conditioned subset's members that reached that level. Every hop
    carries its n."""
    def hops(ids):
        out = []
        for hop_tier, sid, label in CHAIN:
            cars = [corpus.edges[(i, sid)] for i in ids if (i, sid) in corpus.edges]
            if not cars:
                continue
            out.append({"tier": hop_tier, "series_id": sid, "label": label, "n": len(cars),
                        "signed_median_pct": round(st.median(cars), 2), "avg_pct": round(st.mean(cars), 2),
                        "lo": round(min(cars), 1), "hi": round(max(cars), 1),
                        "material_move_pct": round(100 * sum(1 for v in cars if abs(v) >= DISRUPTION_MIN) / len(cars)),
                        "no_lasting_move_pct": round(100 * sum(1 for v in cars if abs(v) < 5) / len(cars))})
        return out
    ids_all = [a["event_id"] for a in subset if a.get("tier") == "daily"]      # edges exist on the daily tier only
    out = {"ALL": {"contributing_n": len(ids_all), "hops": hops(ids_all)}}
    for b in LEVELS:
        ids = [a["event_id"] for a in subset if a.get("tier") == "daily" and a.get("outcome") == b]
        if ids:
            out[b] = {"level": LEVEL_MEANING[b], "contributing_n": len(ids), "hops": hops(ids)}
    out["caveat"] = "PRICE side measured from edges (1987+, daily tier); historical FLOW per branch is a stated gap"
    return out


def _field_evidence():
    try:
        return json.load(open(WF / "summary.json")).get("field_evidence") or {}
    except Exception:
        return {}


def differencing(target, analogs, evidence=None):
    ev = evidence if evidence is not None else _field_evidence()
    rows = []
    for a in analogs:
        cand_fields = {}
        for blk, c in a["blocks"].items():
            for f, d in c["fields"].items():
                cand_fields[f] = d
        likes, diffs = [], []
        for f, d in sorted(cand_fields.items()):
            now = target["fields"].get(f)
            row = {"field": f, "block": S.kind_of(f)[0], "now": now, "distance": d}
            (likes if d == 0 else diffs).append(row | ({"evidence": ev.get(f, "judgment, unmeasured (the walk has not measured this field's shift)")} if d else {}))
        rows.append({"event_id": a["event_id"], "date": a["date"], "similarity": a["similarity"],
                     "likenesses": likes, "differences": diffs})
    return rows


def read(corpus, target, as_of=None, weighting=None, k=None, break_filtration=False, horizon=None,
         with_propagation=True, with_differencing=True):
    """The read for `target` (an events-table dict, or a state-vector-shaped dict for a live story)
    as of `as_of` (default: the target's date). Returns G/P/F/M with n, propagation, differencing,
    and the analogs with per-block contributions -- or the no-precedent envelope with NO numbers."""
    if "fields" not in target:
        tgt = corpus.vector(target["event_id"]) if target.get("event_id") in corpus.by_id else \
            S.state_vector(target, info=corpus.info, schema_extra=corpus.schema_extra)
    else:
        tgt = target
    tgt = dict(tgt)
    tgt["tier"] = tgt.get("tier") or corpus.tier_of(tgt["date"])
    as_of = str(pd.Timestamp(as_of or tgt["date"]).date())
    tier = tgt["tier"]
    cands = corpus.pool(tgt, as_of, break_filtration=break_filtration, horizon=horizon)
    t_for_scale = FAR_FUTURE if break_filtration else as_of
    ret = S.retrieve(tgt, cands, corpus.info, t=t_for_scale, weighting=weighting, k=k, schema_extra=corpus.schema_extra)
    envelope = {"event_id": tgt.get("event_id"), "date": tgt["date"], "as_of": as_of, "type": tgt["type"], "tier": tier,
                "weighting": ret["weighting"], "k": ret["k"], "threshold": ret["threshold"],
                "filtration": {"rule": "class pool; event_date < as_of; outcome window closed by as_of; scale from data before as_of",
                               "broken": bool(break_filtration), "n_pool": ret["n_pool"]},
                "state": {"n_known": tgt["n_known"], "unknown": tgt["unknown"]},
                "max_similarity": ret["max_similarity"], "conditioned_n": ret["conditioned_n"]}
    if ret["no_adequate_precedent"]:
        return envelope | {"no_adequate_precedent": True, "analogs": [], "G": None, "P": None, "F": None, "M": None,
                           "propagation": None, "differencing": None,
                           "note": f"max similarity {ret['max_similarity']} below the registered threshold {ret['threshold']}: no numbers"}
    analogs = ret["analogs"]
    subset = [r for r in ret["ranked"] if r["similarity"] >= ret["threshold"]]
    by_id = {c["event_id"]: c for c in cands}
    for a in analogs + subset:
        c = by_id[a["event_id"]]
        a["tier"], a["p_closed"], a["g_closed"] = c["tier"], c["p_closed"], c["g_closed"]
    p = p_distribution(corpus, analogs, tier, horizon)
    out = envelope | {
        "no_adequate_precedent": False,
        "analogs": [{k_: v for k_, v in a.items() if k_ != "blocks"} | {"blocks": {b: {"distance": c["distance"], "n_fields": c["n_fields"], "share_of_distance": c.get("share_of_distance", 0.0)} for b, c in a["blocks"].items()}} for a in analogs],
        "G": g_distribution(analogs) if tgt["type"] in GEO_TYPES else {"applicable": False, "note": "the IES-90 escalation level applies to geopolitical classes only"},
        "P": p, "F": f_read(p), "M": m_read(corpus, analogs, tier),
        "block_contributions": {b: round(float(np.mean([a["blocks"][b]["share_of_distance"] for a in analogs if b in a["blocks"]] or [0.0])), 4)
                                for b in sorted({b for a in analogs for b in a["blocks"]})},
    }
    if with_propagation:
        out["propagation"] = propagation(corpus, subset, tier)
    if with_differencing:
        out["differencing"] = differencing(tgt, analogs)
    return out


if __name__ == "__main__":
    from _db import connect
    conn = connect(read_only=True)
    corpus = Corpus.from_db(conn)
    eid = sys.argv[1] if len(sys.argv) > 1 else "abqaiq_attack_2019"
    r = read(corpus, corpus.by_id[eid], weighting=S.load_menu()["items"][0])
    slim = {k: v for k, v in r.items() if k not in ("differencing", "propagation", "analogs")}
    slim["analogs"] = [(a["date"], a["similarity"], a["outcome"], a["title"][:40]) for a in r["analogs"]]
    slim["propagation_ALL_hops"] = [(h["label"], h["n"], h["signed_median_pct"]) for h in (r.get("propagation") or {}).get("ALL", {}).get("hops", [])]
    print(json.dumps(slim, indent=1, default=str)[:5000])
