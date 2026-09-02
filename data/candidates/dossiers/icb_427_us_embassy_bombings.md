# Dossier icb_427_us_embassy_bombings — US EMBASSY BOMBINGS

```json
{
 "id": "icb_427_us_embassy_bombings",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv)",
  "crisno": 427,
  "source": "icb",
  "source_id": "427",
  "detail": "US EMBASSY BOMBINGS 1998-08-07..1998-08-20 viol 2.0",
  "url": "https://www.icb.umd.edu/dataviewer/?crisno=427",
  "trigdate": "1998-08-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1998-08-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.usa",
   "role": "unknown"
  },
  {
   "entity": "country.sudan",
   "role": "unknown"
  },
  {
   "entity": "country.afg",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Us Embassy Bombings 1998",
  "search_url": "https://history.state.gov/search?q=Us+Embassy+Bombings+1998&within=documents",
  "search_status": 200,
  "window": [
   "1998-07-08",
   "1998-09-06"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:48+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
ICB v16 system-level (icb1v16.csv) + actors (icb2v16.csv) record 427 **US EMBASSY BOMBINGS**: US EMBASSY BOMBINGS 1998-08-07..1998-08-20 viol 2.0 trigdate 1998-08-07, termdate None, viol None, forout None. Page: https://www.icb.umd.edu/dataviewer/?crisno=427

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 2: country.usa (registered state set)
- 625: country.sudan
- 700: country.afg

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.usa:unknown, country.sudan:unknown, country.afg:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Us Embassy Bombings 1998` (https://history.state.gov/search?q=Us+Embassy+Bombings+1998&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1998-07-08..1998-09-06. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier icb_427_us_embassy_bombings --approved-by joe`. The code never runs it.
