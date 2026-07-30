"""
cross_asset_conditioned.py -- does H1 generalize? The conditioned ripple MAP (Pillar 4).

H1 proved (for oil) that a geopolitical shock ripples harder when VIX stress is elevated. The
differentiator vs a per-asset risk score is a MAP: does that same stress-amplification mechanism
show up in gas, the dollar, and rates -- each validated through the SAME gate (clustered median
split + cluster-bootstrap CI + permutation p + BH-FDR across assets)? Where it validates, the map
grows; where it doesn't, that's an honest null cell. Reuses cross_asset.asset_returns + the event
study + robustness clustering + src/validate.py. numpy-only; point-in-time (state at t-1).

Run:  python3 src/cross_asset_conditioned.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns, ASSETS
from event_study import car_for_event, PRE
from derive_signals import load_wide, build_signals
from robustness import assign_clusters
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "cross_asset_conditioned.json"
VIX = "derived.vix_pct"
FDR_Q = 0.10


def _amp_for_asset(conn, asset, events, vixs, vix_median):
    """Clustered H1-style amplification of |CAR+20| for one daily asset, in its own unit
    (% for prices, bps for yields), with a cluster-bootstrap CI and a permutation p."""
    ret = asset_returns(conn, asset["series"], asset["kind"])
    if ret is None or len(ret) < 200:
        return None
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)   # t-1
        vix = vixs.asof(cutoff) if len(vixs) else np.nan
        if pd.isna(vix):
            continue
        mag = abs(float(car[PRE + 20]))           # |CAR+20| in the asset's natural unit
        mag = mag * 100 if asset["kind"] == "price" else mag   # prices -> %, yields already bps
        rows.append({"event_id": ev["event_id"], "date": ev["event_date"], "mag": mag, "vix": vix})
    if len(rows) < 12:
        return None
    df = assign_clusters(pd.DataFrame(rows))
    clustered = df.groupby("cluster").first().reset_index()
    mags = clustered["mag"].to_numpy(float)
    states = clustered["vix"].to_numpy(float)
    boot = validate.cluster_bootstrap_amp(mags, states, sign=+1)      # high VIX amplifies
    perm = validate.permutation_p(mags, states, sign=+1)
    return {"label": asset["label"], "unit": asset["unit"], "n_episodes": boot["n"],
            "amp": boot["obs"], "ci95": [boot["lo"], boot["hi"]],
            "ci_excludes_zero": (boot["lo"] is not None and (boot["lo"] > 0 or boot["hi"] < 0)),
            "perm_p": perm["p"]}


def run():
    conn = sqlite3.connect(DB)
    signals = build_signals(load_wide(conn))
    vixs = signals[VIX].dropna() if VIX in signals else pd.Series(dtype=float)
    vix_median = float(vixs.median()) if len(vixs) else 50.0
    events = pd.read_sql("SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)

    daily = [a for a in ASSETS if a["kind"] in ("price", "yield")]
    cells = [c for c in (_amp_for_asset(conn, a, events, vixs, vix_median) for a in daily) if c]
    conn.close()

    fdr = validate.bh_fdr([c["perm_p"] if c["perm_p"] is not None else 1.0 for c in cells], q=FDR_Q)
    for c, surv, q in zip(cells, fdr["survive"], fdr["qvalues"]):
        c["survives_fdr"] = bool(surv); c["fdr_q"] = q
        # generalizes = CI excludes zero (positive) AND survives multiple-asset FDR correction
        c["generalizes"] = bool(c["ci_excludes_zero"] and c["amp"] and c["amp"] > 0 and surv)

    gen = [c["label"] for c in cells if c["generalizes"]]
    report = {
        "what": "Does H1 (VIX stress amplifies the geopolitical ripple) generalize across assets? "
                "Same gate as oil: clustered median split + bootstrap CI + permutation + BH-FDR.",
        "sample": "clustered (de-overlapped), state at t-1", "n_assets": len(cells),
        "assets_generalizing": gen, "fdr_q": FDR_Q, "map": cells,
        "verdict": (f"The stress-amplification mechanism generalizes to: {', '.join(gen)}. "
                    "Other assets are honest null cells."
                    if gen else
                    "Beyond oil, the stress-amplification mechanism does not clear the gate at this N "
                    "on the other assets -- honest nulls. The oil (H1) edge stands on its own."),
    }
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    print("=" * 82)
    print("CONDITIONED RIPPLE MAP -- does H1 (stress amplifies) generalize across assets?")
    print("=" * 82)
    print(f"  {'asset':<12}{'n':>4}{'amp (|CAR20|)':>16}{'95% CI':>22}{'perm p':>9}{'FDR':>6}  verdict")
    for c in r["map"]:
        ci = c["ci95"]
        cis = f"[{ci[0]:+.1f},{ci[1]:+.1f}]" if ci[0] is not None else "n/a"
        verdict = "GENERALIZES" if c["generalizes"] else "null"
        print(f"  {c['label']:<12}{c['n_episodes']:>4}{c['amp']:>+13.1f} {c['unit']:<2}{cis:>22}"
              f"{str(c['perm_p']):>9}{('Y' if c['survives_fdr'] else 'n'):>6}  {verdict}")
    print(f"\n  {r['verdict']}")


if __name__ == "__main__":
    main()
