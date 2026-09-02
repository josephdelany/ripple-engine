# Dossier ucdp_16900_government_of_turkey_vs_tkp_ml — Government of Turkey vs TKP-ML

```json
{
 "id": "ucdp_16900_government_of_turkey_vs_tkp_ml",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "16900",
  "detail": "dyad 16900 Government of Turkey vs TKP-ML (Turkey) onset 2000-04-25 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "2000-04-25",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "2000-04-25",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.turkey",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Turkey Vs Tkp Ml 2000",
  "search_url": "https://history.state.gov/search?q=Government+Of+Turkey+Vs+Tkp+Ml+2000&within=documents",
  "search_status": 200,
  "window": [
   "2000-03-26",
   "2000-05-25"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:56:15+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 16900 **Government of Turkey vs TKP-ML**: dyad 16900 Government of Turkey vs TKP-ML (Turkey) onset 2000-04-25 intensity 1 trigdate 2000-04-25, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 640: country.turkey (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.turkey:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Turkey Vs Tkp Ml 2000` (https://history.state.gov/search?q=Government+Of+Turkey+Vs+Tkp+Ml+2000&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 2000-03-26..2000-05-25. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_16900_government_of_turkey_vs_tkp_ml --approved-by joe`. The code never runs it.
