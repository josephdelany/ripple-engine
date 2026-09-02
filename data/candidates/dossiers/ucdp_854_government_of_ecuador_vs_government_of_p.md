# Dossier ucdp_854_government_of_ecuador_vs_government_of_p — Government of Ecuador vs Government of Peru

```json
{
 "id": "ucdp_854_government_of_ecuador_vs_government_of_p",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "854",
  "detail": "dyad 854 Government of Ecuador vs Government of Peru (Ecuador, Peru) onset 1995-01-31 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1995-01-31",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1995-01-31",
 "date_precision": "day",
 "proposed_class": "conflict_escalation",
 "proposed_severity": 2,
 "proposed_surprise": 3,
 "proposed_confidence": "medium",
 "entities": [
  {
   "entity": "country.ecuador",
   "role": "unknown"
  },
  {
   "entity": "country.peru",
   "role": "unknown"
  }
 ],
 "unmapped_ccodes": [],
 "second_source": {
  "found": false,
  "status": "none_found",
  "route": "FRUS",
  "query": "Government Of Ecuador Vs Government Of Peru 1995",
  "search_url": "https://history.state.gov/search?q=Government+Of+Ecuador+Vs+Government+Of+Peru+1995&within=documents",
  "search_status": 200,
  "window": [
   "1995-01-01",
   "1995-03-02"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:59+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 854 **Government of Ecuador vs Government of Peru**: dyad 854 Government of Ecuador vs Government of Peru (Ecuador, Peru) onset 1995-01-31 intensity 1 trigdate 1995-01-31, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 130: country.ecuador (registered state set)
- 135: country.peru

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.ecuador:unknown, country.peru:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of Ecuador Vs Government Of Peru 1995` (https://history.state.gov/search?q=Government+Of+Ecuador+Vs+Government+Of+Peru+1995&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1995-01-01..1995-03-02. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_854_government_of_ecuador_vs_government_of_p --approved-by joe`. The code never runs it.
