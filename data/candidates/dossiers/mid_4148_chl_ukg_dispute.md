# Dossier mid_4148_chl_ukg_dispute — CHL UKG dispute

```json
{
 "id": "mid_4148_chl_ukg_dispute",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
  "crisno": null,
  "source": "mid",
  "source_id": "4148",
  "detail": "dispute 4148 CHL-UKG 1996-03-06..1996-03-28 hihost 4",
  "url": "https://correlatesofwar.org/data-sets/mids/",
  "trigdate": "1996-03-06",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1996-03-06",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.chile",
   "role": "unknown"
  },
  {
   "entity": "country.gbr",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Chl Ukg Dispute 1996",
  "search_url": "https://history.state.gov/search?q=Chl+Ukg+Dispute+1996&within=documents",
  "search_status": 200,
  "window": [
   "1996-02-05",
   "1996-04-05"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:55:09+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
COW Dyadic MID 4.03 (dyadic_mid_4.03.csv) record 4148 **CHL UKG dispute**: dispute 4148 CHL-UKG 1996-03-06..1996-03-28 hihost 4 trigdate 1996-03-06, termdate None, viol None, forout None. Page: https://correlatesofwar.org/data-sets/mids/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 155: country.chile
- 200: country.gbr (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.chile:unknown, country.gbr:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Chl Ukg Dispute 1996` (https://history.state.gov/search?q=Chl+Ukg+Dispute+1996&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1996-02-05..1996-04-05. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier mid_4148_chl_ukg_dispute --approved-by joe`. The code never runs it.
