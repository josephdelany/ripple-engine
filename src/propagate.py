"""
propagate.py -- B3: Layer P, the FLOW read and the realized-disruption fraction (spec §4.3; A4).

Walk the oil value chain and report, at each hop, the MEASURED market reaction of the events in
a class -- PRICE side (signed CAR: avg, n, range) beside a FLOW read -- plus the
realized-disruption fraction: the share of contributing events whose Brent move was a large,
sustained, one-directional supply signal (a real disruption) versus the majority that were a
two-sided risk premium. This is the "conflict doesn't stop trade" headline, reported as a
fraction with n, never a slogan.

BRANCH-CONDITIONING REMOVED, 2026-09-03. This module used to take a Layer-G branch
(CONTAINED / LIMITED_RETALIATION / WIDENING / RESOLUTION_BY_DEAL) and filter its contributing
events on `sr_outcome_90`. That label was retired at κ≈0 against ICB/MID/UCDP on 2026-09-02
(OUTCOME_MAPPING.md Amendment 1) -- it is corpus-derived, not an outcome -- and nothing may
condition on a retired label. The parameter is gone rather than defaulted, so a caller that
still asks for a branch fails loudly instead of quietly getting unfiltered numbers.

The Story page's "where does it travel" band no longer comes from here at all: it reads the
registered local projections in data/ripple/irf.json (DESIGN.md Amendment 1, story_read.travel).
What remains of this module is the CAR-based hop read and the live-transit flow side.

Reuses the measured `edges` (event x asset CAR) and live transits; recomputes nothing.
"""
from __future__ import annotations

import statistics as st

from _db import connect

GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
# the value chain as ordered hops: (tier, series_id, label)
CHAIN = [
    ("crude", "fred.DCOILBRENTEU", "Brent crude"),
    ("crude", "fred.DCOILWTICO", "WTI crude"),
    ("refined", "fred.DHOILNYH", "Heating oil / diesel"),
    ("refined", "fred.DGASUSGULF", "Gulf gasoline"),
    ("margin", "derived.gasoline_crack", "Gasoline crack"),
    ("margin", "derived.diesel_crack", "Diesel crack"),
    ("gas_lng", "fred.DHHNGSP", "Henry Hub gas"),
    ("gas_lng", "yf.ttf", "TTF gas (EU)"),
    ("gas_lng", "yf.jkm", "JKM LNG (Asia)"),
    ("ngl", "fred.DPROPANEMBTX", "Propane"),
    ("fertilizer", "fred.PCU325311325311", "Nitrogen fertilizer PPI"),
    ("cross", "yf.sp500", "S&P 500"),
    ("cross", "fred.BAMLH0A0HYM2", "US HY credit"),
]
DISRUPTION_MIN = 10.0    # |CAR20| >= this AND signed-consistent => a real, sustained supply move


def _contributing(conn, event_type=None):
    q = f"SELECT event_id FROM events WHERE type IN ({','.join('?'*len(GEO_TYPES))})"
    args = list(GEO_TYPES)
    if event_type:
        q += " AND type=?"; args.append(event_type)
    return [r[0] for r in conn.execute(q, args)]


def _hop(conn, series_id, event_ids):
    if not event_ids:
        return None
    ph = ",".join("?" * len(event_ids))
    rows = conn.execute(
        f"SELECT car20 FROM edges WHERE target_series=? AND units='%' AND car20 IS NOT NULL "
        f"AND event_id IN ({ph})", [series_id] + event_ids).fetchall()
    cars = [r[0] for r in rows]
    if not cars:
        return None
    n = len(cars)
    signed_med = round(st.median(cars), 2)
    disrupted = sum(1 for v in cars if abs(v) >= DISRUPTION_MIN)
    return {"n": n, "signed_median_pct": signed_med,
            "avg_pct": round(st.mean(cars), 2),
            "lo": round(min(cars), 1), "hi": round(max(cars), 1),
            "no_lasting_move_pct": round(100 * sum(1 for v in cars if abs(v) < 5) / n),
            "material_move_pct": round(100 * disrupted / n)}


def _live_flow(conn):
    out = {}
    for cp in ("hormuz", "bab_el_mandeb", "suez", "cape_of_good_hope"):
        vals = [r[0] for r in conn.execute(
            "SELECT value FROM observations WHERE series_id=? ORDER BY obs_date",
            (f"portwatch.{cp}.n_tanker",))]
        if len(vals) >= 14:
            base = st.mean(vals); rec = st.mean(vals[-7:])
            out[cp] = round((rec / base - 1) * 100) if base else None
    return out


def propagate(conn, event_type=None):
    ids = _contributing(conn, event_type=event_type)
    hops = []
    for tier, sid, label in CHAIN:
        h = _hop(conn, sid, ids)
        if h:
            hops.append({"tier": tier, "series_id": sid, "label": label, **h})
    # realized-disruption fraction on the crude node (the headline)
    crude = next((h for h in hops if h["series_id"] == "fred.DCOILBRENTEU"), None)
    disruption_fraction = (crude["material_move_pct"] if crude else None)
    return {
        "event_type": event_type or "ALL",
        "contributing_n": len(ids),
        "hops": hops,
        "realized_disruption_fraction_pct": disruption_fraction,
        "flow_now": _live_flow(conn),
        "reading": (f"Of the {crude['n']} events on record in "
                    f"{event_type or 'this class'}, {crude['material_move_pct']}% produced a "
                    f"large sustained Brent move (>= {DISRUPTION_MIN:.0f}%); the majority "
                    f"({crude['no_lasting_move_pct']}% within +/-5%) did not — the flow held and "
                    f"the market carried a risk premium, not a realized cut.") if crude else
                   "insufficient measured edges for this branch/type.",
        "caveat": "PRICE side is measured from edges (1987+); FLOW history begins 2026 "
                  "(live transits shown), so per-branch historical flow is a stated gap.",
    }


if __name__ == "__main__":
    import json
    c = connect(read_only=True)
    for t in (None, "infrastructure_attack", "chokepoint_disruption"):
        p = propagate(c, event_type=t)
        print(f"\n=== class={p['event_type']} n={p['contributing_n']} disruption={p['realized_disruption_fraction_pct']}% ===")
        for h in p["hops"][:6]:
            print(f"  {h['label']:<22} signed_med {h['signed_median_pct']:>6}%  n={h['n']:<3} material {h['material_move_pct']}% no-lasting {h['no_lasting_move_pct']}%")
