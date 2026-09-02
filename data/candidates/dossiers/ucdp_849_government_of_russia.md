# Dossier ucdp_849_government_of_russia — Government of Russia

```json
{
 "id": "ucdp_849_government_of_russia",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "849",
  "detail": "dyad 849 Government of Russia (Soviet Union) vs Parliamentary Forces (Russia (Soviet Union)) onset 1993-10-03 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1993-10-03",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1993-10-03",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.russia",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Russia 1993",
  "search_url": "https://history.state.gov/search?q=Government+Of+Russia+1993&within=documents",
  "search_status": 200,
  "window": [
   "1993-09-03",
   "1993-11-02"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1918Russiav01/d220",
    "title": "The Minister in Sweden (Morris) to the Secretary of State (1918, Volume I, Russia)",
    "page_date": "1917-11-19",
    "retrieved_at": "2026-09-02T19:54:26+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1867p1/d91",
    "title": "Mr. Adams to Mr. Seward (1867, Part I, Accompanying the Annual Message of the President to the Second Session of the Fortieth Congress)",
    "page_date": "1867-06-11",
    "retrieved_at": "2026-09-02T19:54:26+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1955-57v24/d32",
    "title": "32. Telegram From the Embassy in the Soviet Union to the Department of State (1955\u20131957, Volume XXIV, Soviet Union, Eastern Mediterranean)",
    "page_date": "1956-03-07",
    "retrieved_at": "2026-09-02T19:54:27+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1915/d673",
    "title": "The Secretary of State ad interim to Senator Lodge. (1915, With the Address of the President to Congress December 7, 1915)",
    "page_date": "1915-06-09",
    "retrieved_at": "2026-09-02T19:54:27+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:54:25+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 849 **Government of Russia**: dyad 849 Government of Russia (Soviet Union) vs Parliamentary Forces (Russia (Soviet Union)) onset 1993-10-03 intensity 1 trigdate 1993-10-03, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 365: country.russia (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.russia:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Russia 1993` (https://history.state.gov/search?q=Government+Of+Russia+1993&within=documents, HTTP 200) returned 4 document(s) opened, none dated inside 1993-09-03..1993-11-02. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Minister in Sweden (Morris) to the Secretary of State (1 (1917-11-19); Mr. Adams to Mr. Seward (1867, Part I, Accompanying the Annu (1867-06-11); 32. Telegram From the Embassy in the Soviet Union to the Dep (1956-03-07); The Secretary of State ad interim to Senator Lodge. (1915, W (1915-06-09)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_849_government_of_russia --approved-by joe`. The code never runs it.
