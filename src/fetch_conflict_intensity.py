"""
fetch_conflict_intensity.py -- per-situation media conflict intensity (Stage 3: widen data).

fetch_gdelt_tone covers oil TOPICS; this covers the SITUATIONS -- for each active theatre
(Israel-Iran, Russia-Ukraine, China-Taiwan, Israel-Lebanon) it pulls GDELT DOC's coverage
VOLUME and TONE, so the engine has eyes on every theatre, not just oil. Free, no token.

Two honest signals per situation:
  - volume ratio  = today's share of world coverage vs its own 7-day baseline -> a SURGE
    band (surge / elevated / normal / quiet). Attention, not truth.
  - tone          = average sentiment (negative = darker coverage).
Both are media CLAIMS (what the press is saying / how loudly), tagged as such -- never a
verified fact and never a registered statistic. UCDP's verified-fact feed now needs a
token, so we use the free firehose and label it honestly.

Reuses the polite 429-backoff pattern from fetch_gdelt_tone. Deterministic parsing; no LLM.
Run:  python3 src/fetch_conflict_intensity.py
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "conflict_intensity.json"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
UA = {"User-Agent": "Mozilla/5.0 (ripple-engine research)"}

# situation label -> GDELT DOC query (the theatre's terms).
SITUATIONS = {
    "Israel-Iran": '("Israel" "Iran") OR "Israel-Iran"',
    "Russia-Ukraine": '("Russia" "Ukraine") OR "Russia-Ukraine war"',
    "China-Taiwan": '("China" "Taiwan") OR "Taiwan Strait"',
    "Israel-Lebanon": '("Israel" "Lebanon") OR "Hezbollah"',
}
PACING = 8            # > GDELT's 5s floor, with margin
RETRIES = 4
BUDGET_SECS = 240     # global deadline: GDELT throttling could make 4 theatres x 2 modes x backoff
                      # exceed the pipeline step timeout and HANG the whole run. Past this, we write
                      # whatever we have and exit 0 -- a partial cycle is fine; a hang is not.
_DEADLINE = None      # set in main()


def past_deadline():
    return _DEADLINE is not None and time.monotonic() >= _DEADLINE


def timeline_values(json_text):
    """Parse a GDELT DOC timeline response -> list of numeric values (pure, testable)."""
    try:
        tl = json.loads(json_text).get("timeline", [])
        data = tl[0].get("data", []) if tl else []
        return [float(d["value"]) for d in data]
    except (ValueError, KeyError, IndexError, TypeError):
        return []


def intensity_band(ratio):
    """Volume today vs its own baseline -> a typed band (pure, testable)."""
    if ratio is None:
        return "n/a"
    if ratio >= 1.8:
        return "surge"
    if ratio >= 1.25:
        return "elevated"
    if ratio <= 0.6:
        return "quiet"
    return "normal"


def _fetch(query, mode):
    params = {"query": query, "mode": mode, "timespan": "7d", "format": "json"}
    delay = PACING
    for _ in range(RETRIES):
        if past_deadline():
            return None                       # out of time budget -- give up this fetch cleanly
        try:
            r = requests.get(API, params=params, headers=UA, timeout=40)
            # GDELT returns its "limit requests to one every 5 seconds" notice as plain
            # TEXT with HTTP 200 (not a 429) -- treat any non-JSON 200 as a throttle.
            throttled = r.ok and not r.text.lstrip().startswith("{")
            if r.status_code == 429 or throttled:
                time.sleep(delay); delay *= 2; continue
            return r.text if r.ok else None
        except requests.RequestException:
            time.sleep(delay); delay *= 2
    return None


def assess(query):
    """Volume ratio + band + tone for one situation query."""
    vol = timeline_values(_fetch(query, "TimelineVol") or "")
    ratio = None
    if len(vol) >= 3:
        baseline = sum(vol[:-1]) / len(vol[:-1])
        ratio = round(vol[-1] / baseline, 2) if baseline else None
    time.sleep(PACING)
    tone_vals = timeline_values(_fetch(query, "TimelineTone") or "")
    tone = round(tone_vals[-1], 2) if tone_vals else None
    return {"vol_ratio": ratio, "band": intensity_band(ratio), "tone": tone,
            "mood": "negative" if (tone or 0) < -1 else "positive" if (tone or 0) > 1
            else "neutral"}


def main():
    global _DEADLINE
    _DEADLINE = time.monotonic() + BUDGET_SECS
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = []
    for i, (label, query) in enumerate(SITUATIONS.items()):
        if past_deadline():
            print(f"  (time budget {BUDGET_SECS}s reached -- writing {len(out)} of "
                  f"{len(SITUATIONS)} theatres, partial is fine)")
            break
        if i:
            time.sleep(PACING)
        a = assess(query)
        a["situation"] = label
        out.append(a)
        print(f"  {a['band']:>8}  {label:<16} vol x{a['vol_ratio']}  tone {a['tone']}")
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now, "source": "GDELT DOC 2.0 (free)",
         "note": "Per-situation media coverage volume (vs 7d baseline) + tone. Media CLAIMS "
                 "-- attention & sentiment, not verified facts. Context only.",
         "situations": out}, indent=2))
    print(f"fetch_conflict_intensity -- {len(out)} theatres.")


if __name__ == "__main__":
    main()
