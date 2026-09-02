# Dossier ucdp_508_government_of_india_vs_nscn_im — Government of India vs NSCN-IM

```json
{
 "id": "ucdp_508_government_of_india_vs_nscn_im",
 "built_by": "session A",
 "built_at": "2026-09-02T20:57:22+00:00",
 "rule": "data/candidates/DOSSIER_RULE.md (2026-09-02)",
 "primary": {
  "dataset": "UCDP Dyadic v26.1 (Dyadic_v26_1.csv)",
  "crisno": null,
  "source": "ucdp",
  "source_id": "508",
  "detail": "dyad 508 Government of India vs NSCN-IM (India) onset 1992-08-05 intensity 1",
  "url": "https://ucdp.uu.se/downloads/",
  "trigdate": "1992-08-05",
  "termdate": null,
  "viol": null,
  "forout": null
 },
 "event_date": "1992-08-05",
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
  "query": "Government Of India Vs Nscn Im 1992",
  "search_url": "https://history.state.gov/search?q=Government+Of+India+Vs+Nscn+Im+1992&within=documents",
  "search_status": 200,
  "window": [
   "1992-07-06",
   "1992-09-04"
  ],
  "opened": [],
  "retrieved_at": "2026-09-02T19:54:05+00:00",
  "also_tried": []
 },
 "admissible": false,
 "approved_by": null,
 "approved_at": null
}
```

## Primary record (source 1)
UCDP Dyadic v26.1 (Dyadic_v26_1.csv) record 508 **Government of India vs NSCN-IM**: dyad 508 Government of India vs NSCN-IM (India) onset 1992-08-05 intensity 1 trigdate 1992-08-05, termdate None, viol None, forout None. Page: https://ucdp.uu.se/downloads/

## Actors (ICB actors mapped through countries.py; unmapped COW codes kept)
- 750: country.india (registered state set)

## Proposed coding (provisional, rule §2 — Joe decides)
- class: `conflict_escalation`; severity 2 (from viol None); surprise 3 (provisional); confidence medium
- entities: country.india:unknown

## Second source (rule §3)
- **second source: none found — not admissible.** FRUS search `Government Of India Vs Nscn Im 1992` (https://history.state.gov/search?q=Government+Of+India+Vs+Nscn+Im+1992&within=documents, HTTP 200) returned 0 document(s) opened, none dated inside 1992-07-06..1992-09-04. 
- UN Security Council pages, OPEC archive: HTTP 403 to scripts; EIA chronology: URL gone; NYT: no key — not searched (rule §3).

## Admissible: **no**

Joe: to admit, write the approval line and run
`python3 src/admit.py --dossier ucdp_508_government_of_india_vs_nscn_im --approved-by joe`. The code never runs it.
