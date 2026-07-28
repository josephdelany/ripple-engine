"""
fetch_wiki_attention.py -- Wikipedia pageview attention: the "how alarmed is the
world" modality.

A sudden spike in views of a page like "Bab el-Mandeb" or "2026 Iran war" is a
clean, free proxy for a surge of global attention -- often ahead of tidy coverage.
Wikimedia's pageviews API is free, no key, reliable, and batch-friendly (daily, ~1-2
day lag). We track the pages tied to the engine's chokepoints, situation, and actors,
store daily views, and flag a 'spike' when the latest is well above its trailing norm.

DISCIPLINE: this is an ATTENTION/context signal -- noisy, gameable, display only,
never a registered statistic. It is deliberately NOT added as a hard corroboration
vote: attention rises when ships stop, so it is correlated with the physical-flow
signal, and naively counting both would double-count (the #1 fusion trap). It is
surfaced as context alongside the harder signals.

Run:  python3 src/fetch_wiki_attention.py
"""

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "wiki_attention.json"
API = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
       "en.wikipedia.org/all-access/user/{article}/daily/{start}/{end}")
UA = {"User-Agent": "ripple-engine/1.0 (research; oil-market OSINT)"}

# (wiki article, slug, display) -- pages tied to the engine's world.
PAGES = [
    ("Strait_of_Hormuz", "hormuz", "Strait of Hormuz"),
    ("Bab-el-Mandeb", "bab_el_mandeb", "Bab el-Mandeb"),
    ("Suez_Canal", "suez", "Suez Canal"),
    ("2026_Iran_war", "iran_war", "2026 Iran war"),
    ("Houthi_movement", "houthis", "Houthi movement"),
    ("Saudi_Aramco", "aramco", "Saudi Aramco"),
]
LOOKBACK_DAYS = 60
SPIKE = 2.0            # latest > 2x trailing median -> attention spike
ELEVATED = 1.4
QUIET = 0.5


def assess(views):
    """views OLDEST-first. Latest vs trailing-median flag. Pure (testable)."""
    vals = [v for v in views if v is not None]
    if not vals:
        return None
    latest = vals[-1]
    trailing = vals[:-1] or vals
    med = median(trailing)
    pct = (latest / med) if med else None
    flag = "normal"
    if pct is not None:
        flag = ("spike" if pct >= SPIKE else "elevated" if pct >= ELEVATED
                else "quiet" if pct < QUIET else "normal")
    return {"latest": int(latest), "median": round(med, 0),
            "pct_of_median": round(pct, 2) if pct is not None else None, "flag": flag}


def fetch_page(article, start, end):
    """(timestamp, views) daily list oldest-first, or [] on failure."""
    try:
        r = requests.get(API.format(article=article, start=start, end=end),
                         headers=UA, timeout=30)
        return [(i["timestamp"], i["views"]) for i in r.json().get("items", [])] \
            if r.ok else []
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"  wiki '{article}' failed ({type(e).__name__}) -- skipped.")
        return []


def main():
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat(timespec="seconds")
    start = (now - timedelta(days=LOOKBACK_DAYS)).strftime("%Y%m%d")
    end = now.strftime("%Y%m%d")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    summary = []
    for article, slug, disp in PAGES:
        rows = fetch_page(article, start, end)
        if not rows:
            continue
        sid = f"wiki.views.{slug}"
        cur.execute("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (sid, f"Wikipedia daily pageviews: {disp}", None, "views",
                     "daily", "Wikimedia", f"https://en.wikipedia.org/wiki/{article}",
                     "attention signal (context only)"))
        cur.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                        [(sid, f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}", float(v),
                          f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}", now_iso) for ts, v in rows])
        st = assess([v for _, v in rows])
        if st:
            summary.append({"page": disp, "slug": slug, "article": article, **st})
    conn.commit()
    conn.close()
    summary.sort(key=lambda s: (s["flag"] not in ("spike", "elevated"), -s["latest"]))
    OUT.write_text(json.dumps(
        {"as_of": end, "generated_at": now_iso, "source": "Wikimedia pageviews (free)",
         "note": "Daily pageviews; 'spike' = latest >= 2x trailing median. Attention "
                 "signal, context only -- never a registered statistic.",
         "pages": summary}, indent=2))
    print(f"fetch_wiki_attention -- {len(summary)} pages assessed.")
    for s in summary:
        print(f"  {s['flag']:>8}  {s['page']:<20} views={s['latest']:>7,} "
              f"({s['pct_of_median']}x median)")


if __name__ == "__main__":
    main()
