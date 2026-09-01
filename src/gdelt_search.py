"""
gdelt_search.py -- comprehensive, $0, keyless news search via the GDELT DOC 2.0 API.

Search ANY topic across the global press. GDELT indexes online news worldwide (~65
languages, rolling ~3-month window, refreshed every 15 min) and returns real article
URLs + metadata. We add honest COVERAGE stats -- how many articles, how many distinct
outlets, how many countries, over time -- the SOURCE-DIVERSITY view.

What this is NOT: political-bias labels (left/center/right). Those require proprietary
or non-commercial licensed data (AllSides = CC BY-NC, MBFC = paid); ingesting a scraped
copy would be a licensing violation. So bias is a documented gap (see NEWS_LAYER.md), and
"coverage" here means outlet/country DIVERSITY from GDELT's own free metadata -- honest.

Discipline & limits (stated, not hidden):
  * GDELT licenses URLs + metadata, NOT article bodies -- we fetch bodies separately,
    per-article, on demand (src/backend.py::wb_extract). We store metadata, not bodies.
  * GDELT throttles bursts and, when it does, returns HTTP 200 with a PLAIN-TEXT body
    (not a 429, not JSON). We detect throttling by the BODY, never the status code.
  * GDELT counts REPORTS, not events; it is English/Western-skewed; it does no dedup for
    you (we dedup on url + normalized title). Counts are coverage, not ground truth.
  * $0 forever: no key, no account, so no bill is possible -- it fails, it never charges.
  * Attribution required: "GDELT Project" (https://gdeltproject.org).
"""

import json
import re
import time
from collections import Counter

import requests

API = "https://api.gdeltproject.org/api/v2/doc/doc"
UA = {"User-Agent": "Mozilla/5.0 (ripple-engine research; +https://gdeltproject.org)"}
CACHE_TTL = 600                      # seconds; be polite, GDELT throttles bursts
MAXREC = 250                         # GDELT hard cap per query (no paging)
_cache = {}                          # (query, timespan) -> (ts, result)


def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def parse_articles(body):
    """Parse a GDELT DOC ArtList JSON body -> (articles|None, error). Pure/testable.
    Returns error='rate_limited' when GDELT sends its 200-plain-text throttle message."""
    if body is None:
        return None, "no_response"
    if not body.lstrip().startswith(("{", "[")):
        return None, "rate_limited"          # 200 + plain text == throttled
    try:
        data = json.loads(body)
    except ValueError:
        return None, "bad_response"
    return (data.get("articles", []) if isinstance(data, dict) else []), None


def _coverage(arts):
    """Honest coverage stats over a deduped article list: distinct outlets, countries,
    and a per-day volume histogram. Source DIVERSITY, not bias."""
    domains = Counter(a["domain"] for a in arts if a.get("domain"))
    countries = Counter(a["country"] for a in arts if a.get("country"))
    langs = Counter(a["language"] for a in arts if a.get("language"))
    days = Counter((a.get("seendate") or "")[:8] for a in arts if a.get("seendate"))
    return {
        "n_articles": len(arts), "n_domains": len(domains),
        "n_countries": len(countries), "n_languages": len(langs),
        "top_domains": domains.most_common(10),
        "top_countries": countries.most_common(10),
        "by_day": [{"day": d, "n": n} for d, n in sorted(days.items()) if len(d) == 8],
    }


def search(query, timespan="1week", maxrecords=150):
    """Search GDELT for a topic. Returns deduped real articles + coverage stats, or an
    honest error object (rate-limited / unreadable). Cached per (query, timespan)."""
    query = (query or "").strip()
    if not query:
        return {"ok": False, "error": "empty query"}
    key = (query, timespan)
    now = time.time()
    if key in _cache and now - _cache[key][0] < CACHE_TTL:
        return _cache[key][1]
    params = {"query": query, "mode": "artlist", "format": "json", "sort": "datedesc",
              "maxrecords": min(max(int(maxrecords), 1), MAXREC), "timespan": timespan}
    try:
        r = requests.get(API, params=params, headers=UA, timeout=45)
        arts, err = parse_articles(r.text)
    except requests.RequestException as e:
        return {"ok": False, "error": "unreachable", "query": query,
                "note": f"Couldn't reach GDELT ({type(e).__name__})."}
    if err:
        return {"ok": False, "error": err, "query": query,
                "note": ("GDELT is throttling bursts — wait a few seconds and try again."
                         if err == "rate_limited" else "GDELT returned an unreadable response.")}
    seen, out = set(), []
    for a in arts:
        k = (a.get("url"), _norm_title(a.get("title")))
        if not a.get("url") or k in seen:
            continue
        seen.add(k)
        out.append({"url": a.get("url"), "title": a.get("title"), "domain": a.get("domain"),
                    "seendate": a.get("seendate"), "language": a.get("language"),
                    "country": a.get("sourcecountry")})
    result = {"ok": True, "query": query, "timespan": timespan, "articles": out,
              "coverage": _coverage(out),
              "attribution": "Source: GDELT Project (gdeltproject.org)",
              "note": "GDELT indexes global online news (~3-month window, ~65 languages). "
                      "Counts are coverage (reports), not verified events; no bias labels."}
    _cache[key] = (now, result)
    return result


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "Strait of Hormuz"
    r = search(q)
    if r.get("ok"):
        c = r["coverage"]
        print(f"{q!r}: {c['n_articles']} articles · {c['n_domains']} outlets · "
              f"{c['n_countries']} countries")
        for a in r["articles"][:10]:
            print(f"  [{a['country']}] {a['domain']:24} {(a['title'] or '')[:60]}")
    else:
        print("error:", r.get("error"), "--", r.get("note"))
