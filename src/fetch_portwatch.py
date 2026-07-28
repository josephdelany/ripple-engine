"""
fetch_portwatch.py -- IMF PortWatch chokepoint transits: the PHYSICAL-FLOW modality.

This is the ground-truth layer the news+odds stack lacked. IMF PortWatch publishes
daily AIS-derived ship-transit counts through the world's chokepoints -- free, no key.
We track the oil-relevant ones (Hormuz, Bab el-Mandeb, Suez) plus Cape of Good Hope
(the reroute-around-Africa tell). When tanker transits DROP at a chokepoint, that is
physical corroboration of a disruption -- far stronger than any headline alone, and a
new independent "vote" the corroboration brain can fuse (news says blockade AND the
ships actually stopped).

We store the daily tanker counts as observations and compute a simple anomaly (latest
vs trailing median) -> a 'reduced'/'normal'/'elevated' flag per chokepoint. Official
IMF data, daily, point-in-time; tagged as a physical-flow signal (not yet a registered
statistic -- it can be promoted to a variable once validated).

Run:  python3 src/fetch_portwatch.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "portwatch.json"
BASE = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/"
        "Daily_Chokepoints_Data/FeatureServer/0/query")
UA = {"User-Agent": "ripple-engine/1.0 (research)"}

# The oil-relevant chokepoints -> our slugs. Cape of Good Hope = the reroute tell.
CHOKEPOINTS = {
    "Strait of Hormuz": "hormuz",
    "Bab el-Mandeb Strait": "bab_el_mandeb",
    "Suez Canal": "suez",
    "Cape of Good Hope": "cape_of_good_hope",
}
LOOKBACK = 90          # days of history to pull per chokepoint
REDUCED = 0.60         # latest < 60% of trailing median -> 'reduced' (disruption)
ELEVATED = 1.40        # latest > 140% -> 'elevated' (surge / rerouting inflow)


def assess(values):
    """values = tanker counts NEWEST-first. Return latest vs trailing-median status.
    Pure (testable). Trailing median excludes the latest point."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    latest = vals[0]
    trailing = vals[1:] or vals
    med = median(trailing)
    pct = (latest / med) if med else None
    flag = "normal"
    if pct is not None:
        flag = "reduced" if pct < REDUCED else "elevated" if pct > ELEVATED else "normal"
    return {"latest": latest, "median": round(med, 1),
            "pct_of_median": round(pct, 2) if pct is not None else None, "flag": flag}


def fetch_chokepoint(name):
    """Recent daily rows for one chokepoint, newest-first, or [] on failure."""
    params = {"where": f"portname='{name}'", "outFields": "date,n_tanker,capacity_tanker",
              "orderByFields": "date DESC", "resultRecordCount": LOOKBACK, "f": "json"}
    try:
        r = requests.get(BASE, params=params, headers=UA, timeout=30)
        return [f["attributes"] for f in r.json().get("features", [])] if r.ok else []
    except (requests.RequestException, ValueError) as e:
        print(f"  PortWatch '{name}' failed ({type(e).__name__}) -- skipped.")
        return []


def _iso(ms_or_str):
    """PortWatch 'date' can be epoch-ms or a string; return YYYY-MM-DD."""
    if isinstance(ms_or_str, (int, float)):
        return datetime.fromtimestamp(ms_or_str / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    return str(ms_or_str)[:10]


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    summary = []
    for name, slug in CHOKEPOINTS.items():
        rows = fetch_chokepoint(name)
        if not rows:
            continue
        for r in rows:
            d = _iso(r.get("date"))
            for field, sid in (("n_tanker", f"portwatch.{slug}.n_tanker"),
                               ("capacity_tanker", f"portwatch.{slug}.capacity_tanker")):
                conn.execute(
                    "INSERT OR IGNORE INTO series (series_id, name, entity_id, unit, "
                    "frequency, source, source_url, notes) VALUES (?,?,?,?,?,?,?,?)",
                    (sid, f"{name} daily {field}", f"chokepoint.{slug}",
                     "count" if field == "n_tanker" else "dwt", "daily", "IMF PortWatch",
                     "https://portwatch.imf.org", "physical-flow signal"))
                v = r.get(field)
                if v is not None:
                    conn.execute("INSERT OR IGNORE INTO observations "
                                 "(series_id, obs_date, value, as_of, retrieved_at) "
                                 "VALUES (?,?,?,?,?)", (sid, d, float(v), d, now))
        st = assess([r.get("n_tanker") for r in rows])
        if st:
            summary.append({"chokepoint": name, "slug": slug,
                            "latest_date": _iso(rows[0].get("date")), **st})
    conn.commit()
    conn.close()
    summary.sort(key=lambda s: (s["flag"] != "reduced", s["chokepoint"]))
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now, "source": "IMF PortWatch (free)",
         "note": "Daily AIS-derived tanker transits; 'reduced' = latest below 60% of "
                 "trailing median (physical disruption signal). Data tail lags ~1 week.",
         "chokepoints": summary}, indent=2))
    print(f"fetch_portwatch -- {len(summary)} chokepoints assessed.")
    for s in summary:
        print(f"  {s['flag']:>8}  {s['chokepoint']:<22} tankers={s['latest']} "
              f"(median {s['median']}, {s['pct_of_median']}x) @ {s['latest_date']}")


if __name__ == "__main__":
    main()
