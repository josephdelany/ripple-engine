"""
fetch_firms.py -- NASA FIRMS satellite fire detection: the OVERHEAD/thermal modality.

When an oil facility is struck, a satellite sees the heat. NASA FIRMS publishes
near-real-time (~3 h) active-fire / thermal-anomaly detections (VIIRS), free with a
key. We watch a curated gazetteer of oil facilities + chokepoints and record daily
detections near each -- so a thermal spike at Abqaiq's coordinates can CONFIRM an
attack independent of any news report (cross-modal corroboration, the strongest kind).

THE FLARING CAVEAT (why this measures anomalies, not raw fires): major oil facilities
routinely FLARE gas, so FIRMS almost always shows fire there. A raw "fire near Abqaiq"
is meaningless. So we track daily detection COUNT and total FRP (fire radiative power)
per facility and flag an ANOMALY -- a jump well above the facility's own flaring
baseline. That requires history to accumulate; early runs just build the baseline.

KEY HANDLING: FIRMS_KEY from the environment (a free MAP_KEY, added as a repo Secret),
mirroring the EIA pattern -- never printed, never committed. If it is not set this
adapter is DORMANT: it prints a note and exits cleanly (0), so the pipeline never
fails for a missing optional key.

Get a free key: https://firms.modaps.eosdis.nasa.gov/api/map_key/

Run:  python3 src/fetch_firms.py
"""

import csv
import io
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "firms.json"
# VIIRS 375m near-real-time; area CSV route: /api/area/csv/KEY/SOURCE/BBOX/DAYS
API = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/VIIRS_SNPP_NRT/{bbox}/{days}"
UA = {"User-Agent": "ripple-engine/1.0 (research)"}

# Curated oil-infrastructure + chokepoint gazetteer: (name, slug, lat, lon).
FACILITIES = [
    ("Abqaiq (Aramco)", "abqaiq", 25.93, 49.67),
    ("Ras Tanura", "ras_tanura", 26.64, 50.16),
    ("Khurais", "khurais", 25.06, 48.15),
    ("Kharg Island (Iran)", "kharg", 29.25, 50.32),
    ("Ras Laffan (Qatar)", "ras_laffan", 25.90, 51.57),
    ("Jamnagar (India)", "jamnagar", 22.35, 69.85),
    ("Strait of Hormuz", "hormuz", 26.57, 56.25),
    ("Bab el-Mandeb", "bab_el_mandeb", 12.58, 43.33),
]
BOX = 0.15          # +/- degrees (~16 km) around each point
DAYS = 2            # look-back window
ELEVATED = 1.6     # today's FRP > 1.6x trailing median -> 'elevated' (above flaring)


def parse_firms_csv(text):
    """FIRMS area CSV -> list of detections (lat, lon, acq_date, confidence, frp).
    Pure (testable)."""
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            out.append({"lat": float(row["latitude"]), "lon": float(row["longitude"]),
                        "acq_date": row.get("acq_date", ""),
                        "confidence": (row.get("confidence") or "").strip(),
                        "frp": float(row.get("frp") or 0.0)})
        except (KeyError, ValueError):
            continue
    return out


def bbox(lat, lon):
    return f"{lon - BOX},{lat - BOX},{lon + BOX},{lat + BOX}"


def fetch_facility(key, lat, lon):
    try:
        r = requests.get(API.format(key=key, bbox=bbox(lat, lon), days=DAYS),
                         headers=UA, timeout=40)
        return parse_firms_csv(r.text) if r.ok and "," in r.text else []
    except requests.RequestException as e:
        print(f"  FIRMS fetch failed ({type(e).__name__}) -- skipped.")
        return []


def trailing_frp(conn, slug):
    """Prior daily total-FRP values for a facility (for the anomaly baseline)."""
    rows = conn.execute(
        "SELECT value FROM observations WHERE series_id=? ORDER BY obs_date DESC "
        "LIMIT 30", (f"firms.{slug}.frp",)).fetchall()
    return [r[0] for r in rows]


def main():
    key = os.environ.get("FIRMS_KEY")
    if not key:
        print("fetch_firms -- FIRMS_KEY not set; DORMANT (add the free key as a "
              "secret to activate the satellite-fire modality). Skipping cleanly.")
        return
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    today = now[:10]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    summary = []
    for name, slug, lat, lon in FACILITIES:
        dets = fetch_facility(key, lat, lon)
        n = len(dets)
        frp = round(sum(d["frp"] for d in dets), 1)
        base = trailing_frp(conn, slug)
        med = median(base) if base else None
        flag = "elevated" if (med and frp > ELEVATED * med and frp > 0) else "baseline"
        for field, val, sid in (("count", n, f"firms.{slug}.count"),
                                ("frp", frp, f"firms.{slug}.frp")):
            cur.execute("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)",
                        (sid, f"FIRMS {name} daily {field}", None,
                         "count" if field == "count" else "MW", "daily", "NASA FIRMS",
                         "https://firms.modaps.eosdis.nasa.gov",
                         "overhead/thermal signal; anomaly = above flaring baseline"))
            cur.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)",
                        (sid, today, float(val), today, now))
        summary.append({"facility": name, "slug": slug, "detections": n,
                        "frp": frp, "baseline_frp": round(med, 1) if med else None,
                        "flag": flag})
    conn.commit()
    conn.close()
    summary.sort(key=lambda s: (s["flag"] != "elevated", s["facility"]))
    OUT.write_text(__import__("json").dumps(
        {"as_of": today, "generated_at": now, "source": "NASA FIRMS VIIRS (free)",
         "note": "Daily thermal detections near oil facilities. Facilities FLARE, so "
                 "'baseline' is normal; 'elevated' = FRP well above the flaring norm "
                 "(possible strike). Needs history to build the baseline.",
         "facilities": summary}, indent=2))
    print(f"fetch_firms -- {len(summary)} facilities scanned.")
    for s in summary:
        print(f"  {s['flag']:>9}  {s['facility']:<22} dets={s['detections']} "
              f"frp={s['frp']} (base {s['baseline_frp']})")


if __name__ == "__main__":
    main()
