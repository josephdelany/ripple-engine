# Dossier icb_350_omdurman_bombing — OMDURMAN BOMBING

```json
{
 "id": "icb_350_omdurman_bombing",
 "built_by": "session A",
 "built_at": "2026-09-02T19:19:36+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 350,
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=350",
  "trigdate": "1984-03-16",
  "termdate": "1984-01-01",
  "viol": 2,
  "forout": 7
 },
 "event_date": "1984-03-16",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 3,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "actor"
  },
  {
   "entity": "country.sudan",
   "role": "target"
  },
  {
   "entity": "country.egypt",
   "role": "target"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "route": "FRUS",
  "query": "Omdurman Bombing 1984",
  "search_url": "https://history.state.gov/search?q=Omdurman+Bombing+1984&within=documents",
  "search_status": 200,
  "window": [
   "1984-02-15",
   "1984-01-31"
  ],
  "opened": [
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d32",
    "title": "32. Telegram From the Department of State to the Embassy in Morocco (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1984-03-30",
    "retrieved_at": "2026-09-02T19:19:35+00:00"
   },
   {
    "url": "https://history.state.gov/historicaldocuments/frus1981-88v24/d316",
    "title": "316. Telegram From the Department of State to the Embassy in Tunisia (1981\u20131988, Volume XXIV, North Africa)",
    "page_date": "1984-04-21",
    "retrieved_at": "2026-09-02T19:19:36+00:00"
   }
  ],
  "retrieved_at": "2026-09-02T19:19:34+00:00"
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB crisis 350 **OMDURMAN BOMBING**: trigdate 1984-03-16, termdate 1984-01-01, viol 2, forout 7. Page: https://www.icb.umd.edu/dataviewer/?crisno=350

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 620: country.libya (registered state set)
- 625: country.sudan
- 651: country.egypt (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 3 (from viol 2); surprise 3 (provisional); confidence medium
- entities: country.libya:actor, country.sudan:target, country.egypt:target

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Omdurman Bombing 1984` (https://history.state.gov/search?q=Omdurman+Bombing+1984&within=documents, HTTP 200) returned 2 document(s) opened, none dated inside 1984-02-15..1984-01-31.
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).
- opened: 32. Telegram From the Department of State to the Embassy in  (1984-03-30); 316. Telegram From the Department of State to the Embassy in (1984-04-21)

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_350_omdurman_bombing --approved-by joe`. The code never runs it.
