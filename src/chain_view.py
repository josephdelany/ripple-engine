"""
chain_view.py -- the value chain measured hop by hop (VISION_ROADMAP V1.2/V1.3).

The cross-asset map (cross_asset.py) asks "how does each asset react to a geopolitical EVENT?".
This asks a different, complementary question: "how does a move in one node of the value chain pass
THROUGH to the next node?" -- crude -> refined products -> petrochemicals/fertilizer -> food. That is
the transmission an analyst reasons along ("crude spiked, so diesel, then freight, then food...").

For each HOP (upstream -> downstream) it measures, on the hop's OWN cadence (never mixing daily and
monthly silently):
  * pass-through beta -- OLS slope of the downstream log-return on the upstream log-return at the
    best lag (elasticity: a 1% upstream move maps to ~beta% downstream);
  * lag -- the lag (in the cadence's units: DAYS for daily hops, MONTHS for monthly) that maximises
    the return correlation (how long the ripple takes to arrive);
  * corr + a descriptive strength label at that lag;
  * n -- overlapping observations, and the cadence, on every cell.

STRICTLY DESCRIPTIVE. These are co-movements, not causal proofs, and the lag is the best-fitting
descriptive lag, not a tested claim. Anything CONFIRMATORY (a directional hypothesis with a decision
rule) requires a REGISTERED amendment filed BEFORE results, ded2419-style (Joe's gate). Nothing here
does that. numpy/pandas only; free/local.

Writes data/chain_report.txt (human) and data/chain_view.json (for surfaces later).
Run:  python3 src/chain_view.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
TXT = ROOT / "data" / "chain_report.txt"
JSON = ROOT / "data" / "chain_view.json"

MIN_N_DAILY = 250      # ~1y of overlapping trading days before a beta means anything
MIN_N_MONTHLY = 36     # ~3y of months
MAXLAG_DAILY = 10      # scan 0..10 trading days
MAXLAG_MONTHLY = 3     # scan 0..3 months

# Node labels for the report (series_id -> short name)
NODE = {
    "fred.DCOILWTICO": "WTI crude", "fred.DCOILBRENTEU": "Brent crude", "fred.DHHNGSP": "HH natgas",
    "fred.DGASUSGULF": "Gasoline (Gulf)", "fred.DHOILNYH": "Diesel/heat-oil", "fred.DPROPANEMBTX": "Propane",
    "yf.ttf": "TTF (EU gas)", "yf.jkm": "JKM (Asia LNG)",
    "fred.PCU325211325211": "Petchem PPI", "fred.PCU325311325311": "Fertilizer PPI",
    "yf.wheat": "Wheat", "yf.corn": "Corn",
}

# The chain, tier by tier. Each hop: (upstream, downstream, cadence).
HOPS = [
    # Tier 1 -- crude -> refined products (daily)
    ("fred.DCOILWTICO", "fred.DGASUSGULF",   "daily"),
    ("fred.DCOILWTICO", "fred.DHOILNYH",     "daily"),
    ("fred.DCOILWTICO", "fred.DPROPANEMBTX", "daily"),
    # Tier 1' -- the gas complex (daily): does US gas / crude lead the EU + Asian hubs?
    ("fred.DHHNGSP",    "yf.ttf",            "daily"),
    ("fred.DHHNGSP",    "yf.jkm",            "daily"),
    ("fred.DCOILWTICO", "yf.jkm",            "daily"),   # oil-indexed LNG contracts
    # Tier 2 -- feedstock -> petrochemicals / fertilizer (MONTHLY: PPIs are monthly)
    ("fred.DCOILWTICO", "fred.PCU325211325211", "monthly"),   # crude -> resins
    ("fred.DHHNGSP",    "fred.PCU325211325211", "monthly"),   # gas  -> ethylene -> resins
    ("fred.DHHNGSP",    "fred.PCU325311325311", "monthly"),   # gas  -> ammonia  -> N-fertilizer
    ("fred.DCOILWTICO", "fred.PCU325311325311", "monthly"),
    # Tier 3 -- fertilizer -> food (MONTHLY)
    ("fred.PCU325311325311", "yf.wheat", "monthly"),
    ("fred.PCU325311325311", "yf.corn",  "monthly"),
]

TIERS = [
    ("Tier 1  crude -> refined products", HOPS[0:3]),
    ("Tier 1' the gas complex",           HOPS[3:6]),
    ("Tier 2  feedstock -> petchem/fertilizer", HOPS[6:10]),
    ("Tier 3  fertilizer -> food",        HOPS[10:12]),
]


def _levels(conn, sid):
    df = pd.read_sql("SELECT obs_date, value FROM observations WHERE series_id=? ORDER BY obs_date",
                     conn, params=[sid])
    if df.empty:
        return None
    s = pd.Series(df["value"].to_numpy(float),
                  index=pd.to_datetime(df["obs_date"])).sort_index().dropna()
    return s[~s.index.duplicated(keep="last")]


def _returns(levels, cadence):
    """Log returns on the hop's cadence. Monthly = month-end last value then diff (never a daily
    series silently treated as monthly)."""
    s = levels.resample("ME").last().dropna() if cadence == "monthly" else levels
    s = s[s > 0]                        # log-returns need positive levels (also drops resample gaps)
    return np.log(s).diff().dropna()


def _strength(corr):
    a = abs(corr)
    return ("strong" if a >= 0.5 else "moderate" if a >= 0.3 else
            "weak" if a >= 0.15 else "negligible")


def passthrough(up_ret, down_ret, cadence):
    """Best-lag pass-through: scan lags, keep the one with the largest |correlation|. Returns
    {lag, beta, corr, n, strength} or None if never enough overlap."""
    maxlag = MAXLAG_MONTHLY if cadence == "monthly" else MAXLAG_DAILY
    min_n = MIN_N_MONTHLY if cadence == "monthly" else MIN_N_DAILY
    best = None
    for lag in range(0, maxlag + 1):
        pair = pd.concat([up_ret.shift(lag), down_ret], axis=1, join="inner").dropna()
        if len(pair) < min_n:
            continue
        x = pair.iloc[:, 0].to_numpy(); y = pair.iloc[:, 1].to_numpy()
        if x.std() == 0 or y.std() == 0:
            continue
        corr = float(np.corrcoef(x, y)[0, 1])
        beta = float(np.polyfit(x, y, 1)[0])
        if best is None or abs(corr) > abs(best["corr"]):
            best = {"lag": lag, "beta": round(beta, 3), "corr": round(corr, 3),
                    "n": int(len(pair)), "strength": _strength(corr)}
    return best


def run():
    conn = sqlite3.connect(DB)
    levels = {sid: _levels(conn, sid) for sid in NODE}
    conn.close()

    results = []
    for up, down, cadence in HOPS:
        cell = {"up": up, "up_label": NODE[up], "down": down, "down_label": NODE[down],
                "cadence": cadence, "result": None}
        lu, ld = levels.get(up), levels.get(down)
        if lu is not None and ld is not None:
            cell["result"] = passthrough(_returns(lu, cadence), _returns(ld, cadence), cadence)
        results.append(cell)
    return results


def _fmt(cell):
    lagunit = "mo" if cell["cadence"] == "monthly" else "d"
    r = cell["result"]
    left = f"{cell['up_label']:>15} -> {cell['down_label']:<16}"
    if r is None:
        return f"  {left} {cell['cadence']:<8} {'insufficient overlap':<38}"
    return (f"  {left} {cell['cadence']:<8} n={r['n']:>5}  lag={r['lag']:>2}{lagunit}  "
            f"beta={r['beta']:>+6.3f}  corr={r['corr']:>+6.3f}  {r['strength']}")


def write_report(results):
    L = []
    w = L.append
    w("=" * 96)
    w("VALUE-CHAIN CHAIN VIEW -- pass-through hop by hop (DESCRIPTIVE, no causal claim, no verdict)")
    w("=" * 96)
    w("Question: how does a move in one node pass THROUGH to the next -- crude -> products ->")
    w("petchem/fertilizer -> food? Each hop measured on its OWN cadence (daily vs monthly, never mixed).")
    w("  beta = OLS slope of downstream log-return on upstream log-return at the best lag (elasticity).")
    w("  lag  = the lag maximising return correlation (DAYS for daily hops, MONTHS for monthly).")
    w("  corr = correlation at that lag; strength is a descriptive band (|corr|>=.5 strong, >=.3")
    w("         moderate, >=.15 weak, else negligible). n + cadence shown on every cell.")
    w("CAUTION: co-movement, not causation; the lag is the best-FITTING descriptive lag, not a tested")
    w("claim. A CONFIRMATORY hop-transmission claim needs a REGISTERED amendment BEFORE results.")
    w("")
    for title, hops in TIERS:
        w(title)
        w("  " + "-" * 92)
        by_key = {(c["up"], c["down"]): c for c in results}
        for up, down, cadence in hops:
            w(_fmt(by_key[(up, down)]))
        w("")
    # honest roll-up: which hops read as real transmission (descriptive), which don't
    strong = [f"{c['up_label']}->{c['down_label']}" for c in results
              if c["result"] and c["result"]["strength"] in ("strong", "moderate")]
    weak = [f"{c['up_label']}->{c['down_label']}" for c in results
            if c["result"] and c["result"]["strength"] in ("weak", "negligible")]
    na = [f"{c['up_label']}->{c['down_label']}" for c in results if c["result"] is None]
    w("READ (descriptive):")
    w(f"  material co-movement (strong/moderate): {', '.join(strong) or 'none'}")
    w(f"  weak/negligible: {', '.join(weak) or 'none'}")
    if na:
        w(f"  insufficient overlap (honest n/a): {', '.join(na)}")
    w("")
    w("Confirmatory transmission claims require a registered amendment (Joe's gate). This is a map,")
    w("not a verdict.")
    TXT.write_text("\n".join(L) + "\n")
    return "\n".join(L)


def main():
    results = run()
    text = write_report(results)
    JSON.write_text(json.dumps({"what": "value-chain hop-by-hop pass-through (descriptive)",
                                "hops": results}, indent=2))
    print(text)
    print(f"\nWrote {TXT} and {JSON}")


if __name__ == "__main__":
    main()
