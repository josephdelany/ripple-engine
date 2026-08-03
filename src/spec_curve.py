"""
spec_curve.py -- specification-curve analysis of H1 (VISION_ROADMAP V-Q2).

The attack a spec curve kills: "you tuned the pipeline to get +5pp." The defence (Simonsohn/Simmons/
Nelson): recompute the SAME finding across EVERY defensible analysis choice and publish the whole
distribution -- if the result only survives one lucky spec it dies; if it holds across the grid it is
robust. This is done EVEN THOUGH the spec was pre-registered, because "pre-registered" answers "did
you fish?" not "is it fragile?".

H1 = |CAR+20| in Brent is LARGER when VIX stress is high (clustered high-minus-low amplification).
We recompute that amplification across the grid of defensible specs:
  * estimation window   90 / 120 / 150 trading days   (gap t-11 fixed)
  * event window        +15 / +20 / +25 days
  * cluster threshold   25 / 35 / 45 days              (de-overlap window)
  * split               median   vs   tercile (top third - bottom third)
  * scale               raw |CAR| (pp)   vs   standardized |SCAR| (CAR / est-vol*sqrt(L))
= 108 specs. The registered spec (130/+20/35/median/raw) is computed exactly as the reference and
must reproduce the +5.0pp headline (a faithfulness check on this re-implementation).

Point-in-time throughout: VIX state read at t-1 (derived.vix_pct), same as the registered study.
Writes data/spec_curve.json + data/spec_curve.png. numpy/pandas/matplotlib; free/local.

Run:  python3 src/spec_curve.py
"""

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "spec_curve.json"
PNG = ROOT / "data" / "spec_curve.png"
BRENT = "fred.DCOILBRENTEU"
GAP = 11                    # t-11 gap before the estimation window (fixed, as in event_study.py)

# The defensible grid.
EST_LENS = [90, 120, 150]
POSTS = [15, 20, 25]
CLUSTERS = [25, 35, 45]
SPLITS = ["median", "tercile"]
SCALES = ["raw", "std"]
# The exact registered spec (event_study.py: EST_START=130, EST_END=11, PRE=5, POST=20; cluster 35).
REGISTERED = {"est_len": 119, "post": 20, "cluster": 35, "split": "median", "scale": "raw"}
PRE = 5


def brent_returns(conn):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? ORDER BY obs_date",
                     conn, params=[BRENT])
    s = pd.Series(df["value"].to_numpy(float), index=pd.to_datetime(df["obs_date"])).sort_index()
    return np.log(s).diff().dropna()


def event_mag(ret, event_date, est_len, post, scale):
    """|CAR+post| for one event, raw (pp) or standardized (SCAR). None if not enough data."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(event_date))
    est_start = est_len + GAP
    if pos >= len(dates) or pos - est_start < 0 or pos + post >= len(dates):
        return None
    est = ret.iloc[pos - est_start: pos - GAP]
    mu = est.mean()
    window = ret.iloc[pos - PRE: pos + post + 1]
    car_post = float((window - mu).cumsum().to_numpy()[PRE + post])   # CAR at +post
    if scale == "raw":
        return abs(car_post) * 100.0                                  # percentage points
    sigma = float(est.std())
    L = PRE + post + 1
    if sigma == 0:
        return None
    return abs(car_post / (sigma * np.sqrt(L)))                       # standardized |SCAR|


def cluster_ids(dates, cluster_days):
    """De-overlap: consecutive events within cluster_days share a cluster id (robustness.py logic)."""
    ids, last, cid = [], None, 0
    for d in dates:
        if last is not None and (d - last).days <= cluster_days:
            ids.append(cid)
        else:
            cid += 1; ids.append(cid)
        last = d
    return ids


def amplification(mags, states, split):
    """High-minus-low mean |CAR|, split on states. Returns (amp, n) or (None, n)."""
    mags, states = np.asarray(mags, float), np.asarray(states, float)
    if split == "median":
        med = np.median(states)
        hi, lo = mags[states > med], mags[states <= med]
    else:                                              # tercile: top third minus bottom third
        t1, t2 = np.percentile(states, [33.333, 66.667])
        hi, lo = mags[states >= t2], mags[states <= t1]
    if len(hi) == 0 or len(lo) == 0:
        return None, len(mags)
    return float(hi.mean() - lo.mean()), len(mags)


def one_spec(ret, events, vixs, est_len, post, cluster, split, scale):
    rows = []
    for _, ev in events.iterrows():
        mag = event_mag(ret, ev["event_date"], est_len, post, scale)
        if mag is None:
            continue
        state = vixs.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))   # t-1
        if pd.isna(state):
            continue
        rows.append((pd.Timestamp(ev["event_date"]), mag, float(state)))
    if len(rows) < 12:
        return None
    rows.sort(key=lambda r: r[0])
    cids = cluster_ids([r[0] for r in rows], cluster)
    df = pd.DataFrame(rows, columns=["date", "mag", "state"]); df["cluster"] = cids
    clustered = df.groupby("cluster").first()               # de-overlap: keep first per cluster
    amp, n = amplification(clustered["mag"].to_numpy(), clustered["state"].to_numpy(), split)
    if amp is None:
        return None
    return {"est_len": est_len, "post": post, "cluster": cluster, "split": split, "scale": scale,
            "amp": round(amp, 4), "n": int(n), "positive": bool(amp > 0)}


def run():
    conn = sqlite3.connect(DB)
    ret = brent_returns(conn)
    vixs = build_signals(load_wide(conn))["derived.vix_pct"].dropna()
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    conn.close()

    specs = []
    for est_len in EST_LENS:
        for post in POSTS:
            for cluster in CLUSTERS:
                for split in SPLITS:
                    for scale in SCALES:
                        s = one_spec(ret, events, vixs, est_len, post, cluster, split, scale)
                        if s:
                            specs.append(s)

    reg = one_spec(ret, events, vixs, REGISTERED["est_len"], REGISTERED["post"],
                   REGISTERED["cluster"], REGISTERED["split"], REGISTERED["scale"])

    raw_specs = [s for s in specs if s["scale"] == "raw"]        # pp-comparable subset for the headline
    amps_raw = np.array([s["amp"] for s in raw_specs])
    pos_all = np.mean([s["positive"] for s in specs]) if specs else float("nan")
    summary = {
        "n_specs": len(specs),
        "share_positive_all": round(float(pos_all), 3),
        "raw_pp": {
            "n": len(raw_specs),
            "median_amp_pp": round(float(np.median(amps_raw)), 3) if len(amps_raw) else None,
            "iqr_pp": [round(float(np.percentile(amps_raw, 25)), 3),
                       round(float(np.percentile(amps_raw, 75)), 3)] if len(amps_raw) else None,
            "min_pp": round(float(amps_raw.min()), 3) if len(amps_raw) else None,
            "max_pp": round(float(amps_raw.max()), 3) if len(amps_raw) else None,
            "share_positive": round(float(np.mean(amps_raw > 0)), 3) if len(amps_raw) else None,
        },
    }
    return {"registered": reg, "summary": summary, "specs": specs}


def _tradeable(reg_amp_pp, conn):
    """Tradeable-terms framing (standing rule): the amplification also in $/bbl, research-not-advice."""
    px = conn.execute("SELECT value FROM observations WHERE series_id=? ORDER BY obs_date DESC LIMIT 1",
                      (BRENT,)).fetchone()
    brent = float(px[0]) if px else None
    usd = round(reg_amp_pp / 100.0 * brent, 2) if brent else None
    return brent, usd


def figure(result):
    specs = sorted([s for s in result["specs"] if s["scale"] == "raw"], key=lambda s: s["amp"])
    if not specs:
        return
    amps = [s["amp"] for s in specs]
    colors = ["#1a7f37" if a > 0 else "#c0392b" for a in amps]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(range(len(amps)), amps, color=colors, width=1.0)
    ax.axhline(0, color="black", lw=0.8)
    reg = result["registered"]
    if reg:
        ax.axhline(reg["amp"], color="#2c3e50", ls="--", lw=1.2,
                   label=f"registered spec = {reg['amp']:.1f}pp (n={reg['n']})")
    med = result["summary"]["raw_pp"]["median_amp_pp"]
    ax.axhline(med, color="#e67e22", ls=":", lw=1.2, label=f"grid median = {med:.1f}pp")
    ax.set_title("H1 specification curve: VIX-stress amplification of the Brent ripple\n"
                 f"across {len(amps)} defensible raw-scale specs "
                 f"({result['summary']['raw_pp']['share_positive']*100:.0f}% positive)")
    ax.set_xlabel("specification (sorted by amplification)")
    ax.set_ylabel("|CAR+h| high-minus-low amplification (pp)")
    ax.legend(fontsize=9); ax.grid(alpha=0.3, axis="y")
    fig.savefig(PNG, dpi=130, bbox_inches="tight")
    plt.close(fig)


def main():
    result = run()
    JSON.write_text(json.dumps(result, indent=2))
    figure(result)
    reg, s = result["registered"], result["summary"]
    print("=" * 84)
    print("H1 SPECIFICATION CURVE -- is the +5pp amplification robust across defensible specs?")
    print("=" * 84)
    if reg:
        print(f"  registered spec (130/+20/35/median/raw): amp = {reg['amp']:+.2f}pp  (n={reg['n']})"
              f"   <- faithfulness check vs the +5.0pp headline")
    r = s["raw_pp"]
    print(f"  raw-scale grid (n={r['n']}): median {r['median_amp_pp']:+.2f}pp   "
          f"IQR [{r['iqr_pp'][0]:+.2f}, {r['iqr_pp'][1]:+.2f}]   "
          f"range [{r['min_pp']:+.2f}, {r['max_pp']:+.2f}]")
    print(f"  direction agreement: {r['share_positive']*100:.0f}% of raw specs positive; "
          f"{s['share_positive_all']*100:.0f}% of ALL {s['n_specs']} specs (incl. standardized) positive")
    conn = sqlite3.connect(DB)
    brent, usd = _tradeable(reg["amp"], conn) if reg else (None, None)
    conn.close()
    if usd is not None:
        print(f"\n  TRADEABLE TERMS (research, NOT advice): the registered {reg['amp']:.1f}pp amplification"
              f"\n  ~= ${usd}/bbl of extra 20-day abnormal move at Brent ${brent:.0f}. A directional 20-day"
              f"\n  oil position pays ~$0.03-0.05/bbl spread + carry; this is effect SIZE, not a signal.")
    print(f"\n  Published as computed. Wrote {JSON} and {PNG}")


if __name__ == "__main__":
    main()
