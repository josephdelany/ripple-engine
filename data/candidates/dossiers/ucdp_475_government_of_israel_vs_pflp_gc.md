# Dossier ucdp_475_government_of_israel_vs_pflp_gc — Government of Israel vs PFLP-GC

```json
{
 "id": "ucdp_475_government_of_israel_vs_pflp_gc",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "475",
  "detail": "dyad 475 Government of Israel vs PFLP-GC (Israel) onset 1989-09-02 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1989-09-02",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1989-09-02",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.israel",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Israel Vs Pflp Gc 1989",
  "search_url": "https://history.state.gov/search?q=Government+Of+Israel+Vs+Pflp+Gc+1989&within=documents",
  "search_status": 200,
  "window": [
   "1989-08-03",
   "1989-10-02"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:53:10+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 475 **Government of Israel vs PFLP-GC**: dyad 475 Government of Israel vs PFLP-GC (Israel) onset 1989-09-02 intensity 1 trigdate 1989-09-02, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 666: country.israel (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.israel:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Israel Vs Pflp Gc 1989` (https://history.state.gov/search?q=Government+Of+Israel+Vs+Pflp+Gc+1989&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1989-08-03..1989-10-02. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_475_government_of_israel_vs_pflp_gc --approved-by joe`. The code never runs it.
