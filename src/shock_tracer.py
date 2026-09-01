"""
shock_tracer.py -- walk a shock through the ripple graph (the Kharg -> product ->
downstream story), composing what the engine already measured. NO recompute, NO new
tables, NO fabrication: every arc is a stored measured reaction (edges.car20) or a
sourced structural fact (criticality.yaml / propagation_edges); every node carries its
live level from observations.

Given an anchor -- an entity (country/commodity/chokepoint), a product series, or a live
situation -- it returns a directed ripple:
  root entity
   - events_involving   : real corpus events where this entity was actor/target/location
   - measured_reactions : the products those events actually moved (avg 20d CAR, n, range,
                          live level) -- "attacks involving X historically moved these Y%"
   - physical_exposure  : (country) strategic commodities it is supply-critical for
                          (criticality.yaml, sourced share + stage) -- the physical channel
   - chokepoint_flow     : (chokepoint) its live tanker-transit series -- did flow actually move
   - transmission        : validated downstream arcs (propagation_edges, status='validated')
Honesty: a small mean with a wide range is flagged "priced as risk, not realized disruption"
(the measured 'conflicts rarely stop the flow' finding). Missing links are gaps, not guesses.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

import yaml
from fastapi.responses import JSONResponse

from _db import connect

ROOT = Path(__file__).resolve().parent.parent
CRIT = ROOT / "data" / "criticality.yaml"


def _latest(cur, series_id):
    r = cur.execute("SELECT obs_date, value FROM observations WHERE series_id=? "
                    "ORDER BY obs_date DESC LIMIT 1", (series_id,)).fetchone()
    return ({"obs_date": r[0], "value": r[1]} if r else None)


def _series_for_entity(cur, entity_id):
    r = cur.execute("SELECT series_id, name, unit FROM series WHERE entity_id=? LIMIT 1",
                    (entity_id,)).fetchone()
    return r


def _reaction_read(avg, lo, hi):
    spread = (hi - lo) if (hi is not None and lo is not None) else 0
    return ("priced as risk, not realized disruption"
            if abs(avg or 0) * 4 < (spread or 0) else "directional")


def _asof(cur, series_id, date):
    r = cur.execute("SELECT value FROM observations WHERE series_id=? AND obs_date<=? "
                    "ORDER BY obs_date DESC LIMIT 1", (series_id, date)).fetchone()
    return r[0] if r else None


def state_context(cur, events):
    """The 'then vs now' differencing, through the VALIDATED conditioner (H1: VIX stress
    amplifies the oil ripple; H2 inventories / H3 positioning are REJECTED, shown as context
    only). Point-in-time: VIX percentile as-of each past event date vs the current reading.
    This is why history rhymes rather than repeats — the SAME shock lands in a different
    world-state, so the measured reaction above must be read up or down accordingly."""
    import statistics
    bs = {r[0]: r[1] for r in cur.execute("SELECT variable_id, value FROM belief_state")}
    now_vix = bs.get("derived.vix_pct")
    thens = [v for v in (_asof(cur, "derived.vix_pct", e["date"]) for e in events) if v is not None]
    if not thens or now_vix is None:
        return {"available": False}
    past_median = round(statistics.median(thens), 1)
    share_on = round(100 * sum(1 for v in thens if v >= 50) / len(thens))
    now_on = now_vix >= 50
    if now_vix < past_median - 10:
        read = (f"Today's stress is LOWER than most of these analogs (VIX {now_vix:.0f}th pct "
                f"now vs ~{past_median:.0f}th typical then). Under the validated H1 edge, stress "
                f"amplifies the oil ripple — so today is a DAMPENING regime and the measured "
                f"reactions above likely OVERSTATE the move a similar shock would cause now.")
    elif now_vix > past_median + 10:
        read = (f"Today's stress is HIGHER than most of these analogs (VIX {now_vix:.0f}th pct "
                f"now vs ~{past_median:.0f}th typical then). Under H1, stress amplifies the oil "
                f"ripple — today is an AMPLIFYING regime, so a similar shock could move more "
                f"than the measured averages above.")
    else:
        read = (f"Today's stress (VIX {now_vix:.0f}th pct) is broadly in line with these analogs "
                f"(~{past_median:.0f}th typical). H1 conditioning is roughly neutral vs history.")
    return {
        "available": True,
        "conditioner": "H1 — VIX stress (validated; H2 inventories & H3 positioning rejected)",
        "now": {"vix_pct": now_vix, "inv_sigma": bs.get("derived.inv_sigma"),
                "cot_pct": bs.get("derived.cot_pct"), "regime": "stress-ON" if now_on else "stress-OFF"},
        "then": {"vix_pct_median": past_median, "pct_events_stress_on": share_on, "n": len(thens)},
        "read": read,
        "context_note": "inv_sigma (inventories) and cot_pct (positioning) shown as context; "
                        "both were tested as amplifiers and REJECTED — not used to condition the read.",
    }


def _crit_exposure(country_slug):
    """Strategic commodities this country is supply-critical for (sourced)."""
    try:
        data = yaml.safe_load(CRIT.read_text())
    except Exception:
        return []
    out = []
    for commodity, spec in (data.get("commodities") or {}).items():
        for field, stage_note in (("top", spec.get("stage")), ("mine_top", "mine"),
                                  ("refining_top", "refining")):
            tops = spec.get(field) or {}
            if country_slug in tops:
                out.append({"commodity": commodity, "stage": stage_note,
                            "share_pct": tops[country_slug],
                            "source": spec.get("source")})
                break
    return sorted(out, key=lambda d: -(d["share_pct"] or 0))


def _flow_vs_price(cur, dom_type):
    """Does trade actually stop, or does the market just price risk? Measured two ways:
    (1) PRICE PERSISTENCE (deep history) — a durable supply cut shows a consistent, persistent
    SIGNED CAR; a risk premium shows a signed median ~0 with large two-sided dispersion.
    (2) LIVE FLOW — recent AIS tanker transits vs their own baseline (2026-only, noisy; labelled).
    No fabrication: price from edges, transits from observations; the historical-flow gap
    (PortWatch starts 2026) is stated, not filled."""
    import statistics as st
    rows = cur.execute(
        """SELECT e.car5, e.car20 FROM edges e JOIN events ev ON ev.event_id=e.event_id
           WHERE ev.type=? AND e.target_series='fred.DCOILBRENTEU' AND e.units='%'
           AND e.car5 IS NOT NULL AND e.car20 IS NOT NULL""", (dom_type,)).fetchall()
    price = None
    if rows:
        c5 = [r[0] for r in rows]; c20 = [r[1] for r in rows]
        price = {
            "type": dom_type, "n": len(rows),
            "signed_median_car20": round(st.median(c20), 1),
            "median_abs_car5": round(st.median([abs(x) for x in c5]), 1),
            "median_abs_car20": round(st.median([abs(x) for x in c20]), 1),
            "share_small_pct": round(100 * sum(1 for v in c20 if abs(v) < 5) / len(c20)),
        }
    transits = []
    for cp in ("hormuz", "bab_el_mandeb", "suez", "cape_of_good_hope"):
        vals = [r[0] for r in cur.execute(
            "SELECT value FROM observations WHERE series_id=? ORDER BY obs_date",
            (f"portwatch.{cp}.n_tanker",))]
        if len(vals) >= 14:
            base = st.mean(vals); recent = st.mean(vals[-7:])
            transits.append({"chokepoint": cp, "recent7d": round(recent, 1),
                             "baseline": round(base, 1),
                             "pct_vs_norm": round((recent / base - 1) * 100) if base else None})
    read = None
    if price:
        durable = abs(price["signed_median_car20"]) >= 5
        read = (f"{dom_type.replace('_',' ')} events show a SIGNED median Brent move of "
                f"{price['signed_median_car20']:+.1f}% at 20 days on n={price['n']} — "
                + ("a persistent directional move (looks like a real, durable supply effect)."
                   if durable else
                   "≈0 despite a typical MAGNITUDE of "
                   f"{price['median_abs_car20']:.0f}%. That is the signature of a priced RISK "
                   "premium resolving in both directions, not a durable supply cut: if the flow "
                   "were truly and lastingly severed, the signed move would persist positive. "
                   "Live transits (right panel) say whether the physical flow is moving now."))
    return {"price_persistence": price, "live_transits": transits, "read": read,
            "caveat": "Price is deep history (edges); live transits are AIS-derived and begin "
                      "2026 (no historical flow around older events — a stated gap, not filled)."}


def list_anchors():
    """Traceable anchors: entities that appear in the corpus, grouped by type, with how
    many events involve them (so the picker leads with the ones that actually rippled)."""
    conn = connect(read_only=True)
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT en.entity_id, en.type, en.name, COUNT(DISTINCT ee.event_id) n
           FROM entities en JOIN event_entities ee ON ee.entity_id=en.entity_id
           GROUP BY en.entity_id HAVING n>0 ORDER BY en.type, n DESC""").fetchall()
    conn.close()
    groups = {}
    for r in rows:
        groups.setdefault(r[1], []).append({"entity_id": r[0], "name": r[2], "n_events": r[3]})
    order = ["country", "chokepoint", "commodity", "institution", "situation", "conflict"]
    return {"groups": [{"type": t, "items": groups[t]} for t in order if t in groups]}


def trace(entity=None, series=None, situation=None):
    conn = connect(read_only=True)
    cur = conn.cursor()

    # ---- resolve the anchor entity ----
    entity_id = entity
    if series and not entity_id:
        r = cur.execute("SELECT entity_id FROM series WHERE series_id=?", (series,)).fetchone()
        entity_id = r[0] if r else None
    if situation and not entity_id:
        r = cur.execute("SELECT actor_entity FROM situation_log WHERE situation_id=? "
                        "AND actor_entity IS NOT NULL ORDER BY ts DESC LIMIT 1",
                        (situation,)).fetchone()
        entity_id = r[0] if r else None
    if not entity_id:
        conn.close()
        return JSONResponse({"error": "could not resolve an anchor entity from "
                             "entity/series/situation"}, status_code=404)
    ent = cur.execute("SELECT entity_id, type, name FROM entities WHERE entity_id=?",
                      (entity_id,)).fetchone()
    ent = dict(zip(["entity_id", "type", "name"], ent)) if ent else \
        {"entity_id": entity_id, "type": "unknown", "name": entity_id}

    # ---- events where this entity was involved ----
    evrows = cur.execute(
        """SELECT ev.event_id, ev.event_date, ev.type, ev.title, ev.source_url, ee.role,
                  ev.severity, ev.surprise
           FROM event_entities ee JOIN events ev ON ev.event_id=ee.event_id
           WHERE ee.entity_id=? ORDER BY ev.event_date DESC""", (entity_id,)).fetchall()
    events = [dict(zip(["event_id", "date", "type", "title", "source_url", "role",
                        "severity", "surprise"], r)) for r in evrows]
    ev_ids = [e["event_id"] for e in events]

    # ---- measured reactions: what those events actually moved ----
    reactions = []
    if ev_ids:
        ph = ",".join("?" * len(ev_ids))
        q = f"""SELECT e.target_series, COUNT(*) n, ROUND(AVG(e.car20),2) avg20,
                       ROUND(MIN(e.car20),1) lo, ROUND(MAX(e.car20),1) hi
                FROM edges e WHERE e.event_id IN ({ph}) AND e.units='%'
                GROUP BY e.target_series ORDER BY ABS(AVG(e.car20)) DESC"""
        rrows = cur.execute(q, ev_ids).fetchall()   # materialize before inner lookups (single-cursor safety)
        for r in rrows:
            sname = cur.execute("SELECT name, entity_id FROM series WHERE series_id=?",
                                (r[0],)).fetchone()
            reactions.append({
                "series_id": r[0], "name": sname[0] if sname else r[0],
                "entity_id": sname[1] if sname else None,
                "n": r[1], "avg20": r[2], "lo": r[3], "hi": r[4],
                "read": _reaction_read(r[2], r[3], r[4]),
                "live": _latest(cur, r[0]),
            })

    # ---- physical exposure (country) ----
    exposure = []
    if ent["type"] == "country":
        exposure = _crit_exposure(entity_id.split(".")[-1])

    # ---- chokepoint flow (did trade actually move) ----
    chokepoint_flow = []
    if ent["type"] == "chokepoint":
        crows = cur.execute("SELECT series_id, name, unit FROM series WHERE entity_id=?",
                            (entity_id,)).fetchall()   # materialize before _latest (single-cursor safety)
        for r in crows:
            chokepoint_flow.append({"series_id": r[0], "name": r[1], "unit": r[2],
                                    "live": _latest(cur, r[0])})

    # ---- validated transmission arcs (how a shock propagates) ----
    transmission = [dict(zip(["from", "to", "lag", "strength", "mechanism"], r))
                    for r in cur.execute(
        """SELECT from_node, to_node, lag, strength, mechanism FROM propagation_edges
           WHERE status='validated' ORDER BY ABS(strength) DESC LIMIT 12""")]

    state_ctx = state_context(cur, events) if events else {"available": False}

    from collections import Counter
    dom_type = Counter(e["type"] for e in events).most_common(1)[0][0] if events else None
    flow = _flow_vs_price(cur, dom_type) if dom_type else None

    anchor_live = None
    s = _series_for_entity(cur, entity_id)
    if s:
        anchor_live = {"series_id": s[0], "name": s[1], "unit": s[2],
                       "live": _latest(cur, s[0])}
    conn.close()

    return {
        "anchor": ent, "anchor_live": anchor_live,
        "state_context": state_ctx,
        "flow_vs_price": flow,
        "n_events_involving": len(events),
        "events_involving": events[:20],
        "measured_reactions": reactions,
        "physical_exposure": exposure,
        "chokepoint_flow": chokepoint_flow,
        "transmission_validated": transmission,
        "note": "Every reaction is the measured 20-day cumulative move of that product to "
                "the real events this entity was involved in (n, range shown). A small mean "
                "with a wide range = the market priced risk; the flow usually did not stop. "
                "Physical exposure and transmission arcs are sourced structural facts, not "
                "forecasts. Missing links are documented gaps.",
    }
