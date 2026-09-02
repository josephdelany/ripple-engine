"""
similarity.py -- PATH Step 6 / BUILD_V3 S5: similarity on the state.

WHAT IT DOES (plain English)
A "state vector" is everything the engine knew about the world when a shock landed: who did
what to whom (the coded situation fields), and what the market already said (VIX, curve,
inventories, positioning, geopolitical-risk index, crude momentum...). This module measures
how far two such states are apart, block by block, using ONLY information available at the
date of the read, and returns the nearest past states as analogs -- or says "no adequate
precedent" when nothing on record is close enough.

DISCIPLINE (each item is unit-tested in tests/test_similarity.py)
  - identical states -> distance 0 (similarity 1).
  - a field unknown on EITHER side is excluded from the distance and COUNTED (never imputed).
  - continuous fields are standardized (z-scored) within the information set at t: mean and sd
    come only from observations dated STRICTLY BEFORE t. A value that arrives after t cannot move
    the scale (asserted by injecting a future outlier).
  - categorical fields: match 0 / mismatch 1.
  - block-wise: per-block distance is the field-weighted mean of field distances over the KNOWN
    fields; the total is the block-weighted mean over blocks that have >= 1 known field. Per-block
    contributions are returned so the read can show why an analog is an analog.
  - retrieval threshold: max similarity below RETRIEVE_MIN -> no precedent, no numbers.
  - the weights are the registered menu (data/walk_forward/menu.json, <= 12 items; protocol §5);
    field weights are uniform within a block.

THE SEAM FOR THE STATE PANEL (PATH Steps 2-3, built by session A)
Today's fields are the situation codings on `events` (sr_*) and the market signals in
`observations`. When `situation_state(event_id, field, value, vintage, source)` lands, rows with
vintage <= t are merged by apply_panel(); their block comes from WORLD_STATE_CODEBOOK.md (parsed
by codebook_schema()), continuous vs categorical from the value. Nothing here imports src/state/.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
MENU_PATH = DATA / "walk_forward" / "menu.json"
CODEBOOK_PATH = ROOT / "WORLD_STATE_CODEBOOK.md"

GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
# The G target (OUTCOME_MAPPING.md Amendment 1, 2026-09-02): the IES-90 ordinal level reached in (d, d+90] from
# independent DATED sources, plus a DEAL flag. sr_outcome_90 is RETIRED as an outcome: never a target, a feature or
# analog evidence. Levels are strings so a sealed read round-trips through JSON unchanged.
LEVELS = ("0", "1", "2", "3")
LEVEL_MEANING = {"0": "none", "1": "threat or display of force", "2": "use of force", "3": "war"}
# the six framework blocks (WORLD_STATE_FRAMEWORK §3) plus "situation" = the coded sr_* fields we have today
BLOCKS = ("situation", "market", "physical", "actors", "dyads", "system", "narrative")
UNKNOWN = (None, "unknown", "")
Z_CAP = 3.0            # a z-gap of 3 sd or more counts as a full mismatch (distance 1)
RETRIEVE_MIN = 0.40    # registered default (escalation.py kept it; the menu may vary it)
COND_MIN_N = 8         # a conditioned subset needs this many members (escalation.py, unchanged)
DEFAULT_K = 8
MIN_STD_N = 30         # fewer prior observations than this -> the field is "unknown" at t (no scale yet)
MIN_COMPARED = 3       # a candidate with fewer comparable fields than this cannot be a precedent (registered)

# ---- today's fields: name -> (block, kind); kind "cat" (match/mismatch) or "num" (standardized) ----
SCHEMA = {
    "actor": ("situation", "cat"), "target": ("situation", "cat"),
    "conflict_scope": ("situation", "cat"), "tempo": ("situation", "cat"),
    "prior_dyad": ("situation", "cat"), "asset_role": ("situation", "cat"),
    "propensity": ("situation", "num"),
    # market block: value observed strictly before t (state at t-1; CLAUDE.md point-in-time rule)
    "vix_pct": ("market", "num"), "ovx_pct": ("market", "num"), "brent_vol20": ("market", "num"),
    "inv_sigma": ("market", "num"), "cot_pct": ("market", "num"), "curve_2s10s": ("market", "num"),
    "usd_z": ("market", "num"), "credit_stress": ("market", "num"), "real_rate": ("market", "num"),
    "gpr": ("market", "num"), "conflict_intensity_pct": ("market", "num"),
    "diesel_crack": ("market", "num"), "brent_wti_spread_z": ("market", "num"),
    "brent_chg20_pct": ("market", "num"),      # daily tier momentum: Brent t-1 vs t-21 trading days
    "wti_m_chg3_pct": ("market", "num"),       # monthly tier momentum: WTISPLC t-1 vs t-4 months
}
MARKET_SERIES = {
    "vix_pct": "derived.vix_pct", "ovx_pct": "derived.ovx_pct", "brent_vol20": "derived.brent_vol20",
    "inv_sigma": "derived.inv_sigma", "cot_pct": "derived.cot_pct", "curve_2s10s": "derived.curve_2s10s",
    "usd_z": "derived.usd_z", "credit_stress": "derived.credit_stress", "real_rate": "derived.real_rate",
    "gpr": "gpr.GPRD", "conflict_intensity_pct": "derived.conflict_intensity_pct",
    "diesel_crack": "derived.diesel_crack", "brent_wti_spread_z": "derived.brent_wti_spread_z",
}
MOMENTUM = {  # field -> (series, lag in observations)
    "brent_chg20_pct": ("fred.DCOILBRENTEU", 20),
    "wti_m_chg3_pct": ("fred.WTISPLC", 3),
}
SR_MAP = {"actor": "sr_actor", "target": "sr_target", "conflict_scope": "sr_conflict_scope",
          "tempo": "sr_tempo", "prior_dyad": "sr_prior_dyad", "asset_role": "sr_asset_role",
          "propensity": "sr_actor_propensity"}


def is_unknown(v):
    if v in UNKNOWN:
        return True
    try:
        return bool(np.isnan(float(v))) if isinstance(v, (float, int, np.floating)) else False
    except (TypeError, ValueError):
        return False


# ============================================================================ the information set

# WALK_FORWARD_PROTOCOL.md Amendment G (2026-09-02): release lags applied in the engine, in calendar days. An
# observation dated d is visible at t only if d + lag < t. cot_pct: CFTC COT positions as of Tuesday, released
# Friday (3); inv_sigma: EIA WPSR week ending Friday, released the following Wednesday (5). Holidays not modelled.
RELEASE_LAGS = {"cot_pct": 3, "inv_sigma": 5}


def _cutoff(field, t):
    """The exclusive upper bound on observation dates visible at t: t - lag(field)."""
    return np.datetime64(pd.Timestamp(t) - pd.Timedelta(days=RELEASE_LAGS.get(field, 0)))


class InfoSet:
    """Everything dated, so that any statistic can be asked 'as of t' and use only data before t.

    series: {field: pd.Series indexed by Timestamp} for continuous fields. Standardization stats
    (mean, sd, n) at t are computed from values with date < t only -- expanding window, never the
    full history. Cumulative sums make each query O(log n)."""

    def __init__(self, series: dict):
        self._s = {}
        for f, s in series.items():
            s = s.dropna().astype(float).sort_index()
            if s.empty:
                continue
            v = s.to_numpy()
            self._s[f] = (s.index.to_numpy(), v, np.cumsum(v), np.cumsum(v * v))

    @classmethod
    def from_db(cls, conn, extra: dict | None = None):
        """Load today's market fields (and momentum) from observations; `extra` adds event-level
        numeric fields as {field: Series indexed by event_date} (e.g. propensity, or panel fields)."""
        series = {}
        for f, sid in MARKET_SERIES.items():
            series[f] = _series(conn, sid)
        for f, (sid, lag) in MOMENTUM.items():
            s = _series(conn, sid)
            if not s.empty:
                series[f] = (s / s.shift(lag) - 1.0) * 100.0
        if extra:
            series.update(extra)
        return cls(series)

    def fields(self):
        return list(self._s)

    def value_before(self, field, t):
        """Last observed value dated strictly before t, else None."""
        if field not in self._s:
            return None
        idx, v, _, _ = self._s[field]
        i = np.searchsorted(idx, _cutoff(field, t)) - 1   # last index with date < t - lag (Amendment G)
        return float(v[i]) if i >= 0 else None

    def independent_value_before(self, field, t):
        """The same question answered by a boolean mask instead of searchsorted -- the filtration audit's
        independent path (Amendment F.1). Returns (value, obs_date) or (None, None)."""
        if field not in self._s:
            return None, None
        idx, v, _, _ = self._s[field]
        ok = idx < _cutoff(field, t)
        if not ok.any():
            return None, None
        j = int(np.flatnonzero(ok)[-1])
        return float(v[j]), str(pd.Timestamp(idx[j]).date())

    def stats(self, field, t):
        """(mean, sd, n) over observations dated strictly before t. None if n < MIN_STD_N or sd == 0."""
        if field not in self._s:
            return None
        idx, v, c1, c2 = self._s[field]
        n = int(np.searchsorted(idx, _cutoff(field, t)))   # count of dates < t
        if n < MIN_STD_N:
            return None
        mean = c1[n - 1] / n
        var = max(c2[n - 1] / n - mean * mean, 0.0)
        sd = float(np.sqrt(var))
        return (float(mean), sd, n) if sd > 0 else None


def _series(conn, sid):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                     "ORDER BY obs_date, as_of", conn, params=(sid,))
    if df.empty:
        return pd.Series(dtype=float)
    df = df.drop_duplicates("obs_date", keep="last")
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    return df.set_index("obs_date")["value"].astype(float)


# ============================================================================ the codebook seam

def codebook_schema(path=CODEBOOK_PATH):
    """Parse WORLD_STATE_CODEBOOK.md (session A, PATH Step 1) into {field: (block, kind)}.
    Tolerant: finds the first markdown table whose header names a 'field' and a 'block' column.
    kind = 'cat' when the unit column says category/code/label/text/bool, else 'num'.
    Returns {} when the codebook does not exist yet (the seam is inert until Step 1 lands)."""
    p = Path(path)
    if not p.exists():
        return {}
    out, header = {}, None
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            header = None if header and not out else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if header is None:
            if "field" in low and "block" in low:
                header = low
            continue
        if set(c.replace("-", "").replace(":", "") for c in cells) <= {""}:
            continue                                        # the |---|---| separator row
        row = dict(zip(header, cells))
        f, b = row.get("field", ""), row.get("block", "").lower()
        if not f or not b:
            continue
        unit = row.get("unit", "").lower()
        kind = "cat" if any(w in unit for w in ("categor", "code", "label", "text", "bool", "flag")) else "num"
        out[f] = (b, kind)
    return out


def apply_panel(fields, rows, as_of, schema_extra=None):
    """Merge situation_state-shaped rows into a field dict, honouring the vintage rule.
    rows: iterable of dicts/tuples (field, value, vintage[, source]). A row with vintage > as_of
    is invisible at as_of (PATH Step 3 test_vintage_rule, enforced here as well). Fields not in
    SCHEMA are typed from the codebook (schema_extra) or, failing that, by value (float -> num)."""
    as_of = pd.Timestamp(as_of)
    added = {}
    for r in rows or []:
        if isinstance(r, dict):
            f, v, vin = r.get("field"), r.get("value"), r.get("vintage")
        else:
            f, v, vin = r[0], r[1], r[2] if len(r) > 2 else None
        if f is None or is_unknown(v) or str(f).startswith("sr_"):
            continue                                        # sr_* rows are the situation record (Amendment H): read.Corpus.vector applies them
        if vin is not None and pd.Timestamp(vin) > as_of:
            continue                                        # not knowable at as_of
        added[f] = v
    fields.update(added)
    return fields


def kind_of(field, schema_extra=None, value=None):
    """(block, kind) for a field: SCHEMA first, then the codebook, then typed by value under 'panel'."""
    if field in SCHEMA:
        return SCHEMA[field]
    if schema_extra and field in schema_extra:
        return schema_extra[field]
    try:
        float(value); return ("panel", "num")
    except (TypeError, ValueError):
        return ("panel", "cat")


# ============================================================================ state vectors

def state_vector(event, as_of=None, info: InfoSet | None = None, panel_rows=None, schema_extra=None):
    """The state the engine sees for `event` (a dict from the events table) as of `as_of`
    (default: the event date). Market fields are the last observation strictly before as_of;
    a field with fewer than MIN_STD_N prior observations is 'unknown' (no scale yet)."""
    as_of = pd.Timestamp(as_of or event["event_date"])
    fields = {}
    for f, col in SR_MAP.items():
        v = event.get(col)
        fields[f] = None if is_unknown(v) else v
    if info is not None:
        for f in list(MARKET_SERIES) + list(MOMENTUM):
            v = info.value_before(f, as_of)
            fields[f] = None if (v is None or info.stats(f, as_of) is None) else v
    if panel_rows:
        apply_panel(fields, panel_rows, as_of, schema_extra)
    known = [f for f, v in fields.items() if not is_unknown(v)]
    return {"event_id": event.get("event_id"), "date": str(as_of.date()), "type": event.get("type"),
            "title": event.get("title", ""), "outcome": None, "deal": None,     # IES-90 label: attached by read.Corpus.vector
            "fields": fields, "n_known": len(known),
            "unknown": sorted(f for f in fields if f not in known)}


# ============================================================================ distance

def field_distance(f, a, b, info: InfoSet | None, t, schema_extra=None):
    """Distance in [0,1] for one field, or None when unknown on either side / no scale at t."""
    if is_unknown(a) or is_unknown(b):
        return None
    _, kind = kind_of(f, schema_extra, a)
    if kind == "cat":
        return 0.0 if str(a) == str(b) else 1.0
    st = info.stats(f, t) if info is not None else None
    if st is None:
        return None                                         # no point-in-time scale -> not comparable
    mean, sd, _ = st
    za, zb = (float(a) - mean) / sd, (float(b) - mean) / sd
    return float(min(abs(za - zb) / Z_CAP, 1.0))


def distance(target, cand, info: InfoSet | None, t=None, block_weights=None, field_weights=None,
             schema_extra=None):
    """Block-wise weighted distance between two state vectors as of t (default: target date).
    Returns (distance, detail) with per-block contributions and the unknown count."""
    t = pd.Timestamp(t or target["date"])
    bw = block_weights or {}
    fw = field_weights or {}
    per_block = {}
    n_unknown = 0
    fields = set(target["fields"]) | set(cand["fields"])
    for f in sorted(fields):
        a, b = target["fields"].get(f), cand["fields"].get(f)
        d = field_distance(f, a, b, info, t, schema_extra)
        blk, _ = kind_of(f, schema_extra, a if not is_unknown(a) else b)
        if d is None:
            n_unknown += 1
            continue
        w = float(fw.get(f, 1.0))
        pb = per_block.setdefault(blk, {"num": 0.0, "den": 0.0, "n_fields": 0, "fields": {}})
        pb["num"] += w * d; pb["den"] += w; pb["n_fields"] += 1; pb["fields"][f] = round(d, 4)
    num = den = 0.0
    contrib = {}
    for blk, pb in per_block.items():
        w = float(bw.get(blk, 1.0))
        d_blk = pb["num"] / pb["den"] if pb["den"] else 0.0
        contrib[blk] = {"distance": round(d_blk, 4), "weight": w, "n_fields": pb["n_fields"], "fields": pb["fields"]}
        num += w * d_blk; den += w
    if den <= 0:
        return 1.0, {"blocks": contrib, "n_unknown": n_unknown, "n_compared": 0, "comparable": False}
    total = num / den
    for blk, c in contrib.items():
        c["share_of_distance"] = round((c["weight"] * c["distance"]) / num, 4) if num > 0 else 0.0
    return float(total), {"blocks": contrib, "n_unknown": n_unknown,
                          "n_compared": sum(c["n_fields"] for c in contrib.values()), "comparable": True}


def similarity(target, cand, info=None, t=None, block_weights=None, field_weights=None, schema_extra=None):
    d, detail = distance(target, cand, info, t, block_weights, field_weights, schema_extra)
    return 1.0 - d, detail


# ============================================================================ the menu + retrieval

def load_menu(path=MENU_PATH):
    m = json.load(open(path))
    n_w = sum(1 for it in m["items"] if it.get("kind") != "recalibrated")
    assert n_w <= 12, "protocol §5: the menu is capped at 12 weightings (Amendment C adds one recalibrated item, not a weighting)"
    return m


def weighting_items(menu):
    """The retrieval weightings only (M01-M12); the recalibrated item (Amendment C) is not a weighting."""
    return [it for it in menu["items"] if it.get("kind") != "recalibrated"]


def retrieve(target, candidates, info=None, t=None, weighting=None, k=None, schema_extra=None):
    """Nearest states among `candidates` (already filtered to the information set by the caller:
    the read enforces date < t and closed outcome windows). Returns the ranked list, the analogs
    (top k at/above retrieve_min), the conditioned count, and the no-precedent flag."""
    w = weighting or {}
    bw = w.get("block_weights")
    thr = float(w.get("retrieve_min", RETRIEVE_MIN))
    k = int(k or w.get("k") or DEFAULT_K)
    t = pd.Timestamp(t or target["date"])
    ranked = []
    for c in candidates:
        if c.get("event_id") == target.get("event_id"):
            continue
        s, detail = similarity(target, c, info, t, bw, schema_extra=schema_extra)
        if not detail["comparable"] or detail["n_compared"] < MIN_COMPARED:
            continue                                        # too little measurable in common: not a precedent
        ranked.append({"event_id": c["event_id"], "date": c["date"], "type": c["type"], "title": c.get("title", ""),
                       "outcome": c.get("outcome"), "deal": c.get("deal"), "similarity": round(s, 4), "blocks": detail["blocks"],
                       "n_compared": detail["n_compared"], "n_unknown": detail["n_unknown"]})
    ranked.sort(key=lambda r: (-r["similarity"], r["date"]))
    out = {"threshold": thr, "k": k, "n_pool": len(ranked),
           "max_similarity": ranked[0]["similarity"] if ranked else None,
           "weighting": w.get("id", "uniform")}
    if not ranked or ranked[0]["similarity"] < thr:
        out.update(no_adequate_precedent=True, analogs=[], ranked=ranked[:k], conditioned_n=0)
        return out
    at_thr = [r for r in ranked if r["similarity"] >= thr]
    out.update(no_adequate_precedent=False, analogs=at_thr[:k], ranked=ranked, conditioned_n=len(at_thr))
    return out


def load_events(conn, types=None):
    cols = [c[1] for c in conn.execute("PRAGMA table_info(events)")]
    q = "SELECT * FROM events"
    args = []
    if types:
        q += f" WHERE type IN ({','.join('?' * len(types))})"; args = list(types)
    q += " ORDER BY event_date, event_id"
    return [dict(zip(cols, r)) for r in conn.execute(q, args)]


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from _db import connect
    conn = connect(read_only=True)
    events = load_events(conn)
    info = InfoSet.from_db(conn)
    eid = sys.argv[1] if len(sys.argv) > 1 else "abqaiq_attack_2019"
    ev = next(e for e in events if e["event_id"] == eid)
    tgt = state_vector(ev, info=info)
    # a candidate's state is the world as it stood at ITS OWN date; only the scale is the target's (as of t)
    cands = [state_vector(e, info=info) for e in events
             if e["type"] == ev["type"] and e["event_date"] < ev["event_date"]]
    menu = load_menu() if MENU_PATH.exists() else {"items": [{}]}
    r = retrieve(tgt, cands, info, weighting=menu["items"][0])
    print(json.dumps({"target": {k: v for k, v in tgt.items() if k != "fields"},
                      "known_fields": {f: v for f, v in tgt["fields"].items() if not is_unknown(v)},
                      "retrieval": {k: v for k, v in r.items() if k != "ranked"}}, indent=1, default=str)[:4000])
