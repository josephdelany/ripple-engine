"""
fetch_ucdp.py -- verified conflict intensity from UCDP GED (the gold-standard fatality dataset).

UCDP's Georeferenced Event Dataset codes every organized-violence event (date, country, region,
best-fatality estimate, actors) from vetted sources. We aggregate it into monthly conflict-intensity
series -- global + per region -- so the engine has a VERIFIED conflict measure (far better than
GDELT media-tone), available as context / a future conditioner / a corroboration modality.

  * $0 but token-gated (like the EIA key). The token is read at runtime from the env var UCDP_TOKEN or
    ~/.openbb_platform/user_settings.json (credentials.ucdp_access_token) -- NEVER hardcoded/committed.
  * Rate-limit-safe: 5000 requests/day. We CACHE the raw pull (data/cache/, gitignored) and only re-hit
    the API when the cache is missing or --refresh is passed.
  * Point-in-time: aggregated by event date_start (the day it occurred). UCDP publishes with a lag, so
    the most recent months are incomplete -- flagged via the cadence override, not pretended fresh.

Run:  python3 src/fetch_ucdp.py                 # use cache if present, else pull, then aggregate + load
      python3 src/fetch_ucdp.py --refresh        # force a fresh API pull
      python3 src/fetch_ucdp.py --max-pages 20   # bounded pull (testing)
"""

import json
import os
import sqlite3
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CACHE = ROOT / "data" / "cache" / "ucdp_ged_26.1.json"
VERSION = "26.1"
API = f"https://ucdpapi.pcr.uu.se/api/gedevents/{VERSION}"
PAGESIZE = 1000
# region label -> our series id (UCDP 'region' values)
REGIONS = {"Middle East": "ucdp.fat_middle_east", "Africa": "ucdp.fat_africa",
           "Asia": "ucdp.fat_asia", "Europe": "ucdp.fat_europe", "Americas": "ucdp.fat_americas"}


def get_token():
    tok = os.environ.get("UCDP_TOKEN")
    if tok:
        return tok
    try:
        us = Path.home() / ".openbb_platform" / "user_settings.json"
        cred = json.loads(us.read_text()).get("credentials", {})
        return cred.get("ucdp_access_token") or cred.get("ucdp_token")
    except (OSError, ValueError):
        return None


def _get_page(url, token, tries=4):
    """One page, with retry/backoff -- the ~418-page pull must survive a transient read timeout."""
    last = None
    for attempt in range(tries):
        try:
            r = requests.get(url, headers={"x-ucdp-access-token": token}, timeout=90)
            r.raise_for_status()
            return r.json()
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            last = e
            time.sleep(2.0 * (2 ** attempt))
    raise last


def pull(token, max_pages=None):
    """Follow NextPageUrl, collecting a slim projection of each event. Returns list of dicts."""
    events, url, page = [], f"{API}?pagesize={PAGESIZE}", 0
    while url:
        page += 1
        d = _get_page(url, token)
        for e in d.get("Result", []):
            events.append({"date_start": e.get("date_start"), "region": e.get("region"),
                           "country": e.get("country"), "best": e.get("best") or 0,
                           "tov": e.get("type_of_violence")})
        if page == 1:
            print(f"  UCDP GED {VERSION}: {d.get('TotalCount')} events, {d.get('TotalPages')} pages")
        url = d.get("NextPageUrl") or None
        if max_pages and page >= max_pages:
            print(f"  (stopped at max-pages={max_pages}; partial)")
            break
        time.sleep(0.2)                          # be polite; well under 5000/day
    return events


def load_cache_or_pull(token, refresh, max_pages):
    if CACHE.exists() and not refresh and not max_pages:
        return json.loads(CACHE.read_text()), "cache"
    events = pull(token, max_pages=max_pages)
    if not max_pages:                            # only persist a COMPLETE pull as the cache
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(events))
    return events, "api"


def aggregate(events):
    """Monthly best-fatalities: global + per region. Keyed by month-end date."""
    by = defaultdict(lambda: defaultdict(float))   # series_id -> {month -> fatalities}
    for e in events:
        d = (e.get("date_start") or "")[:7]        # YYYY-MM
        if len(d) != 7:
            continue
        month_end = f"{d}-28"                       # a stable within-month PIT anchor
        best = float(e.get("best") or 0)
        by["ucdp.fat_global"][month_end] += best
        sid = REGIONS.get(e.get("region"))
        if sid:
            by[sid][month_end] += best
    return by


def write(conn, by):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)",
                ("conflict.ucdp", "conflict", "UCDP conflict data",
                 "Uppsala Conflict Data Program georeferenced events"))
    total = 0
    names = {"ucdp.fat_global": "UCDP fatalities (global, monthly)", **{v: f"UCDP fatalities ({k}, monthly)"
             for k, v in REGIONS.items()}}
    for sid, months in by.items():
        cur.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (sid, names.get(sid, sid), "conflict.ucdp", "fatalities (best est.)", "monthly",
                     "UCDP GED (Uppsala)", "src/fetch_ucdp.py",
                     "Verified organized-violence fatalities; context/corroboration, not a market series."))
        payload = [(sid, m, float(v), m, now) for m, v in sorted(months.items())]
        cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", payload)
        total += len(payload)
        print(f"  {sid:<24} {len(payload):>5} months  latest {sorted(months)[-1] if months else '-'}")
    conn.commit()
    return total


def main():
    refresh = "--refresh" in sys.argv
    max_pages = None
    if "--max-pages" in sys.argv:
        max_pages = int(sys.argv[sys.argv.index("--max-pages") + 1])
    need_pull = refresh or bool(max_pages) or not CACHE.exists()
    token = get_token()
    if need_pull and not token:
        # No token AND nothing cached -> nothing to do. Don't fail the pipeline; just skip cleanly.
        print("UCDP: no cache and no token -> skipping (set UCDP_TOKEN or add ucdp_access_token to "
              "~/.openbb_platform/user_settings.json to pull; kept OUT of the repo).")
        return
    events, src = load_cache_or_pull(token, refresh, max_pages)
    print(f"  {len(events)} events ({src})")
    by = aggregate(events)
    conn = sqlite3.connect(DB)
    n = write(conn, by)
    conn.close()
    print(f"UCDP: wrote {n} monthly observations across {len(by)} series (verified conflict intensity).")


if __name__ == "__main__":
    main()
