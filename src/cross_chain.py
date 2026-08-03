"""
cross_chain.py -- THE PRE-REGISTERED CROSS-CHAIN BATTERY (VISION_ROADMAP V3).

V1 built the value chain (crude -> products -> petchem/fertilizer -> food) and measured it descriptively
(chain_view.py). This asks the CONFIRMATORY question, under the same discipline as edge_battery.py: do
specific cross-chain transmissions hold when tested with a decision rule fixed in advance and corrected
across the family? Most may be null -- that is the point; the honest scorecard is the product.

THE DOCSTRING + THE HYPOTHESES TUPLE BELOW ARE THE PRE-REGISTRATION. Directions and rules are declared
HERE, in code, BEFORE the result is seen (git history proves this file predates data/cross_chain.json;
see also the PRE_REGISTRATION.md amendment 2026-08-03). $0 / keyless / point-in-time throughout.

=========================== THE REGISTERED FAMILY (frozen, directions fixed) ===========================
Event-driven (constant-mean SIGNED event study around the event; node's own trading-day index):
  CC1 supply -> diesel crack WIDENS   -- physical supply-shock events (chokepoint_disruption U
        infrastructure_attack) push the distillate crack UP over +10 trading days (product tightens
        faster than crude). Predicted sign: +. Unit: $/bbl (CAR of the crack's daily change).
  CC2 supply -> gasoline crack WIDENS -- same events, gasoline crack up +10d. Predicted sign: +.
  CC3 sanctions -> copper DOWN        -- trade-friction/sanctions events are growth-negative for the
        industrial metal; copper CAR+20 < 0. Predicted sign: - (log-return %).
Node-to-node pass-through (monthly log-returns; fertilizer is a monthly PPI):
  CC4 fertilizer -> wheat             -- fertilizer-cost pass-through lifts wheat; monthly beta > 0.
  CC5 fertilizer -> corn              -- monthly beta > 0.

DECISION RULE (fixed): an edge is VALIDATED iff its 95% bootstrap CI excludes zero IN THE PREDICTED
DIRECTION *and* it survives the family-wise BH-FDR (q=0.10). Bonferroni (alpha=0.05) reported alongside,
stricter. Raw (uncorrected) perm-p is ALWAYS reported next to the corrected verdict -- breadth never
manufactures a discovery. A PLACEBO (shuffled event dates / shuffled pairing) must send the family null.

Run:  python3 src/cross_chain.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns
from robustness import assign_clusters
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "cross_chain.json"
TXT = ROOT / "data" / "cross_chain_results.txt"
SEED = 19900802
PRE, POST_D = 5, 10          # event window for the crack tests (+10 trading days)
POST_COPPER = 20
FDR_Q = 0.10

SUPPLY_TYPES = ("chokepoint_disruption", "infrastructure_attack")

# (id, kind, spec...) -- kind drives the test. Directions are fixed above.
HYPOTHESES = [
    {"id": "CC1_supply_diesel_crack", "kind": "event", "series": "derived.diesel_crack",
     "unit": "$/bbl", "ret": "diff", "types": SUPPLY_TYPES, "post": POST_D, "sign": +1},
    {"id": "CC2_supply_gasoline_crack", "kind": "event", "series": "derived.gasoline_crack",
     "unit": "$/bbl", "ret": "diff", "types": SUPPLY_TYPES, "post": POST_D, "sign": +1},
    {"id": "CC3_sanctions_copper", "kind": "event", "series": "yf.copper",
     "unit": "%", "ret": "logret", "types": ("sanctions",), "post": POST_COPPER, "sign": -1},
    {"id": "CC4_fertilizer_wheat", "kind": "passthrough", "up": "fred.PCU325311325311",
     "down": "yf.wheat", "sign": +1},
    {"id": "CC5_fertilizer_corn", "kind": "passthrough", "up": "fred.PCU325311325311",
     "down": "yf.corn", "sign": +1},
]


def _value_returns(conn, series, how):
    """Node 'return' on its OWN observation index: 'diff' (level change, for a spread/margin) or
    'logret' (for a price). Returned as a date-indexed Series."""
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                     "GROUP BY obs_date ORDER BY obs_date", conn, params=[series])
    s = pd.Series(df["value"].to_numpy(float), index=pd.to_datetime(df["obs_date"])).sort_index()
    return (np.log(s[s > 0]).diff() if how == "logret" else s.diff()).dropna()


def _signed_car(ret, event_date, post, est=120, gap=11):
    """Signed constant-mean CAR at +post for one event, on the node's own trading-day index."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(str(event_date)))
    if pos >= len(dates) or pos - (est + gap) < 0 or pos + post >= len(dates):
        return None
    mu = ret.iloc[pos - est - gap: pos - gap].mean()
    car = (ret.iloc[pos - PRE: pos + post + 1] - mu).cumsum().to_numpy()
    return float(car[PRE + post])


def _one_sample(vals, sign, n_iter=10000, seed=SEED):
    """Directional one-sample test: is the mean in the predicted `sign` direction? Sign-flip
    permutation p (H0: symmetric about 0) + bootstrap CI on the mean. Unit = the input's unit."""
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if len(v) < 6:
        return {"ok": False, "reason": f"too few episodes (n={len(v)})", "n": int(len(v))}
    obs = sign * v.mean()
    rng = np.random.default_rng(seed)
    flips = rng.choice([-1, 1], size=(n_iter, len(v)))
    perm = sign * (flips * v).mean(axis=1)
    perm_p = float((perm >= obs).mean())
    boot = sign * v[rng.integers(0, len(v), (n_iter, len(v)))].mean(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"ok": True, "amp": round(float(v.mean()), 4), "signed_amp": round(float(obs), 4),
            "ci": [round(float(lo), 4), round(float(hi), 4)],
            "ci_excludes_zero_in_dir": bool(lo > 0), "perm_p": round(perm_p, 4), "n": int(len(v))}


def _event_test(conn, h, events, shuffle_dates=None):
    ret = _value_returns(conn, h["series"], h["ret"])
    ev = events[events["type"].isin(h["types"])].copy()
    if shuffle_dates is not None:                         # placebo: fake dates, no episode receipts
        src = [{"event_id": None, "date": d, "source_url": ""} for d in shuffle_dates]
    else:
        src = [{"event_id": r.event_id, "date": r.event_date, "source_url": r.source_url}
               for r in ev.itertuples()]
    rows = []
    for s in src:
        c = _signed_car(ret, s["date"], h["post"])
        if c is not None:
            rows.append({"event_id": s["event_id"], "date": pd.Timestamp(str(s["date"])),
                         "source_url": s["source_url"], "car": c})
    if len(rows) < 6:
        return {"id": h["id"], "ok": False, "reason": f"too few episodes ({len(rows)})", "n": len(rows)}
    df = assign_clusters(pd.DataFrame(rows)).groupby("cluster").first().reset_index()
    r = _one_sample(df["car"].to_numpy(float), h["sign"])
    r["id"] = h["id"]; r["unit"] = h["unit"]; r["predicted_sign"] = "+" if h["sign"] > 0 else "-"
    # per-episode receipts (real run only) so the evidence pack can re-derive n and trace sources
    r["episodes"] = ([] if shuffle_dates is not None else
                     [{"event_id": e.event_id, "date": str(e.date.date()),
                       "source_url": e.source_url or "", "car": round(float(e.car), 4)}
                      for e in df.itertuples()])
    return r


def _passthrough_test(conn, h, n_iter=10000, seed=SEED):
    # monthly log-returns for both (fertilizer PPI is monthly; food resampled to month-end)
    def monthly(series):
        df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                         "GROUP BY obs_date ORDER BY obs_date", conn, params=[series])
        s = pd.Series(df["value"].to_numpy(float), index=pd.to_datetime(df["obs_date"])).sort_index()
        s = s.resample("ME").last().dropna()
        return np.log(s[s > 0]).diff().dropna()
    u, d = monthly(h["up"]), monthly(h["down"])
    pair = pd.concat([u, d], axis=1, join="inner").dropna()
    if len(pair) < 24:
        return {"id": h["id"], "ok": False, "reason": f"too few months ({len(pair)})", "n": len(pair)}
    x, y = pair.iloc[:, 0].to_numpy(), pair.iloc[:, 1].to_numpy()
    beta = float(np.polyfit(x, y, 1)[0])
    rng = np.random.default_rng(seed)
    perm = np.array([np.polyfit(x, rng.permutation(y), 1)[0] for _ in range(n_iter)])
    perm_p = float((h["sign"] * perm >= h["sign"] * beta).mean())
    boot = np.array([np.polyfit(*(lambda i: (x[i], y[i]))(rng.integers(0, len(x), len(x))), 1)[0]
                     for _ in range(2000)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"id": h["id"], "ok": True, "amp": round(beta, 4), "signed_amp": round(h["sign"] * beta, 4),
            "ci": [round(float(lo), 4), round(float(hi), 4)], "ci_excludes_zero_in_dir": bool(lo > 0),
            "perm_p": round(perm_p, 4), "n": int(len(pair)), "unit": "beta", "predicted_sign": "+"}


def run():
    conn = sqlite3.connect(DB)
    events = pd.read_sql("SELECT event_id, event_date, type, source_url FROM events ORDER BY event_date", conn)
    results = []
    for h in HYPOTHESES:
        results.append(_event_test(conn, h, events) if h["kind"] == "event"
                       else _passthrough_test(conn, h))
    # family-wise FDR + Bonferroni over the tests that ran
    ran = [r for r in results if r.get("ok")]
    pvals = [r["perm_p"] for r in ran]
    fdr = validate.bh_fdr(pvals, q=FDR_Q) if pvals else {"survive": [], "qvalues": []}
    m = len(pvals)
    for r, surv, q in zip(ran, fdr["survive"], fdr["qvalues"]):
        r["survives_fdr"] = bool(surv); r["fdr_q"] = round(float(q), 4)
        r["survives_bonferroni"] = bool(r["perm_p"] <= 0.05 / m) if m else False
        r["validated"] = bool(r["ci_excludes_zero_in_dir"] and surv)

    # PLACEBO: shuffle each event hypothesis's dates within the price window -> family must go null
    rng = np.random.default_rng(SEED)
    all_dates = events["event_date"].tolist()
    placebo_val = 0
    for h in [h for h in HYPOTHESES if h["kind"] == "event"]:
        fake = list(rng.permutation(all_dates))[:sum(events["type"].isin(h["types"]))]
        pr = _event_test(conn, h, events, shuffle_dates=fake)
        if pr.get("ok") and pr["ci_excludes_zero_in_dir"] and pr["perm_p"] < 0.05:
            placebo_val += 1
    conn.close()

    report = {"what": "Pre-registered cross-chain battery (V3): directions fixed before results; "
                      "BH-FDR q=0.10 across the family; raw perm-p reported alongside.",
              "n_tested": m, "family_fdr_q": FDR_Q,
              "validated": [r["id"] for r in ran if r.get("validated")],
              "placebo_false_positives": placebo_val,
              "placebo_note": "shuffled event dates; a sound family yields ~0 placebo hits",
              "results": results}
    OUT.write_text(json.dumps(report, indent=2))
    return report


def _fmt(r):
    if not r.get("ok"):
        return f"  {r['id']:28} n/a ({r.get('reason')})"
    v = "VALIDATED" if r.get("validated") else "null"
    return (f"  {r['id']:28} amp={r['signed_amp']:+8.3f} {r['unit']:<6} "
            f"CI[{r['ci'][0]:+.3f},{r['ci'][1]:+.3f}] dir={r['predicted_sign']} "
            f"raw_p={r['perm_p']:.3f} FDR={'Y' if r.get('survives_fdr') else 'n'} "
            f"n={r['n']:>3}  {v}")


def main():
    r = run()
    L = ["=" * 92,
         "CROSS-CHAIN BATTERY (V3) -- confirmatory, directions pre-registered, FDR-corrected + raw",
         "=" * 92]
    for res in r["results"]:
        L.append(_fmt(res))
    L += ["",
          f"  validated (CI excludes 0 in predicted dir AND survives BH-FDR q={FDR_Q}): "
          f"{r['validated'] or 'none -- honest nulls'}",
          f"  placebo false-positives (shuffled dates): {r['placebo_false_positives']} "
          f"(a sound family -> ~0)",
          "  Raw perm-p shown next to every corrected verdict; nulls are results."]
    text = "\n".join(L)
    TXT.write_text(text + "\n")
    print(text)
    print(f"\n  Wrote {OUT} and {TXT}")


if __name__ == "__main__":
    main()
