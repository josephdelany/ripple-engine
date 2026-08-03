"""
influence.py -- leave-one-event-out influence diagnostics (VISION_ROADMAP V-Q3).

The attack: "your +5pp is one dramatic event (say 2020) doing all the work." The defence (leave-one-out
/ Cook's distance): recompute the headline with EACH single event removed, one at a time, and report the
largest swing. If no single event moves it much, the finding rests on the pattern, not on one episode.
If one event IS decisive, that gets said out loud -- honestly.

Headline under test: H1 = VIX-stress amplification of the |CAR+20| Brent ripple, at the EXACT registered
spec (est 130 / +20 / cluster 35 / median split / raw pp). The per-spec amplification and its faithful
reproduction of the +5.0pp headline are reused from spec_curve.py (no re-implementation), so this is the
same number the evidence pack reports. Leave-one-out is done on RAW events (then re-clustered), so
removing the first event of a cluster genuinely changes that cluster's representative.

Writes data/influence.json. numpy/pandas; free/local; point-in-time (state at t-1, via spec_curve).

Run:  python3 src/influence.py
"""

import json
import sqlite3
from pathlib import Path

import pandas as pd

from spec_curve import brent_returns, one_spec, REGISTERED
from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "influence.json"
BRENT = "fred.DCOILBRENTEU"
# Materiality: a single event is "decisive" if removing it drops the amplification below this floor
# or flips its sign. 1.0pp is a fifth of the headline -- a conservative bar to shout at.
DECISIVE_FLOOR_PP = 1.0


def _amp(ret, events, vixs):
    s = one_spec(ret, events, vixs, REGISTERED["est_len"], REGISTERED["post"],
                 REGISTERED["cluster"], REGISTERED["split"], REGISTERED["scale"])
    return s if s else None


def run():
    conn = sqlite3.connect(DB)
    ret = brent_returns(conn)
    vixs = build_signals(load_wide(conn))["derived.vix_pct"].dropna()
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    conn.close()

    base = _amp(ret, events, vixs)
    if base is None:
        return {"error": "baseline amplification could not be computed"}
    base_amp = base["amp"]

    loo = []
    for eid in events["event_id"]:
        sub = events[events["event_id"] != eid]
        s = _amp(ret, sub, vixs)
        if s is None:
            continue
        loo.append({"event_id": eid, "amp_without": s["amp"],
                    "delta": round(s["amp"] - base_amp, 4)})

    # Sort by how much REMOVING the event lowers the amplification (most load-bearing first)
    loo.sort(key=lambda r: r["delta"])
    amps_without = [r["amp_without"] for r in loo]
    max_abs = max((abs(r["delta"]) for r in loo), default=0.0)
    most = min(loo, key=lambda r: r["delta"]) if loo else None       # largest DROP when removed (load-bearing)
    raises = max(loo, key=lambda r: r["delta"]) if loo else None     # largest RISE when removed (dampening)
    min_amp = min(amps_without) if amps_without else base_amp
    ever_flips = any(a <= 0 for a in amps_without)
    ever_below_floor = min_amp < DECISIVE_FLOOR_PP
    decisive = ever_flips or ever_below_floor

    return {
        "headline": "H1 VIX-stress amplification of |CAR+20| Brent, registered spec (130/+20/35/median/raw)",
        "baseline_amp_pp": base_amp, "baseline_n": base["n"],
        "n_events_tested": len(loo),
        "max_single_event_influence_pp": round(max_abs, 3),
        "most_load_bearing": most,               # removing it lowers the amplification most
        "most_dampening": raises,                # removing it raises the amplification most
        "min_amp_when_any_one_removed_pp": round(min_amp, 3),
        "sign_ever_flips": bool(ever_flips),
        "decisive_floor_pp": DECISIVE_FLOOR_PP,
        "any_single_event_decisive": bool(decisive),
        "top5_load_bearing": loo[:5],
        "verdict": (
            f"No single event is decisive: removing any one leaves the amplification at "
            f">= {round(min_amp,2)}pp (never below {DECISIVE_FLOOR_PP}pp, never flips sign); the largest "
            f"single-event swing is {round(max_abs,2)}pp."
            if not decisive else
            f"LOUD FLAG: a single event IS decisive -- removing '{most['event_id'] if most else '?'}' moves "
            f"the amplification to {round(min_amp,2)}pp (flips={ever_flips}). The headline leans on one episode."
        ),
    }


def main():
    r = run()
    JSON.write_text(json.dumps(r, indent=2))
    if "error" in r:
        print("influence: " + r["error"]); return
    print("=" * 84)
    print("H1 INFLUENCE -- leave-one-event-out: does one episode carry the +5pp?")
    print("=" * 84)
    print(f"  baseline amplification: {r['baseline_amp_pp']:+.2f}pp (n_clusters={r['baseline_n']}), "
          f"{r['n_events_tested']} events tested")
    print(f"  max single-event influence: {r['max_single_event_influence_pp']:.2f}pp")
    print(f"  min amplification when ANY one event removed: {r['min_amp_when_any_one_removed_pp']:+.2f}pp "
          f"(sign flips: {r['sign_ever_flips']})")
    print("  most load-bearing events (largest drop when removed):")
    for e in r["top5_load_bearing"]:
        print(f"    {e['event_id']:<44} delta {e['delta']:+.2f}pp -> {e['amp_without']:+.2f}pp")
    if r.get("most_dampening"):
        d = r["most_dampening"]
        print(f"  (for symmetry, removing '{d['event_id']}' RAISES it most: "
              f"{d['delta']:+.2f}pp -> {d['amp_without']:+.2f}pp)")
    print(f"\n  VERDICT: {r['verdict']}")
    print(f"  Wrote {JSON}")


if __name__ == "__main__":
    main()
