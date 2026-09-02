# Dossier mid_4219_col_ven_dispute — COL VEN dispute

```json
{
 "id": "mid_4219_col_ven_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4219",
  "detail": "dispute 4219 COL-VEN 1994-01-07..1994-01-09 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1994-01-07",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-01-07",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.col",
   "role": "unknown"
  },
  {
   "entity": "country.venezuela",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Col Ven Dispute 1994",
  "search_url": "https://history.state.gov/search?q=Col+Ven+Dispute+1994&within=documents",
  "search_status": 200,
  "window": [
   "1993-12-08",
   "1994-02-06"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:35+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4219 **COL VEN dispute**: dispute 4219 COL-VEN 1994-01-07..1994-01-09 hihost 4 trigdate 1994-01-07, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 100: country.col (registered state set)
- 101: country.venezuela (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.col:unknown, country.venezuela:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Col Ven Dispute 1994` (https://history.state.gov/search?q=Col+Ven+Dispute+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-12-08..1994-02-06. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4219_col_ven_dispute --approved-by joe`. The code never runs it.
