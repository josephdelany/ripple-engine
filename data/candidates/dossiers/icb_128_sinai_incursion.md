# Dossier icb_128_sinai_incursion — SINAI INCURSION

```json
{
 "id": "icb_128_sinai_incursion",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:21+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 128,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=128",
  "trigdate": "1948-12-25",
  "termdate": "1949-01-10",
  "viol": 3,
  "forout": 4
 },
 "event_date": "1948-12-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 4,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.gbr",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "target"
  },
  {
   "entity": "country.israel",
   "role": "actor"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Sinai Incursion 1948",
  "search_url": "https://history.state.gov/search?q=Sinai+Incursion+1948&within=documents",
  "search_status": 200,
  "window": [
   "1948-11-25",
   "1949-02-09"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v16/d671",
    "title": "671. Memorandum of a Conversation, Department of State, Washington, December 28, 1956, 4:05 p.m. (1955\u20131957, Volume XVI, Suez Crisis, July 26\u2013December 31, 1956)",
    "page_date": "1956-12-28",
    "retrieved_at": "2026-09-02T19:13:20+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1977-80v13/d138",
    "title": "138. Memorandum of Conversation (1977\u20131980, Volume XIII, China)",
    "page_date": "1978-10-03",
    "retrieved_at": "2026-09-02T19:13:21+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:13:19+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 128 **SINAI INCURSION**: trigdate 1948-12-25, termdate 1949-01-10, viol 3, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=128

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 200: country.gbr (registered state set)
- 651: country.egypt (registered state set)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 4 (from viol 3); surprise 3 (provisional); confidence medium
- entities: country.gbr:target, country.egypt:target, country.israel:actor

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Sinai Incursion 1948` (https://history.state.gov/search?q=Sinai+Incursion+1948&within=documents, HTTP 200) returned 2 document(s) opened, none dated inside 1948-11-25..1949-02-09.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 671. Memorandum of a Conversation, Department of State, Wash (1956-12-28); 138. Memorandum of Conversation (1977–1980, Volume XIII, Chi (1978-10-03)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_128_sinai_incursion --approved-by joe`. The code never runs it.
