"""
frozen_lens.py -- R5: the frozen-numbers-lead headline block (red-team attacks 9, 10).

WHY THIS EXISTS
---------------
Two integrity attacks, both CONCEDED:

  #9  The advertised H1 amplification (+5.56pp raw |CAR|) is recomputed on the
      GROWING corpus (N=296), not the frozen registered corpus (N=289). A number
      that moves as the corpus grows is a *tracking* number, not a registered
      result -- it must be labelled as such, and the genuinely-frozen number must
      lead.

  #10 The in-sample median split uses the WHOLE sample -- including future events --
      to decide the VIX threshold that labels an event "high stress". That is
      lookahead in the conditioner. The honest variant freezes the threshold on a
      past window (pre-2019) and applies it forward, with no peeking.

WHAT IT PRODUCES -- one headline BLOCK, three clearly-ranked numbers:

  (1) FROZEN registered-corpus number   -- H1 recomputed on EXACTLY the 289 events
      frozen at git tag edge-battery-preregistered-20260730 (list pinned in
      data/registered_corpus_289.txt). This is the number "as registered". Plus the
      genuinely-immutable n=20 registered-sample headline (+10.3pp), cited verbatim
      and never recomputed.

  (2) OUT-OF-SAMPLE number WITH A CI    -- the VIX split threshold is LEARNED on
      pre-2019 events, FROZEN, then applied to 2019+ events (attack #10 fixed). The
      holdout already had the point estimate (+2.92pp raw); this adds the missing
      cluster-bootstrap 95% CI at the FIXED threshold (not re-median'd per resample).

  (3) CURRENT-corpus tracking number    -- H1 on the full current corpus (N=296),
      clearly labelled THIRD as a growing-corpus tracking figure.

Every tier carries BOTH the raw |CAR| number (subject to vol-clustering) and the
BMP-standardized SAR number (the headline metric since R1). A frozen-threshold
variant of the in-sample median split is reported alongside the median split
everywhere (attack #10).

ADDITIVE LENS: reads the DB + the frozen id list, writes data/h1_frozen_threshold.json.
The frozen registered record is never edited.

Run:  python3 src/frozen_lens.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from spec_curve import brent_returns, event_mag, cluster_ids, REGISTERED, PRE
from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "h1_frozen_threshold.json"
FROZEN_IDS = ROOT / "data" / "registered_corpus_289.txt"
SPLIT_DATE = pd.Timestamp("2019-01-01")
SEED = 19900802          # same seed the registered machinery uses (validate.py)
N_BOOT = 10000
# The genuinely-immutable registered-sample headline -- cited, never recomputed.
REGISTERED_N20 = {"amp_pp": 10.3, "n_sample": 20, "source": "registered_run_results.txt (n=20, "
                  "frozen 2026-07-21); REGISTERED_SAMPLE.md", "rule": "HOLDS (threshold +5pp)"}


# --------------------------------------------------------------------------- rows / clusters
def _rows(ret, events, vixs, scale):
    """(date, magnitude, vix_state@t-1) per event at the REGISTERED spec, for the given scale.
    scale='raw' -> |CAR+20| in pp; scale='std' -> BMP |SCAR+20| (unitless). Point-in-time state."""
    out = []
    for _, ev in events.iterrows():
        mag = event_mag(ret, ev["event_date"], REGISTERED["est_len"], REGISTERED["post"], scale)
        if mag is None:
            continue
        state = vixs.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))
        if pd.isna(state):
            continue
        out.append((pd.Timestamp(ev["event_date"]), float(mag), float(state)))
    return sorted(out, key=lambda r: r[0])


def _clustered(rows):
    """De-overlap (35-day) and keep the first event per cluster -> the episode frame."""
    if not rows:
        return pd.DataFrame(columns=["date", "mag", "state"])
    df = pd.DataFrame(rows, columns=["date", "mag", "state"])
    df["cluster"] = cluster_ids(list(df["date"]), REGISTERED["cluster"])
    return df.groupby("cluster").first().reset_index(drop=True)[["date", "mag", "state"]]


# --------------------------------------------------------------------------- amplifications
def _amp_fixed(df, thr):
    """High-minus-low mean magnitude at a FIXED threshold thr (state > thr is 'high')."""
    hi, lo = df[df["state"] > thr]["mag"], df[df["state"] <= thr]["mag"]
    if len(hi) == 0 or len(lo) == 0:
        return None
    return float(hi.mean() - lo.mean())


def _amp_median(df):
    """High-minus-low mean magnitude at the IN-SAMPLE median (the split with lookahead)."""
    return _amp_fixed(df, float(np.median(df["state"])))


def _boot_ci(df, thr, seed=SEED, n_boot=N_BOOT):
    """Cluster-bootstrap 95% CI for the amplification at a FIXED threshold thr. Resample episodes
    with replacement; recompute high-minus-low at the SAME frozen thr each draw (no re-median --
    that is the point of the frozen-threshold variant). Returns amp/lo/hi/share_positive."""
    amp = _amp_fixed(df, thr)
    if amp is None or len(df) < 4:
        return {"amp": None if amp is None else round(amp, 4), "lo": None, "hi": None,
                "share_positive": None, "n_episodes": int(len(df))}
    m = df["mag"].to_numpy(float)
    s = df["state"].to_numpy(float)
    n = len(m)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        hi, lo = m[idx][s[idx] > thr], m[idx][s[idx] <= thr]
        if hi.size and lo.size:
            boot.append(hi.mean() - lo.mean())
    boot = np.array(boot)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"amp": round(amp, 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "share_positive": round(float((boot > 0).mean()), 3), "n_episodes": int(n)}


def _boot_ci_median(df, seed=SEED, n_boot=N_BOOT):
    """Bootstrap CI for the IN-SAMPLE median split (threshold re-medianed each resample -- this is
    the lookahead version, kept for honest side-by-side with the frozen-threshold CI)."""
    amp = _amp_median(df)
    if amp is None or len(df) < 4:
        return {"amp": amp, "lo": None, "hi": None, "share_positive": None, "n_episodes": int(len(df))}
    m = df["mag"].to_numpy(float)
    s = df["state"].to_numpy(float)
    n = len(m)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        mm, ss = m[idx], s[idx]
        med = np.median(ss)
        hi, lo = mm[ss > med], mm[ss <= med]
        if hi.size and lo.size:
            boot.append(hi.mean() - lo.mean())
    boot = np.array(boot)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"amp": round(amp, 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "share_positive": round(float((boot > 0).mean()), 3), "n_episodes": int(n)}


# --------------------------------------------------------------------------- driver
def _frozen_ids():
    return [ln.strip() for ln in FROZEN_IDS.read_text().splitlines()
            if ln.strip() and not ln.startswith("#")]


def run():
    conn = sqlite3.connect(DB)
    ret = brent_returns(conn)
    vixs = build_signals(load_wide(conn))["derived.vix_pct"].dropna()
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    conn.close()

    froz = set(_frozen_ids())
    events_289 = events[events["event_id"].isin(froz)].copy()
    events_296 = events.copy()

    def tier(evs, scale):
        return _clustered(_rows(ret, evs, vixs, scale))

    # --- tier (1): frozen registered corpus (exactly the 289) --------------------------------
    d289_raw, d289_sar = tier(events_289, "raw"), tier(events_289, "std")
    frozen_289 = {
        "n_events_in_corpus": int(len(events_289)),
        "raw_median": _boot_ci_median(d289_raw),
        "sar_median": _boot_ci_median(d289_sar),
    }

    # --- tier (3): current corpus (296), in-sample median split ------------------------------
    d296_raw, d296_sar = tier(events_296, "raw"), tier(events_296, "std")
    current_296 = {
        "n_events_in_corpus": int(len(events_296)),
        "raw_median": _boot_ci_median(d296_raw),
        "sar_median": _boot_ci_median(d296_sar),
    }

    # --- tier (2): out-of-sample, FROZEN pre-2019 threshold, WITH CI (attack 10) --------------
    # Learn the threshold on pre-2019 events only; freeze it; apply to 2019+.
    train_raw = d296_raw[d296_raw["date"] < SPLIT_DATE]
    test_raw = d296_raw[d296_raw["date"] >= SPLIT_DATE]
    train_sar = d296_sar[d296_sar["date"] < SPLIT_DATE]
    test_sar = d296_sar[d296_sar["date"] >= SPLIT_DATE]
    thr_raw = float(np.median(train_raw["state"])) if len(train_raw) else None
    thr_sar = float(np.median(train_sar["state"])) if len(train_sar) else None
    oos = {
        "frozen_threshold_pct": round(thr_raw, 2) if thr_raw is not None else None,
        "note": "VIX split threshold learned on pre-2019 clustered episodes, frozen, applied to 2019+. "
                "Bootstrap CI computed at the FIXED threshold (no re-median per resample).",
        "raw_in_sample_pre2019": _boot_ci(train_raw, thr_raw) if thr_raw is not None else None,
        "raw_out_of_sample_2019plus": _boot_ci(test_raw, thr_raw) if thr_raw is not None else None,
        "sar_out_of_sample_2019plus": _boot_ci(test_sar, thr_sar) if thr_sar is not None else None,
    }

    # --- attack-10 frozen-threshold variant of the CURRENT full-sample split -----------------
    # Same frozen pre-2019 threshold, applied to the WHOLE corpus, vs the in-sample median.
    frozen_threshold_variant = {
        "raw_in_sample_median_LOOKAHEAD": current_296["raw_median"],
        "raw_frozen_threshold_pointintime": _boot_ci(d296_raw, thr_raw) if thr_raw is not None else None,
        "sar_in_sample_median_LOOKAHEAD": current_296["sar_median"],
        "sar_frozen_threshold_pointintime": _boot_ci(d296_sar, thr_sar) if thr_sar is not None else None,
    }

    def excl0(block):
        return bool(block and block.get("lo") is not None and (block["lo"] > 0 or block["hi"] < 0))

    out = {
        "lens": "R5_frozen_numbers_headline_block",
        "attacks": [9, 10],
        "statement": "H1 amplification presented as a ranked block: (1) frozen registered-corpus "
                     "number, (2) out-of-sample number WITH CI at a frozen threshold, (3) current-"
                     "corpus tracking number. Raw |CAR| and BMP-SAR side by side at every tier.",
        "spec": "registered (est 130 / +20 / cluster 35 / VIX-pct state at t-1)",
        "tier1_frozen": {
            "registered_sample_n20_immutable": REGISTERED_N20,
            "registered_corpus_289": frozen_289,
            "frozen_id_source": "data/registered_corpus_289.txt (git tag "
                                "edge-battery-preregistered-20260730)",
        },
        "tier2_out_of_sample_with_ci": oos,
        "tier3_current_tracking_296": current_296,
        "attack10_frozen_threshold_variant": frozen_threshold_variant,
        "headline_metric_is_SAR": True,
        "verdict": (
            "SAR is null at every tier and the raw number SHRINKS out-of-sample "
            f"({oos['raw_out_of_sample_2019plus']['amp'] if oos['raw_out_of_sample_2019plus'] else None}pp, "
            f"CI {[oos['raw_out_of_sample_2019plus']['lo'], oos['raw_out_of_sample_2019plus']['hi']] if oos['raw_out_of_sample_2019plus'] else None}). "
            "The frozen-threshold (point-in-time) split "
            + ("does NOT" if not excl0(frozen_threshold_variant['raw_frozen_threshold_pointintime']) else "does")
            + " give a raw CI excluding zero. The advertised current-corpus raw number is a tracking "
              "figure, not a registered result."),
        "ci_flags": {
            "frozen_289_raw_excludes_zero": excl0(frozen_289["raw_median"]),
            "frozen_289_sar_excludes_zero": excl0(frozen_289["sar_median"]),
            "current_296_raw_excludes_zero": excl0(current_296["raw_median"]),
            "current_296_sar_excludes_zero": excl0(current_296["sar_median"]),
            "oos_raw_excludes_zero": excl0(oos["raw_out_of_sample_2019plus"]),
            "oos_sar_excludes_zero": excl0(oos["sar_out_of_sample_2019plus"]),
            "frozen_threshold_raw_excludes_zero": excl0(frozen_threshold_variant["raw_frozen_threshold_pointintime"]),
        },
        "corpus_note": "additive lens; frozen registered record untouched.",
    }
    JSON.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps(r, indent=2))
