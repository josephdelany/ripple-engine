"""
fetch_breakevens.py -- the FISCAL-STRESS gap for oil producers (IMF breakevens vs live oil).

The genuinely useful find: the IMF's Regional Economic Outlook publishes a FISCAL BREAKEVEN
OIL PRICE per country (the Brent price a state needs to balance its budget), and FRED mirrors
it as a machine-readable annual series (e.g. SAUPZPIOILBEGUSD). So instead of a one-off
article number, we track a permanent GAP:

    fiscal_gap = live Brent - a country's breakeven
    negative = the state is running its oil economy UNDERWATER (fiscal stress).

This is a standing signal the engine can watch: Saudi at ~$91 breakeven with Brent in the
$80s is bleeding (deficits, dividend cuts, NEOM downsizing); UAE at ~$50 is comfortable --
which is the structural engine behind their OPEC split. Free: FRED fredgraph CSV, no key.

Run:  python3 src/fetch_breakevens.py
"""

import csv
import io
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
MARKET = ROOT / "data" / "market_live.json"
OUT = ROOT / "data" / "breakevens.json"
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

# country slug -> IMF fiscal-breakeven FRED series (ISO3 + PZPIOILBEGUSD). Missing ones skip.
PRODUCERS = {
    "saudi_arabia": "SAUPZPIOILBEGUSD", "uae": "AREPZPIOILBEGUSD",
    "iraq": "IRQPZPIOILBEGUSD", "kuwait": "KWTPZPIOILBEGUSD",
    "iran": "IRNPZPIOILBEGUSD", "algeria": "DZAPZPIOILBEGUSD",
    "qatar": "QATPZPIOILBEGUSD", "oman": "OMNPZPIOILBEGUSD",
    "bahrain": "BHRPZPIOILBEGUSD", "kazakhstan": "KAZPZPIOILBEGUSD",
}


def _fetch_csv(url):
    """FRED fredgraph CSV, robustly: requests first (works in CI), curl fallback (works when
    the python client is throttled/slow, as it is intermittently). Empty string on failure."""
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0 (ripple-engine)"})
        if r.ok and r.text:
            return r.text
    except requests.RequestException:
        pass
    try:
        import subprocess
        return subprocess.run(["curl", "-s", "--max-time", "25", url],
                              capture_output=True, text=True, timeout=35).stdout
    except Exception:
        return ""


def latest_breakeven(sid):
    """(value, year) of the most recent IMF fiscal breakeven for a series, or (None, None).
    Rejects implausible/garbled values (e.g. a stray $1.00) so bad data never surfaces."""
    text = _fetch_csv(FRED_CSV.format(sid=sid))
    rows = [row for row in csv.reader(io.StringIO(text)) if len(row) == 2 and row[0] != "DATE"]
    vals = [(d, v) for d, v in rows if v not in ("", ".")]
    if not vals:
        return None, None
    d, v = vals[-1]
    try:
        val = round(float(v), 2)
    except ValueError:
        return None, None
    if not (15 <= val <= 250):                    # a real fiscal breakeven is never $1 or $500
        return None, None
    return val, d[:4]


def live_brent():
    if not MARKET.exists():
        return None
    a = (json.loads(MARKET.read_text()).get("assets") or {}).get("live.brent") or {}
    return a.get("price")


def stress_band(gap):
    """Typed fiscal-stress bucket from the breakeven gap (live oil - breakeven)."""
    if gap is None:
        return "n/a"
    if gap < -10:
        return "acute stress"
    if gap < 0:
        return "stress"
    if gap < 15:
        return "balanced"
    return "comfortable"


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    brent = live_brent()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    rows = []
    for slug, sid in PRODUCERS.items():
        be, year = latest_breakeven(sid)
        if be is None:
            continue
        gap = round(brent - be, 2) if brent is not None else None
        rows.append({"country": slug, "breakeven": be, "be_year": year,
                     "brent": brent, "gap": gap, "band": stress_band(gap), "source": sid})
        # store the breakeven as a tracked observation (point-in-time on its IMF year).
        obs_sid = f"imf.breakeven.{slug}"
        cur.execute("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (obs_sid, f"IMF fiscal breakeven oil price: {slug}", None, "USD/bbl",
                     "yearly", "IMF REO (via FRED)", FRED_CSV.format(sid=sid),
                     "Brent price the state needs to balance its budget"))
        cur.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)",
                    (obs_sid, f"{year}-01-01", be, f"{year}-01-01", now))
    conn.commit()
    conn.close()
    rows.sort(key=lambda r: (r["gap"] if r["gap"] is not None else 999))   # most-stressed first
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now, "brent": brent,
         "note": "Fiscal-stress gap = live Brent - IMF fiscal breakeven. Negative = the state "
                 "is running its oil economy underwater. Source IMF REO via FRED. Annual "
                 "breakeven vs live oil; DISPLAY/context.", "producers": rows}, indent=2))
    print(f"fetch_breakevens -- {len(rows)} producers vs Brent ${brent}:")
    for r in rows:
        g = f"{r['gap']:+.2f}" if r["gap"] is not None else "n/a"
        print(f"  {r['country']:<14} breakeven ${r['breakeven']:<7} gap {g:<8} {r['band']}")


if __name__ == "__main__":
    main()
