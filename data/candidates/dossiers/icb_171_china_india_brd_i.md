# Dossier icb_171_china_india_brd_i — CHINA/INDIA BRD. I

```json
{
 "id": "icb_171_china_india_brd_i",
 "built_by": "session A",
 "built_at": "2026-09-02T19:14:26+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 171,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=171",
  "trigdate": "1959-08-25",
  "termdate": "1960-04-19",
  "viol": 2,
  "forout": 2
 },
 "event_date": "1959-08-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.china",
   "role": "target"
  },
  {
   "entity": "country.india",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "China India Brd  I 1959",
  "search_url": "https://history.state.gov/search?q=China+India+Brd++I+1959&within=documents",
  "search_status": 200,
  "window": [
   "1959-07-26",
   "1960-05-19"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:14:25+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 171 **CHINA/INDIA BRD. I**: trigdate 1959-08-25, termdate 1960-04-19, viol 2, forout 2. Page: https://www.icb.umd.edu/dataviewer/?crisno=171

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 710: country.china (registered state set)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.china:target, country.india:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `China India Brd  I 1959` (https://history.state.gov/search?q=China+India+Brd++I+1959&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1959-07-26..1960-05-19.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_171_china_india_brd_i --approved-by joe`. The code never runs it.
