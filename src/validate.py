"""
validate.py -- THE VALIDATION FRAMEWORK (Phase A: "the courtroom before the trials").

Every signal in this engine must pass through here before it may be called an EDGE.
This module is the reusable rigor layer -- the standard anti-overfitting statistics a
quant researcher expects, ported (not imported) from the legacy quant_engine/ste/ modules
into ripple-engine so nothing depends on the read-only legacy tree.

WHAT IT PROVIDES (each function is small and hand-verifiable; see tests/test_validate.py):

  Multiple-testing correction  -- when you test many hypotheses, some look "significant"
    by chance. bh_fdr / bonferroni adjust for that so you don't fool yourself.
      bh_fdr(p, q)            Benjamini-Hochberg false-discovery-rate control
      bonferroni(p, alpha)    the conservative family-wise correction

  Confidence intervals         -- a number without an interval is a guess with a decimal.
      wilson_ci(k, n)         CI for a proportion / base rate
      bootstrap_ci(x, ...)    CI for any statistic by resampling the data
      cluster_bootstrap_amp() CI for an event-study amplification (resamples episodes)

  Assumption-free significance -- with tiny N, parametric p-values lie; shuffle instead.
      permutation_p(...)      directional permutation test (matches src/inference.py)

  Out-of-sample / anti-overfitting -- nothing is an edge until it survives OOS.
      cpcv_splits(...)        purged Combinatorial CV: many train/test paths, no leakage
      pbo_cscv(perf, S)       Probability of Backtest Overfitting (Lopez de Prado)
      deflated_sharpe(...)    is a Sharpe real after searching over many trials?
      diebold_mariano(a, b)   is forecaster A's error series really better than B's?

DEPENDENCIES: numpy only. scipy is used *if present* for exact tails, but every function
falls back to a hand-rolled approximation so this runs in CI (which installs no scipy).
That matches requirements.txt: "the engine's statistics are hand-rolled on numpy/pandas."

CLI (retro-apply the framework to the engine's existing claims):
    python3 src/validate.py claims     # H1/H2/H3: bootstrap CIs + FDR across hypotheses
    python3 src/validate.py analogue   # the forecaster: CPCV + PBO + Diebold-Mariano
    python3 src/validate.py            # both
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

# scipy is OPTIONAL. If it's here (your workstation) we use exact tails; if not (CI) we
# fall back to numpy approximations below. Either way the numbers are the same to ~3 dp.
try:
    from scipy import stats as _sps
    _HAS_SCIPY = True
except Exception:                 # pragma: no cover  (CI path)
    _HAS_SCIPY = False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


# ======================================================================================
# MULTIPLE-TESTING CORRECTION
# ======================================================================================
def bh_fdr(pvals, q=0.10):
    """Benjamini-Hochberg step-up procedure for controlling the False Discovery Rate.

    THE PROBLEM: test 20 dead hypotheses at p<0.05 and ~1 will look "significant" by luck.
    THE FIX: sort the p-values ascending; the largest rank k with p_(k) <= q*k/m sets the
    cutoff -- everything at or below that rank survives. This bounds the expected share of
    false positives among the survivors at q.

    Returns dict with:
      survive  : boolean list, True = passes FDR at level q
      qvalues  : BH-adjusted p-values (monotone; directly comparable to q)
      n_survive
    """
    p = np.asarray(pvals, float)
    m = len(p)
    if m == 0:
        return {"survive": [], "qvalues": [], "n_survive": 0, "q": q}
    order = np.argsort(p)                      # indices that sort p ascending
    ranks = np.arange(1, m + 1)

    # survive mask: find the largest rank meeting the BH line p_(k) <= q*k/m
    thresh_rank = 0
    for rank, idx in enumerate(order, 1):
        if p[idx] <= q * rank / m:
            thresh_rank = rank
    survive = np.zeros(m, bool)
    for rank, idx in enumerate(order, 1):
        if rank <= thresh_rank:
            survive[idx] = True

    # BH-adjusted q-values: p_(k)*m/k, then enforce monotonicity from the largest p down
    sorted_p = p[order]
    adj_sorted = sorted_p * m / ranks
    adj_sorted = np.minimum.accumulate(adj_sorted[::-1])[::-1]   # running min from the top
    adj_sorted = np.clip(adj_sorted, 0, 1)
    qvalues = np.empty(m)
    qvalues[order] = adj_sorted

    return {"survive": survive.tolist(), "qvalues": [round(float(v), 4) for v in qvalues],
            "n_survive": int(survive.sum()), "q": q}


def bonferroni(pvals, alpha=0.05):
    """Bonferroni: the strict family-wise correction. Adjusted p = min(1, p*m); a hypothesis
    survives if adjusted p < alpha. Controls the chance of ANY false positive (harsher than BH)."""
    p = np.asarray(pvals, float)
    m = len(p)
    adj = np.clip(p * m, 0, 1) if m else p
    return {"adjusted": [round(float(v), 4) for v in adj],
            "survive": [bool(v < alpha) for v in adj],
            "n_survive": int((adj < alpha).sum()) if m else 0, "alpha": alpha}


# ======================================================================================
# CONFIDENCE INTERVALS
# ======================================================================================
def wilson_ci(k, n, z=1.96):
    """Wilson score interval for a proportion k/n -> reads as '72% [61-81%], N=76'.
    Better than the naive p +/- z*sqrt(p(1-p)/n) at small n and near 0/1."""
    if n == 0:
        return {"p": None, "lo": None, "hi": None, "n": 0}
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = (z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return {"p": round(p, 3), "lo": round(center - half, 3),
            "hi": round(center + half, 3), "n": n}


def bootstrap_ci(values, stat="mean", n_boot=10000, ci=0.95, seed=19900802):
    """Percentile bootstrap CI for a statistic of a 1-D sample.

    Resample the data WITH REPLACEMENT n_boot times, recompute the statistic each time,
    and read the CI off the percentiles of that bootstrap distribution. `stat` is 'mean',
    'median', or any callable taking a numpy array. Seeded -> reproducible."""
    x = np.asarray([v for v in values if v is not None and np.isfinite(v)], float)
    n = len(x)
    if n < 2:
        return {"stat": None, "lo": None, "hi": None, "n": n}
    fn = {"mean": np.mean, "median": np.median}.get(stat, stat)
    rng = np.random.default_rng(seed)
    boot = np.array([fn(x[rng.integers(0, n, n)]) for _ in range(n_boot)])
    lo, hi = np.percentile(boot, [100 * (1 - ci) / 2, 100 * (1 + ci) / 2])
    return {"stat": round(float(fn(x)), 4), "lo": round(float(lo), 4),
            "hi": round(float(hi), 4), "n": n, "ci": ci}


def _directional_amp(mags, states, med, sign):
    """sign * (high-bucket mean - low-bucket mean) of `mags`, split on `states` at `med`.
    sign>0: the HIGH-state bucket is predicted bigger (H1/H3). sign<0: LOW bigger (H2)."""
    hi, lo = mags[states >= med], mags[states < med]
    if hi.size == 0 or lo.size == 0:
        return np.nan
    return sign * (hi.mean() - lo.mean())


def cluster_bootstrap_amp(mags, states, sign, n_boot=10000, seed=19900802):
    """Bootstrap CI for an event-study amplification (in the same units as `mags`).

    The analysis unit is the episode: resample the (magnitude, state) rows WITH REPLACEMENT,
    recompute the median split and the directional amplification each time. The CI is the
    percentile spread; `share_positive` is the bootstrap chance the amplification points the
    predicted way. At tiny N this interval is honestly wide -- that IS the finding."""
    mags = np.asarray(mags, float)
    states = np.asarray(states, float)
    keep = np.isfinite(mags) & np.isfinite(states)
    mags, states = mags[keep], states[keep]
    n = len(mags)
    obs = _directional_amp(mags, states, np.median(states), sign)
    if n < 4 or not np.isfinite(obs):
        return {"obs": None if not np.isfinite(obs) else round(float(obs), 4), "n": n,
                "lo": None, "hi": None, "share_positive": None}
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        m, s = mags[idx], states[idx]
        a = _directional_amp(m, s, np.median(s), sign)
        if np.isfinite(a):
            boot.append(a)
    boot = np.array(boot)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"obs": round(float(obs), 4), "n": n,
            "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "share_positive": round(float((boot > 0).mean()), 3)}


# ======================================================================================
# ASSUMPTION-FREE SIGNIFICANCE
# ======================================================================================
def permutation_p(mags, states, sign, n_perm=10000, seed=19900802):
    """Directional permutation test: hold the magnitudes fixed, SHUFFLE the state labels,
    and count how often chance alone matches/beats the observed directional amplification.
    Matches src/inference.py exactly (same median-at-observed convention, same seed default)."""
    mags = np.asarray(mags, float)
    states = np.asarray(states, float)
    keep = np.isfinite(mags) & np.isfinite(states)
    mags, states = mags[keep], states[keep]
    med = np.median(states)
    obs = _directional_amp(mags, states, med, sign)
    if not np.isfinite(obs):
        return {"p": None, "obs": None, "n": len(mags)}
    rng = np.random.default_rng(seed)
    count = sum(1 for _ in range(n_perm)
                if _directional_amp(mags, rng.permutation(states), med, sign) >= obs)
    return {"p": count / n_perm, "obs": round(float(obs), 4), "n": len(mags), "n_perm": n_perm}


# ======================================================================================
# OUT-OF-SAMPLE / ANTI-OVERFITTING
# ======================================================================================
def cpcv_splits(n, k_folds=6, k_test=2, embargo=0):
    """Purged Combinatorial CV (Lopez de Prado). Split n time-ordered rows into k_folds
    contiguous folds; use every C(k_folds, k_test) combination of folds as the TEST set and
    the rest as TRAIN. Rows within `embargo` of the test block are PURGED from train to kill
    leakage from serial correlation. Yields (train_idx, test_idx). More paths than a single
    split, so you see the DISPERSION of OOS performance, not one lucky number."""
    folds = np.array_split(np.arange(n), k_folds)
    for combo in itertools.combinations(range(k_folds), k_test):
        test = np.concatenate([folds[c] for c in combo])
        test_set = set(int(i) for i in test)
        # Train = every non-test row that is NOT within `embargo` of ANY test row. This purges
        # only the bands adjacent to each (possibly non-contiguous) test fold; rows sitting
        # BETWEEN two separated test folds stay in train. With embargo=0, train = all non-test.
        train = np.array([i for i in range(n)
                          if i not in test_set
                          and all(abs(i - t) > embargo for t in test_set)],
                         dtype=int)
        yield train, test


def pbo_cscv(perf, S=8):
    """Probability of Backtest Overfitting via Combinatorially-Symmetric CV.

    perf: (T observations x N candidate configs) matrix of a performance we MAXIMIZE
    (e.g. -Brier loss per event per config). Split the T rows into S blocks; for every way
    to choose S/2 blocks as in-sample, pick the best config IS, then look at its rank OUT-of-
    sample. PBO = the share of splits where the in-sample winner lands BELOW the OOS median.
    High PBO => the "best" config is an in-sample mirage. Rule of thumb: want PBO < ~0.2."""
    perf = np.asarray(perf, float)
    if perf.ndim != 2:
        return {"ok": False, "reason": "perf must be 2-D (T x N)"}
    T, N = perf.shape
    if N < 2 or T < S:
        return {"ok": False, "reason": "need >=2 configs and T>=S"}
    blocks = np.array_split(np.arange(T), S)
    logits = []
    for combo in itertools.combinations(range(S), S // 2):
        is_idx = np.concatenate([blocks[b] for b in combo])
        oos_idx = np.concatenate([blocks[b] for b in range(S) if b not in combo])
        is_perf = perf[is_idx].mean(axis=0)
        oos_perf = perf[oos_idx].mean(axis=0)
        n_star = int(np.argmax(is_perf))                 # best config in-sample
        rank = (oos_perf < oos_perf[n_star]).sum() / N   # its OOS percentile (0=worst,1=best)
        rank = min(max(rank, 1e-6), 1 - 1e-6)
        logits.append(np.log(rank / (1 - rank)))
    logits = np.array(logits)
    pbo = float((logits <= 0).mean())
    return {"ok": True, "pbo": round(pbo, 3), "n_splits": len(logits),
            "verdict": "overfit risk HIGH" if pbo > 0.5 else
                       ("overfit risk elevated" if pbo > 0.2 else "overfit risk acceptable")}


def deflated_sharpe(sharpe, n_obs, n_trials, skew=0.0, kurt=3.0):
    """Deflated Sharpe Ratio (Bailey & Lopez de Prado): after you searched over n_trials
    strategies, the expected MAX Sharpe under the null (no skill) is already > 0. DSR is the
    probability the true Sharpe > 0 once you subtract off that selection bias. Wants > 0.95."""
    if n_trials < 1 or n_obs < 3:
        return {"ok": False}
    e_max = ((1 - np.euler_gamma) * _z(1 - 1.0 / n_trials)
             + np.euler_gamma * _z(1 - 1.0 / (n_trials * np.e)))
    num = (sharpe - e_max) * np.sqrt(n_obs - 1)
    den = np.sqrt(max(1e-12, 1 - skew * sharpe + (kurt - 1) / 4.0 * sharpe ** 2))
    dsr = _ncdf(num / den)
    return {"ok": True, "deflated_sharpe_prob": round(float(dsr), 3),
            "expected_max_sharpe_null": round(float(e_max), 3),
            "verdict": "real" if dsr > 0.95 else "not distinguishable from overfit"}


def diebold_mariano(loss_a, loss_b, h=1):
    """Diebold-Mariano test of EQUAL predictive accuracy between two forecasters, using their
    per-observation LOSS series (e.g. Brier losses of the analogue vs the base rate).

    d_t = loss_a - loss_b. If A is better, d has a negative mean. The statistic is dbar over
    its standard error; we apply the Harvey-Leybourne-Newbold small-sample correction and,
    for h=1, use the plain sample variance (no autocovariance term). Two-sided p via Student-t
    (scipy) or a normal approximation (fallback). Negative stat + small p => A beats B."""
    a = np.asarray(loss_a, float)
    b = np.asarray(loss_b, float)
    keep = np.isfinite(a) & np.isfinite(b)
    d = (a - b)[keep]
    T = len(d)
    if T < 3:
        return {"ok": False, "reason": "need >=3 paired losses"}
    dbar = d.mean()
    # HAC (Newey-West) variance of the mean with h-1 lags; for h=1 this is just gamma_0/T
    gamma0 = d.var(ddof=0)
    var = gamma0
    for lag in range(1, h):
        cov = np.mean((d[lag:] - dbar) * (d[:-lag] - dbar))
        var += 2 * cov
    var_dbar = var / T
    if var_dbar <= 0:
        return {"ok": False, "reason": "degenerate (zero variance) loss difference"}
    dm = dbar / np.sqrt(var_dbar)
    # Harvey-Leybourne-Newbold small-sample correction factor
    corr = np.sqrt(max(1e-12, (T + 1 - 2 * h + h * (h - 1) / T) / T))
    dm_star = dm * corr
    if _HAS_SCIPY:
        p = 2 * (1 - _sps.t.cdf(abs(dm_star), df=T - 1))
    else:
        p = 2 * (1 - _ncdf(abs(dm_star)))     # normal approximation
    better = "A" if dbar < 0 else ("B" if dbar > 0 else "tie")
    return {"ok": True, "dm_stat": round(float(dm_star), 3), "p_value": round(float(p), 4),
            "mean_loss_diff": round(float(dbar), 5), "n": T,
            "better": better,
            "significant_5pct": bool(p < 0.05)}


# ---- numpy fallbacks for the normal/error functions (so scipy is optional) ----
def _z(p):
    """Inverse normal CDF (quantile)."""
    if _HAS_SCIPY:
        return float(_sps.norm.ppf(min(max(p, 1e-9), 1 - 1e-9)))
    return float(np.sqrt(2) * _erfinv(2 * min(max(p, 1e-9), 1 - 1e-9) - 1))


def _ncdf(x):
    """Standard normal CDF."""
    if _HAS_SCIPY:
        return float(_sps.norm.cdf(x))
    return 0.5 * (1 + _erf(x / np.sqrt(2)))


def _erf(x):
    """Abramowitz-Stegun 7.1.26 approximation of erf (max abs error ~1.5e-7)."""
    t = 1 / (1 + 0.3275911 * abs(x))
    y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
              - 0.284496736) * t + 0.254829592) * t * np.exp(-x * x)
    return np.sign(x) * y


def _erfinv(y):
    """Winitzki approximation of the inverse error function."""
    a = 0.147
    ln = np.log(1 - y * y)
    f = 2 / (np.pi * a) + ln / 2
    return np.sign(y) * np.sqrt(np.sqrt(f * f - ln / a) - f)


# ======================================================================================
# RETRO-APPLY #1 -- the pre-registered H1/H2/H3 conditioning claims
# ======================================================================================
def validate_claims():
    """Add confidence intervals (cluster bootstrap) and multiple-testing correction (across
    the THREE registered hypotheses) to H1/H2/H3.

    IMPORTANT -- this is a POST-REGISTRATION robustness lens, exactly like src/inference.py.
    It does NOT change the registered +5pp clustered decision rule or its verdicts (H1 HOLDS,
    H2 HOLDS, H3 FAILS). It only tells you how much to trust them: does the amplification's
    CI exclude zero, and does the permutation significance survive correcting for the fact
    that we tested three hypotheses, not one?"""
    import sqlite3
    import numpy as _np
    import pandas as pd
    # Rebuild the EXACT registered sample the way robustness.py does (NOT inference.py, which
    # additionally drops events without a valid standardization sigma -- a different, smaller
    # sample). Same primitives, same clustering -> obs amplification == the registered number.
    from event_study import load_returns, car_for_event, PRE
    from derive_signals import load_wide, build_signals
    from robustness import REGISTERED, assign_clusters, split

    conn = sqlite3.connect(DATA / "oil.db")
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date AS date, type FROM events "
                         "ORDER BY event_date", conn)
    conn.close()
    n_events_total = len(events)

    rows_f = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["date"]) - pd.Timedelta(days=1)   # t-1, no lookahead
        row = {"event_id": ev["event_id"], "date": ev["date"], "abs_car": abs(car[PRE + 20])}
        for _h, sid, key, _s, _d in REGISTERED:
            s = signals[sid].dropna() if sid in signals else pd.Series(dtype=float)
            row[key] = s.asof(cutoff) if len(s) else _np.nan
        rows_f.append(row)
    df = assign_clusters(pd.DataFrame(rows_f))
    clustered = df.groupby("cluster").first().reset_index()     # the registered decision sample
    skipped = []

    # What ENGINE.md documented from the ORIGINAL 20-event registered run (2026-07-22).
    documented = {"H1": ("HOLDS", 10.3), "H2": ("HOLDS", 5.4), "H3": ("FAILS", -6.8)}
    HOLD_PP = 5.0
    rows, pvals = [], []
    for hid, sid, key, sign, desc in REGISTERED:
        sub = clustered[clustered[key].notna()]
        mags = sub["abs_car"].to_numpy(float) * 100.0   # pp, matching robustness.split units
        states = sub[key].to_numpy(float)
        reg = split(clustered, key)                     # the registered split math on the CURRENT sample
        boot = cluster_bootstrap_amp(mags, states, sign)
        if reg is not None:                             # pin obs to the registered directional amp
            boot["obs"] = round(float(sign * reg["amp"]), 4)
        # The registered +5pp rule, applied to the CURRENT (grown) sample -- this is what the
        # pipeline computes today, which may differ from the documented 20-event result.
        cur_verdict = ("HOLDS" if (boot["obs"] is not None and boot["obs"] > HOLD_PP)
                       else "FAILS")
        doc_v, doc_amp = documented[hid]
        perm = permutation_p(mags * 1.0, states, sign)  # raw-pp permutation p
        p = perm["p"]
        pvals.append(p if p is not None else 1.0)
        rows.append({"hid": hid, "variable": sid, "desc": desc,
                     "documented_verdict_20ev": doc_v, "documented_amp_pp": doc_amp,
                     "current_verdict": cur_verdict, "drifted": cur_verdict != doc_v,
                     "amp_pp": boot["obs"], "n_episodes": boot["n"],
                     "ci95_pp": [boot["lo"], boot["hi"]],
                     "ci_excludes_zero": (boot["lo"] is not None
                                          and (boot["lo"] > 0 or boot["hi"] < 0)),
                     "boot_share_predicted_dir": boot["share_positive"],
                     "perm_p_raw": p})

    fdr = bh_fdr(pvals, q=0.10)
    bonf = bonferroni(pvals, alpha=0.05)
    for r, qv, surv, badj, bsurv in zip(rows, fdr["qvalues"], fdr["survive"],
                                        bonf["adjusted"], bonf["survive"]):
        r["fdr_qvalue"] = qv
        r["survives_fdr_10pct"] = bool(surv)
        r["bonferroni_p"] = badj
        r["survives_bonferroni_5pct"] = bool(bsurv)

    drifted = [r["hid"] for r in rows if r["drifted"]]
    report = {
        "what": "Rigor lens on the pre-registered H1/H2/H3 conditioning claims",
        "discipline": ("Applies the SAME registered +5pp clustered rule, and adds (a) a "
                       "cluster-bootstrap 95% CI on each amplification and (b) BH-FDR + "
                       "Bonferroni correction across the three hypotheses tested together."),
        "SAMPLE_DRIFT_WARNING": (
            "The pre-registration was run once on 20 events (2026-07-22); the DB now holds "
            "%d events (history loaded back to 1987). The registered scripts recompute on the "
            "grown sample, so today's numbers differ from what ENGINE.md documents. Drifted "
            "verdicts: %s. This is a scientific-integrity decision for Joe: freeze the "
            "registered sample, or re-baseline the study on the expanded N."
            % (n_events_total, drifted or "none")),
        "n_hypotheses": len(rows),
        "current_sample_events": n_events_total,
        "multiple_testing": {"fdr_q": fdr["q"], "n_survive_fdr": fdr["n_survive"],
                             "n_survive_bonferroni": bonf["n_survive"]},
        "hypotheses": rows,
        "honest_note": ("At N ~ %d episodes the bootstrap CIs are wide by construction -- a "
                        "small sample cannot promote a claim to a confident edge. The value "
                        "here is honesty about uncertainty, and the multiple-testing context: "
                        "we ran three tests, so a single small p is worth less than it looks."
                        % clustered.shape[0]),
    }
    (DATA / "validation_claims.json").write_text(json.dumps(report, indent=2))
    return report


def _print_claims(r):
    print("=" * 82)
    print("VALIDATION -- H1/H2/H3 conditioning claims (post-registration rigor)")
    print("=" * 82)
    print(r["discipline"])
    print("!! SAMPLE DRIFT: " + r["SAMPLE_DRIFT_WARNING"])
    print("-" * 82)
    for h in r["hypotheses"]:
        ci = h["ci95_pp"]
        ci_s = f"[{ci[0]:+.1f}, {ci[1]:+.1f}] pp" if ci[0] is not None else "n/a"
        drift = "  <-- DRIFTED" if h["drifted"] else ""
        print(f"{h['hid']} ({h['variable'].split('.')[-1]:<9}) doc(20ev)={h['documented_verdict_20ev']}@"
              f"{h['documented_amp_pp']:+.1f}  now(52ev)={h['current_verdict']}@{h['amp_pp']:+.1f}pp"
              f"  95%CI {ci_s}{drift}")
        print(f"     CI excludes 0: {h['ci_excludes_zero']!s:<5}   "
              f"boot P(predicted dir)={h['boot_share_predicted_dir']}   "
              f"perm p(raw)={h['perm_p_raw']}")
        print(f"     across-3 correction: FDR q={h['fdr_qvalue']} "
              f"(survive@10%={h['survives_fdr_10pct']})   "
              f"Bonferroni p={h['bonferroni_p']} (survive@5%={h['survives_bonferroni_5pct']})")
    mt = r["multiple_testing"]
    print("-" * 82)
    print(f"Across 3 hypotheses: {mt['n_survive_fdr']} survive FDR@{mt['fdr_q']}, "
          f"{mt['n_survive_bonferroni']} survive Bonferroni@5%.")
    print(r["honest_note"])
    print("Registered verdicts stand unchanged; this is a trust lens, not a re-decision.")


# ======================================================================================
# RETRO-APPLY #2 -- the analogue forecaster (the mandatory OOS gate)
# ======================================================================================
def validate_analogue():
    """The anti-overfitting gate every candidate forecaster must clear, applied to the
    analogue turbulence forecaster's walk-forward record (data/backtest_analogue.json).

    Three honest tests at this N:
      CPCV  -- dispersion of OOS skill-vs-base across many purged train/test paths (is the
               skill stable, or one lucky split?).
      PBO   -- over a shrinkage grid (how hard to shrink the raw signal toward the base rate):
               does the in-sample-best shrinkage overfit out-of-sample?
      DM    -- Diebold-Mariano: is the analogue's Brier-loss series significantly better than
               just predicting the base rate?
    Deflated Sharpe is intentionally NOT run here: it scores a P&L Sharpe, not a probability
    Brier. It belongs to the edge/accountability layer (Phase E), not this forecaster gate."""
    bt_path = DATA / "backtest_analogue.json"
    if not bt_path.exists():
        return {"ok": False, "reason": "run src/backtest_analogue.py first"}
    recs = json.loads(bt_path.read_text()).get("records", [])
    recs = sorted(recs, key=lambda r: r["date"])          # time order for purged CV
    n = len(recs)
    if n < 12:
        return {"ok": False, "reason": f"too few records ({n}) for CPCV/PBO"}
    p = np.array([r["p"] for r in recs], float)
    y = np.array([float(r["outcome"]) for r in recs], float)
    base = y.mean()

    # ---- headline (full-sample, for reference only) ----
    brier = float(np.mean((p - y) ** 2))
    base_brier = float(np.mean((base - y) ** 2))

    # ---- CPCV: OOS skill-vs-base across many purged paths ----
    # base rate is computed POINT-IN-TIME on each split's TRAIN fold (no peeking at test).
    skills = []
    for train, test in cpcv_splits(n, k_folds=6, k_test=2, embargo=1):
        if len(train) < 4 or len(test) < 2:
            continue
        b = y[train].mean()
        oos_brier = np.mean((p[test] - y[test]) ** 2)
        oos_base = np.mean((b - y[test]) ** 2)
        skills.append(oos_base - oos_brier)               # >0 => beats base rate OOS
    skills = np.array(skills)
    cpcv = {"n_paths": len(skills),
            "skill_mean": round(float(skills.mean()), 4) if len(skills) else None,
            "skill_std": round(float(skills.std()), 4) if len(skills) else None,
            "skill_median": round(float(np.median(skills)), 4) if len(skills) else None,
            "share_paths_positive": round(float((skills > 0).mean()), 3) if len(skills) else None}

    # ---- PBO over a shrinkage grid (the "hyperparameter" = how far to trust the raw signal) ----
    # config j predicts: base + lam_j*(p - base). lam=0 is the base rate, lam=1 is raw.
    lams = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25]
    perf = np.column_stack([-((base + lam * (p - base)) - y) ** 2 for lam in lams])  # -Brier
    pbo = pbo_cscv(perf, S=8)
    pbo["configs"] = {"shrinkage_lambdas": lams,
                      "note": "lam=0 -> base rate, lam=1 -> raw analogue signal"}

    # ---- Diebold-Mariano: analogue loss vs base-rate loss ----
    dm = diebold_mariano((p - y) ** 2, (base - y) ** 2, h=1)

    # ---- verdict (consistent with the standing null; nothing is promoted by this) ----
    passes = (cpcv["skill_mean"] is not None and cpcv["skill_mean"] > 0
              and (cpcv["share_paths_positive"] or 0) >= 0.5
              and pbo.get("pbo", 1.0) <= 0.2
              and dm.get("significant_5pct") and dm.get("better") == "A")
    report = {
        "what": "OOS validation gate on the analogue turbulence forecaster",
        "n_scored": n, "base_rate": round(float(base), 3),
        "full_sample_brier": round(brier, 4), "base_rate_brier": round(base_brier, 4),
        "full_sample_skill_vs_base": round(base_brier - brier, 4),
        "cpcv": cpcv, "pbo": pbo, "diebold_mariano": dm,
        "gate_passes": bool(passes),
        "verdict": ("PASSES the OOS gate -- promotable." if passes else
                    "DOES NOT PASS the OOS gate -- stays experimental / null. Consistent with "
                    "the standing finding: no OOS edge at this N. The honest fix is more N "
                    "(Phase B: grow the corpus), not tuning."),
    }
    (DATA / "validation_analogue.json").write_text(json.dumps(report, indent=2))
    return report


def _print_analogue(r):
    print("=" * 82)
    print("VALIDATION -- analogue forecaster OOS gate (CPCV + PBO + Diebold-Mariano)")
    print("=" * 82)
    if not r.get("ok", True) and "reason" in r:
        print("  " + r["reason"]); return
    print(f"N scored {r['n_scored']}   base rate {r['base_rate']}   "
          f"full-sample skill vs base {r['full_sample_skill_vs_base']:+}")
    c = r["cpcv"]
    print(f"  CPCV ({c['n_paths']} purged paths): skill mean {c['skill_mean']:+} "
          f"(sd {c['skill_std']}), median {c['skill_median']:+}, "
          f"share of paths beating base {c['share_paths_positive']}")
    pb = r["pbo"]
    if pb.get("ok"):
        print(f"  PBO over shrinkage grid: {pb['pbo']}  ({pb['verdict']}, {pb['n_splits']} splits)")
    else:
        print(f"  PBO: {pb.get('reason')}")
    d = r["diebold_mariano"]
    if d.get("ok"):
        print(f"  Diebold-Mariano vs base: stat {d['dm_stat']}  p {d['p_value']}  "
              f"(better={d['better']}, sig@5%={d['significant_5pct']})")
    print("-" * 82)
    print(f"  GATE: {r['verdict']}")


# ======================================================================================
# CLI
# ======================================================================================
def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("claims", "all"):
        _print_claims(validate_claims())
        print()
    if what in ("analogue", "all"):
        _print_analogue(validate_analogue())


if __name__ == "__main__":
    main()
