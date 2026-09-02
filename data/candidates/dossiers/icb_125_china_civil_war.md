# Dossier icb_125_china_civil_war — CHINA CIVIL WAR

```json
{
 "id": "icb_125_china_civil_war",
 "built_by": "session A",
 "built_at": "2026-09-02T19:13:18+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 125,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=125",
  "trigdate": "1948-09-23",
  "termdate": "1949-12-08",
  "viol": 4,
  "forout": 4
 },
 "event_date": "1948-09-23",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 5,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.taiwan",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "China Civil War 1948",
  "search_url": "https://history.state.gov/search?q=China+Civil+War+1948&within=documents",
  "search_status": 200,
  "window": [
   "1948-08-24",
   "1950-01-07"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v08/d48",
    "title": "The Acting Secretary of State to the Ambassador in China (Stuart) (1948, Volume VIII, The Far East: China)",
    "page_date": "1948-04-02",
    "retrieved_at": "2026-09-02T19:13:14+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v07/d86",
    "title": "The Consul General at Peiping (Clubb) to the Secretary of State (1948, Volume VII, The Far East: China)",
    "page_date": "1948-02-24",
    "retrieved_at": "2026-09-02T19:13:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v07/d12",
    "title": "The Ambassador in China (Stuart) to the Secretary of State (1948, Volume VII, The Far East: China)",
    "page_date": "1948-01-09",
    "retrieved_at": "2026-09-02T19:13:15+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v07/d318",
    "title": "The Secretary of State to the Ambassador in China (Stuart) (1948, Volume VII, The Far East: China)",
    "page_date": "1948-08-12",
    "retrieved_at": "2026-09-02T19:13:16+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v08/d232",
    "title": "The Ambassador in China (Stuart) to the Secretary of State (1948, Volume VIII, The Far East: China)",
    "page_date": "1948-04-17",
    "retrieved_at": "2026-09-02T19:13:17+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1948v07/d39",
    "title": "The Ambassador in China (Stuart) to the Secretary of State (1948, Volume VII, The Far East: China)",
    "page_date": "1948-01-23",
    "retrieved_at": "2026-09-02T19:13:17+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:13:13+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 125 **CHINA CIVIL WAR**: trigdate 1948-09-23, termdate 1949-12-08, viol 4, forout 4. Page: https://www.icb.umd.edu/dataviewer/?crisno=125

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 713: country.taiwan

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 5 (from viol 4); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.taiwan:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `China Civil War 1948` (https://history.state.gov/search?q=China+Civil+War+1948&within=documents, HTTP 200) returned 6 document(s) opened, none dated inside 1948-08-24..1950-01-07.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: The Acting Secretary of State to the Ambassador in China (St (1948-04-02); The Consul General at Peiping (Clubb) to the Secretary of St (1948-02-24); The Ambassador in China (Stuart) to the Secretary of State ( (1948-01-09); The Secretary of State to the Ambassador in China (Stuart) ( (1948-08-12); The Ambassador in China (Stuart) to the Secretary of State ( (1948-04-17); The Ambassador in China (Stuart) to the Secretary of State ( (1948-01-23)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_125_china_civil_war --approved-by joe`. The code never runs it.
