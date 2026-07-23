"""
inference.py -- standardized ripples + permutation inference (a robustness LENS).

This module does NOT add a hypothesis or change a verdict. The pre-registered
+5pp clustered rule and its results (H1 HOLDS, H2 HOLDS, H3 FAILS) stand exactly
as registered. This is an ADDITIONAL, post-registration check that answers the
two things a sharp referee attacks first (FRONTIER_AUDIT F1, F2).

--------------------------------------------------------------------------------
F1 -- WHY STANDARDIZE (the volatility-clustering defence), in plain English:
Volatility clusters: big moves follow big moves, so some calendar periods are
simply more turbulent in EVERYTHING. High-VIX periods have larger |returns|
across the board. That means a raw |CAR+20| will look bigger for shocks that
happened in high-VIX states even if geopolitics amplified nothing -- "turbulent
times are turbulent." So H1's raw amplification could be partly mechanical.

The fix (Boehmer-Musumeci-Poulsen 1991): judge each ripple against ITS OWN normal
volatility. Divide CAR+20 by the standard deviation of daily returns over that
event's own estimation window (t-130..t-11), times sqrt(the number of days in the
CAR) -- because a k-day cumulative return has std ~ sigma*sqrt(k) under a random
walk. The result is "how many normal-period sigmas was this move." Now a high-VIX
event only shows amplification if its move was large RELATIVE to its already-
elevated normal vol. If H1 survives on standardized magnitudes, it is not just
volatility clustering. If it dies, the honest finding is "the conditioning was
volatility clustering" -- publishable either way.

F2 -- PERMUTATION INFERENCE (honest p without normality assumptions):
With this few events, parametric p-values are untrustworthy. Instead: hold the
|CAR| values fixed and SHUFFLE the state-variable labels across events many times.
Each shuffle asks "if the state label had nothing to do with the ripple, how often
would chance alone produce an amplification this big, in the predicted direction?"
The fraction of shuffles that match/beat the observed amplification is the
permutation p-value. Seeded, so two runs are identical.
--------------------------------------------------------------------------------

Import-only reuse: the clustering, the split math, the registered variables and
directions, and the CAR all come from robustness.py / event_study.py unchanged.
Any divergence from those samples/numbers would be a bug, not a choice.

Run:  python3 src/inference.py
"""

import sqlite3
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

# Import only -- these modules are NOT modified.
from event_study import load_returns, car_for_event, PRE, POST, EST_START, EST_END
from robustness import assign_clusters, split, REGISTERED, VOL_OUTLIER
from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "inference_results.txt"

PERMUTATION_SEED = 19900802     # fixed -> reproducible (nod to the first event)
N_PERM = 10_000
# CAR+20 cumulates the abnormal returns over t-5..t+20, i.e. PRE+20+1 daily
# returns. That count is the k in the sigma*sqrt(k) scaling.
CAR20_LEN = PRE + 20 + 1


def sigma_for_event(ret, event_date):
    """Standard deviation of daily returns over the event's OWN estimation window
    (t-130..t-11) -- the same window event_study.car_for_event uses for its mean.
    Returns None with the same bounds car_for_event uses, so the sample matches."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(event_date))
    if pos >= len(dates) or pos - EST_START < 0 or pos + POST >= len(dates):
        return None
    est = ret.iloc[pos - EST_START: pos - EST_END]
    sd = est.std()                                 # ddof=1, the sample sd
    return float(sd) if sd and np.isfinite(sd) and sd > 0 else None


def build_frame(conn):
    """One row per analysable event: raw |CAR+20|, standardized |CAR+20|, each
    registered state var at t-1, and Brent vol at t-1 (for the no-outlier cut).
    Clustered with robustness.assign_clusters -- the exact same sample."""
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql(
        "SELECT event_id, event_date AS date, type FROM events ORDER BY event_date",
        conn)

    rows, skipped_sigma = [], []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["date"])
        if car is None:
            continue
        sigma = sigma_for_event(ret, ev["date"])
        car20 = car[PRE + 20]
        if sigma is None:
            skipped_sigma.append(ev["event_id"])     # honesty: report, don't fudge
            continue
        std_car20 = car20 / (sigma * sqrt(CAR20_LEN))
        cutoff = pd.Timestamp(ev["date"]) - pd.Timedelta(days=1)   # t-1, no lookahead
        row = {"event_id": ev["event_id"], "date": ev["date"], "type": ev["type"],
               "abs_car_raw": abs(car20), "abs_car_std": abs(std_car20)}
        for _hid, sid, key, _sign, _desc in REGISTERED:
            s = signals[sid].dropna() if sid in signals else pd.Series(dtype=float)
            row[key] = s.asof(cutoff) if len(s) else np.nan
        bv = signals["derived.brent_vol20"].dropna()
        row["brent_vol"] = bv.asof(cutoff) if len(bv) else np.nan
        rows.append(row)

    df = assign_clusters(pd.DataFrame(rows))
    return df, skipped_sigma


def samples(df):
    """The three samples robustness.py uses, built identically."""
    clustered = df.groupby("cluster").first().reset_index()
    no_outlier = clustered[clustered["brent_vol"] < VOL_OUTLIER]
    return [("baseline (all events)", df),
            ("clustered", clustered),
            ("clustered, no outlier", no_outlier)]


def split_amp(df, state_col, mag_col):
    """Reuse robustness.split verbatim by pointing its 'abs_car' column at the
    magnitude we want (raw or standardized). Returns the split dict or None."""
    d = df.assign(abs_car=df[mag_col])
    return split(d, state_col)


def directional_amp(mags, states, med, sign):
    """Amplification in the PREDICTED direction: sign * (high-bucket - low-bucket)
    mean magnitude. sign>0 => high side amplifies (H1), sign<0 => low side (H2)."""
    hi, lo = mags[states >= med], mags[states < med]
    if hi.size == 0 or lo.size == 0:
        return np.nan
    return sign * (hi.mean() - lo.mean())


def permutation_p(mags, states, sign):
    """Fraction of label-shuffles whose directional amplification >= observed.
    Seeded per call, so it is byte-for-byte reproducible."""
    med = np.median(states)
    obs = directional_amp(mags, states, med, sign)
    if np.isnan(obs):
        return None, obs
    rng = np.random.default_rng(PERMUTATION_SEED)
    count = 0
    for _ in range(N_PERM):
        if directional_amp(mags, rng.permutation(states), med, sign) >= obs:
            count += 1
    return count / N_PERM, obs


def hypothesis_report(df, hid, sid, key, sign, desc, verdict_note):
    """Build the text block for one hypothesis: raw, standardized, permutation."""
    lines = [f"{hid} -- {sid} -- {desc}   [registered: {verdict_note}]"]

    lines.append("  RAW |CAR+20| amplification (high bucket - low bucket):")
    for label, samp in samples(df):
        r = split_amp(samp, key, "abs_car_raw")
        lines.append(f"    {label:<24} " +
                     ("not enough events" if r is None else
                      f"n={r['n']:<2}  {r['amp']:+.1f} pp"))

    lines.append("  STANDARDIZED |CAR+20 / (sigma*sqrt(%d))| amplification (high - low):"
                 % CAR20_LEN)
    for label, samp in samples(df):
        r = split_amp(samp, key, "abs_car_std")
        # split scales by 100 for pp; standardized values are already in sigma,
        # so divide that back out to report the difference in sigma units.
        lines.append(f"    {label:<24} " +
                     ("not enough events" if r is None else
                      f"n={r['n']:<2}  {r['amp'] / 100:+.2f} sigma"))

    clustered = samples(df)[1][1]
    lines.append(f"  PERMUTATION (clustered, directional, N={N_PERM:,}, "
                 f"seed={PERMUTATION_SEED}):")
    perm = {}
    for mag_col, unit, scale in [("abs_car_raw", "pp", 100.0),
                                 ("abs_car_std", "sigma", 1.0)]:
        sub = clustered[clustered[key].notna()]
        mags = sub[mag_col].to_numpy(dtype=float)
        states = sub[key].to_numpy(dtype=float)
        p, obs = permutation_p(mags, states, sign)
        perm[mag_col] = (p, obs)
        if p is None:
            lines.append(f"    {mag_col.split('_')[-1]:<12} could not be computed")
        else:
            lines.append(f"    {mag_col.split('_')[-1]:<12} observed "
                         f"{obs * scale:+.2f} {unit:<6} p = {p:.4f}")
    return lines, perm


def main():
    conn = sqlite3.connect(DB)
    df, skipped = build_frame(conn)
    conn.close()

    # Registered verdicts are fixed context here (not recomputed).
    verdict_note = {"H1": "HOLDS", "H2": "HOLDS", "H3": "FAILS (fenced)"}

    clustered_n = df.groupby("cluster").ngroups
    out = []
    bar = "#" * 78
    out += [bar,
            "STANDARDIZED RIPPLES + PERMUTATION INFERENCE",
            "A POST-REGISTRATION ROBUSTNESS LENS (FRONTIER_AUDIT F1, F2) -- NOT a new",
            "hypothesis. The pre-registered +5pp clustered rule and its verdicts stand",
            "unchanged; standardization and the permutation p are ADDITIONAL checks.",
            bar,
            f"Events analysed: {len(df)}   Clustered episodes: {clustered_n}",
            f"Standardization: CAR+20 / (estimation-window sigma * sqrt({CAR20_LEN})).",
            f"Permutation: {N_PERM:,} label-shuffles, seed {PERMUTATION_SEED} "
            f"(reproducible).",
            ""]
    if skipped:
        out.append(f"NOTE: {len(skipped)} event(s) lacked a valid estimation-window "
                   f"sigma and were excluded from standardization: {', '.join(skipped)}")
        out.append("")

    perms = {}
    for hid, sid, key, sign, desc in REGISTERED:
        block, perm = hypothesis_report(df, hid, sid, key, sign, desc,
                                        verdict_note[hid])
        perms[hid] = perm
        out += block + [""]

    # --- Plain-English summary; H1 (VIX) called out specifically ---
    out += ["=" * 78, "SUMMARY (plain English)", "=" * 78]
    for hid, sid, key, sign, desc in REGISTERED:
        raw = split_amp(samples(df)[1][1], key, "abs_car_raw")
        std = split_amp(samples(df)[1][1], key, "abs_car_std")
        raw_dir = None if raw is None else sign * raw["amp"]
        std_dir = None if std is None else sign * std["amp"] / 100
        p_std = perms[hid]["abs_car_std"][0]
        if raw_dir is None or std_dir is None:
            out.append(f"{hid}: insufficient events to judge.")
            continue
        survives = std_dir > 0            # still points the predicted way after scaling
        verb = "SURVIVES" if survives else "DOES NOT SURVIVE"
        out.append(
            f"{hid} ({sid.split('.')[-1]}): raw clustered {raw_dir:+.1f} pp in "
            f"predicted direction; standardized {std_dir:+.2f} sigma; permutation "
            f"p(std) = {p_std:.4f}.  -> {verb} standardization.")
    out += ["",
            "H1 (VIX) read: " + _h1_sentence(df, perms),
            "",
            "Reminder: verdicts are unchanged. The registered rule is +5pp on RAW",
            "clustered amplification; these lenses only tell you how much to trust it.",
            ""]

    text = "\n".join(out)
    OUT.write_text(text)
    print(text)
    print(f"Wrote {OUT}")


def _h1_sentence(df, perms):
    """One honest sentence on whether the VIX result survives standardization --
    reporting the raw-vs-standardized permutation p contrast, not overclaiming."""
    _hid, _sid, key, sign, _desc = REGISTERED[0]       # H1
    std = split_amp(samples(df)[1][1], key, "abs_car_std")
    if std is None:
        return "insufficient events to judge."
    std_dir = sign * std["amp"] / 100
    p_raw = perms["H1"]["abs_car_raw"][0]
    p_std = perms["H1"]["abs_car_std"][0]
    if std_dir > 0:
        return (f"the amplification stays in the predicted direction after removing "
                f"each event's own volatility ({std_dir:+.2f} sigma), so it is not "
                f"purely volatility clustering -- but its permutation significance "
                f"weakens from p={p_raw:.4f} (raw) to p={p_std:.4f} (standardized), "
                f"so at this sample size the standardized effect is suggestive, not "
                f"conclusive.")
    return (f"the amplification vanishes or flips once each event's own volatility is "
            f"scaled out ({std_dir:+.2f} sigma, permutation p={p_std:.4f} vs "
            f"p={p_raw:.4f} raw) -- consistent with the effect being volatility "
            f"clustering rather than transmission.")


if __name__ == "__main__":
    main()
