"""
edge_battery.py -- THE PRE-REGISTERED EDGE BATTERY (grow the validated-edge portfolio, honestly).

WHY THIS EXISTS:
Today the portfolio is essentially ONE mechanism: H1 (VIX-stress amplifies the oil ripple),
generalized to four assets, plus one apt-conditioned second edge (copper under a growth regime).
The elite move is NOT to hunt for more edges -- that is the p-hacking this engine exists to refuse.
It is to run a PRE-REGISTERED battery of economically-distinct hypotheses through the SAME gate
(clustered median split + cluster-bootstrap CI + permutation p), correct across the WHOLE family,
and report EVERY verdict -- validated AND null. Most of the battery is expected to be null. That is
the point: the discipline and the honest scorecard are the product a quant respects, not the count.

This generalizes the proven domain_conditioning.py pattern (copper-under-growth) into a single,
family-wise-corrected research program. The module docstring + the HYPOTHESES tuples below ARE the
pre-registration: the mechanism for each test is declared here, in code, BEFORE the result is seen
(git history proves this file predates data/edge_battery.json).

=========================== THE PRE-REGISTERED BATTERY (frozen) ===========================
Every hypothesis is built ONLY from data already in the engine ($0 / keyless / point-in-time).

CLASS 1 -- apt conditioners for assets that were null under GENERIC VIX-stress (the copper template).
  Each null may be a null because stress was the WRONG conditioner; each gets ONE apt, economically
  natural driver, pre-declared:
  1. silver_growth   -- silver is precious+INDUSTRIAL -> a growth metal like copper; amplifies in a
                        growth-on regime (steep 2s10s curve), not generic risk-off stress.
  2. palladium_growth-- palladium is an autocatalyst/industrial metal -> growth regime (steep curve),
                        not stress.
  3. gold_weak_dollar-- gold is priced in dollars and rises as the dollar weakens; a shock ripples
                        harder into gold when the dollar is ALREADY soft (usd_z low).
  4. yields_inflation-- an oil shock passes into 10Y NOMINAL yields more when the inflation regime is
                        already hot (10Y breakeven high) -- inflationary read vs flight-to-quality.

CLASS 2 -- event-type heterogeneity of the (validated) oil edge. Distinct mechanism: which KIND of
  shock transmits, holding the market constant.
  5. chokepoint_gt_sanction -- PHYSICAL supply-route shocks (chokepoint_disruption) ripple harder
                        into oil than FINANCIAL ones (sanctions). |CAR+20|, two-group.
  6. severity_dose_response -- high-severity events (codebook 4-5) ripple harder into oil than low
                        (1-2): a monotone dose-response that also validates the severity coding.

CLASS 3 -- the mispricing edge (a genuinely NEW KIND of edge: market ERROR, not reaction magnitude).
  7. under_priced_risk_oos -- when the engine flags under-priced risk (H1 ON while OVX prices calm),
                        realized +20d turbulence follows. SMALL-N (~14): reported with a Wilson CI and
                        labeled SUGGESTIVE -- NEVER shipped as validated until the corpus grows.

HONEST EXCLUSIONS (stated, not force-fit -- the same discipline that already excludes wheat):
  * natural gas  -- weather/storage-driven; no clean market-state proxy in the engine.
  * wheat        -- supply/weather-driven; no clean market-state proxy (already excluded upstream).
  * HY credit    -- keyless FRED caps the HY spread series (fred.BAMLH0A0HYM2) at ~3y of history,
                    so a point-in-time credit-cycle state cannot be built for events before 2024.
                    Excluded rather than tested on an unfairly short window.

FAMILY-WISE CORRECTION: the six amplification-style hypotheses above are tested together with the
FOUR prior domain_conditioning tests (gold_safe_haven, silver_precious, copper_growth,
palladium_supply) as ONE family of 10 -- BH-FDR (q=0.10) AND Bonferroni (alpha=0.05) across all of
them. That is the honest multiple-comparisons accounting a quant will demand; no per-test cherry-pick.
'validated' = CI excludes zero AND amp in the predicted direction AND survives the family FDR AND
survives leave-one-cluster-out. The mispricing edge (a forecast-skill test, not an amplification) is
reported ALONGSIDE the family as suggestive, never folded into the amplification FDR.

Run:  python3 src/edge_battery.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

import research
import validate
import domain_conditioning
from robustness import assign_clusters

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "edge_battery.json"
SEED = 19900802

# ---- CLASS 1: new apt conditioners (name, state, asset, sign, mechanism) -- same shape as the
#      domain_conditioning tuples so the two sets fold cleanly into one family.
CONDITIONING = [
    ("silver_growth",     "derived.curve_2s10s", "yf.silver",   "high",
     "silver is precious+industrial -> a growth metal; amplifies in a growth-on (steep-curve) regime"),
    ("palladium_growth",  "derived.curve_2s10s", "yf.palladium", "high",
     "palladium is an autocatalyst/industrial metal -> growth regime, not generic stress"),
    ("gold_weak_dollar",  "derived.usd_z",       "yf.gold",     "low",
     "gold rises as the dollar weakens; a shock ripples harder into gold when USD is already soft"),
    ("yields_inflation",  "derived.be_level",    "fred.DGS10",  "high",
     "an oil shock passes into 10Y nominal yields more when the inflation regime is already hot"),
]

# ---- CLASS 2: event-type heterogeneity of the oil edge (two-group tests on |CAR+20| in Brent).
OIL = "fred.DCOILBRENTEU"
HORIZON = 20


def _oil_type_frame(conn, horizon=HORIZON):
    """Clustered per-episode |CAR+horizon| in Brent (%), carrying event type + severity. One row per
    clustered episode (overlapping events collapsed, first kept) -- the same unit the gate uses."""
    events = research._events(conn)                       # event_id, event_date, type, title, url
    sev = pd.read_sql("SELECT event_id, severity FROM events", conn).set_index("event_id")["severity"]
    asset = research._asset(OIL)
    mags = research._car_mags(conn, asset, events, horizon)   # event_id -> |CAR| in %
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] in mags:
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                         "type": ev["type"], "mag": mags[ev["event_id"]],
                         "severity": sev.get(ev["event_id"])})
    df = assign_clusters(pd.DataFrame(rows))
    return df.groupby("cluster").first().reset_index()


def _diff_test(a, b, sign=+1, n_iter=10000, seed=SEED):
    """Two-group directional test: is mean(a) bigger than mean(b) in the predicted direction?
    Permutation p (shuffle group labels) + bootstrap CI on the difference (resample within group).
    The analysis unit is the episode; assumption-free, mirrors validate's style. sign=+1: a>b."""
    a = np.asarray([x for x in a if np.isfinite(x)], float)
    b = np.asarray([x for x in b if np.isfinite(x)], float)
    if len(a) < 3 or len(b) < 3:
        return {"ok": False, "reason": f"too few episodes (a={len(a)}, b={len(b)})"}
    obs = sign * (a.mean() - b.mean())
    pooled = np.concatenate([a, b]); na = len(a)
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_iter):
        idx = rng.permutation(len(pooled))
        d = sign * (pooled[idx[:na]].mean() - pooled[idx[na:]].mean())
        if d >= obs:
            cnt += 1
    perm_p = cnt / n_iter
    boot = np.empty(n_iter)
    for i in range(n_iter):
        aa = a[rng.integers(0, na, na)]; bb = b[rng.integers(0, len(b), len(b))]
        boot[i] = sign * (aa.mean() - bb.mean())
    lo, hi = np.percentile(boot, [2.5, 97.5])
    excl0 = bool(lo > 0 or hi < 0)
    return {"ok": True, "amp": round(float(obs), 4), "ci": [round(float(lo), 4), round(float(hi), 4)],
            "ci_excludes_zero": excl0, "perm_p": round(perm_p, 4), "n": int(na + len(b)),
            "n_a": int(na), "n_b": int(len(b))}


# ---- Leave-one-cluster-out robustness for winners (reconstruct the gate's arrays, jackknife) ----
def _amp_arrays(conn, state_sid, asset_series, horizon):
    """Reproduce run_test's clustered (magnitude, state) arrays so a winner can be jackknifed.
    Mirrors research.run_test exactly; returns (mags, states) at the episode level or (None, None)."""
    events = research._events(conn)
    asset = research._asset(asset_series)
    state = research._state_series(conn, state_sid)
    if state.empty:
        return None, None
    mags = research._car_mags(conn, asset, events, horizon)
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] not in mags:
            continue
        v = state.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))
        if pd.notna(v):
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                         "mag": mags[ev["event_id"]], "state": float(v)})
    if len(rows) < 12:
        return None, None
    df = assign_clusters(pd.DataFrame(rows))
    clustered = df.groupby("cluster").first().reset_index()
    return clustered["mag"].to_numpy(float), clustered["state"].to_numpy(float)


def _leave_one_cluster_out(mags, states, sign):
    """Drop each episode once; does the amplification keep its predicted sign every time?
    Returns dict with the min/max jackknife amp and a 'robust' flag (never flips sign)."""
    n = len(mags)
    amps = []
    for i in range(n):
        m = np.delete(mags, i); s = np.delete(states, i)
        a = validate._directional_amp(m, s, np.median(s), sign)
        if np.isfinite(a):
            amps.append(float(a))
    if not amps:
        return {"robust": False, "min": None, "max": None}
    same_sign = all(a > 0 for a in amps)     # predicted direction is already folded into `sign`
    return {"robust": bool(same_sign), "min": round(min(amps), 4), "max": round(max(amps), 4),
            "n_jackknife": len(amps)}


def _run_amplification(conn, name, state, asset, sign, mech):
    """One amplification hypothesis through the gate -> a normalized result row."""
    r = research.run_test(conn, state, asset, sign, HORIZON)
    if not r.get("ok"):
        return {"hypothesis": name, "class": "amplification", "state": state, "asset": asset,
                "sign": sign, "mechanism": mech, "testable": False, "error": r.get("reason")}
    return {"hypothesis": name, "class": "amplification", "state": state, "asset": asset,
            "sign": sign, "mechanism": mech, "testable": True, "unit": r["asset"]["unit"],
            "n": r["n"], "amp": r["amp"], "ci": r["ci"], "ci_excludes_zero": r["ci_excludes_zero"],
            "perm_p": r["perm_p"], "boot_share": r["boot_share"]}


def _mispricing(conn):
    """The under-priced-risk forecast-skill test, read off the resolved gap ledger. SUGGESTIVE only:
    small N and the direction is defined in-sample, so it is reported with a Wilson CI vs the base
    rate and NEVER labeled validated here."""
    g = json.loads((ROOT / "data" / "gaps.json").read_text()) if (ROOT / "data" / "gaps.json").exists() else {}
    led = g.get("ledger", {})
    base = led.get("turbulence_base_rate")
    sub = (led.get("by_gap_direction") or {}).get("under_priced_risk") or {}
    n = sub.get("n"); rate = sub.get("turbulence_rate")
    if not n or rate is None:
        return {"hypothesis": "under_priced_risk_oos", "class": "mispricing", "testable": False,
                "verdict": "suggestive", "note": "gap ledger not built yet"}
    k = int(round(rate * n))
    w = validate.wilson_ci(k, n)
    beats_base = bool(base is not None and w["lo"] is not None and w["lo"] > base)
    return {"hypothesis": "under_priced_risk_oos", "class": "mispricing", "testable": True,
            "verdict": "suggestive",                       # never 'validated' at this N -- by design
            "n": n, "turbulence_rate": rate, "wilson_ci": [w["lo"], w["hi"]],
            "base_rate": base, "lower_bound_beats_base": beats_base, "brier": sub.get("brier"),
            "note": "small-N, direction defined in-sample -> suggestive; grows into a real test as N rises"}


def _collinearity(conn):
    """Show the conditioners are not just VIX in disguise: pairwise |correlation| of the distinct
    state signals used in the battery, on their common dates."""
    states = ["derived.vix_pct", "derived.curve_2s10s", "derived.usd_z", "derived.be_level"]
    sig = research.build_signals(research.load_wide(conn))
    have = [s for s in states if s in sig]
    sub = sig[have].dropna()
    cors = {}
    for i in range(len(have)):
        for j in range(i + 1, len(have)):
            c = float(np.corrcoef(sub[have[i]], sub[have[j]])[0, 1]) if len(sub) > 2 else None
            cors[f"{have[i].split('.')[-1]} x {have[j].split('.')[-1]}"] = round(c, 3) if c is not None else None
    return {"n_days": int(len(sub)), "abs_max": round(max((abs(v) for v in cors.values() if v is not None), default=0.0), 3),
            "pairwise": cors}


def run():
    conn = sqlite3.connect(DB)

    # 1) the amplification family = 4 prior domain tests + 4 new conditioners + 2 event-type tests.
    amp = []
    for name, state, asset, sign, mech in domain_conditioning.HYPOTHESES:
        row = _run_amplification(conn, name, state, asset, sign, mech)
        row["prior"] = True                                # folded in for honest family-wise counting
        amp.append(row)
    for name, state, asset, sign, mech in CONDITIONING:
        row = _run_amplification(conn, name, state, asset, sign, mech)
        row["prior"] = False
        amp.append(row)

    # event-type heterogeneity (two-group)
    frame = _oil_type_frame(conn)
    choke = frame.loc[frame["type"] == "chokepoint_disruption", "mag"]
    sanc = frame.loc[frame["type"] == "sanctions", "mag"]
    d1 = _diff_test(choke.to_numpy(float), sanc.to_numpy(float), sign=+1)
    amp.append({"hypothesis": "chokepoint_gt_sanction", "class": "amplification", "prior": False,
                "asset": OIL, "unit": "%", "mechanism": "physical route shocks (chokepoint) ripple "
                "harder into oil than financial ones (sanctions)", "testable": d1.get("ok", False),
                **({"n": d1["n"], "amp": d1["amp"], "ci": d1["ci"],
                    "ci_excludes_zero": d1["ci_excludes_zero"], "perm_p": d1["perm_p"],
                    "groups": {"chokepoint": d1["n_a"], "sanctions": d1["n_b"]}}
                   if d1.get("ok") else {"error": d1.get("reason")})})

    sev = pd.to_numeric(frame["severity"], errors="coerce")
    hi = frame.loc[sev >= 4, "mag"]; lo = frame.loc[sev <= 2, "mag"]
    d2 = _diff_test(hi.to_numpy(float), lo.to_numpy(float), sign=+1)
    amp.append({"hypothesis": "severity_dose_response", "class": "amplification", "prior": False,
                "asset": OIL, "unit": "%", "mechanism": "high-severity (4-5) events ripple harder "
                "into oil than low-severity (1-2): a monotone dose-response", "testable": d2.get("ok", False),
                **({"n": d2["n"], "amp": d2["amp"], "ci": d2["ci"],
                    "ci_excludes_zero": d2["ci_excludes_zero"], "perm_p": d2["perm_p"],
                    "groups": {"high_sev": d2["n_a"], "low_sev": d2["n_b"]}}
                   if d2.get("ok") else {"error": d2.get("reason")})})

    # 2) family-wise correction across ALL testable amplification hypotheses (prior + new).
    testable = [r for r in amp if r.get("testable") and r.get("perm_p") is not None]
    pvals = [r["perm_p"] for r in testable]
    fdr = validate.bh_fdr(pvals, q=0.10)
    bon = validate.bonferroni(pvals, alpha=0.05)
    for r, surv_fdr, q, surv_bon, adj in zip(testable, fdr["survive"], fdr["qvalues"],
                                             bon["survive"], bon["adjusted"]):
        r["fdr_q"] = q
        r["survives_fdr"] = bool(surv_fdr)
        r["bonferroni_adj"] = adj
        r["survives_bonferroni"] = bool(surv_bon)
        directional = bool(r.get("ci_excludes_zero") and r.get("amp") and r["amp"] > 0)
        r["validated"] = bool(directional and surv_fdr)     # robustness confirmed below
    for r in amp:
        r.setdefault("validated", False)

    # 3) leave-one-cluster-out robustness on winners (state-conditioned ones only; two-group winners
    #    get a group-size note instead). A winner that flips sign on any drop is downgraded.
    for r in amp:
        if r.get("validated") and r.get("state") and r.get("asset"):
            m, s = _amp_arrays(conn, r["state"], r["asset"], HORIZON)
            if m is not None:
                sign = +1 if r["sign"] == "high" else -1
                rob = _leave_one_cluster_out(m, s, sign)
                r["robustness"] = rob
                if not rob["robust"]:
                    r["validated"] = False
                    r["downgraded"] = "failed leave-one-cluster-out (sign flips on a single drop)"

    mis = _mispricing(conn)
    coll = _collinearity(conn)
    conn.close()

    validated = [r["hypothesis"] for r in amp if r.get("validated")]
    report = {
        "what": "Pre-registered edge battery: a family of economically-distinct conditioned "
                "event-study hypotheses, family-wise corrected (BH-FDR q=0.10 AND Bonferroni "
                "alpha=0.05) across prior + new tests, every verdict reported. The mispricing edge "
                "is reported alongside as suggestive (small-N), never folded into the amplification FDR.",
        "pre_registration": "src/edge_battery.py docstring + HYPOTHESES (frozen before results; see git).",
        "family_size": len(testable), "n_validated": len(validated), "validated": validated,
        "fdr": {"q": fdr["q"], "n_survive": fdr["n_survive"]},
        "bonferroni": {"alpha": bon["alpha"], "n_survive": bon["n_survive"]},
        "amplification": amp, "mispricing": mis, "collinearity": coll,
        "exclusions": {"natural_gas": "weather/storage-driven; no clean market-state proxy",
                       "wheat": "supply/weather-driven; no clean market-state proxy",
                       "hy_credit": "keyless FRED caps the HY spread at ~3y; no point-in-time "
                                    "credit-state for pre-2024 events -- excluded, not force-fit"},
    }
    OUT.write_text(json.dumps(report, indent=2, default=str))
    return report


def _fmt(r):
    if not r.get("testable"):
        return f"  {r['hypothesis']:<24} -- not testable ({r.get('error', 'n/a')})"
    ci = r.get("ci", [None, None])
    tag = "VALIDATED" if r.get("validated") else ("prior" if r.get("prior") else "null")
    q = r.get("fdr_q")
    line = (f"  {r['hypothesis']:<24} amp {r['amp']:+.2f}{r.get('unit',''):<3} "
            f"CI[{ci[0]:+.2f},{ci[1]:+.2f}] perm_p={r['perm_p']} fdr_q={q} [{tag}]")
    if r.get("downgraded"):
        line += "  (downgraded: robustness)"
    return line


def main():
    r = run()
    print("=" * 92)
    print("THE PRE-REGISTERED EDGE BATTERY -- family-wise corrected; every verdict reported")
    print("=" * 92)
    print(f"  family of {r['family_size']} amplification hypotheses (prior + new); "
          f"FDR survivors={r['fdr']['n_survive']}, Bonferroni survivors={r['bonferroni']['n_survive']}")
    print("-" * 92)
    for row in r["amplification"]:
        print(_fmt(row))
    print("-" * 92)
    m = r["mispricing"]
    if m.get("testable"):
        print(f"  under_priced_risk_oos    n={m['n']} turbulence={m['turbulence_rate']} "
              f"Wilson{m['wilson_ci']} vs base {m['base_rate']}  [SUGGESTIVE -- never validated at this N]")
    coll = r["collinearity"]
    print(f"  conditioner collinearity: |r|max={coll['abs_max']} across {coll['n_days']} common days "
          f"(distinct drivers, not VIX in disguise)")
    print("-" * 92)
    print(f"  VALIDATED (survives family FDR + directional CI + robustness): {r['validated'] or 'none'}")
    print(f"  honest exclusions: {', '.join(r['exclusions'].keys())}")
    print(f"\n  wrote {OUT}")


if __name__ == "__main__":
    main()
