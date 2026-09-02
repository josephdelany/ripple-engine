# Dossier ucdp_850_government_of_mexico_vs_ezln — Government of Mexico vs EZLN

```json
{
 "id": "ucdp_850_government_of_mexico_vs_ezln",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "850",
  "detail": "dyad 850 Government of Mexico vs EZLN (Mexico) onset 1994-01-01 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1994-01-01",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1994-01-01",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.mex",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Mexico Vs Ezln 1994",
  "search_url": "https://history.state.gov/search?q=Government+Of+Mexico+Vs+Ezln+1994&within=documents",
  "search_status": 200,
  "window": [
   "1993-12-02",
   "1994-01-31"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:34+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 850 **Government of Mexico vs EZLN**: dyad 850 Government of Mexico vs EZLN (Mexico) onset 1994-01-01 intensity 1 trigdate 1994-01-01, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 70: country.mex (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.mex:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Mexico Vs Ezln 1994` (https://history.state.gov/search?q=Government+Of+Mexico+Vs+Ezln+1994&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1993-12-02..1994-01-31. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_850_government_of_mexico_vs_ezln --approved-by joe`. The code never runs it.
