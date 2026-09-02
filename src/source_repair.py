"""source_repair.py -- Priority E: repair the sources of events ALREADY in the corpus (DOSSIER_RULE.md §6).

72 events feed the engine on a weak source: 31 cite an encyclopaedia, 9 cite a bare eia.gov root, 32 carry "DRAFT
coding" in their description. For each, this searches the routes that are actually reachable by script, primary
documents first, and writes a repair dossier under data/candidates/repairs/<event_id>.md with one of three outcomes:

  closed-primary   a government document with its own date inside [d-3d, d+30d] naming the event (FRUS, Federal
                   Register). This is the only outcome that repairs an event (§6.5).
  partial          a UK National Archives FILE whose covering dates contain d and whose title names the subject
                   (a pointer to primary material, never a record of the event)
  press_candidate  a dated article whose title shares the event's terms (GDELT). Keyword overlap cannot identify an
                   event -- four tightenings were each defeated -- so this is a place for Joe to look, never a repair.
  blocked-by-declassification
              no reachable route could answer: the era is served only by CREST / the UN / OPEC archives, all of
              which refuse scripted access. A statement about ACCESS, never about whether a source exists.

A route that refuses or errors is `undetermined` and is never written as an absence (§5.1); a query that can name
nobody is not run (§5.2). Nothing is admitted and nothing in `events` is edited: Joe decides on the dossier.

Run:  python3 src/source_repair.py                # all 72
      python3 src/source_repair.py --limit 5      # smoke
      python3 src/source_repair.py --cohort encyclopaedia
"""
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "state"))
import countries as C  # noqa: E402
from dossier import _get, GDELT_FROM, frus_candidates, frus_doc_date, gdelt_second_source, query_terms, searchable  # noqa: E402

OUT = ROOT / "data" / "candidates" / "repairs"
INDEX = ROOT / "data" / "candidates" / "repairs_index.json"
RULE = "data/candidates/DOSSIER_RULE.md §6 (2026-09-02)"
TNA = "https://discovery.nationalarchives.gov.uk/API/search/records"
FEDREG = "https://www.federalregister.gov/api/v1/documents.json"
FEDREG_FROM = "1994-01-01"          # ROUTE_TABLE.md §1: verified coverage
# §6.3(2): a listing/aggregator page names no event and is never a source
AGGREGATOR = re.compile(r"latest news|photos\s*,\s*videos|news\s*,\s*photos|live updates|/topics?/|: latest news", re.I)
PRIMARY_ROUTES = {"FRUS", "Federal Register"}          # §6.3(1): these yield primary documents; GDELT yields press
BEFORE, AFTER = 3, 30                       # the window [d-3d, d+30d], as §6.2
FRUS_TO = "1994-12-31"                      # FRUS volumes run to the early 1990s (§6.1)
UNREACHABLE = ["CIA CREST (cia.gov/readingroom): every search form redirects to the landing page; results need JavaScript",
               "UN Security Council / UN Digital Library: HTTP 403 to scripts; the digital library serves a JS challenge",
               "OPEC archive (opec.org): HTTP 403 (Cloudflare)",
               "US NARA catalog: the API path returns the JavaScript app shell"]

COHORTS = {
    "encyclopaedia": ("source_url matches wikipedia/britannica", lambda r: bool(re.search(r"wikipedia|britannica", r["source_url"] or "", re.I))),
    "bare_eia": ("source_url is exactly https://www.eia.gov", lambda r: bool(re.match(r"^https?://(www\.)?eia\.gov/?$", (r["source_url"] or "").strip(), re.I))),
    "draft": ('description contains "DRAFT coding"', lambda r: bool(re.search(r"DRAFT coding", r["description"] or "", re.I))),
}


# ----------------------------------------------------------------------------- the corpus side

def weak_events(conn, cohort=None, date_from=None, date_to=None):
    rows = [dict(zip(("event_id", "event_date", "type", "title", "description", "source_url"), r))
            for r in conn.execute("SELECT event_id, event_date, type, title, description, source_url FROM events ORDER BY event_date")]
    ents = defaultdict(list)
    for eid, en in conn.execute("SELECT event_id, entity_id FROM event_entities WHERE entity_id LIKE 'country.%'"):
        ents[eid].append(en)
    out = []
    for r in rows:
        for name, (_desc, pred) in COHORTS.items():
            if pred(r):
                r = dict(r, cohort=name, parties=[C.ALL[e][3].split(" (")[0] for e in ents.get(r["event_id"], []) if e in C.ALL])
                out.append(r)
                break
    return [r for r in out if cohort in (None, r["cohort"])
            and (date_from is None or r["event_date"] >= date_from)
            and (date_to is None or r["event_date"] <= date_to)]


# ----------------------------------------------------------------------------- the routes (§6.1)

def frus_route(ev, d):
    """A FRUS document with its own date inside the window (§6.2 closed). Covers to the early 1990s."""
    if d.date().isoformat() > FRUS_TO:
        return {"route": "FRUS", "status": "out_of_coverage", "note": f"FRUS volumes run to the early 1990s; the event is {d.date()}"}
    terms = query_terms(ev["title"], ev["parties"])
    if not searchable(ev["title"], ev["parties"]):
        return {"route": "FRUS", "status": "not_run", "note": f"no query can name a state or carry two content terms of '{ev['title']}' (§5.2)"}
    query = " ".join(dict.fromkeys(terms))
    cands, srec = frus_candidates(f"{query} {d.year}")
    if srec.get("status") != 200:
        return {"route": "FRUS", "status": "undetermined", "search_status": srec.get("status"), "query": query, "note": "the source refused or failed (§5.1)"}
    lo, hi = (d - pd.Timedelta(days=BEFORE)).date().isoformat(), (d + pd.Timedelta(days=AFTER)).date().isoformat()
    opened = []
    keys = [t.lower() for t in terms]
    for c in cands[:6]:
        dt, _ = frus_doc_date(c["url"])
        opened.append({"url": c["url"], "title": c["title"], "doc_date": dt})
        if dt and lo <= dt <= hi and any(k in c["title"].lower() for k in keys):
            return {"route": "FRUS", "status": "closed-primary", "url": c["url"], "title": c["title"], "date": dt, "window": [lo, hi],
                    "query": query, "search_url": srec.get("url"), "opened": opened}
    return {"route": "FRUS", "status": "none_found", "query": query, "search_url": srec.get("url"), "window": [lo, hi], "opened": opened}


def tna_route(ev, d):
    """A UK National Archives FILE whose covering dates contain d and whose title names the subject (§6.2 partial)."""
    if not searchable(ev["title"], ev["parties"]):
        return {"route": "UK National Archives", "status": "not_run", "note": "no query can name a state or carry two content terms (§5.2)"}
    terms = query_terms(ev["title"], ev["parties"])
    query = " ".join(dict.fromkeys(terms))
    lo, hi = (d - pd.Timedelta(days=BEFORE)), (d + pd.Timedelta(days=AFTER))
    rec = _get(TNA, {"sps.searchQuery": query, "sps.dateFrom": lo.date().isoformat(), "sps.dateTo": hi.date().isoformat(), "sps.resultsPageSize": 10})
    if rec.get("status") != 200:
        return {"route": "UK National Archives", "status": "undetermined", "search_status": rec.get("status"), "query": query, "note": "the source refused or failed (§5.1)"}
    try:
        body = json.loads(rec["text"])
    except ValueError:
        return {"route": "UK National Archives", "status": "undetermined", "query": query, "note": "reply was not JSON"}
    keys = [t.lower() for t in terms]
    opened = []
    for x in (body.get("records") or [])[:10]:
        title, ref, cov = (x.get("title") or ""), (x.get("reference") or ""), (x.get("coveringDates") or "")
        opened.append({"reference": ref, "title": title[:140], "covering_dates": cov})
        if any(k in title.lower() for k in keys):
            return {"route": "UK National Archives", "status": "partial", "reference": ref, "title": title[:200], "covering_dates": cov,
                    "url": f"https://discovery.nationalarchives.gov.uk/details/r/{x.get('id')}", "query": query, "window": [lo.date().isoformat(), hi.date().isoformat()],
                    "n_hits": body.get("count"), "opened": opened}
    return {"route": "UK National Archives", "status": "none_found", "query": query, "n_hits": body.get("count"),
            "window": [lo.date().isoformat(), hi.date().isoformat()], "opened": opened}


def fedreg_route(ev, d):
    """A Federal Register document (rule, notice, presidential document) with its own publication date inside the
    window and a title naming the event or a party (ROUTE_TABLE.md §1). Keyless. 1994 onward."""
    if d.date().isoformat() < FEDREG_FROM:
        return {"route": "Federal Register", "status": "out_of_coverage", "note": f"Federal Register API coverage begins {FEDREG_FROM}"}
    if not searchable(ev["title"], ev["parties"]):
        return {"route": "Federal Register", "status": "not_run", "note": "no query can name a state or carry two content terms (§5.2)"}
    terms = query_terms(ev["title"], ev["parties"])
    query = " ".join(dict.fromkeys(terms))
    lo, hi = (d - pd.Timedelta(days=BEFORE)).date().isoformat(), (d + pd.Timedelta(days=AFTER)).date().isoformat()
    rec = _get(FEDREG, {"conditions[term]": query, "conditions[publication_date][gte]": lo,
                        "conditions[publication_date][lte]": hi, "per_page": 10})
    if rec.get("status") != 200:
        return {"route": "Federal Register", "status": "undetermined", "search_status": rec.get("status"), "query": query, "note": "the source refused or failed (§5.1)"}
    try:
        body = json.loads(rec["text"])
    except ValueError:
        return {"route": "Federal Register", "status": "undetermined", "query": query, "note": "reply was not JSON"}
    keys = [t.lower() for t in terms]
    opened = []
    for x in (body.get("results") or [])[:10]:
        title, pub = (x.get("title") or ""), (x.get("publication_date") or "")
        opened.append({"title": title[:140], "doc_date": pub, "type": x.get("type")})
        if pub and lo <= pub <= hi and any(k in title.lower() for k in keys):
            return {"route": "Federal Register", "status": "closed-primary", "url": x.get("html_url"), "title": title[:200], "date": pub,
                    "doc_type": x.get("type"), "query": query, "window": [lo, hi], "n_hits": body.get("count"), "opened": opened}
    return {"route": "Federal Register", "status": "none_found", "query": query, "n_hits": body.get("count"), "window": [lo, hi], "opened": opened}


def gdelt_route(ev, d):
    """A dated article, 2017 onward only. Yields `press_candidate` -- a place for Joe to look, never a repair (§6.5)."""
    if d.date().isoformat() < GDELT_FROM:
        return {"route": "GDELT DOC 2.0", "status": "out_of_coverage", "note": f"GDELT DOC coverage begins {GDELT_FROM}"}
    ss = gdelt_second_source(ev["title"], ev["parties"], d)
    content = [t.lower() for t in query_terms(ev["title"], [])]          # §6.4: the event's own words, parties excluded
    hit_title = (ss.get("title") or "").lower()
    if ss.get("found") and content and not any(c in hit_title for c in content):
        return {**{k: v for k, v in ss.items() if k != "found"}, "status": "none_found", "rejected_title": ss.get("title"),
                "note": f"the hit named a party but no content term of the event's title ({', '.join(content)}) -- naming a party is not naming the event (§6.4)"}
    if ss.get("found") and not content:
        return {**{k: v for k, v in ss.items() if k != "found"}, "status": "none_found", "rejected_title": ss.get("title"),
                "note": "the event's title yields no content term, so no press hit can be matched to it (§6.4)"}
    if ss.get("found") and AGGREGATOR.search(ss.get("title") or ""):
        return {**{k: v for k, v in ss.items() if k != "found"}, "status": "none_found",
                "rejected_title": ss.get("title"), "note": "the only hit was an aggregator/listing page, which names no event (§6.3(2))"}
    # §6.5: a press hit is a place for Joe to look, never a closure. The matched terms travel with it so he can dismiss it fast.
    st = "press_candidate" if ss.get("found") else ss.get("status", "none_found")
    return {**{k: v for k, v in ss.items() if k != "found"}, "status": st, "matched_terms": content}


def repair(ev, routes=None):
    """Run the reachable routes in the registered order and decide the outcome (§6.2)."""
    d = pd.Timestamp(ev["event_date"])
    tried = [r(ev, d) for r in (routes or [frus_route, fedreg_route, gdelt_route, tna_route])]
    prim = [t for t in tried if t["status"] == "closed-primary"]
    press = [t for t in tried if t["status"] == "press_candidate"]
    closed = prim + press
    partial = [t for t in tried if t["status"] == "partial"]
    answered = [t for t in tried if t["status"] in ("closed-primary", "press_candidate", "partial", "none_found")]
    if prim:
        outcome = "closed-primary"
    elif partial:
        outcome = "partial"
    elif press:
        outcome = "press_candidate"
    elif False:
        outcome = "partial"
    elif not answered:
        outcome = "blocked-by-declassification"
    else:
        outcome = "none_found"
    return {"outcome": outcome, "routes": tried, "closed": closed, "partial": partial}


# ----------------------------------------------------------------------------- the dossier

def write_repair(ev, res):
    OUT.mkdir(parents=True, exist_ok=True)
    front = {"event_id": ev["event_id"], "event_date": ev["event_date"], "cohort": ev["cohort"], "outcome": res["outcome"],
             "built_by": "session A", "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "rule": RULE,
             "current_source": ev["source_url"], "parties": ev["parties"],
             "proposed_sources": [{k: r.get(k) for k in ("route", "url", "title", "date", "reference", "covering_dates")}
                                  for r in res["closed"] + res["partial"]],
             "approved_by": None, "approved_at": None}
    L = [f"# Source repair — {ev['event_id']} ({ev['event_date']})", "", "```json", json.dumps(front, indent=1, default=str), "```", "",
         f"**{ev['title']}**", "",
         f"- cohort: `{ev['cohort']}` — {COHORTS[ev['cohort']][0]}",
         f"- current source: {ev['source_url']}",
         f"- parties on the event: {', '.join(ev['parties']) or 'none mapped'}", "",
         "## Outcome: **" + res["outcome"] + "**", ""]
    if res["outcome"] == "closed-primary":
        r = res["closed"][0]
        L += [f"A PRIMARY document dated inside the window: **{r['title']}** ({r['date']}) via {r['route']}.", f"  {r['url']}", ""]
    elif res["outcome"] == "press_candidate":
        r = res["closed"][0]
        L += [f"**A PLACE TO LOOK, not a repair (§6.5).** A dated article inside the window whose title shares the terms "
              f"`{', '.join(r.get('matched_terms') or [])}` with this event: **{r['title']}** ({r['date']}, {r['route']}).",
              f"  {r['url']}", "",
              "Keyword overlap cannot identify a specific event -- four tightenings of the match were each defeated -- so this "
              "is offered for Joe's eye and is NOT counted as a repair. No primary document was reachable for this date.", ""]
    elif res["outcome"] == "partial":
        r = res["partial"][0]
        L += [f"No dated document; an archival FILE at the right time on the right subject: **{r['reference']} {r['title']}**, "
              f"covering dates {r['covering_dates']} ({r['route']}). This is a pointer to primary material, NOT a record of the event.",
              f"  {r['url']}", ""]
    elif res["outcome"] == "blocked-by-declassification":
        L += ["No reachable route could answer. This is a statement about ACCESS, not about whether a source exists:", ""] + \
             [f"  - {u}" for u in UNREACHABLE] + [""]
    else:
        L += ["Every reachable route answered and none held a document or file matching this event in the window. "
              "That is an absence in the reachable record, not in history.", ""]
    L += ["## Routes tried", ""]
    for r in res["routes"]:
        bits = [f"`{r['status']}`"] + [f"{k}={r[k]}" for k in ("query", "n_hits", "search_status") if r.get(k) not in (None, "")]
        L.append(f"- **{r['route']}** — {'; '.join(bits)}{'. ' + r['note'] if r.get('note') else ''}")
        for o in (r.get("opened") or [])[:4]:
            L.append(f"    - opened: {o.get('title', '')[:90]} ({o.get('doc_date') or o.get('covering_dates') or o.get('page_date') or 'no date'})")
    L += ["", "Joe: this replaces nothing until you say so. `events` is untouched; the current source above still stands."]
    (OUT / f"{ev['event_id']}.md").write_text("\n".join(L) + "\n")
    return front


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    cohort = sys.argv[sys.argv.index("--cohort") + 1] if "--cohort" in sys.argv else None
    # session A owns the post-2000 half of the encyclopaedia and bare-root cohorts; E owns pre-2000 (ownership split
    # 2026-09-02). --from / --to keep the two from writing the same dossier.
    date_from = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None
    date_to = sys.argv[sys.argv.index("--to") + 1] if "--to" in sys.argv else None
    tag = sys.argv[sys.argv.index("--index-tag") + 1] if "--index-tag" in sys.argv else None
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    evs = weak_events(conn, cohort, date_from, date_to)
    evs = evs[:limit] if limit else evs
    conn.close()
    fronts = []
    for i, ev in enumerate(evs, 1):
        res = repair(ev)
        fronts.append(write_repair(ev, res))
        print(f"  [{i}/{len(evs)}] {ev['event_id']:<38} {ev['event_date']}  {ev['cohort']:<14} {res['outcome']}", flush=True)
    by_dec = defaultdict(Counter)
    for f in fronts:
        by_dec[f["event_date"][:3] + "0s"][f["outcome"]] += 1
    global INDEX
    if tag:
        INDEX = INDEX.with_name(f"repairs_index_{tag}.json")
    idx = {"rule": RULE, "route_table": "data/candidates/ROUTE_TABLE.md", "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "scope": {"cohort": cohort, "date_from": date_from, "date_to": date_to, "owner": "session A" if date_from else "unsplit"}, "n": len(fronts),
           "cohorts": {k: v for k, v in Counter(f["cohort"] for f in fronts).items()},
           "outcomes": dict(Counter(f["outcome"] for f in fronts)),
           "by_decade": {d: dict(c) for d, c in sorted(by_dec.items())},
           "unreachable_routes": UNREACHABLE,
           "repairs": [{k: f[k] for k in ("event_id", "event_date", "cohort", "outcome")} |
                       {"proposed": f["proposed_sources"][0] if f["proposed_sources"] else None} for f in fronts]}
    INDEX.write_text(json.dumps(idx, indent=1))
    print(f"\n{len(fronts)} repair dossiers: {idx['outcomes']}")
    for d, c in idx["by_decade"].items():
        print(f"  {d}: {dict(c)}")
    print(f"-> {INDEX.relative_to(ROOT)}; nothing admitted, nothing in events changed")


if __name__ == "__main__":
    main()
