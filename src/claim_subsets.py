"""
claim_subsets.py -- R4: the claim-matched corpus (red-team attacks 3, 4, 5).

Attacks 3-5 say the H1 "geopolitical shocks ripple into oil" claim is tested on a
set that is mostly OPEC meetings and macro crises, and that several big high-VIX
episodes are ENDOGENOUS -- OPEC/policy reactions to a price move already underway
(the 2008/2020 emergency cuts, coordinated reserve releases), so their +20d CAR is
the pre-existing move continuing, not the event's ripple.

This lens does two things:

(i) FLAG endogenous_response with a DOCUMENTED, POINT-IN-TIME rule (no lookahead),
    so the flag list is reproducible, not opinion -- then hand it to Joe to review:
      endogenous_response = True  iff  type in {opec_decision, policy_response}
      AND the trailing 20-trading-day Brent return BEFORE t-1 exceeded +/-15%
      (the policy was reacting to a sharp move already in progress).
    The threshold and the trailing window are the criteria; Joe adjusts the list.

(ii) Re-run H1 (SAR headline + raw secondary) on three corpora:
      full  |  ex-endogenous  |  geopolitical-only
      (geopolitical = conflict_escalation U chokepoint_disruption U
       infrastructure_attack U sanctions).

Writes data/h1_subsets.json (the numbers) and data/endogenous_flags.json (the flag
list FOR JOE'S REVIEW). Additive; frozen record untouched. The public claim is
re-worded to whatever the subset supports ONLY after Joe signs off the flag list.

Run:  python3 src/claim_subsets.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns
import research
import sar_lens

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
HORIZON = 20

ENDO_TYPES = {"opec_decision", "policy_response"}
TRAILING_DAYS = 20
TRAILING_THRESH = 0.15            # |trailing 20d Brent return| > 15% -> reacting to a move in progress
GEO_TYPES = {"conflict_escalation", "chokepoint_disruption", "infrastructure_attack", "sanctions"}


def _trailing_return(ret, event_date, ndays=TRAILING_DAYS):
    """Cumulative Brent return over the ndays trading days ending at t-1 (point-in-time, no lookahead)."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(event_date))
    if pos - ndays - 1 < 0 or pos >= len(dates):
        return None
    window = ret.iloc[pos - ndays - 1: pos - 1]      # up to and including t-1
    return float(window.sum())


def _flag_endogenous(conn, events):
    """Return (flag_dict event_id->bool, detail list) using the documented point-in-time rule."""
    ret = asset_returns(conn, sar_lens.ASSET_SERIES, "price")
    flags, detail = {}, []
    for _, ev in events.iterrows():
        tr = _trailing_return(ret, ev["event_date"])
        is_endo = bool(ev["type"] in ENDO_TYPES and tr is not None and abs(tr) > TRAILING_THRESH)
        flags[ev["event_id"]] = is_endo
        if is_endo:
            detail.append({"event_id": ev["event_id"], "date": ev["event_date"], "type": ev["type"],
                           "title": ev.get("title", ""), "trailing_20d_return_pct": round(tr * 100, 1),
                           "reason": f"{ev['type']} following a {tr*100:+.1f}% 20d Brent move -> reacting "
                                     f"to a price move already in progress"})
    detail.sort(key=lambda d: d["date"])
    return flags, detail


def _gate_subset(conn, events):
    raw = sar_lens._mags(conn, events, HORIZON, standardized=False)
    sar = sar_lens._mags(conn, events, HORIZON, standardized=True)
    m_sar, s_sar = sar_lens._episodes(conn, events, sar)
    m_raw, s_raw = sar_lens._episodes(conn, events, raw)
    if m_sar is None:
        return {"ok": False, "reason": "too few episodes", "n_events": int(len(events))}
    return {"ok": True, "n_events": int(len(events)),
            "sar": sar_lens._gate(m_sar, s_sar), "raw": sar_lens._gate(m_raw, s_raw)}


def run():
    conn = sqlite3.connect(DB)
    events = research._events(conn)
    flags, detail = _flag_endogenous(conn, events)

    ev_full = events
    ev_exendo = events[~events["event_id"].map(flags).fillna(False)]
    ev_geo = events[events["type"].isin(GEO_TYPES)]

    subsets = {
        "full": _gate_subset(conn, ev_full),
        "ex_endogenous": _gate_subset(conn, ev_exendo),
        "geopolitical_only": _gate_subset(conn, ev_geo),
    }
    conn.close()

    # flag list FOR JOE
    flag_doc = {
        "lens": "R4_endogenous_flags",
        "attack": 4,
        "status": "AWAITING JOE'S REVIEW -- sign-off gate per RED_TEAM_1_RESPONSE.md R4(i)",
        "criterion": {
            "rule": "endogenous_response = True iff type in {opec_decision, policy_response} AND "
                    "|trailing 20-trading-day Brent return ending at t-1| > 15%",
            "rationale": "flags policy/OPEC decisions made in reaction to a sharp price move already "
                         "underway, whose +20d CAR reflects the ongoing move, not the event's ripple.",
            "point_in_time": True, "trailing_days": TRAILING_DAYS, "threshold_pct": TRAILING_THRESH * 100,
        },
        "n_flagged": len(detail),
        "flagged": detail,
    }
    (ROOT / "data" / "endogenous_flags.json").write_text(json.dumps(flag_doc, indent=2))

    def line(g):
        if not g.get("ok"):
            return {"ok": False, "reason": g.get("reason"), "n_events": g.get("n_events")}
        return {"n_events": g["n_events"],
                "sar": {k: g["sar"][k] for k in ("amp", "ci95", "perm_p", "ci_excludes_zero", "n_episodes")},
                "raw": {k: g["raw"][k] for k in ("amp", "ci95", "perm_p", "ci_excludes_zero", "n_episodes")}}

    out = {
        "lens": "R4_claim_subsets",
        "attacks": [3, 4, 5],
        "headline_metric": "SAR (|SCAR+20| high-minus-low)",
        "endogenous_rule": flag_doc["criterion"]["rule"],
        "n_flagged_endogenous": len(detail),
        "flag_list_status": "AWAITING JOE'S REVIEW (data/endogenous_flags.json)",
        "geopolitical_types": sorted(GEO_TYPES),
        "subsets": {k: line(v) for k, v in subsets.items()},
        "note": "ex_endogenous uses the PROVISIONAL flag list; numbers may shift after Joe edits it. "
                "Public claim re-wording is deferred to Joe's sign-off.",
    }
    (ROOT / "data" / "h1_subsets.json").write_text(json.dumps(out, indent=2))
    return out, flag_doc


if __name__ == "__main__":
    o, f = run()
    print(json.dumps(o, indent=2))
    print("\n---- ENDOGENOUS FLAG LIST (for Joe) ----")
    print(json.dumps(f["flagged"], indent=2))
