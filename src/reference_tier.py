"""
reference_tier.py -- the BACKGROUND tier: machine-scale events, queryable but NEVER corpus (V2.4).

Recorded decision: "Reference tier for machine-scale data: background only, never causal." GDELT
(and UCDP) surface far more candidate events than the 2-source codebook will ever admit. Throwing
them away loses useful context; letting them into the causal corpus would poison it (single-source,
unverified). So they live HERE -- queryable for list / count / nearest, and EVERY result is stamped
with a loud label so it can never be mistaken for corpus.

  * list   -- background events, optionally filtered by type / since / entity.
  * count  -- how many background events, by type and by year.
  * nearest-- the background events most similar to a query (date proximity + entity overlap + type),
             for "what else was going on around then?" context -- NOT analogues, NOT evidence.

Source: data/candidate_events.csv rows with candidate_source == 'gdelt' (the machine feed). These
failed the corpus admission rule (single-source) by construction. numpy-free.

Run:  python3 src/reference_tier.py --count
      python3 src/reference_tier.py --nearest 2020-03-06 --type opec_decision
"""

import csv
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "candidate_events.csv"

LABEL = "BACKGROUND — machine-scale (GDELT); NEVER analyzed causally, NEVER corpus, NOT evidence."


def _load():
    if not CANDIDATES.exists():
        return []
    return [r for r in csv.DictReader(open(CANDIDATES, newline="", encoding="utf-8"))
            if r.get("candidate_source") == "gdelt"]


def _entities(row):
    return {p.split(":", 1)[0].strip() for p in (row.get("entities") or "").split(";") if p.strip()}


def count():
    rows = _load()
    return {"tier_label": LABEL, "total": len(rows),
            "by_type": dict(Counter(r.get("type", "?") for r in rows).most_common()),
            "by_year": dict(sorted(Counter((r.get("event_date") or "?")[:4] for r in rows).items()))}


def listing(type="", since="", entity="", limit=50):
    out = []
    for r in _load():
        if type and r.get("type") != type:
            continue
        if since and (r.get("event_date") or "") < since:
            continue
        if entity and entity not in _entities(r):
            continue
        out.append({"event_id": r.get("event_id"), "event_date": r.get("event_date"),
                    "type": r.get("type"), "title": (r.get("title") or "")[:120],
                    "source_url": r.get("source_url")})
        if len(out) >= limit:
            break
    return {"tier_label": LABEL, "n": len(out), "events": out}


def nearest(date, type="", entity="", k=8):
    try:
        target = datetime.strptime(date[:10], "%Y-%m-%d").date()
    except ValueError:
        return {"tier_label": LABEL, "error": "date must be YYYY-MM-DD"}
    ent = {entity} if entity else set()
    scored = []
    for r in _load():
        try:
            ed = datetime.strptime((r.get("event_date") or "")[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        days = abs((ed - target).days)
        score = -days / 365.0
        if type and r.get("type") == type:
            score += 2.0
        overlap = len(ent & _entities(r)) if ent else 0
        score += overlap
        scored.append((score, days, r))
    scored.sort(key=lambda t: t[0], reverse=True)
    events = [{"event_id": r.get("event_id"), "event_date": r.get("event_date"),
               "type": r.get("type"), "title": (r.get("title") or "")[:120],
               "days_from_query": days, "source_url": r.get("source_url")}
              for _, days, r in scored[:k]]
    return {"tier_label": LABEL, "query": {"date": date, "type": type, "entity": entity},
            "similarity_note": "date proximity + type match + entity overlap — context only, NOT analogues",
            "n": len(events), "events": events}


def main():
    a = sys.argv[1:]
    if "--count" in a:
        import json; print(json.dumps(count(), indent=2)); return
    if "--nearest" in a:
        i = a.index("--nearest"); date = a[i + 1]
        t = a[a.index("--type") + 1] if "--type" in a else ""
        import json; print(json.dumps(nearest(date, type=t), indent=2)); return
    import json; print(json.dumps(count(), indent=2))
    print("\n" + LABEL)


if __name__ == "__main__":
    main()
