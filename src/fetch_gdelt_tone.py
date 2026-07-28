"""
fetch_gdelt_tone.py -- GDELT DOC 2.0 media TONE per topic (the sentiment modality).

The watcher already ingests GDELT's discrete EVENTS. This complements them with
GDELT DOC's near-real-time COVERAGE TONE: for each oil/geopolitics topic it pulls the
average sentiment of global news coverage over the last week. A sharp swing NEGATIVE
in tone about "Strait of Hormuz" or "oil supply" is an alarm signal -- the world's
coverage turning dark -- distinct from raw event counts. Free, no key.

GDELT DOC throttles bursts (HTTP 429), so this is deliberately polite: one request
per topic, spaced, with exponential backoff on 429. Tone is stored as a signal
(gdelt.tone.<topic>); DISPLAY/context only, never a registered statistic.

Run:  python3 src/fetch_gdelt_tone.py
"""

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "gdelt_tone.json"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
UA = {"User-Agent": "Mozilla/5.0 (ripple-engine research)"}

# topic slug -> GDELT DOC query.
TOPICS = {
    "hormuz": '"Strait of Hormuz"',
    "bab_el_mandeb": '"Bab el-Mandeb" OR "Red Sea shipping"',
    "oil_supply": '(theme:ECON_OIL) (attack OR strike OR blockade OR sanctions)',
    "opec": 'OPEC (production OR cut OR quota)',
}
PACING = 6            # seconds between requests (GDELT throttles bursts)
RETRIES = 3


def latest_tone(json_text):
    """Parse a GDELT DOC TimelineTone response -> latest average-tone value, or None.
    Pure (testable)."""
    try:
        tl = json.loads(json_text).get("timeline", [])
        data = tl[0].get("data", []) if tl else []
        return float(data[-1]["value"]) if data else None
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def fetch_tone(query):
    """One TimelineTone request with 429-backoff. Returns latest tone or None."""
    params = {"query": query, "mode": "TimelineTone", "timespan": "7d",
              "format": "json"}
    delay = PACING
    for attempt in range(RETRIES):
        try:
            r = requests.get(API, params=params, headers=UA, timeout=40)
            if r.status_code == 429:
                time.sleep(delay)
                delay *= 2
                continue
            if r.ok:
                return latest_tone(r.text)
            return None
        except requests.RequestException:
            time.sleep(delay)
            delay *= 2
    return None


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    today = now[:10]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    summary = []
    for i, (slug, query) in enumerate(TOPICS.items()):
        if i:
            time.sleep(PACING)                # be polite between topics
        tone = fetch_tone(query)
        if tone is None:
            print(f"  gdelt tone '{slug}' -- no data (throttled/empty).")
            continue
        sid = f"gdelt.tone.{slug}"
        cur.execute("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (sid, f"GDELT coverage tone: {slug}", None, "tone", "daily",
                     "GDELT DOC", "https://api.gdeltproject.org",
                     "avg media sentiment (negative = alarm); context only"))
        cur.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)",
                    (sid, today, tone, today, now))
        summary.append({"topic": slug, "tone": round(tone, 2),
                        "mood": "negative" if tone < -1 else "positive" if tone > 1
                        else "neutral"})
    conn.commit()
    conn.close()
    if summary:
        OUT.write_text(json.dumps(
            {"as_of": today, "generated_at": now, "source": "GDELT DOC 2.0 (free)",
             "note": "Average coverage tone over 7d per topic; negative = darker "
                     "coverage. Context only, never a registered statistic.",
             "topics": summary}, indent=2))
    print(f"fetch_gdelt_tone -- {len(summary)} topics.")
    for s in summary:
        print(f"  {s['mood']:>8}  {s['topic']:<16} tone={s['tone']}")


if __name__ == "__main__":
    main()
