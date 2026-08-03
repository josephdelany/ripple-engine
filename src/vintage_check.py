"""
vintage_check.py -- does any headline number depend on REVISED history? (VISION_ROADMAP V-Q1)

Reproducibility standard (AER data editor): a finding must not change when you rebuild it against the
data as it was KNOWN at registration time, because revisions embed information nobody had then. The
intended check: re-fetch H1's inputs at their registration-time ALFRED vintage and recompute.

THIS RECEIPT IS HONEST ABOUT WHAT IS POSSIBLE HERE. It probes, live, whether a real point-in-time
vintage can be obtained, and reports the truth instead of faking a diff:

  1. ALFRED vintage probe -- ask ALFRED for a heavily-revised series (INDPRO) at an OLD vintage and
     check whether the response actually honors it. In this environment the endpoint returns only the
     CURRENT vintage (the response column is named for today's date), so a registration-time vintage
     cannot be pulled here. (Real ALFRED honors it; the simulated FRED mirror does not.)
  2. DB bitemporal depth -- check whether the observations table retained any prior `as_of` vintages
     for the headline inputs. It does not (as_of == obs_date on every row), so there is no internal
     snapshot to diff against either.
  3. Revision-class of the headline inputs -- the decisive point that stands regardless: H1's inputs
     are DAILY MARKET CLOSES (Brent/WTI spot, VIX), which are FINAL at publication and not
     retroactively revised (unlike GDP/payrolls/industrial production). A headline built only on
     non-revised series cannot depend on revised history BY CONSTRUCTION.

It writes data/vintage_check.txt (the receipt) and flags, honestly, that fetch_fred_alfred.py's
`as_of` labels are not true vintages in this environment (it is NOT in the refresh cycle and its
demo series have 0 rows in the live DB, so it does not contaminate any headline today).

Run:  python3 src/vintage_check.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "vintage_check.txt"
ALFRED = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={sid}&vintage_dates={v}"

# Headline claims and the priced inputs they depend on, with each input's revision class.
# 'market-close' = final at publication, not revised. 'revised-macro' = subject to revisions.
HEADLINE_INPUTS = {
    "H1 (+5.0pp VIX-stress amplification of the Brent ripple)": [
        ("fred.DCOILBRENTEU", "Brent spot", "market-close"),
        ("fred.DCOILWTICO",   "WTI spot",   "market-close"),
        ("fred.VIXCLS",       "VIX",        "market-close"),
    ],
}
OLD_VINTAGE = "2020-06-15"     # a date long before now; if honored, a revised series shows old values


def alfred_probe(sid=" INDPRO".strip(), vintage=OLD_VINTAGE):
    """Return (honored: bool|None, detail). honored=True if the response's vintage column is dated at
    the REQUESTED vintage; False if it returns a different (current) vintage; None if the probe failed."""
    try:
        r = requests.get(ALFRED.format(sid=sid, v=vintage), timeout=30)
        r.raise_for_status()
        header = r.text.splitlines()[0]
        col = header.split(",")[-1].strip()           # e.g. INDPRO_20260803
        stamp = col.split("_")[-1]                     # 20260803
        req = vintage.replace("-", "")                 # 20200615
        honored = (stamp == req)
        return honored, f"requested vintage {vintage} -> response column '{col}' (vintage {stamp})"
    except Exception as e:
        return None, f"probe failed: {type(e).__name__}: {e}"


def db_vintage_depth(conn, sid):
    """(n_rows, n_multi_asof) -- how many obs_dates carry >1 as_of (a true stored vintage)."""
    n = conn.execute("SELECT COUNT(*) FROM observations WHERE series_id=?", (sid,)).fetchone()[0]
    multi = conn.execute(
        "SELECT COUNT(*) FROM (SELECT obs_date FROM observations WHERE series_id=? "
        "GROUP BY obs_date HAVING COUNT(DISTINCT as_of) > 1)", (sid,)).fetchone()[0]
    return n, multi


def run():
    conn = sqlite3.connect(DB)
    honored, probe_detail = alfred_probe()
    inputs = []
    for claim, series in HEADLINE_INPUTS.items():
        for sid, label, cls in series:
            n, multi = db_vintage_depth(conn, sid)
            inputs.append({"claim": claim, "series": sid, "label": label, "class": cls,
                           "rows": n, "multi_asof": multi})
    conn.close()
    all_market_close = all(i["class"] == "market-close" for i in inputs)
    any_internal_vintage = any(i["multi_asof"] > 0 for i in inputs)
    return {"probe_honored": honored, "probe_detail": probe_detail, "inputs": inputs,
            "all_market_close": all_market_close, "any_internal_vintage": any_internal_vintage}


def write_receipt(r):
    L = []
    w = L.append
    w("=" * 92)
    w("VINTAGE CHECK -- does any headline number depend on REVISED history? (V-Q1)")
    w(f"generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    w("=" * 92)
    w("")
    w("1. CAN A REGISTRATION-TIME VINTAGE BE OBTAINED HERE?")
    if r["probe_honored"] is True:
        w("   ALFRED probe: HONORED -- real point-in-time vintages are available. Empirical diff CAN")
        w("   be run; extend this receipt to recompute headlines on the registration vintage.")
    elif r["probe_honored"] is False:
        w("   ALFRED probe: NOT honored -- the endpoint returns only the CURRENT vintage.")
        w(f"     {r['probe_detail']}")
        w("   -> a registration-time vintage CANNOT be pulled in this environment (simulated FRED")
        w("      mirror does not implement ALFRED vintages; real ALFRED does).")
    else:
        w(f"   ALFRED probe: unavailable ({r['probe_detail']}).")
    w("")
    w("2. DID THE DB RETAIN ANY PRIOR VINTAGES (bitemporal as_of)?")
    for i in r["inputs"]:
        w(f"   {i['series']:20} rows={i['rows']:>6}  obs_dates with >1 as_of: {i['multi_asof']}")
    w("   -> " + ("some inputs carry stored vintages -- an internal diff is possible."
                  if r["any_internal_vintage"] else
                  "as_of == obs_date on every row; NO prior vintage is stored to diff against."))
    w("")
    w("3. REVISION CLASS OF THE HEADLINE INPUTS (the decisive point):")
    for claim in {i["claim"] for i in r["inputs"]}:
        w(f"   {claim}")
        for i in [x for x in r["inputs"] if x["claim"] == claim]:
            w(f"     - {i['label']:12} ({i['series']}): {i['class']}")
    w("")
    if r["all_market_close"]:
        w("   VERDICT: every headline input above is a DAILY MARKET CLOSE (spot price / index close).")
        w("   Such series are FINAL at publication and are NOT retroactively revised (unlike GDP,")
        w("   payrolls, industrial production). Therefore the headline CANNOT depend on revised")
        w("   history BY CONSTRUCTION -- the revised-history attack does not apply to it.")
    else:
        w("   NOTE: a headline input is a revision-prone macro series -- an empirical vintage diff is")
        w("   needed (and, per section 1, must wait for real ALFRED here).")
    w("")
    w("HONEST LIMITATION + FLAG:")
    w("  * This receipt does NOT fake an empirical vintage diff by comparing today's data to itself.")
    w("    Where a real vintage is unobtainable here, the argument is from the input series' revision")
    w("    class, which is stated plainly above.")
    w("  * fetch_fred_alfred.py stores each requested vintage under its own as_of, but in this")
    w("    environment the endpoint returns TODAY's data for any requested date -- so those as_of")
    w("    labels would be current data mislabeled as old vintages. It is NOT in the refresh cycle and")
    w("    its demo series (INDPRO/PAYEMS) have 0 rows in the live DB, so it does not contaminate any")
    w("    headline today. Do not trust it for point-in-time work here without a fix.")
    w("")
    w("Frozen quarterly DB snapshots (src/db_snapshot.py) preserve today's DB so a future rebuild can")
    w("be diffed against this quarter -- the reproducibility half of V-Q1 that IS fully available here.")
    OUT.write_text("\n".join(L) + "\n")
    return "\n".join(L)


def main():
    r = run()
    text = write_receipt(r)
    print(text)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
