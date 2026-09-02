# Dossier ucdp_739_government_of_india_vs_attf — Government of India vs ATTF

```json
{
 "id": "ucdp_739_government_of_india_vs_attf",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "739",
  "detail": "dyad 739 Government of India vs ATTF (India) onset 1992-10-12 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1992-10-12",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-10-12",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.india",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of India Vs Attf 1992",
  "search_url": "https://history.state.gov/search?q=Government+Of+India+Vs+Attf+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-09-12",
   "1992-11-11"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:10+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 739 **Government of India vs ATTF**: dyad 739 Government of India vs ATTF (India) onset 1992-10-12 intensity 1 trigdate 1992-10-12, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of India Vs Attf 1992` (https://history.state.gov/search?q=Government+Of+India+Vs+Attf+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-09-12..1992-11-11. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_739_government_of_india_vs_attf --approved-by joe`. The code never runs it.
