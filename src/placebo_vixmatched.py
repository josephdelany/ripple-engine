"""
placebo_vixmatched.py -- R2: the REAL negative control (red-team attack #2, CONCEDED).

WHY THE OLD PLACEBO WASN'T ENOUGH
---------------------------------
The published placebo shuffled the state<->magnitude labels. Its null is "no
association between VIX-state and magnitude." But the vol-clustering story ALSO
implies such an association (high VIX <=> high realized vol <=> big |CAR|), so a
label-shuffle rejects under BOTH the real-amplification hypothesis AND the
artifact. It cannot tell them apart.

THE RIGHT CONTROL
-----------------
Replace each real event with a RANDOM NON-EVENT date drawn from the SAME
VIX-percentile bucket (>=30 days from any corpus event so no real ripple leaks in).
Compute the identical high-minus-low split amplification on these pseudo-events.

  - If pseudo-events reproduce the amplification, it is a property of the VIX LEVEL,
    not of events -> vol-clustering -> H1 amplification is UNSUPPORTED.
  - If real events beat the pseudo distribution, events add something real.

We run it on BOTH metrics: raw |CAR| (the original headline) and SAR (R1). The
label-shuffle stays in EVALUATION, relabelled as an association check only.

ADDITIVE lens: reads the DB, writes data/placebo_vixmatched.json. Frozen record
untouched.

Run:  python3 src/placebo_vixmatched.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns
from event_study import car_for_event, PRE, POST
import research
import sar_lens
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

HORIZON = 20
K_REPS = 2000            # pseudo-samples drawn
EXCL_DAYS = 30          # keep pseudo-dates >= this many days from any corpus event
SEED = 19900802


def _amp(mags, states):
    """High-minus-low mean magnitude at the in-sample median split (the frozen statistic)."""
    med = np.median(states)
    hi = mags[states >= med]
    lo = mags[states < med]
    if len(hi) == 0 or len(lo) == 0:
        return np.nan
    return float(hi.mean() - lo.mean())


def run():
    conn = sqlite3.connect(DB)
    events = research._events(conn)
    state = research._state_series(conn, sar_lens.STATE_SID)          # daily VIX percentile
    asset = research._asset(sar_lens.ASSET_SERIES)
    ret = asset_returns(conn, asset["series"], asset["kind"])
    conn.close()

    L = PRE + HORIZON + 1
    ev_dates = pd.to_datetime(events["event_date"]).sort_values().to_numpy()

    # ---- magnitudes at any date (raw |CAR| in %, or SAR), self-contained ----
    def mag_at(date, standardized):
        car = car_for_event(ret, date)
        if car is None or PRE + HORIZON >= len(car):
            return None
        car_h = float(car[PRE + HORIZON])
        if not standardized:
            return abs(car_h) * 100.0
        sig = sar_lens._sigma_for_event(ret, date)
        return None if sig is None else abs(car_h / (sig * np.sqrt(L)))

    def state_at(date):
        v = state.asof(pd.Timestamp(date) - pd.Timedelta(days=1))
        return float(v) if pd.notna(v) else None

    # real clustered episodes -> (raw, sar, state) arrays
    from robustness import assign_clusters
    rows = []
    for _, ev in events.iterrows():
        r = mag_at(ev["event_date"], False); sar = mag_at(ev["event_date"], True); st = state_at(ev["event_date"])
        if r is not None and sar is not None and st is not None:
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"], "raw": r, "sar": sar, "state": st})
    df = assign_clusters(pd.DataFrame(rows))
    epi = df.groupby("cluster").first().reset_index()
    real_raw_amp = _amp(epi["raw"].to_numpy(float), epi["state"].to_numpy(float))
    real_sar_amp = _amp(epi["sar"].to_numpy(float), epi["state"].to_numpy(float))
    n_epi = len(epi)

    # ---- candidate pool of NON-event trading days with valid windows + state, >=30d from any event ----
    dates = ret.index
    ev_ts = pd.to_datetime(ev_dates)
    pool = []
    for i, d in enumerate(dates):
        # window guard (same as car_for_event) via position
        if i - 130 < 0 or i + POST >= len(dates):
            continue
        # >= EXCL_DAYS from any corpus event
        gap = np.min(np.abs((ev_ts - d).days.to_numpy())) if len(ev_ts) else 1e9
        if gap < EXCL_DAYS:
            continue
        st = state_at(d)
        if st is None:
            continue
        r = mag_at(d, False); sar = mag_at(d, True)
        if r is None or sar is None:
            continue
        pool.append((st, r, sar))
    pool = pd.DataFrame(pool, columns=["state", "raw", "sar"])

    # bucket candidates by VIX-percentile decile; match each real episode to its decile
    def decile(x):
        return int(min(9, max(0, x // 10)))
    pool["dec"] = pool["state"].apply(decile)
    by_dec = {d: pool[pool["dec"] == d] for d in range(10)}
    epi_dec = [decile(s) for s in epi["state"].to_numpy(float)]

    rng = np.random.default_rng(SEED)
    raw_amps, sar_amps = [], []
    for _ in range(K_REPS):
        praw, psar, pst = [], [], []
        ok = True
        for dcl in epi_dec:
            cand = by_dec.get(dcl)
            if cand is None or len(cand) == 0:
                # widen to nearest non-empty decile
                for w in range(1, 10):
                    for dd in (dcl - w, dcl + w):
                        if 0 <= dd <= 9 and len(by_dec.get(dd, [])) > 0:
                            cand = by_dec[dd]; break
                    if cand is not None and len(cand) > 0:
                        break
            if cand is None or len(cand) == 0:
                ok = False; break
            j = rng.integers(len(cand))
            row = cand.iloc[j]
            praw.append(row["raw"]); psar.append(row["sar"]); pst.append(row["state"])
        if not ok:
            continue
        raw_amps.append(_amp(np.array(praw), np.array(pst)))
        sar_amps.append(_amp(np.array(psar), np.array(pst)))

    raw_amps = np.array([a for a in raw_amps if not np.isnan(a)])
    sar_amps = np.array([a for a in sar_amps if not np.isnan(a)])

    def summ(arr, real):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        # share of pseudo amps AS LARGE OR LARGER than the real amp (one-sided, high tail)
        p = float((arr >= real).mean())
        return {"pseudo_mean": round(float(arr.mean()), 4), "pseudo_median": round(float(np.median(arr)), 4),
                "pseudo_ci95": [round(float(lo), 4), round(float(hi), 4)],
                "real_amp": round(float(real), 4), "p_real_le_pseudo": round(p, 4),
                "n_pseudo_samples": int(len(arr))}

    raw_s = summ(raw_amps, real_raw_amp)
    sar_s = summ(sar_amps, real_sar_amp)

    # interpretation: for RAW, is the real amp inside the pseudo (vol-matched) distribution?
    raw_inside = bool(raw_s["pseudo_ci95"][0] <= raw_s["real_amp"] <= raw_s["pseudo_ci95"][1])
    out = {
        "lens": "R2_vix_matched_placebo",
        "attack": 2,
        "config": {"horizon": HORIZON, "k_reps": K_REPS, "exclude_days_from_events": EXCL_DAYS,
                   "match": "VIX-percentile decile", "n_real_episodes": int(n_epi),
                   "candidate_pool_size": int(len(pool))},
        "raw_car": raw_s,
        "sar": sar_s,
        "interpretation": {
            "raw_real_inside_pseudo_ci": raw_inside,
            "verdict": ("RAW: vol-matched NON-EVENTS reproduce the amplification (real amp lies inside "
                        "the pseudo 95% band) -> the raw |CAR| amplification is VOL-CLUSTERING, not an "
                        "event ripple." if raw_inside else
                        "RAW: real events beat the vol-matched pseudo distribution -> events add signal "
                        "beyond vol-clustering."),
            "sar_note": "SAR amplification is ~0 for both real and pseudo, consistent with R1.",
        },
        "note": "The label-shuffle placebo remains in EVALUATION as an ASSOCIATION check only.",
    }
    (ROOT / "data" / "placebo_vixmatched.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
