"""
research.py -- THE RESEARCH BENCH (interrogate the engine; it never writes your analysis).

You bring the question; the engine returns a deterministic, receipted answer -- a number, a CI, a
verdict, the sources -- and NOTHING ELSE. No prose, no opinion. You do the analysis and the writing.
This is the pull interface a solo analyst uses to falsify their own macro hypotheses with the rigor
that normally needs a quant team. Four modes:

  test   -- declare a hypothesis (does STATE amplify the ripple in ASSET?) -> the full gate
            (clustered median split + cluster-bootstrap CI + permutation p) -> HOLDS / no-effect.
  query  -- how has ASSET moved after shocks of a TYPE (optionally split by a STATE)? base rates,
            CIs, n, and the sourced events behind them.
  gaps   -- where does the engine's view diverge from what the market has priced right now?
  vars   -- what can I test? the available state variables, assets, and event types.

Add your OWN data (events / variables / assets) and test it immediately -- see RESEARCH_BENCH.md.

Examples:
  python3 src/research.py test  --state derived.vix_pct --asset fred.DCOILBRENTEU --sign high
  python3 src/research.py query --type conflict_escalation --horizon 20 --state derived.vix_pct --sign high
  python3 src/research.py gaps
  python3 src/research.py vars
"""

import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns, ASSETS
from event_study import car_for_event, PRE, HORIZONS
from derive_signals import load_wide, build_signals
from robustness import assign_clusters
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ASSET_BY_SERIES = {a["series"]: a for a in ASSETS}


def _events(conn):
    return pd.read_sql("SELECT event_id, event_date, type, title, source_url FROM events "
                       "ORDER BY event_date", conn)


def _state_series(conn, state_sid):
    sig = build_signals(load_wide(conn))
    return sig[state_sid].dropna() if state_sid in sig else pd.Series(dtype=float)


def _asset(series):
    a = ASSET_BY_SERIES.get(series)
    if a:
        return a
    return {"series": series, "label": series, "kind": "price", "unit": "%"}   # assume price


def _car_mags(conn, asset, events, horizon):
    """Per-event |CAR+horizon| in the asset's unit (% for price, bps for yield)."""
    ret = asset_returns(conn, asset["series"], asset["kind"])
    if ret is None:
        return {}
    out = {}
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None or PRE + horizon >= len(car):
            continue
        m = abs(float(car[PRE + horizon]))
        out[ev["event_id"]] = m * 100 if asset["kind"] in ("price", "weekly") else m
    return out


# --------------------------------------------------------------------------- test
def run_test(conn, state_sid, asset_series, sign_str, horizon):
    """The hypothesis gate for ANY state x asset -> a receipted result dict (no I/O). Reusable +
    testable. sign_str 'high'/'low' = which side of the state is predicted to amplify."""
    events = _events(conn)
    asset = _asset(asset_series)
    state = _state_series(conn, state_sid)
    if state.empty:
        return {"ok": False, "reason": f"no such state variable '{state_sid}'"}
    mags = _car_mags(conn, asset, events, horizon)
    sign = +1 if sign_str == "high" else -1
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] not in mags:
            continue
        v = state.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))   # t-1, no lookahead
        if pd.notna(v):
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                         "mag": mags[ev["event_id"]], "state": float(v)})
    if len(rows) < 12:
        return {"ok": False, "reason": f"only {len(rows)} usable events -- too few to test"}
    df = assign_clusters(pd.DataFrame(rows))
    clustered = df.groupby("cluster").first().reset_index()
    m = clustered["mag"].to_numpy(float); s = clustered["state"].to_numpy(float)
    boot = validate.cluster_bootstrap_amp(m, s, sign=sign)
    perm = validate.permutation_p(m, s, sign=sign)
    excl0 = bool(boot["lo"] is not None and (boot["lo"] > 0 or boot["hi"] < 0))
    holds = bool(excl0 and boot["obs"] and boot["obs"] > 0 and perm["p"] is not None and perm["p"] < 0.10)
    return {"ok": True, "asset": asset, "state": state_sid, "sign": sign_str, "horizon": horizon,
            "n": boot["n"], "amp": boot["obs"], "ci": [boot["lo"], boot["hi"]],
            "ci_excludes_zero": excl0, "perm_p": perm["p"],
            "boot_share": boot["share_positive"], "holds": holds}


def cmd_test(args):
    conn = sqlite3.connect(DB)
    r = run_test(conn, args.state, args.asset, args.sign, args.horizon)
    conn.close()
    if not r["ok"]:
        print(f"  {r['reason']}. Try:  python3 src/research.py vars"); return
    a = r["asset"]
    print("=" * 76)
    print(f"HYPOTHESIS TEST -- does {args.state} ({args.sign}) amplify |CAR+{args.horizon}| in {a['label']}?")
    print("=" * 76)
    print(f"  n episodes (clustered): {r['n']}   unit: {a['unit']}")
    print(f"  amplification (predicted-direction high-vs-low): {r['amp']:+} {a['unit']}")
    print(f"  95% bootstrap CI: [{r['ci'][0]:+}, {r['ci'][1]:+}]   (excludes zero: {r['ci_excludes_zero']})")
    print(f"  permutation p: {r['perm_p']}   bootstrap P(predicted direction): {r['boot_share']}")
    print(f"  VERDICT: {'HOLDS -- amplification is real at this N (CI excludes 0, perm p<0.10)' if r['holds'] else 'NO SIGNIFICANT EFFECT -- CI spans zero / p>=0.10 (honest null)'}")
    print("  (single-hypothesis test; correct for multiple testing if you scan many -- see validate.bh_fdr)")


# --------------------------------------------------------------------------- query
def cmd_query(args):
    conn = sqlite3.connect(DB)
    events = _events(conn)
    asset = _asset(args.asset)
    sub = events[events["type"] == args.type] if args.type else events
    if not len(sub):
        print(f"  no events of type '{args.type}'. Try:  python3 src/research.py vars"); return
    # signed CAR at the horizon (direction), per event
    ret = asset_returns(conn, asset["series"], asset["kind"])
    recs = []
    for _, ev in sub.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None or PRE + args.horizon >= len(car):
            continue
        c = float(car[PRE + args.horizon]) * (100 if asset["kind"] in ("price", "weekly") else 1)
        rec = {"event_id": ev["event_id"], "date": ev["event_date"], "car": c,
               "title": ev["title"], "url": ev["source_url"]}
        if args.state:
            st = _state_series(conn, args.state)
            v = st.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)) if len(st) else np.nan
            rec["state"] = float(v) if pd.notna(v) else None
        recs.append(rec)
    if not recs:
        print("  no measurable events for that asset/horizon."); return

    cars = [r["car"] for r in recs]
    ci = validate.bootstrap_ci(cars, stat="mean")
    print("=" * 76)
    print(f"QUERY -- {asset['label']} CAR+{args.horizon} after '{args.type or 'ALL'}' shocks")
    print("=" * 76)
    print(f"  n={len(recs)}   mean CAR {ci['stat']:+} {asset['unit']}   95% CI [{ci['lo']:+}, {ci['hi']:+}]")
    if args.state:
        have = [r for r in recs if r.get("state") is not None]
        if len(have) >= 4:
            med = float(np.median([r["state"] for r in have]))
            hi = [r["car"] for r in have if r["state"] >= med]; lo = [r["car"] for r in have if r["state"] < med]
            print(f"  split on {args.state} at median {med:.1f}:")
            print(f"    high (n={len(hi)}) mean {np.mean(hi):+.1f}   low (n={len(lo)}) mean {np.mean(lo):+.1f} {asset['unit']}")
    print("  sourced events (most recent):")
    for r in sorted(recs, key=lambda r: r["date"], reverse=True)[:6]:
        print(f"    {r['date']}  {r['car']:+6.1f}{asset['unit']:<3} {r['title'][:44]}  {r['url'][:40]}")
    conn.close()


# --------------------------------------------------------------------------- gaps
def cmd_gaps(_args):
    import gaps as G
    conn = sqlite3.connect(DB)
    rows = G.build(conn); conn.close()
    led = G.ledger(rows)
    live = [r for r in rows if r["gap_id"] == "gap.LIVE"]
    print("=" * 76)
    print("GAPS -- where the engine's view diverges from what the market has priced")
    print("=" * 76)
    if live:
        print(f"  LIVE: {live[0]['notes']}")
    if led.get("n_scored"):
        for d, g in (led.get("by_gap_direction") or {}).items():
            if g:
                ci = g["turbulence_rate_ci95"]
                print(f"    {d:<18} n={g['n']:<3} turbulence rate {g['turbulence_rate']} 95%CI [{ci[0]},{ci[1]}]")
    print("  (raw material for YOUR analysis -- small-N, suggestive; see data/gaps.json for receipts)")


# --------------------------------------------------------------------------- vars
def cmd_vars(_args):
    conn = sqlite3.connect(DB)
    sig = build_signals(load_wide(conn))
    states = sorted([c for c in sig.columns if str(c).startswith("derived.")])
    types = [r[0] for r in conn.execute("SELECT DISTINCT type FROM events ORDER BY type")]
    nev = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    conn.close()
    print("=" * 76)
    print(f"WHAT YOU CAN TEST  (corpus: {nev} events)")
    print("=" * 76)
    print("  STATE variables (--state):")
    for s in states:
        print(f"    {s}")
    print("  ASSETS (--asset):")
    for a in ASSETS:
        print(f"    {a['series']:<22} {a['label']} ({a['unit']})")
    print("  EVENT TYPES (--type):")
    for t in types:
        print(f"    {t}")
    print("  add your own events/variables/assets -> see RESEARCH_BENCH.md")


def main():
    ap = argparse.ArgumentParser(description="The research bench -- interrogate the engine.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("test"); t.add_argument("--state", required=True)
    t.add_argument("--asset", default="fred.DCOILBRENTEU"); t.add_argument("--sign", choices=["high", "low"], default="high")
    t.add_argument("--horizon", type=int, default=20, choices=HORIZONS); t.set_defaults(func=cmd_test)
    q = sub.add_parser("query"); q.add_argument("--type", default=None); q.add_argument("--asset", default="fred.DCOILBRENTEU")
    q.add_argument("--horizon", type=int, default=20, choices=HORIZONS); q.add_argument("--state", default=None)
    q.add_argument("--sign", choices=["high", "low"], default="high"); q.set_defaults(func=cmd_query)
    sub.add_parser("gaps").set_defaults(func=cmd_gaps)
    sub.add_parser("vars").set_defaults(func=cmd_vars)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
