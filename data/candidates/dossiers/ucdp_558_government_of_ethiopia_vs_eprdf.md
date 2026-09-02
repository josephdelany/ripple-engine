# Dossier ucdp_558_government_of_ethiopia_vs_eprdf — Government of Ethiopia vs EPRDF

```json
{
 "id": "ucdp_558_government_of_ethiopia_vs_eprdf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "558",
  "detail": "dyad 558 Government of Ethiopia vs EPRDF (Ethiopia) onset 1989-01-08 intensity 2",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1989-01-08",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1989-01-08",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [],
 "unmapped_ccodes": [
  530
 ],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Ethiopia Vs Eprdf 1989",
  "search_url": "https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Eprdf+1989&within=documents",
  "search_status": 200,
  "window": [
   "1988-12-09",
   "1989-02-07"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:52:59+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 558 **Government of Ethiopia vs EPRDF**: dyad 558 Government of Ethiopia vs EPRDF (Ethiopia) onset 1989-01-08 intensity 2 trigdate 1989-01-08, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 530: UNMAPPED (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: none mapped

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Ethiopia Vs Eprdf 1989` (https://history.state.gov/search?q=Government+Of+Ethiopia+Vs+Eprdf+1989&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1988-12-09..1989-02-07. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_558_government_of_ethiopia_vs_eprdf --approved-by joe`. The code never runs it.
