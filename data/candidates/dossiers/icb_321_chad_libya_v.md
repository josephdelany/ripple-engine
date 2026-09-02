# Dossier icb_321_chad_libya_v — CHAD/LIBYA V

```json
{
 "id": "icb_321_chad_libya_v",
 "built_by": "session A",
 "built_at": "2026-09-02T19:18:59+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 321,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=321",
  "trigdate": "1981-01-06",
  "termdate": "1981-11-16",
  "viol": 2,
  "forout": 4
 },
 "event_date": "1981-01-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.fra",
   "role": "target"
  },
  {
   "entity": "country.libya",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Chad Libya V 1981",
  "search_url": "https://history.state.gov/search?q=Chad+Libya+V+1981&within=documents",
  "search_status": 200,
  "window": [
   "1980-12-07",
   "1981-12-16"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d199",
    "title": "199. Memorandum of Conversation (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1982-02-11",
    "retrieved_at": "2026-09-02T19:18:59+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:18:58+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 321 **CHAD/LIBYA V**: trigdate 1981-01-06, termdate 1981-11-16, viol 2, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=321

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 220: country.fra (registered state set)
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.fra:target, country.libya:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chad Libya V 1981` (https://history.state.gov/search?q=Chad+Libya+V+1981&within=documents, HTTP 200) returned 1 document(s) opened, none dated inside 1980-12-07..1981-12-16.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 199. Memorandum of Conversation (1981–1988, Volume XXIV, Nor (1982-02-11)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_321_chad_libya_v --approved-by joe`. The code never runs it.
