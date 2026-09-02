# Dossier ucdp_11932_government_of_india_vs_cpi_ml_j — Government of India vs CPI-ML-J

```json
{
 "id": "ucdp_11932_government_of_india_vs_cpi_ml_j",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "11932",
  "detail": "dyad 11932 Government of India vs CPI-ML-J (India) onset 2000-08-25 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2000-08-25",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2000-08-25",
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
  "query": "Government Of India Vs Cpi Ml J 2000",
  "search_url": "https://history.state.gov/search?q=Government+Of+India+Vs+Cpi+Ml+J+2000&within=documents",
  "search_status": 200,
  "window": [
   "2000-07-26",
   "2000-09-24"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:20+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 11932 **Government of India vs CPI-ML-J**: dyad 11932 Government of India vs CPI-ML-J (India) onset 2000-08-25 intensity 1 trigdate 2000-08-25, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of India Vs Cpi Ml J 2000` (https://history.state.gov/search?q=Government+Of+India+Vs+Cpi+Ml+J+2000&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 2000-07-26..2000-09-24. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_11932_government_of_india_vs_cpi_ml_j --approved-by joe`. The code never runs it.
