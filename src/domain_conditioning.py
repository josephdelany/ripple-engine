"""
domain_conditioning.py -- give each commodity a FAIR, APT, PRE-DECLARED test (Whole-3).

copper/silver/wheat came up null under GENERIC VIX-stress conditioning -- but stress may be the wrong
conditioner. Rather than re-run the same test until it "passes" (p-hacking), we PRE-DECLARE, right
here, one apt hypothesis per commodity against its economically natural driver, then run each through
the SAME gate (cluster-bootstrap CI + permutation) with a BH-FDR correction across the declared set.
Validated or null -- reported either way.

PRE-DECLARED HYPOTHESES (mechanism stated before the test; this docstring is the pre-registration):
  1. GOLD is a safe haven      -> a shock amplifies its ripple when VIX stress is elevated (high).
  2. SILVER is precious+industrial -> same stress channel as gold (high VIX).
  3. COPPER is a growth metal   -> amplifies in a growth-supportive regime, proxied by a STEEP curve
                                   (derived.curve_2s10s high = growth-on), not by risk-off stress.
  4. PALLADIUM is supply-concentrated (Russia/SA) -> stress channel (high VIX).
  (WHEAT is deliberately NOT included: it is supply/weather-driven with no clean market-STATE proxy in
   this engine -- an honest 'not testable here', not a null to force.)

Reuses research.run_test (the bench gate) + validate.bh_fdr. numpy-only; point-in-time.

Run:  python3 src/domain_conditioning.py
"""

import json
import sqlite3
from pathlib import Path

import research
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "domain_conditioning.json"

HYPOTHESES = [
    ("gold_safe_haven",   "derived.vix_pct",      "yf.gold",      "high",
     "gold is a safe haven -> a shock ripples harder when VIX stress is elevated"),
    ("silver_precious",   "derived.vix_pct",      "yf.silver",    "high",
     "silver (precious+industrial) shares gold's stress channel"),
    ("copper_growth",     "derived.curve_2s10s",  "yf.copper",    "high",
     "copper is a growth metal -> amplifies in a growth-on regime (steep 2s10s curve)"),
    ("palladium_supply",  "derived.vix_pct",      "yf.palladium", "high",
     "palladium is supply-concentrated (Russia/SA) -> stress channel"),
]


def run():
    conn = sqlite3.connect(DB)
    results = []
    for name, state, asset, sign, mech in HYPOTHESES:
        r = research.run_test(conn, state, asset, sign, 20)
        results.append({"hypothesis": name, "state": state, "asset": asset, "sign": sign,
                        "mechanism": mech, **({"n": r["n"], "amp": r["amp"], "ci": r["ci"],
                        "ci_excludes_zero": r["ci_excludes_zero"], "perm_p": r["perm_p"]}
                        if r.get("ok") else {"error": r.get("reason")})})
    conn.close()
    # FDR across the pre-declared set (correct for testing 4 apt hypotheses)
    testable = [r for r in results if "perm_p" in r and r["perm_p"] is not None]
    fdr = validate.bh_fdr([r["perm_p"] for r in testable], q=0.10)
    for r, surv, q in zip(testable, fdr["survive"], fdr["qvalues"]):
        r["fdr_q"] = q
        r["validated"] = bool(r["ci_excludes_zero"] and r["amp"] and r["amp"] > 0 and surv)
    for r in results:
        r.setdefault("validated", False)
    val = [r["hypothesis"] for r in results if r.get("validated")]
    report = {"what": "Pre-declared, apt, FDR-corrected conditioning: each commodity vs its natural "
                      "driver (not generic VIX-stress). Pre-registration is the module docstring.",
              "n_hypotheses": len(results), "validated": val, "results": results,
              "note": "wheat excluded on purpose (supply/weather-driven; no clean market-state proxy)."}
    OUT.write_text(json.dumps(report, indent=2, default=str))
    return report


def main():
    r = run()
    print("=" * 80)
    print("DOMAIN-APT CONDITIONING -- each commodity vs its natural driver (pre-declared, FDR)")
    print("=" * 80)
    for x in r["results"]:
        if "amp" not in x:
            print(f"  {x['hypothesis']:<20} -- {x.get('error','n/a')}"); continue
        ci = x["ci"]
        tag = "VALIDATED" if x.get("validated") else "null"
        print(f"  {x['hypothesis']:<20} {x['asset']:<12} via {x['state'].split('.')[-1]:<12} "
              f"amp {x['amp']:+.1f}% CI[{ci[0]:+.1f},{ci[1]:+.1f}] perm_p={x['perm_p']} [{tag}]")
    print(f"\n  validated (apt, FDR-corrected): {r['validated'] or 'none'}")
    print(f"  {r['note']}")


if __name__ == "__main__":
    main()
