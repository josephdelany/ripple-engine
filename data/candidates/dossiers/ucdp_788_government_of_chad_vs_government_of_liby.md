# Dossier ucdp_788_government_of_chad_vs_government_of_liby — Government of Chad vs Government of Libya

```json
{
 "id": "ucdp_788_government_of_chad_vs_government_of_liby",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "788",
  "detail": "dyad 788 Government of Chad vs Government of Libya (Chad, Libya) onset 1987-08-08 intensity 2",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1987-08-08",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1987-08-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.libya",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [
  483
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Chad Vs Government Of Libya 1987",
  "search_url": "https://history.state.gov/search?q=Government+Of+Chad+Vs+Government+Of+Libya+1987&within=documents",
  "search_status": 200,
  "window": [
   "1987-07-09",
   "1987-09-07"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:38+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 788 **Government of Chad vs Government of Libya**: dyad 788 Government of Chad vs Government of Libya (Chad, Libya) onset 1987-08-08 intensity 2 trigdate 1987-08-08, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 483: UNMAPPED
- 620: country.libya (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.libya:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Chad Vs Government Of Libya 1987` (https://history.state.gov/search?q=Government+Of+Chad+Vs+Government+Of+Libya+1987&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1987-07-09..1987-09-07. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_788_government_of_chad_vs_government_of_liby --approved-by joe`. The code never runs it.
