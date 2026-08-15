"""
evidentiary_bar.py -- R7: ONE evidentiary bar, applied retroactively (attacks 15, 16).

THE ATTACK (CONCEDED)
---------------------
#16 Inconsistent bar. gold/palladium survive FDR-on-permutation-p but are (correctly)
    NOT called validated because their bootstrap CI spans zero -- yet permutation-p is
    the primary support cited for H1. Apply ONE bar to H1 too.
#15 The weakest edge (mispricing, n=14, in-sample direction) is conveniently "reported
    alongside, NOT in the FDR family." Every framing choice protects the survivors.

THE ONE BAR (codified here and in EVALUATION.md), applied to EVERY validated claim:
  A claim is `validated` IFF ALL THREE hold --
    (1) SAR-STANDARDIZED effect: the amplification is computed on BMP-standardized
        abnormal returns (each event's CAR / its own estimation-window sigma*sqrt(L)),
        so a "big" move in a noisy regime is not counted as large just for the backdrop;
    (2) REGIME-BLOCK-ROBUST bootstrap CI EXCLUDING ZERO: the 95% cluster-bootstrap CI on
        the SAR amplification excludes zero on the full corpus AND in every regime-block
        leave-out (drop 2008 / 2020 / 2026 / all three);
    (3) PERMUTATION-FDR: its SAR permutation-p survives BH-FDR (q=0.10) across the family.

Whatever fails any leg is DOWNGRADED. This lens computes all three legs for the current
validated set and writes the re-tiering. SAR-standardisation is an event-study abnormal-
return concept; the monthly pass-through edge (CC5) has no abnormal-return SAR, so its
leg (1) is N/A -- flagged explicitly, not silently exempted.

ADDITIVE: reads DB + prior receipts; writes data/evidentiary_bar.json. Registered record untouched.
Run:  python3 src/evidentiary_bar.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns
from event_study import car_for_event, PRE, POST, EST_START, EST_END
from robustness import assign_clusters
import research
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "evidentiary_bar.json"
HORIZON = 20
REGIME_YEARS = [{2008}, {2020}, {2026}, {2008, 2020, 2026}]
REGIME_LABELS = ["drop_2008", "drop_2020", "drop_2026", "drop_all_three"]

# The current validated universe (from edge_battery.json / cross_chain.json / validation_claims.json).
STATE_SPLIT_EDGES = [   # (name, asset_series, state_sid, sign_str)
    ("H1_vix_oil",       "fred.DCOILBRENTEU", "derived.vix_pct",       "high"),
    ("copper_growth",    "yf.copper",         "derived.curve_2s10s",   "high"),
    ("palladium_supply", "yf.palladium",      "derived.vix_pct",       "high"),
    ("hy_credit_stress", "yf.hyg",            "derived.credit_stress", "high"),
]


def _asset_ret(conn, asset_series):
    a = research._asset(asset_series)
    return asset_returns(conn, a["series"], a["kind"])


def _sigma(ret, date):
    """Estimation-window SD of daily returns (same guard as event_study.car_for_event)."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(date))
    if pos >= len(dates) or pos - EST_START < 0 or pos + POST >= len(dates):
        return None
    sd = float(ret.iloc[pos - EST_START: pos - EST_END].std(ddof=1))
    return sd if sd > 0 else None


def _sar_mags(ret, events):
    """Per-event BMP |SCAR+HORIZON| (unitless) for the given asset returns."""
    L = PRE + HORIZON + 1
    out = {}
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None or PRE + HORIZON >= len(car):
            continue
        sig = _sigma(ret, ev["event_date"])
        if sig is None:
            continue
        out[ev["event_id"]] = abs(float(car[PRE + HORIZON]) / (sig * np.sqrt(L)))
    return out


def _episodes(conn, events, mags, state_sid):
    state = research._state_series(conn, state_sid)
    if state.empty:
        return None, None
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] not in mags:
            continue
        v = state.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))   # t-1, point-in-time
        if pd.notna(v):
            rows.append({"date": ev["event_date"], "mag": mags[ev["event_id"]], "state": float(v)})
    if len(rows) < 12:
        return None, None
    df = assign_clusters(pd.DataFrame(rows))
    c = df.groupby("cluster").first().reset_index()
    return c["mag"].to_numpy(float), c["state"].to_numpy(float)


def _gate(m, s, sign):
    boot = validate.cluster_bootstrap_amp(m, s, sign=sign)
    perm = validate.permutation_p(m, s, sign=sign)
    excl0 = bool(boot["lo"] is not None and (boot["lo"] > 0 or boot["hi"] < 0))
    return {"amp": boot["obs"], "ci95": [boot["lo"], boot["hi"]], "perm_p": perm["p"],
            "ci_excludes_zero": excl0, "n_episodes": int(len(m))}


def _state_split_edge(conn, name, asset_series, state_sid, sign_str):
    ret = _asset_ret(conn, asset_series)
    sign = +1 if sign_str == "high" else -1
    events = research._events(conn)
    yr = pd.to_datetime(events["event_date"]).dt.year

    def gate_for(sub):
        m, s = _episodes(conn, sub, _sar_mags(ret, sub), state_sid)
        return _gate(m, s, sign) if m is not None else None

    full = gate_for(events)
    regimes = {}
    for years, label in zip(REGIME_YEARS, REGIME_LABELS):
        regimes[label] = gate_for(events[~yr.isin(years)])
    return {"name": name, "kind": "state_split", "asset": asset_series, "state": state_sid,
            "sign": sign_str, "sar_full": full, "sar_regime_block": regimes}


def _severity_edge(conn):
    """severity_dose_response as a two-group SAR test: high-severity (>=4) minus low-severity (<=2)
    mean |SCAR+20|, with a cluster-bootstrap CI and a group-label permutation p."""
    ret = _asset_ret(conn, "fred.DCOILBRENTEU")
    ev = pd.read_sql("SELECT event_id, event_date, severity FROM events WHERE severity IS NOT NULL "
                     "ORDER BY event_date", conn)
    mags = _sar_mags(ret, ev)

    def frame(sub):
        rows = [{"date": r.event_date, "mag": mags[r.event_id],
                 "grp": (1 if r.severity >= 4 else (0 if r.severity <= 2 else np.nan))}
                for r in sub.itertuples() if r.event_id in mags]
        df = pd.DataFrame(rows).dropna()
        if len(df) < 12:
            return None
        return assign_clusters(df).groupby("cluster").first().reset_index()

    def gate(df):
        if df is None:
            return None
        hi = df[df["grp"] == 1]["mag"].to_numpy(float)
        lo = df[df["grp"] == 0]["mag"].to_numpy(float)
        if len(hi) < 3 or len(lo) < 3:
            return None
        obs = float(hi.mean() - lo.mean())
        rng = np.random.default_rng(19900802)
        allm = np.concatenate([hi, lo]); nh = len(hi)
        # bootstrap CI (resample within each group)
        boot = [rng.choice(hi, nh).mean() - rng.choice(lo, len(lo)).mean() for _ in range(10000)]
        loci, hici = np.percentile(boot, [2.5, 97.5])
        # permutation p: shuffle the high/low labels
        cnt = sum(1 for _ in range(10000)
                  if (lambda p: p[:nh].mean() - p[nh:].mean())(rng.permutation(allm)) >= obs)
        return {"amp": round(obs, 4), "ci95": [round(float(loci), 4), round(float(hici), 4)],
                "perm_p": cnt / 10000, "ci_excludes_zero": bool(loci > 0 or hici < 0),
                "n_episodes": int(len(df))}

    yr = pd.to_datetime(ev["event_date"]).dt.year
    full = gate(frame(ev))
    regimes = {label: gate(frame(ev[~yr.isin(years)]))
               for years, label in zip(REGIME_YEARS, REGIME_LABELS)}
    return {"name": "severity_dose_response", "kind": "two_group_severity", "asset": "fred.DCOILBRENTEU",
            "sar_full": full, "sar_regime_block": regimes}


def _adjudicate(edge):
    full = edge.get("sar_full")
    regimes = edge.get("sar_regime_block", {})
    leg1_sar = full is not None                                   # SAR computed
    cuts = [full] + [regimes[k] for k in regimes]
    leg2 = leg1_sar and all(c is not None and c["ci_excludes_zero"] for c in cuts)
    edge["legs"] = {"1_sar_computed": bool(leg1_sar),
                    "2_regime_block_robust_ci_excludes_zero": bool(leg2)}
    return edge


def run():
    conn = sqlite3.connect(DB)
    edges = [_adjudicate(_state_split_edge(conn, *e)) for e in STATE_SPLIT_EDGES]
    edges.append(_adjudicate(_severity_edge(conn)))
    conn.close()

    # leg 3 -- permutation-FDR across the family, on the SAR full-corpus perm-p.
    named = [e for e in edges if e.get("sar_full")]
    pvals = [e["sar_full"]["perm_p"] for e in named]
    fdr = validate.bh_fdr(pvals, q=0.10) if pvals else {"survive": []}
    for e, surv in zip(named, fdr["survive"]):
        e["legs"]["3_survives_perm_fdr"] = bool(surv)
    for e in edges:
        if "3_survives_perm_fdr" not in e["legs"]:
            e["legs"]["3_survives_perm_fdr"] = False
        L = e["legs"]
        passes = L["1_sar_computed"] and L["2_regime_block_robust_ci_excludes_zero"] and L["3_survives_perm_fdr"]
        e["retier"] = "validated" if passes else "DOWNGRADE (SUGGESTIVE)"

    # Claims adjudicated elsewhere but folded into the one-bar table for completeness.
    external = {
        "CC2_supply_gasoline_crack": {"kind": "cross_chain_event", "retier": "DOWNGRADE (SUGGESTIVE)",
            "why": "R6: survives outlier-drop OR seasonal alone but not jointly (+1.16 [-0.22,2.56]).",
            "receipt": "data/cc2_seasonal.json"},
        "CC5_fertilizer_corn": {"kind": "monthly_passthrough", "retier": "SUGGESTIVE (bar leg-1 N/A)",
            "why": "Monthly cost pass-through beta has no event-study abnormal return, so SAR-"
                   "standardisation (leg 1) does not apply. Held as SUGGESTIVE under the one bar rather "
                   "than validated, since it cannot clear the SAR/regime-block legs by construction.",
            "receipt": "data/cross_chain.json"},
        "under_priced_risk_oos_MISPRICING": {"kind": "forecast_skill", "retier": "SUGGESTIVE (declared)",
            "why": "attack #15: previously reported OUTSIDE the FDR family. Under one honest bar it is a "
                   "small-N (~14), in-sample-direction forecast-skill test -- it is SUGGESTIVE, never "
                   "validated at this N, and its exclusion from the amplification FDR is a property of "
                   "being a different estimand (skill, not amplification), stated plainly -- not a shield.",
            "receipt": "EVALUATION.md, PRE_REGISTRATION.md"},
    }

    out = {
        "lens": "R7_one_evidentiary_bar",
        "attacks": [15, 16],
        "bar": "validated IFF (1) SAR-standardized effect AND (2) regime-block-robust 95% cluster-"
               "bootstrap CI excluding zero (full + drop 2008/2020/2026/all) AND (3) SAR permutation-p "
               "survives BH-FDR q=0.10 across the family.",
        "adjudicated": {e["name"]: {"kind": e["kind"], "legs": e["legs"], "retier": e["retier"],
                                    "sar_full": e.get("sar_full"),
                                    "sar_regime_block": e.get("sar_regime_block")} for e in edges},
        "adjudicated_elsewhere": external,
        "summary": {e["name"]: e["retier"] for e in edges} | {k: v["retier"] for k, v in external.items()},
        "corpus_note": "additive lens; frozen registered record untouched.",
    }
    JSON.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps(r["summary"], indent=2))
    print("\nLEGS:")
    for name, e in r["adjudicated"].items():
        print(f"  {name:20} legs={e['legs']}  -> {e['retier']}")
