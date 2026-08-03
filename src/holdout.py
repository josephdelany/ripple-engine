"""
holdout.py -- formal temporal hold-out of the H1 conditioning rule (VISION_ROADMAP V-Q4).

Out-of-sample discipline (Tetlock; ML validation): a rule fitted on the past must be tested on data it
never saw. H1's conditioning rule is a SPLIT THRESHOLD -- "VIX stress above its median amplifies the
ripple." The honest test: LEARN that threshold on pre-2019 events ONLY, FREEZE it, then apply it to
2019+ events and see whether the amplification still shows up out-of-sample. No peeking at the
post-2019 VIX distribution when setting the split.

Reuses spec_curve.py's registered-spec CAR (est 130 / +20 / cluster 35 / raw pp) so the numbers tie to
the +5.0pp headline. Point-in-time: VIX state at t-1. Writes data/holdout.json.

Run:  python3 src/holdout.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from spec_curve import brent_returns, event_mag, cluster_ids, REGISTERED
from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "holdout.json"
SPLIT_DATE = pd.Timestamp("2019-01-01")


def _rows(ret, events, vixs):
    """(date, |CAR20| pp, vix_state@t-1) per event at the registered spec."""
    out = []
    for _, ev in events.iterrows():
        mag = event_mag(ret, ev["event_date"], REGISTERED["est_len"], REGISTERED["post"], "raw")
        if mag is None:
            continue
        state = vixs.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))
        if pd.isna(state):
            continue
        out.append((pd.Timestamp(ev["event_date"]), mag, float(state)))
    return sorted(out, key=lambda r: r[0])


def _clustered(rows):
    """De-overlap a list of (date,mag,state) rows at the registered cluster threshold."""
    if not rows:
        return pd.DataFrame(columns=["date", "mag", "state", "cluster"])
    df = pd.DataFrame(rows, columns=["date", "mag", "state"])
    df["cluster"] = cluster_ids(list(df["date"]), REGISTERED["cluster"])
    return df.groupby("cluster").first().reset_index(drop=True)


def _amp(df, thr):
    """High-minus-low mean |CAR| using a FIXED threshold thr on the state."""
    hi, lo = df[df["state"] > thr]["mag"], df[df["state"] <= thr]["mag"]
    if len(hi) == 0 or len(lo) == 0:
        return None
    return float(hi.mean() - lo.mean())


def run():
    conn = sqlite3.connect(DB)
    ret = brent_returns(conn)
    vixs = build_signals(load_wide(conn))["derived.vix_pct"].dropna()
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    conn.close()

    rows = _rows(ret, events, vixs)
    train = _clustered([r for r in rows if r[0] < SPLIT_DATE])
    test = _clustered([r for r in rows if r[0] >= SPLIT_DATE])
    full = _clustered(rows)

    # Learn the split threshold on TRAIN only, then FREEZE it.
    train_thr = float(np.median(train["state"])) if len(train) else None
    amp_in = _amp(train, train_thr) if train_thr is not None else None
    amp_oos = _amp(test, train_thr) if train_thr is not None else None      # frozen threshold applied to 2019+
    amp_full = _amp(full, float(np.median(full["state"]))) if len(full) else None

    holds_oos = amp_oos is not None and amp_oos > 0
    return {
        "what": "H1 conditioning rule (VIX-median split) fit on pre-2019, frozen, evaluated on 2019+",
        "spec": "registered (est 130 / +20 / cluster 35 / raw pp)", "split_date": "2019-01-01",
        "frozen_vix_threshold_pct": round(train_thr, 2) if train_thr is not None else None,
        "in_sample_pre2019": {"n_clusters": int(len(train)), "amp_pp": round(amp_in, 3) if amp_in is not None else None},
        "out_of_sample_2019plus": {"n_clusters": int(len(test)), "amp_pp": round(amp_oos, 3) if amp_oos is not None else None},
        "full_sample_reference": {"n_clusters": int(len(full)), "amp_pp": round(amp_full, 3) if amp_full is not None else None},
        "holds_out_of_sample": bool(holds_oos),
        "verdict": (
            f"The pre-2019-fitted rule STILL amplifies out-of-sample: frozen VIX threshold "
            f"{round(train_thr,1)}pct gives +{round(amp_oos,2)}pp on 2019+ events (in-sample "
            f"+{round(amp_in,2)}pp). The conditioning rule is not overfit to its training era."
            if holds_oos else
            f"Out-of-sample the amplification is {round(amp_oos,2) if amp_oos is not None else None}pp -- "
            f"the pre-2019 rule does NOT clearly hold on 2019+. Reported honestly."),
    }


def main():
    r = run()
    JSON.write_text(json.dumps(r, indent=2))
    print("=" * 84)
    print("H1 TEMPORAL HOLD-OUT -- fit the VIX split on pre-2019, freeze, test on 2019+")
    print("=" * 84)
    print(f"  frozen VIX threshold (pre-2019 median): {r['frozen_vix_threshold_pct']} pct")
    ins, oos, full = r["in_sample_pre2019"], r["out_of_sample_2019plus"], r["full_sample_reference"]
    print(f"  in-sample  (pre-2019): {ins['amp_pp']:+.2f}pp  (n_clusters={ins['n_clusters']})")
    print(f"  OUT-OF-SAMPLE (2019+): {oos['amp_pp']:+.2f}pp  (n_clusters={oos['n_clusters']})  <- frozen threshold")
    print(f"  full-sample reference: {full['amp_pp']:+.2f}pp  (n_clusters={full['n_clusters']})")
    print(f"\n  VERDICT: {r['verdict']}")
    print(f"  Wrote {JSON}")


if __name__ == "__main__":
    main()
