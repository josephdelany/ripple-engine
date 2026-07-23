"""
h5_gpr.py -- H5: GPR conditioning, EXPLORATORY and TWO-SIDED (per registered H5).

WHAT "EXPLORATORY" MEANS HERE (and why it is different from H1-H3):
H1-H3 were CONFIRMATORY: a direction and a +5pp decision rule were fixed before
any number was seen, so a result there earns a yes/no. H5 is different. It was
registered (2026-07-23, before computation) with NO direction -- the analyst's
recorded position was "not sure", because two mechanisms pull opposite ways
(high geopolitical tension -> fragility/amplification, vs. high tension already
priced in -> dampening). When you have not committed to a direction, you may not
later claim a one-sided result "worked". So this run is HYPOTHESIS-GENERATING: it
reports the direction OBSERVED and a TWO-SIDED permutation p (which asks how often
chance produces a gap this big in EITHER direction), and it deliberately does not
apply the +5pp rule. It generates a question for a future confirmatory test; it
settles nothing.

Everything else mirrors the established pipeline exactly (import-only reuse, no
forks): the same 42-event sample, the same clustering, the same standardized-CAR
machinery from inference.py. The only new ingredient is the conditioning variable
-- the GPR percentile at t-1.

Run:  python3 src/h5_gpr.py
"""

import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# Import only -- these are NOT modified.
import inference
from inference import (build_frame, samples, split_amp, directional_amp,
                       N_PERM, PERMUTATION_SEED, CAR20_LEN)

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "h5_results.txt"

# Verdict/one-sided language is forbidden in an exploratory report. Enforced below.
BANNED_WORDS = ("holds", "fails", "confirms", "confirm", "predicted", "predict")


def gpr_series(conn):
    """The daily GPR headline index as a date-indexed series."""
    g = pd.read_sql(
        "SELECT obs_date, value FROM observations WHERE series_id = 'gpr.GPRD' "
        "ORDER BY obs_date", conn)
    if g.empty:
        return pd.Series(dtype=float)
    g["obs_date"] = pd.to_datetime(g["obs_date"])
    return g.set_index("obs_date")["value"].sort_index()


def full_history_percentile(all_vals, v):
    """Where v ranks among every GPR day (0-100). None/NaN -> NaN."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return np.nan
    return float((all_vals <= v).mean() * 100)


def attach_gpr_pct(df, s):
    """Add a gpr_pct column: the full-history percentile of the GPR value at t-1.
    Point-in-time -- the value is the last GPR reading STRICTLY BEFORE the event,
    so the event's own GPR spike can never leak into its conditioning variable."""
    all_vals = s.to_numpy()
    pcts = []
    for _, r in df.iterrows():
        t_minus_1 = pd.Timestamp(r["date"]) - pd.Timedelta(days=1)
        v = s.asof(t_minus_1)
        pcts.append(full_history_percentile(all_vals, None if pd.isna(v) else float(v)))
    df = df.copy()
    df["gpr_pct"] = pcts
    return df


def two_sided_permutation(mags, states, n=N_PERM, seed=PERMUTATION_SEED):
    """Two-sided permutation p: hold |CAR| fixed, shuffle the GPR labels, and count
    how often the |high - low| gap is at least as large as observed -- in EITHER
    direction (that is what 'two-sided' means, and it is the honest test when no
    direction was registered). Seeded, so two runs are identical.

    Reuses inference.directional_amp with sign=+1 to get (high - low); we take the
    absolute value for the two-sided comparison."""
    med = np.median(states)
    obs = directional_amp(mags, states, med, 1)          # high - low
    if np.isnan(obs):
        return None, obs
    obs_abs = abs(obs)
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n):
        a = directional_amp(mags, rng.permutation(states), med, 1)
        if not np.isnan(a) and abs(a) >= obs_abs:
            count += 1
    return count / n, obs


def gpr_context():
    """DESCRIPTIVE ONLY -- today's GPR full-history percentile, for the engine-read
    and scenario context. H5 has NO registered direction, so this can NEVER be an
    amplifier; it is a plain readout, fenced off exactly like H3."""
    conn = sqlite3.connect(DB)
    s = gpr_series(conn)
    conn.close()
    if s.empty:
        return {"gpr_pct": None, "gpr_value": None, "as_of": None}
    vals = s.to_numpy()
    latest = float(vals[-1])
    return {"gpr_pct": round(full_history_percentile(vals, latest), 1),
            "gpr_value": round(latest, 1),
            "as_of": s.index[-1].date().isoformat()}


def _enforce_language(text):
    """Guarantee no verdict / one-sided language slipped into an exploratory report."""
    hits = [w for w in BANNED_WORDS if re.search(rf"\b{w}\b", text, re.IGNORECASE)]
    if hits:
        raise SystemExit(f"LANGUAGE CHECK FAILED: exploratory report contains "
                         f"forbidden verdict words {hits}. Fix the template.")


def main():
    conn = sqlite3.connect(DB)
    df, skipped = build_frame(conn)          # SAME sample as inference/robustness
    s = gpr_series(conn)
    conn.close()

    if s.empty:
        print("STOP: no gpr.GPRD data in the database. Run src/fetch_gpr.py first.")
        return

    df = attach_gpr_pct(df, s)
    clustered_n = df.groupby("cluster").ngroups

    lines = []
    def w(x=""):
        lines.append(x)

    bar = "#" * 80
    w(bar)
    w("H5 -- GPR CONDITIONING: EXPLORATORY, TWO-SIDED")
    w("Per registered H5 (BRIEF_SKELETON.md, registered 2026-07-23, before computation).")
    w("H5 was registered with NO direction ('not sure'). This is a HYPOTHESIS-")
    w("GENERATING run: it states the direction OBSERVED and a TWO-SIDED permutation")
    w("p. The +5pp directional rule does not apply to H5, and nothing here is a")
    w("verdict -- it is an exploratory result that raises a question for a future")
    w("confirmatory test, nothing more.")
    w(bar)
    w(f"Events analysed: {len(df)}   Clustered episodes: {clustered_n}")
    w("Conditioning variable: full-history percentile of the daily GPR index at t-1")
    w("(the last GPR reading strictly before the event -- no lookahead).")
    w("Split: high vs low at the event-sample median GPR percentile.")
    w("Standardization + clustering: identical to inference.py / robustness.py.")
    if skipped:
        w(f"NOTE: {len(skipped)} event(s) had no valid estimation-window sigma and "
          f"were excluded: {', '.join(skipped)}")
    w("")

    # --- RAW magnitude amplification across the three samples ---
    w("RAW |CAR+20| difference (high-GPR bucket minus low-GPR bucket):")
    for label, samp in samples(df):
        r = split_amp(samp, "gpr_pct", "abs_car_raw")
        w(f"    {label:<24} " + ("too few events" if r is None
                                  else f"n={r['n']:<2}  {r['amp']:+.1f} pp"))

    # --- STANDARDIZED magnitude amplification (sigma units) ---
    w(f"STANDARDIZED |CAR+20 / (sigma*sqrt({CAR20_LEN}))| difference (high - low):")
    for label, samp in samples(df):
        r = split_amp(samp, "gpr_pct", "abs_car_std")
        w(f"    {label:<24} " + ("too few events" if r is None
                                  else f"n={r['n']:<2}  {r['amp'] / 100:+.2f} sigma"))

    # --- Two-sided permutation on the clustered sample ---
    clustered = samples(df)[1][1]
    sub = clustered[clustered["gpr_pct"].notna()]
    states = sub["gpr_pct"].to_numpy(dtype=float)
    w(f"TWO-SIDED PERMUTATION (clustered, N={N_PERM:,}, seed={PERMUTATION_SEED}):")
    perm = {}
    for mag_col, unit, scale in [("abs_car_raw", "pp", 1.0),
                                 ("abs_car_std", "sigma", 1.0)]:
        mags = sub[mag_col].to_numpy(dtype=float)
        p, obs = two_sided_permutation(mags, states)
        obs_show = obs if mag_col == "abs_car_raw" else obs / 100
        perm[mag_col] = (p, obs_show)
        if p is None:
            w(f"    {mag_col.split('_')[-1]:<12} could not be computed")
        else:
            w(f"    {mag_col.split('_')[-1]:<12} observed gap {abs(obs_show):.2f} "
              f"{unit:<6} two-sided p = {p:.4f}")
    w("")

    # --- Direction OBSERVED (exploratory language only) ---
    clus_raw = split_amp(clustered, "gpr_pct", "abs_car_raw")
    w("=" * 80)
    w("DIRECTION OBSERVED (exploratory -- not a claim, no direction was registered)")
    w("=" * 80)
    if clus_raw is None:
        w("  Too few clustered events to describe a direction honestly.")
    else:
        amp = clus_raw["amp"]
        bigger = "larger" if amp > 0 else "smaller"
        p_raw = perm["abs_car_raw"][0]
        w(f"  In this sample, shocks arriving at high GPR showed {bigger} |CAR+20|")
        w(f"  than shocks arriving at low GPR (clustered gap {amp:+.1f} pp, two-sided")
        w(f"  permutation p = {p_raw:.4f}). This is a direction OBSERVED, offered as a")
        w(f"  hypothesis to be tested confirmatorily in future -- it is not evidence")
        w(f"  for or against any registered direction, because H5 registered none.")
    w("")

    text = "\n".join(lines)
    _enforce_language(text)          # hard stop if any verdict word slipped in
    OUT.write_text(text + "\n")
    print(text)
    print(f"\nWrote {OUT}   (language check passed: no verdict/one-sided words)")


if __name__ == "__main__":
    main()
