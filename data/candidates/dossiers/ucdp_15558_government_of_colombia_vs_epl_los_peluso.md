# Dossier ucdp_15558_government_of_colombia_vs_epl_los_peluso — Government of Colombia vs EPL–Los Pelusos

```json
{
 "id": "ucdp_15558_government_of_colombia_vs_epl_los_peluso",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "15558",
  "detail": "dyad 15558 Government of Colombia vs EPL\u2013Los Pelusos (Colombia) onset 2000-05-17 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2000-05-17",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2000-05-17",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.col",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Colombia Vs Epl Los Pelusos 2000",
  "search_url": "https://history.state.gov/search?q=Government+Of+Colombia+Vs+Epl+Los+Pelusos+2000&within=documents",
  "search_status": 200,
  "window": [
   "2000-04-17",
   "2000-06-16"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:16+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 15558 **Government of Colombia vs EPL–Los Pelusos**: dyad 15558 Government of Colombia vs EPL–Los Pelusos (Colombia) onset 2000-05-17 intensity 1 trigdate 2000-05-17, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 100: country.col (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.col:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Colombia Vs Epl Los Pelusos 2000` (https://history.state.gov/search?q=Government+Of+Colombia+Vs+Epl+Los+Pelusos+2000&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 2000-04-17..2000-06-16. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_15558_government_of_colombia_vs_epl_los_peluso --approved-by joe`. The code never runs it.
